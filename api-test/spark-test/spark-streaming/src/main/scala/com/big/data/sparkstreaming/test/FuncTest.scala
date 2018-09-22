package com.big.data.sparkstreaming.test

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/23
  * Desc: 
  *
  */

object FuncTest extends App{

  val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[2]").setAppName(this.getClass.getSimpleName)
  val ssc = new StreamingContext(conf, Seconds(1)) // 每 1 秒 一个批次

  // 设置检查点目录保存每次状态
  ssc.sparkContext.setCheckpointDir("api-test/spark-test/spark-streaming/checkpoint")


  val ds = ssc.socketTextStream("localhost", 9999)

    //1.无状态 wordcount :DStream 转换为 RDD 使用
    //    ds.transform(rdd=>rdd.flatMap(_.split(" "))).map((_,1)).reduceByKey(_+_).foreachRDD(_.foreach(println))

  //    val windowDS = ds.flatMap(_.split(" ")).map((_,1)).reduceByWindow((a:(String,Int),b:(String,Int)) => (a._1+b._1,a._2+b._2),Seconds(3),Seconds(2))
  //    windowDS.print()

    // 2.有状态无窗口计算
    //    val rddResult = ds.flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_)
    //    def updateMerge = (iters:Seq[Int],state:Option[Int]) => Some(iters.sum + state.getOrElse(0))
    //    val stateResult = rddResult.updateStateByKey[Int](updateMerge)
    //    stateResult.print()

    // 3.每3个批次合并出一个窗口，每隔2个批次合并一次，无状态保存
//    val windowDS = ds.window(Seconds(3),Seconds(2))
//
//    val windowResult = windowDS.flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_)
//    windowResult.print()

    // 4.有状态累计保存
    //    val stateWindowResult = windowDS.flatMap(_.split(" ")).map((_,1)).updateStateByKey((iter:Seq[Int],state:Option[Int])=> Some(iter.sum+state.getOrElse(0)))
    //    stateWindowResult.print()

    // 5.有状态累计保存 (全量汇总）
//    ds.flatMap(_.split(" ")).map((_,1)).reduceByKeyAndWindow((a:Int,b:Int)=>a+b,Seconds(3),Seconds(2))

    // 6.有状态累计保存 (增量汇总）第一次 汇总取 State1(rdd1+rdd2+rdd3) 这3个批次，第二次汇总取 State2(rdd2+rdd3+rdd4) 理论上是State1 + rdd4 - rdd1 = State2
    ds.flatMap(_.split(" ")).map((_,1)).reduceByKeyAndWindow(
      (a:Int,b:Int)=>a+b,
      (a:Int,b:Int)=>a-b,
      Seconds(3),
      Seconds(2)
    ).print()


    ssc.start()
    ssc.awaitTermination()

}
