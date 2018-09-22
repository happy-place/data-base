package com.big.data.spark.sql.exec

import java.io.File

import org.apache.spark.sql.{Row, SparkSession}

case class Record(key: Int, value: String)

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/20
  * Desc: 
  *
  */

object HiveEnableSql extends App{

  // warehouseLocation points to the default location for managed databases and tables
  val warehouseLocation = new File("api-test/spark-test/spark-dataframe/spark-warehouse").getAbsolutePath

  val spark = SparkSession
    .builder()
    .appName("Spark Hive Example")
    .master("local[*]")
    .config("spark.sql.warehouse.dir", warehouseLocation)
    .enableHiveSupport()
    .getOrCreate()

  import spark.implicits._
  import spark.sql

  try{
    // 数据重跑初始化
    sql("drop table if exists src")
    // 必须指定 分隔符，默认分隔符为 ','
    sql("CREATE TABLE IF NOT EXISTS src (key INT, value STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\t'")
    sql("LOAD DATA LOCAL INPATH '/Users/huhao/software/idea_proj/data-base/api-test/spark-test/spark-dataframe/src/main/resources/kv1.txt' INTO TABLE src")

    // Queries are expressed in HiveQL
    sql("SELECT * FROM src").show()
    // +---+-------+
    // |key|  value|
    // +---+-------+
    // |238|val_238|
    // | 86| val_86|
    // |311|val_311|
    // ...

    // Aggregation queries are also supported.
    sql("SELECT COUNT(*) FROM src").show()
    // +--------+
    // |count(1)|
    // +--------+
    // |    500 |
    // +--------+

    // The results of SQL queries are themselves DataFrames and support all normal functions.
    val sqlDF = sql("SELECT key, value FROM src WHERE key < 10 ORDER BY key")

    // The items in DataFrames are of type Row, which allows you to access each column by ordinal.
    val stringsDS = sqlDF.map {
      case Row(key: Int, value: String) => s"Key: $key, Value: $value"
    }
    stringsDS.show()
    // +--------------------+
    // |               value|
    // +--------------------+
    // |Key: 0, Value: val_0|
    // |Key: 0, Value: val_0|
    // |Key: 0, Value: val_0|
    // ...

    // You can also use DataFrames to create temporary views within a SparkSession.
    val recordsDF = spark.createDataFrame((1 to 100).map(i => Record(i, s"val_$i")))
    recordsDF.createOrReplaceTempView("records")

    // Queries can then join DataFrame data with data stored in Hive.
    sql("SELECT * FROM records r JOIN src s ON r.key = s.key").show() // 内连接
    // +---+------+---+------+
    // |key| value|key| value|
    // +---+------+---+------+
    // |  2| val_2|  2| val_2|
    // |  4| val_4|  4| val_4|
    // |  5| val_5|  5| val_5|
    // ...

  }finally {
    spark.stop()
  }




}
