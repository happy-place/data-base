package com.big.data.sparkstreaming.test

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD
import org.apache.spark.streaming.{Seconds, StreamingContext, Time}
import org.apache.spark.util.LongAccumulator

object WordBlacklist {
  // DS设置了从检查点恢复数据时，如果DS 中使用 了广播变量 和 累加器，必须设置为懒汉单例模式，否则会出现初始化错误
  @volatile private var instance: Broadcast[Seq[String]] = null

  def getInstance(sc: SparkContext): Broadcast[Seq[String]] = {
    if (instance == null) {
      synchronized {
        if (instance == null) {
          val wordBlacklist = Seq("a", "b", "c")
          instance = sc.broadcast(wordBlacklist)
        }
      }
    }
    instance
  }
}

object DroppedWordsCounter {
  // 累加器
  @volatile private var instance: LongAccumulator = null

  def getInstance(sc: SparkContext): LongAccumulator = {
    if (instance == null) {
      synchronized {
        if (instance == null) {
          instance = sc.longAccumulator("WordsInBlacklistCounter")
        }
      }
    }
    instance
  }
}

object BroadcastInDS {

  def getOrCreate(checkpointDir:String)={
    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[4]").setAppName(this.getClass.getSimpleName)
    val ssc = new StreamingContext(conf, Seconds(1)) // 每 1 秒 一个批次

    ssc.sparkContext.setCheckpointDir(checkpointDir)

    ssc.checkpoint(checkpointDir)

    val ds = ssc.socketTextStream("localhost", 9999)

    val wordCounts = ds.flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_)

    wordCounts.foreachRDD { (rdd: RDD[(String, Int)], time: Time) =>
      // Get or register the blacklist Broadcast
      val blacklist = WordBlacklist.getInstance(rdd.sparkContext)
      // Get or register the droppedWordsCounter Accumulator
      val droppedWordsCounter = DroppedWordsCounter.getInstance(rdd.sparkContext)
      // Use blacklist to drop words and use droppedWordsCounter to count them

      println(droppedWordsCounter.value)

      val counts = rdd.filter { case (word, count) =>
        if (blacklist.value.contains(word)) {
          droppedWordsCounter.add(count)
          false
        } else {
          true
        }
      }.collect().mkString("[", ", ", "]")
      val output = "Counts at time " + time + " " + counts
      println(output)
    }
    ssc
  }

  def main(args: Array[String]): Unit = {
    val checkpointDir = "api-test/spark-test/spark-streaming/checkpoint"

    val ssc = StreamingContext.getOrCreate(checkpointDir,()=>getOrCreate(checkpointDir))

    ssc.start()

    ssc.awaitTermination()
  }

}


