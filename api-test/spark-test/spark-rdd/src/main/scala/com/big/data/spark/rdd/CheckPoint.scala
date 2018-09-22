package com.big.data.spark.rdd

import com.big.data.spark.rdd.WordCountClusterNodeSubmit.master
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/18
  * Desc: 
  *
  */

object CheckPoint extends App{

  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[*]")
  val sc = new SparkContext(conf)
  // 1.对 sc 设置检查点目录
  sc.setCheckpointDir("hdfs://localhost:9000/apps/spark/spark-rdd/checkpoint")
  // 2.创建rdd
  val rdd1 = sc.parallelize(1 to 100).map(_+1)
  // 3.手动触发rdd执行 checkpoint
  rdd1.checkpoint()
  // 4.对 rdd 执行 action 算子，才会真正存储数据到
  // hcat /apps/spark/spark-rdd/checkpoint/06cfe7ec-1017-4d57-9f73-d6545e250908/rdd-1
  // REPL 中可以检测缓存效果
  rdd1.count()


}
