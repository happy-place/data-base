package com.big.data.traffic

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc:
  *
  */

import java.text.SimpleDateFormat
import java.util.Calendar

import com.alibaba.fastjson.{JSON, TypeReference}
import kafka.serializer.StringDecoder
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
  * 读取kafka中的数据
  * 解析json
  * 按照分钟和卡口id聚合车速和车辆个数
  */
/** ssc 以5s微批次从kafka提取数据，以10s间隔(slider)打包聚合，每次聚合20s之内(window)收集的各批次数据
  * 根据 monitor_id 聚合打包阶段收集到的数据，（monitor_id,(speed,cnt)）
  * 以分区为单位将数据存储到 redis hset => (ymd_moinitorId,hm,speedAndCnt) (key, field, value)
  *
  */

object TrafficDataAggregrater {
  def main(args: Array[String]): Unit = {
    //初始化Spark
    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("TrafficDataAggregrater")
    val sc = new SparkContext(sparkConf)
    val ssc = new StreamingContext(sc, Seconds(5))
    ssc.checkpoint("./traffic-predicting/traffic-consumer/checkpoint")
    //初始化kafka consumer
    val kafkaParams = Map(
      "metadata.broker.list" -> PropertyUtil.getProperty("metadata.broker.list"),
      "serializer.class" -> PropertyUtil.getProperty("serializer.class"))

    //配置topic
    val topics = Set(PropertyUtil.getProperty("topic"))

    //读取kafka中的每一条数据
    val kafkaLineDStream = KafkaUtils
      .createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topics)
      .map(_._2)

    //读取事件
    //{"monitor_id" -> "0001", "speed" -> "050"}
    val event = kafkaLineDStream.map(line => {
      //使用fastjson解析里面的数据
      val lineJavaMap = JSON.parseObject(line, new TypeReference[java.util.Map[String, String]]() {})
      //首先需要将JavaMap转化为Scala Map
      import scala.collection.JavaConverters._
      val lineScalaMap: collection.mutable.Map[String, String] = mapAsScalaMapConverter(lineJavaMap).asScala
      lineScalaMap
    })
    //将每一条数据按照monitor_id聚合，聚合的每一段数据中“车辆速度”，“车辆个数”
    //(monitor_id, (speed, 1))
    val sumOfSpeedAndCount = event
      .map(e => (e.get("monitor_id").get, e.get("speed").get)) //（0001, 050）
      .mapValues(s => (s.toInt, 1)) //（0001, 050） ----> (0001, (050, 1)), (0001, (040, 1))
      .reduceByKeyAndWindow((t1: (Int, Int), t2: (Int, Int)) => (t1._1 + t2._1, t1._2 + t2._2), Seconds(20), Seconds(10))//(0001, (90, 2))

    //按照每分钟聚合数据，并保存到redis里面
    //redis数据库表的索引，从1开始
    val dbIndex = 1
    sumOfSpeedAndCount.foreachRDD(rdd => {
      rdd.foreachPartition(partitionRecord => {
        //(String, (Int, Int))例如： (0001, (90, 2))
        partitionRecord.filter((tuple: (String, (Int, Int))) => tuple._2._2 > 0).foreach(pair => {
          //开始取出这个60秒的window中的所有聚合后的数据
          //1872_15
          val jedis = RedisUtil.pool.getResource
          val monitor_id = pair._1
          val sumOfSpeed = pair._2._1
          val sumOfCount = pair._2._2
          val speedAndCount = sumOfSpeed + "_" + sumOfCount

          val currentDate = Calendar.getInstance().getTime
          val ymdSDF = new SimpleDateFormat("yyyyMMdd")
          val hmSDF = new SimpleDateFormat("HHmm")

          val ymdString = ymdSDF.format(currentDate)
          val hmString = hmSDF.format(currentDate)

          //          jedis.hset("20171218_0001", "1421", "1872_15")
          jedis.select(dbIndex)
          //(key, field, value)
          jedis.hset(ymdString + "_" + monitor_id, hmString, speedAndCount)
          println(s"hget ${ymdString}_$monitor_id $hmString")
          //          jedis.close()
          RedisUtil.pool.returnResource(jedis)
        })
      })
    })

    //启动spark
    ssc.start()
    ssc.awaitTermination()
  }
}

