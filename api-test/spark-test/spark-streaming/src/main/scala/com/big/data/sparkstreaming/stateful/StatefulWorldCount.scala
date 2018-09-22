package com.big.data.sparkstreaming.stateful

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

object StatefulWorldCount {

  def main(args: Array[String]) {

    // 定义更新状态方法，参数values为当前批次单词频度，state为以往批次单词频度
    // Seq 是 从RDD 发射出来的 kv 对，会按 key进行收集，RDD 可以直接通过 map 发射 或 经过 reduce 预先聚合，在发射
    // state 中是基于key 保存的状态
    val updateFunc = (values: Seq[Int], state: Option[Int]) => {
      val currentCount = values.foldLeft(0)(_ + _)
      val previousCount = state.getOrElse(0)
      Some(currentCount + previousCount)
    }

    // 至少启动两个线程 local[2],一个用于采集，一个用于计算
    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true")
        .set("spark.streaming.receiver.writeAheadLog.enable", "true") // >>> receivedData
        .setMaster("local[2]").setAppName(getClass.getSimpleName)
    val ssc = new StreamingContext(conf, Seconds(3))

    // 通过chechpoint 斩断依赖链，提高性能
    ssc.checkpoint("./api-test/spark-test/spark-streaming/checkpoint/") // >> receivedBlockMetadata

    // Create a DStream that will connect to hostname:port, like localhost:9999
    val lines = ssc.socketTextStream("localhost", 9999)

    // 各 RDD 不同分区内部进行 MR 统计
    // Split each line into words
    val words = lines.flatMap(_.split(" "))

    //import org.apache.spark.streaming.StreamingContext._ // not necessary since Spark 1.3
    // Count each word in each batch
    val pairs = words.map(word => (word, 1))

    // 使用updateStateByKey来更新状态，统计从运行开始以来单词总的次数
    // 方案1：各 partition 只执行 map ,然后统一到状态函数中聚合
    //    val stateDstream = pairs.updateStateByKey[Int](updateFunc)

    // 方案2：RDD 内部先汇总，然后在 updateFunc 中对 各RDD 进行汇总
    val wordCounts = pairs.reduceByKey(_ + _)
    val stateDstream = wordCounts.updateStateByKey[Int](updateFunc)

    stateDstream.print()

    //val wordCounts = pairs.reduceByKey(_ + _)

    // Print the first ten elements of each RDD generated in this DStream to the console
    //wordCounts.print()

    ssc.start()             // Start the computation
    ssc.awaitTermination()  // Wait for the computation to terminate
    //ssc.stop()
  }

}

