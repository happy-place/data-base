package com.big.data.sparkstreaming.nostopping

import org.apache.spark.SparkConf
import org.apache.spark.streaming.StreamingContext._
import org.apache.spark.streaming.{Seconds, StreamingContext}


/**
  * Created by xiaojun on 2015/5/25.
  */
object MyRecoverableNetworkWordCount {

  def createContext(ip: String, port: Int, checkpointDirectory: String) = {
    println("Creating new context")
    val sparkConf = new SparkConf().setMaster("local[4]").setAppName("RecoverableNetworkWordCount")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    ssc.checkpoint(checkpointDirectory)
    val updateFunc = (values: Seq[Int], state: Option[Int]) => {
      val currentCount = values.sum
      val previousCount = state.getOrElse(0)
      Some(currentCount + previousCount)
    }

    val lines = ssc.socketTextStream(ip, port)
    val words = lines.flatMap(_.split(" "))
    val wordDstream = words.map(x => (x, 1))

    val stateDstream = wordDstream.updateStateByKey[Int](updateFunc)

    stateDstream.print()
    ssc
  }

  def main(args: Array[String]) {

    val Array(ip, IntParam(port), checkpointDirectory) = args
    val ssc = StreamingContext.getOrCreate(checkpointDirectory,
      () => {
        createContext(ip, port, checkpointDirectory)
      })

    ssc.start()
    ssc.awaitTermination()
  }
}
//extractor
private object IntParam {
  def unapply(str: String): Option[Int] = {
    try {
      Some(str.toInt)
    } catch {
      case e: NumberFormatException => None
    }
  }
}

