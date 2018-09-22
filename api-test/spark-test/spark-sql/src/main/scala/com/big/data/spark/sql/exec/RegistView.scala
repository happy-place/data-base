package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.{SaveMode, SparkSession}

import scala.sys.process._

case class Person(name:String,age:Int)

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/20
  * Desc: 
  *
  */
object RegistView extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()
  val sc = spark.sparkContext

  val catalog = spark.catalog

  try{

    val rdd=sc.parallelize(Seq(("a", 1), ("b", 2), ("a", 3)))
    rdd.foreach{case (a:String,b:Int) => println(s"$a : $b")}

    // 提供 rdd , df，ds 间的隐式转换支持
    import spark.implicits._

    rdd.map{case (name:String,age:Int) => Person(name,age)}.toDS()

    val df11 = rdd.map{case (name:String,age:Int) => (name,age)}.toDF("name","age").as[Person]

    // 基于rdd创建 df,并给各列取别名
//    val df = rdd.toDF().withColumnRenamed("_1","name").withColumnRenamed("_2","age")
    val df = rdd.toDF("name","age")
    df.show()

    df.printSchema()
    // 不参与运算
    df.select("name","age").filter($"age">2).show()
    // 参与运算
    df.select($"name",$"age"+1).show()

    // 注册临时视图，只对当前session 有效
    df.createOrReplaceTempView("df")

    // 缓存视图
    if (!catalog.isCached("df")){
      println("cache df")
      catalog.cacheTable("df")
    }

    // 注册全局视图，对所有session 一直有效
    df.createGlobalTempView("globalDF")

    // 执行sql 查询
    val df2 = spark.sql("select name,age from df where age >1 order by age desc")
    df2.show()

    val df22 = spark.sql("select name,age from global_temp.globalDF where age >1 order by age desc")
    df22.show()

    val rdd23=spark.newSession().sql("select name,age from global_temp.globalDF where age >1 order by age desc")
    rdd23.show()

    var rmCode = "hdfs dfs -rmr hdfs://localhost:9000/tmp/spark/df/out/tsv"!

    println(s"rmCode: $rmCode")

    /* tsv 需要伪装成为 scv 才能正常输出,如果未指定 format 则默认以 parquet 格式输出
       tsv 格式 读写
       SaveMode 》 Append 追加, Overwrite覆盖,ErrorIfExists如果存在就报错,Ignore 如果数据存在就忽略;
    */
    val saveOptions = Map("header"->"true","delimiter"->"\t","path"->"hdfs://localhost:9000/tmp/spark/df/out/tsv")
//    df2.write.format("csv").mode(SaveMode.Overwrite).options(saveOptions).save()
    df2.write.mode(SaveMode.Overwrite).options(saveOptions).save()

    spark.read.parquet("hdfs://localhost:9000/tmp/spark/df/out/parquet").show
    df2.write.parquet("hdfs://localhost:9000/tmp/spark/df/out/parquet")

    spark.sql("select * from parquet.`hdfs://localhost:9000/tmp/spark/df/out/tsv/*.parquet`").show()

    val df3 = spark.read.format("csv").options(saveOptions).load()
    df3.show()

    val df4 = spark.read.json("hdfs://localhost:9000/tmp/sparl/df/in/json/people.json")
    df4.show()

    spark.sql("select * from json.`hdfs://localhost:9000/tmp/sparl/df/in/json/people.json`").show()

    implicit val mapEncoder = org.apache.spark.sql.Encoders.kryo[Map[String,Any]]

    df4.map(person=> person.getValuesMap[Any](List("name","age"))).show()
    /*
    +--------------------+
    |               value|
    +--------------------+
    |[2E 01 02 39 01 0...|
    |[2E 01 02 39 01 0...|
    |[2E 01 02 39 01 0...|
    +--------------------+
     */
    df4.map(person=> person.getValuesMap[Any](List("name","age"))).collect()
    /*
    Array(Map(name -> Michael, age -> null), Map(name -> Andy, age -> 30), Map(name -> Justin, age -> 19))
     */


    // dataframe 转 dataset
    val ds = df4.as[Person]
    ds.show()



    rmCode = "hdfs dfs -rmr hdfs://localhost:9000/tmp/sparl/df/out/json/"!

    println(s"rmCode: $rmCode")

    df4.filter($"age" >21).show()
    df4.write.format("json").save("hdfs://localhost:9000/tmp/sparl/df/out/json")

    val map1 = Person("Yin",12)
    val map2 = Person("Gin",22)
    val map3 = Person("Zin",32)
    val strDS = spark.createDataset(Seq(Person("Gin",22),Person("Gin",22),Person("Zin",32)))
    strDS




//    // 模式匹配提取字段
//    df.map{
//      case Row(a:String,b:Int) => println(s"$a, $b")
//        a
//    }.show()
//
//    // 通过取下标方式获取
//    val rdd2 = df.map(t=>
//      (t.getString(0),t.getAs[Int]("_2"))
//    ).show()
//
//    // .field 方式获取属性
//    val ds = rdd.map{t=>ColTest1(t._1,t._2)}.toDS()
//    ds.map{t=>
//      (t.col1,t.col2)
//    }.show()
//
//    // case 匹配方式提取属性
//    ds.map {
//      case ColTest1(a,b) => (a,b)
//    }.show()

  }catch {
    case ex:Exception => println(ex.getCause)
  }finally {
    // 解除视图缓存
    if (catalog.isCached("df")){
      println("unpersist df")
      catalog.dropTempView("df")
    }
    spark.stop()
  }




}
