package com.big.data.spark.sql.onlinetest

import java.io.File
import org.apache.spark.SparkConf
import org.apache.spark.sql.{DataFrame, SparkSession}
import scala.sys.process._

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/21
  * Desc: 
  *
  */

case class Stock(ordernumber:String,locationid:String,dateid:String) extends Serializable
case class StockDetail(ordernumber:String, rownum:Int, itemid:String, number:Int, price:Double, amount:Double) extends Serializable
case class Date(dateid:String, years:Int, theyear:Int, month:Int, day:Int, weekday:Int, week:Int, quarter:Int, period:Int, halfmonth:Int) extends Serializable


object HiveSelectInsert {

  // 插入数据之前 表不存在
  private def insertHive(spark:SparkSession,table:String,data:DataFrame): Unit ={
    spark.sql("drop table if exists "+ table)
    data.write.saveAsTable(table)
  }

  private def insertMySQL(table:String,data:DataFrame): Unit ={
    data.write
      .format("jdbc")
      .option("url", "jdbc:mysql://localhost:3306/test")
      .option("dbtable", table)
      .option("user", "root")
      .option("password", "root")
      .save()
  }

  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder()
      .master("yarn-cluster")
      .appName(this.getClass.getSimpleName)
      .enableHiveSupport()
      .config("hive.exec.dynamic.partition", true) // 支持 Hive 动态分区
      .config("hive.exec.dynamic.partition.mode", "nonstrict") // 非严格模式
      .getOrCreate()

    import spark.implicits._

    import spark.sql

    try{
      // sql("drop table if exists watch_tmp2")
      // 动态分区
      sql("insert into datareport.vid_uid_tmp_test partition(dt) select * from datareport.t_vid_uid where dt in ('20180511','20180512')")

      val df = sql("select * from datareport.vid_uid_tmp_test where dt in ('20180511','20180512')").toDF("vid","uid","gold","dollar","diamond","day","country","dt")
      df.show(5)

    }finally {
      spark.stop()
    }




  }
}
