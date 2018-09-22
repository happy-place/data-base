package com.big.data.spark.rdd

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/18
  * Desc: 
  *
  */

object BroadcastTest extends App{

  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[*]")
  val sc = new SparkContext(conf)

  try{
    // 定义全局共享变量
    val targetSet = Set(1,2,3)
    // 广播共享变量
    val broadcastSet = sc.broadcast(targetSet)

    val rdd1 = sc.makeRDD(Array((1,4,5),(2,3,6),(9,6,1)),3)
    rdd1.map(t=>{
      // 使用广播变量
      t.productIterator.asInstanceOf[Iterator[Int]].filter(!broadcastSet.value.contains(_)).mkString("|")
    }).foreach(println)
  }finally {
    if(sc.isStopped){
      sc.stop()
    }
  }





}
