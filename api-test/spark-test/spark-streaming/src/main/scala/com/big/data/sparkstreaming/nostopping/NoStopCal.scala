package com.big.data.sparkstreaming.nostopping

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/23
  * Desc: 
  *
  */

object NoStopCal {

  def getOrCreateContext(checkpointDir:String) ={
    print("new context")
    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[2]").setAppName(this.getClass.getSimpleName)
    val ssc = new StreamingContext(conf,Seconds(1))

    ssc.checkpoint(checkpointDir)

    val sockerDS = ssc.socketTextStream("localhost",9999)
    sockerDS.flatMap(_.split(" ")).map((_,1)).updateStateByKey((seq:Seq[Int],state:Option[Int])=> Some(seq.sum + state.getOrElse(0))).print()

    ssc
  }


  def main(args: Array[String]): Unit = {

    val checkpointDir = "api-test/spark-test/spark-streaming/checkpoint"

    // 注 ssc 的消费行为 必须放在 getOrCreateContext 函数内部，否则会抛出异常
    val ssc = StreamingContext.getOrCreate(checkpointDir,()=> getOrCreateContext(checkpointDir))

    ssc.start()
    ssc.awaitTermination()

  }

}
