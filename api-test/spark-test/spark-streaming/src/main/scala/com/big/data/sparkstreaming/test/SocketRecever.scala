package com.big.data.sparkstreaming.test

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}


object SocketRecever {
  def main(args: Array[String]) {

    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[2]").setAppName(this.getClass.getSimpleName)
    val ssc = new StreamingContext(conf, Seconds(1)) // 每 1 秒 一个批次

    // Create a DStream that will connect to hostname:port, like localhost:9999
    /*
      telnet localhost 9999 监控端口
      nc -lk 9999 充当发送数据服务端
      nc localhost 9999 充当结束数据客户端
      netcat 服务端可以向多可 客户端广播消息，但只能与一个客户端绑定，建立连接。
     */
    val lines = ssc.socketTextStream("localhost", 9999)

    // Split each line into words
    val words = lines.flatMap(_.split(" "))

    //import org.apache.spark.streaming.StreamingContext._ // not necessary since Spark 1.3
    // Count each word in each batch
    val pairs = words.map(word => (word, 1))
    val wordCounts = pairs.reduceByKey(_ + _)

    // Print the first ten elements of each RDD generated in this DStream to the console
    wordCounts.print()

    ssc.start() // Start the computation
    ssc.awaitTermination() // Wait for the computation to terminate
  }
}

