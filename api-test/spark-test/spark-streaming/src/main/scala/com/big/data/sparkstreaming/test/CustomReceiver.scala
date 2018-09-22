package com.big.data.sparkstreaming.test

import java.io.{BufferedReader, InputStreamReader}
import java.net.Socket
import java.nio.charset.StandardCharsets
import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.receiver.Receiver
import org.slf4j.LoggerFactory

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/21
  * Desc: 
  *
  */
trait Logging {
  val logger = LoggerFactory.getLogger(this.getClass.getSimpleName)
}
class CustomReceiver(host: String, port: Int)
  extends Receiver[String](StorageLevel.MEMORY_AND_DISK_2) with Logging{

  def onStart() {
    // Start the thread that receives data over a connection
    new Thread("Socket Receiver") {
      override def run() {
        receive()
        logger.info("Socket Receiver Start")
      }
    }.start()
  }

  def onStop() {
    // There is nothing much to do as the thread calling receive()
    // is designed to stop by itself if isStopped() returns false
    logger.info("Socket Receiver Stop")
  }

  /** Create a socket connection and receive data until receiver is stopped */
  private def receive() {
    var socket: Socket = null
    var userInput: String = null
    try {
      // Connect to host:port
      socket = new Socket(host, port)

      // Until stopped or connection broken continue reading
      val reader = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8))
      userInput = reader.readLine()
      while(!isStopped && userInput != null) {
        store(userInput)
        userInput = reader.readLine()
      }
      reader.close()
      socket.close()

      // Restart in an attempt to connect again when server is active again
      restart("Trying to connect again")
      logger.info("Trying to connect again")
    } catch {
      case e: java.net.ConnectException =>
        // restart if could not connect to server
        restart("Error connecting to " + host + ":" + port, e)
      case t: Throwable =>
        // restart if there is any other error
        restart("Error receiving data", t)
    }
  }
}

object CustomReceiverTest extends App{
  // 必须使用 两个以上线程
  val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[2]").setAppName(this.getClass.getSimpleName)
  val ssc = new StreamingContext(conf, Seconds(1)) // 每 1 秒 一个批次

  try{
    val customReceiverStream = ssc.receiverStream(new CustomReceiver("localhost", 9999))
    val words = customReceiverStream.flatMap(_.split(" "))

    val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
    wordCounts.print()

    ssc.start()
    ssc.awaitTermination()

  }finally {
    ssc.stop()
  }
}