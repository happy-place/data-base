package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/20
  * Desc: 
  *
  */

object UDFTest extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()
  val sc = spark.sparkContext

  try{
    spark.udf.register("toUpper",(x:String)=>x.toUpperCase())
    val df = spark.read.json("hdfs://localhost:9000/tmp/sparl/df/in/json/people.json")
    df.createOrReplaceTempView("people")

    val df2 = spark.sql("select toUpper(name),age from people")
    df2.show()
  }finally {
    spark.stop()
  }




}
