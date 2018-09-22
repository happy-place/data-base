package com.big.data.commerce.analysis.advertise

import com.big.data.commerce.common.ConfigManager
import kafka.api.{OffsetRequest, PartitionOffsetRequestInfo, TopicMetadataRequest}
import kafka.common.TopicAndPartition
import kafka.consumer.SimpleConsumer
import kafka.message.MessageAndMetadata
import kafka.serializer.StringDecoder
import kafka.utils.{ZKGroupTopicDirs, ZkUtils}
import org.I0Itec.zkclient.ZkClient
import org.apache.commons.lang3.time.DateFormatUtils
import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.streaming.dstream.InputDStream
import org.apache.spark.streaming.kafka.{HasOffsetRanges, KafkaUtils, OffsetRange}
import org.apache.spark.streaming.{Minutes, Seconds, StreamingContext}

import scala.collection.mutable.ArrayBuffer


object AdvertiseAnysis {

  def main(args: Array[String]): Unit = {

    val sparkConf = new SparkConf().setAppName("advertise").setMaster("local[*]")
    val spark = SparkSession.builder().config(sparkConf).enableHiveSupport().getOrCreate()
    val ssc = new StreamingContext(spark.sparkContext, Seconds(5))

    ssc.checkpoint("./commerce-analysis/multi-analysis/advertise-analysis/checkpoint")

    val topic = ConfigManager.config.getString("kafka.topic")
    val zooKeeper = ConfigManager.config.getString("zookeeper")

    //Zookeeper DIR
//    val topicDirs = new ZKGroupTopicDirs("advertise", topic)
//     val zkTopicPath = s"${topicDirs.consumerOffsetDir}"
//
//     val zkClient = new ZkClient(zooKeeper)
//
//     val children = zkClient.countChildren(zkTopicPath)
//
//     var adRealtimeLogDStream: InputDStream[(String, String)] = null

    val kafkaParams = Map[String, String](
      ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> ConfigManager.config.getString("kafka.broker"), //用于初始化链接到集群的地址
      //用于标识这个消费者属于哪个消费团体
      ConsumerConfig.GROUP_ID_CONFIG -> "advertise",
      //如果没有初始化偏移量或者当前的偏移量不存在任何服务器上，可以使用这个配置属性
      ConsumerConfig.AUTO_OFFSET_RESET_CONFIG -> "largest"
    )

    /*if (children > 0) {
      println("从Zookeeper恢复")
      var fromOffsets: Map[TopicAndPartition, Long] = Map()

      // 为了获得一个topic 所有的Pattiton的主分区Hostname
      val topicList = List(topic)
      val request = new TopicMetadataRequest(topicList, 0)
      val getLeaderConsumer = new SimpleConsumer("linux", 9092, 10000, 10000, "OffsetLookup")
      val response = getLeaderConsumer.send(request)

      val topicMetadataOption = response.topicsMetadata.headOption
      val partitons = topicMetadataOption match {
        case Some(tm) =>
          tm.partitionsMetadata.map(pm => (pm.partitionId, pm.leader.get.host)).toMap[Int, String]
        case None => Map[Int, String]()
      }

      getLeaderConsumer.close()

      println("partitions info is:" + partitons)
      println("children info is:" + children)

      for (i <- 0 until children) {
        val partitionOffset = zkClient.readData[String](s"${topicDirs.consumerOffsetDir}/${i}")
        println("保存的偏移位置是：" + partitionOffset)
        val tp = TopicAndPartition(topic, i)

        val requestMin = OffsetRequest(Map(tp -> PartitionOffsetRequestInfo(OffsetRequest.EarliestTime, 1)))
        val consumerMin = new SimpleConsumer(partitons(i), 9092, 10000, 10000, "getMinOffset")
        val curOffsets = consumerMin.getOffsetsBefore(requestMin).partitionErrorAndOffsets(tp).offsets

        consumerMin.close()

        var nextOffset = partitionOffset.toLong
        if (curOffsets.length > 0 && nextOffset < curOffsets.head) {
          nextOffset = curOffsets.head
        }
        println("修正后的偏移位置是：" + nextOffset)
        fromOffsets += (tp -> nextOffset)
      }

      val messageHandler = (mmd: MessageAndMetadata[String, String]) => (mmd.topic, mmd.message())
      adRealtimeLogDStream = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder, (String, String)](ssc, kafkaParams, fromOffsets, messageHandler)

    } else {
      println("直接创建")
      adRealtimeLogDStream = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, Set(topic))
    }*/

    val adRealtimeLogDStream = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, Set(topic))


    // 需求一：广告点击黑名单
    val filtedAdRealTimeDStream = adRealtimeLogDStream.transform{ rdd =>

      //你应该获取 黑名单
      val blackList = AdBlackListDAO.findAll()
      rdd.map{ item =>
        val params = item._2.split(" ")
        AdvertiseRealTime(params(0).trim.toLong,params(1).trim.toInt,params(2).trim.toInt,params(3).trim.toInt,params(4).trim.toInt)
      }.filter(item => !blackList.contains(item.userid))
    }

    val dailyUserClickDStream = filtedAdRealTimeDStream.map{adRealtime =>
      ((DateFormatUtils.format(adRealtime.timestamp,"yyyy-MM-dd"),adRealtime.userid,adRealtime.adid),1L)
    }.reduceByKey(_ + _)


    dailyUserClickDStream.foreachRDD{rdd =>
      rdd.foreachPartition{ items =>

        val adUserClickCountArray = ArrayBuffer[AdUserClickCount]()
        for(item <- items){
          adUserClickCountArray += AdUserClickCount(item._1._1,item._1._2,item._1._3,item._2)
        }
        AdUserClickCountDAO.updateBatch(adUserClickCountArray.toArray)
      }
    }

    val blacklistDStream = dailyUserClickDStream.filter{ case ((date,userid,adid),count) =>

      if(AdUserClickCountDAO.findClickCountByMultiKey(date,userid.toLong,adid.toLong) >=100)
          true
      else
        false
    }

    // 保存黑名单
    blacklistDStream.foreachRDD{rdd =>
      rdd.foreachPartition{ items =>

        val adBalckList = ArrayBuffer[AdBlacklist]()
        for(item <- items){
          adBalckList += AdBlacklist(item._1._2)
        }
        AdBlackListDAO.insertBatch(adBalckList.toArray)
      }
    }

    // 需求二：每天各省各城市各广告的点击流量实时统计


    // 将DStream转换为  ( date province city adid )  1L

    val dailyAdClickDStream = filtedAdRealTimeDStream.map{adRealtime =>
      ((DateFormatUtils.format(adRealtime.timestamp,"yyyy-MM-dd"),adRealtime.province,adRealtime.city,adRealtime.adid),1L)
    }


    // updateFunc: (Seq[V], Option[S]) => Option[S]
    val aggregatedDStream = dailyAdClickDStream.updateStateByKey[Long]{ (values:Seq[Long], old:Option[Long]) =>
      Some(old.getOrElse[Long](0) + values.sum)
    }

    aggregatedDStream.foreachRDD{rdd =>

      rdd.foreachPartition{items =>

        val adStats = ArrayBuffer[AdStat]()
        for(item <- items){
          adStats += AdStat(item._1._1,item._1._2,item._1._3,item._1._4,item._2)
        }
        AdStatDAO.updateBatch(adStats.toArray)
      }
    }

    val provinceTop3DStream = aggregatedDStream.transform{ rdd =>

      // 每天每省每个广告的实时点击流量
      val aggrDateAdCount = rdd.map{ case ((date,province,city,adid),count) =>
        ((date,province,adid),count)
      }.reduceByKey(_ + _)

      import spark.implicits._
      val aggrDateAdCountDF = aggrDateAdCount.map{ case ((date,province,adid),count) =>
        (date,province,adid,count)
      }.toDF("date","province","adid","count")

      aggrDateAdCountDF.createOrReplaceTempView("aggrDateAdCountDF")

      val provinceTop3DF = spark.sql("select date,province, adid, count from " +
        "(select date, province, adid, count, rank() over(partition by date,province order by count desc) rank from aggrDateAdCountDF) t " +
        "where rank <=3")

      provinceTop3DF.rdd
    }

    provinceTop3DStream.foreachRDD{rdd =>

      rdd.foreachPartition{items =>

        val adProvinceTop3Array = ArrayBuffer[AdProvinceTop3]()

        for(item <- items){

          val date = item.getAs[String]("date")
          val province = item.getAs[Int]("province")
          val adid = item.getAs[Int]("adid")
          val count = item.getAs[Long]("count")
          adProvinceTop3Array += AdProvinceTop3(date,province,adid,count)
        }
        AdProvinceTop3DAO.updateBatch(adProvinceTop3Array.toArray)
      }

    }


    val minute2Count = filtedAdRealTimeDStream.transform{rdd =>
      rdd.map{ item =>
        ((DateFormatUtils.format(item.timestamp,"yyyy-MM-dd HH:mm"),item.adid),1L)
      }
    }

    val windowDstream = minute2Count.reduceByKeyAndWindow((a:Long,b:Long) => a + b, Minutes(60),Seconds(30))

    // 执行周期  1分钟执行
    windowDstream.foreachRDD{rdd =>

      rdd.foreachPartition{items =>
        val adClickTrendArray = ArrayBuffer[AdClickTrend]()
        for (item <- items){
          val date = item._1._1.split(" ")(0)
          val hour = item._1._1.split(" ")(1).split(":")(0)
          val minute = item._1._1.split(" ")(1).split(":")(1)

          val adid = item._1._2
          val count = item._2

          adClickTrendArray += AdClickTrend(date,hour,minute,adid,count)

        }

        AdClickTrendDAO.updateBatch(adClickTrendArray.toArray)

      }

    }

    var offsetRanges = Array[OffsetRange]()

     val adRealtimeLog = adRealtimeLogDStream.transform { rdd =>
       offsetRanges = rdd.asInstanceOf[HasOffsetRanges].offsetRanges
       rdd
     }


    adRealtimeLog.foreachRDD { rdd =>

      for (offset <- offsetRanges)
        println(offset)

      rdd.foreachPartition { items =>
        // 处理了业务
        for (item <- items) {
          //println(item)
        }

      }
      // 创建一个Zookeeper的目录
      val updateTopicDir = new ZKGroupTopicDirs("advertise", topic)
      // 创建一个Zookeeper的客户端
      val updateZkClient = new ZkClient(zooKeeper)

      // 保存了所有Partition的信息
      for (offset <- offsetRanges) {
        val zkPath = s"${updateTopicDir.consumerOffsetDir}/${offset.partition}"
        ZkUtils.updatePersistentPath(updateZkClient, zkPath, offset.untilOffset.toString)
      }

      updateZkClient.close()

    }

    ssc.start()
    ssc.awaitTermination()

  }

}
