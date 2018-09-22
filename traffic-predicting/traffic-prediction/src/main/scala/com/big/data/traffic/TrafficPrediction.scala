package com.big.data.traffic

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import java.text.SimpleDateFormat
import java.util.Date

import org.apache.spark.mllib.classification.LogisticRegressionModel
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable.ArrayBuffer

/**
  * 前端页面传入当前时间，和待预测卡口id
  * 查找内置关系，获取关联卡口 以及目标卡口，在传入时间点向后倒推 3min,2min,1min 时的 监控数据，构建 3min DataX
  * 从redis获取当前时段精度最高模型的 hdfs 路径，加载模块，入参DataX 预测 DataY
  */

object TrafficPrediction {
  def main(args: Array[String]): Unit = {
    val dateTimeSDF = new SimpleDateFormat("yyyy-MM-dd HH:mm")
    val ymdSDF = new SimpleDateFormat("yyyyMMdd")
    val hmSDF = new SimpleDateFormat("HHmm")

    //从前台填写一个表单：2017-12-19 15:29
    val inputDateString = "2018-06-06 18:35"
    val inputDate = dateTimeSDF.parse(inputDateString)
    val ymdString = ymdSDF.format(inputDate)
    val hmString = hmSDF.format(inputDate)

    //配置spark
    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("TrafficPrediction")
    val sc = new SparkContext(sparkConf)
    //想要预测的目标监测点
    val monitorIDs = List("0005", "0015")
    //得到相关监测点
    val monitorRelations = Map(
      "0005" -> Array("0003", "0004", "0005", "0006", "0007"),
      "0015" -> Array("0013", "0014", "0015", "0016", "0017"))

    val dbIndex = 1
    val jedis = RedisUtil.pool.getResource
    jedis.select(dbIndex)

    val temp = monitorIDs.map(monitorID => {
      val monitorRelationList = monitorRelations.get(monitorID).get
      val relationsInfo = monitorRelationList.map(monitorID => (monitorID, jedis.hgetAll(ymdString + "_" + monitorID)))
      //准备数据
      val dataX = ArrayBuffer[Double]()
      for(index <- Range(3, 0, -1)){
        val oneMoment = inputDate.getTime - 60 * index * 1000
        //field
        val oneHM = hmSDF.format(new Date(oneMoment))

        for((k, v) <- relationsInfo){
          if(v.containsKey(oneHM)){
            val speedAndCarCount = v.get(oneHM).split("_")
            val valueX = speedAndCarCount(0).toDouble / speedAndCarCount(1).toDouble
            dataX += valueX
          }else{
            dataX += -1.0
          }
        }
      }

      println(dataX.mkString("\n"))
      //加载模型
      val modelPath = jedis.hget("model", monitorID)
      val model = LogisticRegressionModel.load(sc, modelPath)
      //预测
      val avgSpeedAccuracy = model.predict(Vectors.dense(dataX.toArray))
      println("监测点:" + monitorID + "的预判结果：等级" + avgSpeedAccuracy)

      val sumCount= jedis.hget(s"${ymdString}_$monitorID",s"$hmString").split("_")
      println(s"hget ${ymdString}_$monitorID $hmString")

      val sum = sumCount(0).toInt
      val count = sumCount(1).toInt
      val realAvgSpeed = sum / count
      println("监测点:" + monitorID + "实际数据" + realAvgSpeed)
      //保存结果
      jedis.hset(inputDateString, monitorID, avgSpeedAccuracy.toString)
    })

  }
}
