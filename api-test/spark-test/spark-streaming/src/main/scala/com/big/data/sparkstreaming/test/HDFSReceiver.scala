package com.big.data.sparkstreaming.test

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming._

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/21
  * Desc: 
  *
  */

object HDFSReceiver {

  def main(args: Array[String]) {
    // 必须使用 两个以上线程
    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[2]").setAppName(this.getClass.getSimpleName)
    val ssc = new StreamingContext(conf, Seconds(1)) // 每 1 秒 一个批次

    try{
      val lines = ssc.textFileStream("hdfs://localhost:9000/tmp/spark/ssc/in/")
      val words = lines.flatMap(_.split(" "))

      val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
      wordCounts.print()

      ssc.start()
      ssc.awaitTermination()

    }finally {
      ssc.stop()
    }

  }
}
