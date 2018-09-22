package com.big.data.spark.rdd

import org.apache.hadoop.io.{IntWritable, LongWritable, Text}
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat
import org.apache.spark.rdd.JdbcRDD
import org.apache.spark.{SparkConf, SparkContext}

import scala.sys.process._
/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/18
  * Desc: 
  *
  */


case class Person(name:String,age:Int)

object InputOutput extends App{

  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[*]")
  val sc = new SparkContext(conf)

  // 读取纯文本文件
  val rdd1 = sc.textFile("/Users/huhao/software/virtual_space/tmp")

  val rmCode1 = "hdfs dfs -rmr hdfs://localhost:9000/tmp/spark/out/text"!

  println(s"rmCode1: $rmCode1")
  // 保存RDD到hdfs 可采用适当压缩格式
  rdd1.saveAsTextFile("hdfs://localhost:9000/tmp/spark/out/text" /*,classOf[com.hadoop.compression.lzo.LzopCodec]*/)

  // 保存为SeqFile, 读取SeqFile
  val rdd2 = sc.parallelize(List((1,"a"),(2,"b"),(3,"c")),2)

  val rmCode2 = "hdfs dfs -rmr hdfs://localhost:9000/tmp/spark/out/seq"!

  println(s"rmCode2: $rmCode2")

  rdd2.saveAsSequenceFile("hdfs://localhost:9000/tmp/spark/out/seq") // KV 必须是可 hash 对象，Char 不允许使用

  val rdd3 = sc.sequenceFile("hdfs://localhost:9000/tmp/spark/out/seq",classOf[String],classOf[String])
  rdd3.foreach(println)

  val rmCode22 = "hdfs dfs -rmr hdfs://localhost:9000/tmp/spark/out/hadoop"!

  println(s"rmCode22: $rmCode22")

  rdd2.saveAsNewAPIHadoopFile("hdfs://localhost:9000/tmp/spark/out/hadoop",
      classOf[LongWritable],
      classOf[Text],
      classOf[org.apache.hadoop.mapreduce.lib.output.TextOutputFormat[LongWritable,Text]])

  val rdd22 = sc.newAPIHadoopFile("hdfs://localhost:9000/tmp/spark/out/hadoop",classOf[KeyValueTextInputFormat],classOf[Text],classOf[Text])

  rdd22.foreach(println)

  val rdd4 = sc.makeRDD(Array(Person("aa",12),Person("bb",13),Person("cc",14)))

  val rmCode3 = "hdfs dfs -rmr hdfs://localhost:9000/tmp/spark/out/obj"!

  println(s"rmCode3: $rmCode3")

  rdd4.saveAsObjectFile("hdfs://localhost:9000/tmp/spark/out/obj")
  val rdd5 = sc.objectFile("hdfs://localhost:9000/tmp/spark/out/obj")
  rdd5.foreach(println)

  // JDBCRDD
  val rdd6 = new JdbcRDD(
    sc,
    getConnection = ()=>{
      Class.forName("com.mysql.jdbc.Driver").newInstance()
      java.sql.DriverManager.getConnection("jdbc:mysql://localhost:3306/test","root","root")
    },
    sql="select * from staff where id >=? and id <=?",
    lowerBound=1,
    upperBound=10,
    numPartitions=2,
    mapRow = r=>(r.getInt(1),r.getString(2),r.getString(3))
  )

  rdd6.foreach(println)

  rdd6.map{case(id,name,gender) => (id+20,name.toUpperCase,gender)}
      .foreachPartition{ it =>
         val getConnection = ()=>{
            Class.forName("com.mysql.jdbc.Driver").newInstance()
            java.sql.DriverManager.getConnection("jdbc:mysql://localhost:3306/test","root","root")
          }

          val conn = getConnection()
          conn.setAutoCommit(false)
          val statement = conn.createStatement()
          it.foreach(row =>
          row match {
            case (id,name,gender)=>{
              statement.addBatch(s"insert into staff values($id,'$name','$gender')")
            }
          })
          statement.executeBatch()
          conn.commit()
      }
}
