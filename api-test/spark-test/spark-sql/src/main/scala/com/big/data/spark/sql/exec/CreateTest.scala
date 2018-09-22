package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.types.{IntegerType, StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}

case class ColTest(col1:String,col2:Int) extends Serializable

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/19
  * Desc: 
  *
  */

object CreateTes extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()
  val sc = spark.sparkContext

  try{

    val rdd=sc.parallelize(Seq(("a", 1), ("b", 1), ("a", 1)))

    rdd.cache()
    rdd.unpersist()
    rdd.map{line=>
      line._1
    }

    import spark.implicits._
    val df = rdd.toDF("name","age")
    df.show()

    df.printSchema()
    /*
    root
     |-- name: string (nullable = true)
     |-- age: integer (nullable = true)
     */

    // 不参与运算可直接取值
    df.select("name","age").show()
    // 参与运算 可使用 EL 表达式
    df.select(($"name").alias("myName") , $"age" +1).show()

    df.groupBy("name").count().show()

    val seq = Seq(ColTest("aa",1),ColTest("bb",2),ColTest("cc",3))

    // 基于集合创建DF
    val df2 = seq.toDF("name","age")

    val rdd121 = sc.textFile("hdfs://localhost:9000/tmp/spark/in/txt")
              .map{ line =>
                val data = line.split("\t")
                Row(data(0),data(1).toInt)
              }

    // schema 方式创建 df
    val fields = List("name", "age").map{
      case "name" => StructField("name", StringType, nullable = true)
      case "age" => StructField("age", IntegerType, nullable = true)
    }

    val schema = StructType(fields)

    // 注 RDD 的数据类型 必须 与 schema 严格一致
    val df121 = spark.createDataFrame(rdd121,schema)

    df121.show()




    // 基于 rdd 创建ds
    val ds = rdd.map{t=>ColTest(t._1,t._2)}.toDS()
    ds.show()

    // 基于集合创建DS
    val ds2 = seq.toDS()




  }catch {
    case ex:Exception => println(ex.getCause)
  }finally {
      spark.stop()
  }




}
