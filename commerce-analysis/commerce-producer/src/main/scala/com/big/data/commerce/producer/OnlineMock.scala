package com.big.data.commerce.producer

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */
import java.util.Properties

import com.big.data.commerce.common.ConfigManager
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerConfig, ProducerRecord}

import scala.collection.mutable.ArrayBuffer
import scala.util.Random

object OnlineMock {

  /**
    * 模拟的数据
    * 时间点: 当前时间毫秒
    * userId: 0 - 99
    * 省份、城市 ID相同 ： 1 - 9
    * adid: 0 - 19
    * ((0L,"北京","北京"),(1L,"上海","上海"),(2L,"南京","江苏省"),(3L,"广州","广东省"),(4L,"三亚","海南省"),(5L,"武汉","湖北省"),(6L,"长沙","湖南省"),(7L,"西安","陕西省"),(8L,"成都","四川省"),(9L,"哈尔滨","东北省"))
    * 格式 ：timestamp province city userid adid
    * 某个时间点 某个省份 某个城市 某个用户 某个广告
    */
  def generateMockData(): Array[String] = {
    val array = ArrayBuffer[String]()
    val random = new Random()
    //timestamp province city userid adid
    for (i <- 0 to 50) {

      val timestamp = System.currentTimeMillis()
      val province = random.nextInt(10)
      val city = province
      val adid = random.nextInt(20)
      val userid = random.nextInt(100)

      array += timestamp + " " + province + " " + city + " " + userid + " " + adid
    }

    array.toArray
  }

  def createKafkaProducer(broker: String): KafkaProducer[String, String] = {

    val prop = new Properties()
    prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, broker)
    prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")
    prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")

    new KafkaProducer[String, String](prop)
  }


  def main(args: Array[String]): Unit = {

    val broker = ConfigManager.config.getString("kafka.broker")
    val topic = ConfigManager.config.getString("kafka.topic")

    val kafkaProducer = createKafkaProducer(broker)

    while (true) {

      for (item <- generateMockData()) {
        println(item)
        kafkaProducer.send(new ProducerRecord[String, String](topic, item))
      }

      Thread.sleep(5000)

    }

  }

}

