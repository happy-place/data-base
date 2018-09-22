package com.big.data.traffic

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc:
  *
  */

import java.text.DecimalFormat
import java.util
import java.util.Calendar

import com.alibaba.fastjson.JSON
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}



import scala.util.Random

/**
  * 模拟产生数据，同时把数据实时的发送到kafka
  * //随机产生  监测点id  以及  速度
  * //序列化为json
    //发送给kafka
  */
/**
  * 模拟交通卡口 200s/次 上报一次各自监控到的车速，上报的kafka
  * 车速 300s/次 在高速[30,60)和 低速[1,21)直接切换
  */


object TrafficDataCollector {
  def main(args: Array[String]): Unit = {
    //读取kafka配置信息
    val props = PropertyUtil.properties
    println(props)
    //创建kafka生产者对象
    val producer = new KafkaProducer[String, String](props)

    //模拟生产实时数据
    var startTime = Calendar.getInstance().getTimeInMillis / 1000
    //数据模拟（堵车）切换的周期,单位：秒
    val trafficCycle = 300

    //不停的开始模拟数据
    while(true){
      //模拟产生监测点id 1~20 001~020
      val randomMonitorId = new DecimalFormat("0000").format(Random.nextInt(20) + 1)
      //模拟车速
      var randomSpeed = "000"
      val currentTime = Calendar.getInstance().getTimeInMillis / 1000
      //每5分钟切换一次公路状态
      if(currentTime - startTime > trafficCycle){
        randomSpeed = new DecimalFormat("000").format(Random.nextInt(15)) // 000~015
        if(currentTime - startTime > trafficCycle * 2){
          startTime = currentTime
        }
      }else{
        randomSpeed = new DecimalFormat("000").format(Random.nextInt(30) + 30) // 300~600
      }

      //将产生的数据序列化为JSON
      //      {"monitor_id": "0001", "spedd" : "049"}
      val jsonMap = new util.HashMap[String, String]()
      jsonMap.put("monitor_id", randomMonitorId)
      jsonMap.put("speed", randomSpeed)

      //因为kafka是基于事件的，在此，我们每一条产生的数据都序列化为一个json事件
      val event = JSON.toJSON(jsonMap)
      println(event)

      //将封装好的数据发送给kafka
      producer.send(new ProducerRecord[String, String](props.getProperty("topic"), event.toString))
      Thread.sleep(200)
    }

  }
}

