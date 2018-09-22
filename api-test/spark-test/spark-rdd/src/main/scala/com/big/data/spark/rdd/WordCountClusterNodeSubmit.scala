package com.big.data.spark.rdd

import org.apache.spark.{SparkConf, SparkContext}

import scala.sys.process._

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/17
  * Desc: 
  *  提交 spark节点本地提交到集群运行
  *
jar=/Users/huhao/software/idea_proj/data-base/api-test/spark-test/spark-rdd/target/wordcount-test-jar-with-dependencies.jar
master='local[*]'
input='hdfs://localhost:9000/tmp/spark/wc/in'
output='hdfs://localhost:9000/tmp/spark/wc/out'

/Users/huhao/software/spark-2.1.1-bin-hadoop2.7/bin/spark-submit \
--class com.big.data.spark.rdd.WordCountTest \
--deploy-mode cluster \
--master spark://localhost:7077 \
--executor-memory 1G \
--total-executor-cores 2 \
${jar} ${master} ${input} ${output}

  */

object WordCountClusterNodeSubmit extends App{

  /*
    setMaster("local[1]")
    local 本地单线程
    local[*] 本地多线程
    local[2] 本地2 各线程
   */

//  var master="local[*]"
  var master="local[*]"
  var input= "hdfs://localhost:9000/tmp/spark/wc/in"
  var output="hdfs://localhost:9000/tmp/spark/wc/out"

  if (args.length>0){
    master=args(0)
    input = args(1)
    output = args(2)
  }

  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster(master)
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


    val seq=Seq((1,List('a','b')),(2,List('A','B')))
    val rdd1=sc.makeRDD(seq)
    val rdd2=rdd1.mapPartitions(iter=>{
      val list = scala.collection.mutable.ListBuffer[String]()
      for(t<-iter){
        list.append(t._2.mkString("|"))
      }
      list.iterator
    })

  }catch{
    case ex:Exception => println(ex.getCause)
  }finally {
    if(!sc.isStopped){
      sc.stop()
    }
  }



}
