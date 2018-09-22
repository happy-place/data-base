package com.big.data.spark.rdd

import org.apache.spark.{SparkConf, SparkContext}
import scala.sys.process._

/**
  *  idea 直连集群开发
  * java.lang.ClassCastException: cannot assign instance of scala.collection.immutable.List$SerializationProxy to field org.apache.spark.rdd.RDD.org$apache$spark$rdd$RDD$$dependencies_ of type scala.collection.Seq in instance of org.apache.spark.rdd.MapPartitionsRDD
  */
object WordCountNotClusterNodeSubmit extends App{

  /*
    setMaster("local[1]")
    local 本地单线程
    local[*] 本地多线程
    local[2] 本地2 各线程
   */

  var master="spark://localhost:7077"
  var input= "hdfs://localhost:9000/tmp/spark/wc/in"
  var output="hdfs://localhost:9000/tmp/spark/wc/out"

  if (args.length>0){
    master=args(0)
    input = args(1)
    output = args(2)
  }

  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("yarn")
              .setJars(List("/Users/huhao/software/idea_proj/data-base/api-test/spark-test/spark-rdd/target/spark-rdd-1.0-SNAPSHOT.jar"))
              .setIfMissing("spark.driver.host", "127.0.0.1")

  val sc = new SparkContext(conf)

  // import scala.sys.process._ 通过管道命令提前清空输出目录，注意空行 init_dir 为执行 code
  val init_dir=s"hdfs dfs -rmr $output"!

  println(s"init_dir: $init_dir")

  try{
    val lines = sc.textFile(input,3)

    val words = lines.flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_).repartition(1).sortBy(_._2,false)
      .saveAsTextFile(output)
    // 本地local模式提价的打印信息在本地显示
    println(s"[CMD] hcat ${output}/*")

  }catch{
    case ex:Exception => println(ex.getCause)
  }finally {
    if(!sc.isStopped){
      sc.stop()
    }
  }



}
