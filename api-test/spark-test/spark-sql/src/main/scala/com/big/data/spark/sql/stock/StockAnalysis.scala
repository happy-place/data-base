package com.big.data.spark.sql.stock

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


object StockAnalysis {

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

    var rmCode = "rm -rf  spark-warehouse metastore_db"!

//    val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries", "1000")
    // 使用 注册视图方式 引入SQl
//    val spark = SparkSession.builder().config(sparkconf).getOrCreate()

    // 外置 hive  hdfs://localhost:9000/apps/spark/hive-warehouse
//    val warehouseLocation = new File("/apps/spark/hive-warehouse").getAbsolutePath
//    val spark = SparkSession
//      .builder()
//      .appName("Spark Hive Example")
//      .master("local[*]")
//      .config("spark.sql.warehouse.dir", warehouseLocation)
//      .enableHiveSupport()
//      .getOrCreate()

    // 内置 hive
    val spark = SparkSession
      .builder()
      .appName("Spark Hive Example")
      .master("local[*]")
      .config("spark.sql.warehouse.dir", "api-test/spark-test/spark-dataframe/spark-warehouse")
      .enableHiveSupport()
      .getOrCreate()

    import spark.implicits._

    /*
      数据源加载：
      方案1：使用 Dataset 组织
      方案2：使用 Dataframe 组织
     */

    // RDD => DS
    //  val stockRdd = spark.sparkContext.textFile("api-test/spark-test/spark-dataframe/src/main/resources/tbStock.txt")
    //
    //  val stockDS = stockRdd.map(_.split(",")).map(attr=> Stock(attr(0),attr(1),attr(2))).toDS
    //  stockDS.show(5)
    //
    //  val stockDetailRdd = spark.sparkContext.textFile("api-test/spark-test/spark-dataframe/src/main/resources/tbStockDetail.txt")
    //
    //  val stockDetailDS = stockDetailRdd.map(_.split(",")).map(attr=> StockDetail(attr(0),attr(1).trim().toInt,attr(2),attr(3).trim().toInt,attr(4).trim().toDouble, attr(5).trim().toDouble)).toDS
    //
    //  stockDetailDS.show(5)
    //
    //  val dateRdd = spark.sparkContext.textFile("api-test/spark-test/spark-dataframe/src/main/resources/tbDate.txt")
    //
    //  val dateDS = dateRdd.map(_.split(",")).map(attr=> Date(attr(0),attr(1).trim().toInt, attr(2).trim().toInt,attr(3).trim().toInt, attr(4).trim().toInt, attr(5).trim().toInt, attr(6).trim().toInt, attr(7).trim().toInt, attr(8).trim().toInt, attr(9).trim().toInt)).toDS
    //
    //  dateDS.show(5)
    //
    //  stockDS.createOrReplaceTempView("tbStock")
    //
    //  dateDS.createOrReplaceTempView("tbDate")
    //
    //  stockDetailDS.createOrReplaceTempView("tbStockDetail")

    // DF
    val stockDF = spark.read.csv("api-test/spark-test/spark-dataframe/src/main/resources/tbStock.txt").toDF("ordernumber", "locationid", "dateid")

    val dateDF = spark.read.csv("api-test/spark-test/spark-dataframe/src/main/resources/tbDate.txt").toDF("dateid", "years", "theyear", "month", "day", "weekday", "week", "quarter", "period", "halfmonth")

    val stockDetailDF = spark.read.csv("api-test/spark-test/spark-dataframe/src/main/resources/tbStockDetail.txt").toDF("ordernumber", "rownum", "itemid", "number", "price", "amount")

    /*
      引入SQL 语义
      方案1：注册临时视图，消耗的是 spark节点的内存
      方案2：数据存储到hive, 可重复消费，存储空间不受限
          1) 使用外置hive
            a.拷贝 hive-site.xml 到resource 目录下，
            b. sparkSession 中配置
                .config("spark.sql.warehouse.dir", warehouseLocation)
                .enableHiveSupport()
            c.开启 hiveserver2
          2) 使用内置hive
              sparkSession 中配置 .enableHiveSupport()


     */

//    stockDF.createOrReplaceTempView("tbStock")
//
//    dateDF.createOrReplaceTempView("tbDate")
//
//    stockDetailDF.createOrReplaceTempView("tbStockDetail")

    insertHive(spark,"tbStock",stockDF)
    insertHive(spark,"tbDate",dateDF)
    insertHive(spark,"tbStockDetail",stockDetailDF)

    // 统计历年销售单数，销售总额
    val result1 = spark.sql("SELECT c.theyear, COUNT(DISTINCT a.ordernumber), SUM(b.amount) FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber JOIN tbDate c ON a.dateid = c.dateid GROUP BY c.theyear ORDER BY c.theyear")
    result1.show()
    insertMySQL("yearly_sales",result1)

    // 统计每一个订单的销售额
    val result2 = spark.sql("SELECT a.dateid, a.ordernumber, SUM(b.amount) AS SumOfAmount FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber GROUP BY a.dateid, a.ordernumber")
    result2.show()
    insertMySQL("order_sales",result2)

    // 统计每年最大销售
    val result3 = spark.sql("SELECT theyear, MAX(c.SumOfAmount) AS SumOfAmount FROM (SELECT a.dateid, a.ordernumber, SUM(b.amount) AS SumOfAmount FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber GROUP BY a.dateid, a.ordernumber ) c JOIN tbDate d ON c.dateid = d.dateid GROUP BY theyear ORDER BY theyear DESC")
    result3.show()
    insertMySQL("yearly_max_sales",result3)


    // 统计每年每个货品的销售额
    val result4 = spark.sql("SELECT c.theyear, b.itemid, SUM(b.amount) AS SumOfAmount FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber JOIN tbDate c ON a.dateid = c.dateid GROUP BY c.theyear, b.itemid")
    result4.show()
    insertMySQL("yearly_item_sales",result4)

    // 统计每年每个货品中的最大销售额
    val result5 = spark.sql("SELECT d.theyear, MAX(d.SumOfAmount) AS MaxOfAmount FROM (SELECT c.theyear, b.itemid, SUM(b.amount) AS SumOfAmount FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber JOIN tbDate c ON a.dateid = c.dateid GROUP BY c.theyear, b.itemid ) d GROUP BY d.theyear")
    result5.show()
    insertMySQL("yearly_item_max_sales",result5)

    // 统计每年最畅销的商品(以销售额为参考基准)
    val result6 = spark.sql("SELECT DISTINCT e.theyear, e.itemid, f.maxofamount FROM (SELECT c.theyear, b.itemid, SUM(b.amount) AS sumofamount FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber JOIN tbDate c ON a.dateid = c.dateid GROUP BY c.theyear, b.itemid ) e JOIN (SELECT d.theyear, MAX(d.sumofamount) AS maxofamount FROM (SELECT c.theyear, b.itemid, SUM(b.amount) AS sumofamount FROM tbStock a JOIN tbStockDetail b ON a.ordernumber = b.ordernumber JOIN tbDate c ON a.dateid = c.dateid GROUP BY c.theyear, b.itemid ) d GROUP BY d.theyear ) f ON e.theyear = f.theyear AND e.sumofamount = f.maxofamount ORDER BY e.theyear")
    result6.show()
    insertMySQL("yearly_hot_item",result6)

  }
}
