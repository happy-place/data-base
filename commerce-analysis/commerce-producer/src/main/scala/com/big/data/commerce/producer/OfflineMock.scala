package com.big.data.commerce.producer

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import java.util.UUID

import com.big.data.commerce.common._
import org.apache.commons.lang3.time.DateFormatUtils
import org.apache.spark.SparkConf
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.slf4j.LoggerFactory

import scala.collection.mutable.ArrayBuffer
import scala.util.Random


/**
  * 用于生成模拟数据
  */
object OfflineMock {

  //用于生成用户数据
  /**
    * 数量：100
    *
    *  user_id      用户的ID[1 - 100]
    *  username     用户的名称[user + id]
    *  name         用户的姓名[name + id]
    *  age          用户的年龄[1 - 60]
    *  professional 用户的职业[profess + [1 - 100]
    *  city         用户所在的城市[1 - 10]
    *  sex          用户的性别[male,female]
    */
  def userInfoGenerate(): Array[UserInfo] = {
    val array = ArrayBuffer[UserInfo]()
    val sexes = Array("male", "female")
    //生成随机数的工具类
    val random = new Random()

    for (i <- 0 to 100) {
      val user_id = i
      val username = "user" + user_id
      val name = "name" + user_id
      val age = random.nextInt(60)
      val professional = "profess" + random.nextInt(100)
      val city = random.nextInt(10)
      val sex = sexes(random.nextInt(2))

      array += UserInfo(user_id, username, name, age.toString, professional, city.toString, sex)
    }

    array.toArray
  }

  //用于生成物品数据
  /**
    * 数量：100
    *
    *  product_id   商品的ID[1 - 100]
    *  product_name 商品的名称[product + id]
    *  extend_info  是否为自营商品 [0,1]
    */
  def productInfoGenerate(): Array[ProductInfo] = {
    val array = ArrayBuffer[ProductInfo]()
    val random = new Random()

    for (i <- 0 to 100) {
      val product_id = i
      val product_name = "product" + product_id
      val extend_info = random.nextInt(2)

      array += ProductInfo(product_id, product_name, extend_info.toString)

    }
    array.toArray
  }

  //用于生成行为数据
  /**
    * 100个用户 => 每个用户10个Session => 每个Session100以内随机Action  ("search", "click", "order", "pay")不能同时出现
    *
    *  date               Session发生的日期yyyy-MM-dd
    *  user_id            用户的ID[1 - 100]
    *  session_id         sessionde唯一标识UUID
    *  page_id            用户点击的页面[1 - 10]
    *  action_time        行为发生的具体时间yyyy-MM-dd hh:mm:ss
    *  search_keyword     搜索的关键字，从("火锅", "蛋糕", "重庆辣子鸡", "重庆小面", "呷哺呷哺", "新辣道鱼火锅", "国贸大厦", "太古商场", "日本料理", "温泉")
    *  click_category_id  点击的物品的类别ID[1 - 100]
    *  click_product_id   点击的物品ID类[1 - 100]
    *  order_categroy_ids 下单的物品的类别ID[1 - 100]
    *  order_product_ids  下单的物品ID[1 - 100]
    *  pay_product_ids    支付的物品ID[1 - 100]
    *  pay_categroy_ids   支付的物品的类别的ID[1 - 100]
    *  city_id            行为发生的城市[1 - 10]
    */
  def userVisitActionGenerate(): Array[UserVisitAction] = {
    val array = ArrayBuffer[UserVisitAction]()
    val random = new Random()



    val action = Array("search", "click", "order", "pay")
    val keywords = Array("火锅", "蛋糕", "重庆辣子鸡", "重庆小面", "呷哺呷哺", "新辣道鱼火锅", "国贸大厦", "太古商场", "日本料理", "温泉")

    //用户级别
    for (x <- 0 to 100) {
      val date = DateFormatUtils.format(System.currentTimeMillis(), "yyyy-MM-dd")
      val user_id = x
      val city_id = random.nextInt(10)

      //Session级别
      for (y <- 0 to 10) {
        val session_id = UUID.randomUUID().toString
        val dateHour = date + " " + Utils.fullFill(random.nextInt(24).toString)
        //行为级别
        for (z <- 0 to random.nextInt(100)) {
          val page_id = random.nextInt(10)
          val action_time = dateHour + ":" +
            Utils.fullFill(random.nextInt(60).toString) + ":" +
            Utils.fullFill(random.nextInt(60).toString)

          var search_keyword = "-1"
          var click_category_id = "-1"
          var click_product_id = "-1"
          var order_category_id = "-1"
          var order_product_id = "-1"
          var pay_category_id = "-1"
          var pay_product_id = "-1"

          action(random.nextInt(4)) match {
            case "search" => search_keyword = keywords(random.nextInt(10))
            case "click" => click_category_id = random.nextInt(100).toString; click_product_id = random.nextInt(100).toString
            case "order" => order_category_id = random.nextInt(100).toString; order_product_id = random.nextInt(100).toString
            case "pay" => pay_category_id = random.nextInt(100).toString; pay_product_id = random.nextInt(100).toString
          }

          array += UserVisitAction(date, user_id, session_id, page_id.toString, action_time, search_keyword, click_category_id,
            click_product_id, order_category_id, order_product_id, pay_product_id, pay_category_id, city_id.toString)

        }

      }

    }

    array.toArray
  }

  //插入到HIVE
  def saveInDataWarehouse(spark: SparkSession, table: String, data: DataFrame): Unit = {
    spark.sql("DROP TABLE IF EXISTS " + table)
    data.write.saveAsTable(table)
  }

  def main(args: Array[String]): Unit = {

    val logger = LoggerFactory.getLogger(this.getClass)

    //创建sparkConf
    val sparkConf = new SparkConf().setAppName("mock").setMaster("local[*]")

    //创建SparkSession
    val spark = SparkSession.builder().config(sparkConf).enableHiveSupport().getOrCreate()

    //创建Mock数据
    val userInfoData = this.userInfoGenerate()
    val productInfoData = this.productInfoGenerate()
    val userVisitActionData = this.userVisitActionGenerate()

    import spark.implicits._
    //将Mock数据转换成RDD，DF
    val userInfoDF = spark.sparkContext.makeRDD(userInfoData).toDF
    val productInfoDF = spark.sparkContext.makeRDD(productInfoData).toDF
    val userVisitActionDF = spark.sparkContext.makeRDD(userVisitActionData).toDF

    userInfoDF.show(10)
    productInfoDF.show(10)
    userVisitActionDF.show(10)

    //将数据save到Hive
    saveInDataWarehouse(spark,Constants.TABLE_USER_INFO, userInfoDF)
    saveInDataWarehouse(spark,Constants.TABLE_PRODUCT_INFO, productInfoDF)
    saveInDataWarehouse(spark,Constants.TABLE_USER_VISIT_ACTION, userVisitActionDF)

    //关闭Spark
    spark.stop()
  }
}
