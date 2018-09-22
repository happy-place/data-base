package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.{Row, SparkSession}

case class ColTest1(col1:String,col2:Int) extends Serializable

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/19
  * Desc: 
  *
  */

object GetFields extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()
  val sc = spark.sparkContext

  try{

    val rdd=sc.parallelize(Seq(("a", 1), ("b", 1), ("a", 1)))

    // 直接提取
    rdd.map{line=>
      line._1
    }
    // 通过模式匹配提取
    rdd.map{
      case (a:String,b:Int) => println(s"$a , $b")
        a
    }.count


    import spark.implicits._
    val df = rdd.toDF()
    //val df = rdd.toDF().withColumnRenamed("_1","name").withColumnRenamed("_2","age")
    //val df = rdd.toDF("name","age")
    // 模式匹配提取字段
    df.map{
      case Row(a:String,b:Int) => println(s"$a, $b")
        a
    }.show()

    // 通过取下标方式获取
    val rdd2 = df.map(t=>
      (t.getString(0),t.getAs[Int]("_2"))
    ).show()

    // .field 方式获取属性
    val ds = rdd.map{t=>ColTest1(t._1,t._2)}.toDS()
    ds.map{t=>
      (t.col1,t.col2)
    }.show()

    // case 匹配方式提取属性
    ds.map {
      case ColTest1(a,b) => (a,b)
    }.show()

  }catch {
    case ex:Exception => println(ex.getCause)
  }finally {
      spark.stop()
  }




}
