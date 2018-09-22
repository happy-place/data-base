package com.big.data.spark.sql.exec

import java.util.Properties

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/20
  * Desc: 
  *
  */

object JdbcDF extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()
  val sc = spark.sparkContext

  // Note: JDBC loading and saving can be achieved via either the load/save or jdbc methods
  // Loading data from a JDBC source
  val jdbcDF = spark.read.format("jdbc")
                    .option("url", "jdbc:mysql://localhost:3306/recommend")
                    .option("dbtable", " Movie")
                    .option("user", "root")
                    .option("password", "root")
                    .load()

  println(jdbcDF.count())

  val connectionProperties = new Properties()
  connectionProperties.put("user", "root")
  connectionProperties.put("password", "root")
  val jdbcDF2 = spark.read.jdbc("jdbc:mysql://localhost:3306/recommend", "UserRecs", connectionProperties)

  // Saving data to a JDBC source
  // create table test.Movie like recommend.Movie
  jdbcDF.repartition(1).write
    .format("jdbc")
    .option("url", "jdbc:mysql://localhost:3306/test")
    .option("dbtable", "Movie")
    .option("user", "root")
    .option("password", "root")
    .save()

  jdbcDF2.repartition(1).write.jdbc("jdbc:mysql://localhost:3306/test", "UserRecs", connectionProperties)

  println(jdbcDF2.count())

  // 深度定制 列类型
  jdbcDF.write.option("createTableColumnTypes", "`mid` int(11) DEFAULT NULL")
    .option("createTableColumnTypes", "`name` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`descri` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`timelong` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`issue` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`shoot` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`language` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`genres` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`actors` text COLLATE utf8_bin")
    .option("createTableColumnTypes", "`directors` text COLLATE utf8_bin")
    .jdbc("jdbc:mysql://localhost:3306/test", "Movie3", connectionProperties)

}
