package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

import scala.sys.process._

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/20
  * Desc: 
  *
  */

object ParquetMergeSchame extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()
  val sc = spark.sparkContext

  import spark.implicits._

  try{
    val df1 = sc.makeRDD(1 to 5).map(i => (i, i * 2)).toDF("single", "double")

    var rmCode = "hdfs dfs -rmr -skipTrash /tmp/spark/out/parquet/test_table/key=1"!

    df1.write.parquet("hdfs://localhost:9000/tmp/spark/out/parquet/test_table/key=1")

    // Create another DataFrame in a new partition directory,
    // adding a new column and dropping an existing column
    val df2 = sc.makeRDD(6 to 10).map(i => (i, i * 3)).toDF("single", "triple")

    rmCode = "hdfs dfs -rmr -skipTrash /tmp/spark/out/parquet/test_table/key=2"!

    df2.write.parquet("hdfs://localhost:9000/tmp/spark/out/parquet/test_table/key=2")

    // Read the partitioned table
    val df3 = spark.read.option("mergeSchema", "true").parquet("hdfs://localhost:9000/tmp/spark/out/parquet/test_table")
    df3.printSchema()
    df3.show()

  }finally {
    spark.stop()
  }



}
