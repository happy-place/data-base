package com.big.data.spark.rdd

import org.apache.spark.rdd.RDD
import org.apache.spark.{HashPartitioner, Partitioner, SparkConf, SparkContext}

import scala.collection.immutable.HashMap
import scala.sys.process._

case class Student(name:String,lesson:String,score:Int)

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/17
  * Desc: 
  *  提交 spark节点本地提交到集群运行
  *

/Users/huhao/software/spark-2.1.1-bin-hadoop2.7/bin/spark-submit \
--class com.big.data.spark.rdd.WordCountClusterNodeSubmit \
--master yarn \
--executor-memory 1G \
--total-executor-cores 2 \
/Users/huhao/software/idea_proj/data-base/api-test/spark-test/spark-rdd/target/spark-rdd.jar



  */

object RDDTest extends App{


  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[*]")
  val sc = new SparkContext(conf)

  try{
//    val rdd1=sc.makeRDD(Array('a','b','c','d'),2)
//    val rdd2=rdd1.mapPartitions(iter => {
//      Iterator(iter.mkString("|"))
//    })
//    rdd2.foreach(println)
//
//    val rdd3 = sc.makeRDD(Array('a','b','c','d'),2)
//    val rdd4 = rdd3.mapPartitionsWithIndex((idx,iter)=> Iterator(idx+":"+iter.mkString("|")))
//    rdd4.foreach(println)

//    val rdd5 = sc.makeRDD(Array('a','b','c','d','e','f'))
//    val rdd6 = rdd5.sample(false,0.6,0l)
//    rdd6.foreach(println)

//    val rdd7 = sc.makeRDD(Array('a','a','c'))
//    val rdd8 = sc.makeRDD(Array('a','b','d'))
//    val rdd9 = rdd7.union(rdd8)  // 并集不去重 rdd7 + rdd8
//    val rdd10 = rdd7.subtract(rdd8) // 差集 去重 rdd7 - rdd8
//    val rdd11 = rdd7.intersection(rdd8) // 交集去重
//
//    rdd9.foreach(println)
//    rdd10.foreach(println)
//    rdd11.foreach(println)
//    println(rdd7.distinct())

//    val rdd12 = sc.makeRDD(Array(('a',List(1,2)),('b',List(2,3)),('c',List(3,4,5))))
//    val rdd13 = rdd12.partitionBy(new Partitioner {
//      override def numPartitions: Int = 2
//      override def getPartition(key: Any): Int = key.toString.hashCode % numPartitions
//    })
//
//    rdd13.mapPartitionsWithIndex((idx,iter)=> Iterator(idx+":"+iter.mkString("|"))).foreach(println)
//
//    rdd13.preferredLocations(rdd13.partitions(0)).foreach(println)
//    rdd13.preferredLocations(rdd13.partitions(1)).foreach(println)

//      val rdd14 = sc.makeRDD("hello,world")
//      rdd14.map((_,1)).reduceByKey(_+_).foreach(println)

    // 针对 KV 结构 RDD 依据 key 进行聚合
//    val rdd15 = sc.makeRDD(Array((1,'a'),(2,'b'),(1,'c'),(2,'d'),(1,'e')))
//    rdd15.groupByKey().map(t=>t._1+":"+t._2.mkString("|")).foreach(println)
//
//    // 针对 KV 结构，自定义 Partitioner
//    val rdd16 = sc.makeRDD(Array((1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e')))
//    rdd16.groupByKey(new Partitioner{
//      override def numPartitions: Int = 2
//      override def getPartition(key: Any): Int = key.toString.hashCode % numPartitions
//    }).mapPartitionsWithIndex((idx,iter)=>Iterator(idx+":"+iter.toMap.values.mkString("|") )).foreach(println)


//    def combineByKey[C](
//                         createCombiner: V => C,
//                         mergeValue: (C, V) => C,
//                         mergeCombiners: (C, C) => C): RDD[(K, C)] = self.withScope {
//      combineByKeyWithClassTag(createCombiner, mergeValue, mergeCombiners)(null)
//    }

//    scala> rdd1.combineByKey(
//      |       (v : Int) => v + "_",
//    |       (c : String, v : Int) => c + "@" + v,
//    |       (c1 : String, c2 : String) => c1 + "$" + c2
//    |     ).collect
//    res60: Array[(String, String)] = Array((A,2_$1_), (B,1_$2_), (C,1_))

//    val rdd17 = sc.makeRDD(Array("hello,world")).
//    val avgScoresRDD = rdd17.combineByKey(
//      (line: String) => () ,
//      (acc: (Float, Int), x: ScoreDetail) => (acc._1 + x.score, acc._2 + 1) /*mergeValue*/,
//      (acc1: (Float, Int), acc2: (Float, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2) /*mergeCombiners*/
//      // calculate the average
//    ).map( { case(key, value) => (key, value._1/value._2) })
//
//    avgScoresRDD.collect.foreach(println)

//    val students:List[Student] = List[Student](
//      Student("aa","english",98),
//      Student("aa","math",92),
//      Student("aa","chinese",91),
//      Student("bb","english",91),
//      Student("bb","english",83),
//      Student("cc","math",98),
//      Student("cc","english",92),
//      Student("cc","chinese",98)
//    )
//
//    val getStu = for (i <- students) yield (i.name,i)
//    val stuRDD = sc.parallelize(getStu).partitionBy(new HashPartitioner(3)).cache()
//    stuRDD.combineByKey(
//      (stu:Student) => (stu.score,1),  // map
//      (acc:(Int,Int),stu:Student) => (acc._1 + stu.score,acc._2+1), // partitial merge
//      (acc1:(Int,Int),acc2:(Int,Int)) => (acc1._1 + acc2._1,acc1._2 + acc2._2) // global merge
//    ).map(t=>(t._1,t._2._1 / t._2._2)).foreach(println)

//    val rdd18 = sc.makeRDD(Array(1,2,3,4),2)  // 0:1|2 1:3|4
//
//    rdd18.mapPartitionsWithIndex((idx,iter)=>Iterator(idx+":"+iter.mkString("|"))).foreach(println)
//
//
//    val value = rdd18.aggregate(1)(
//      (x:Int,y:Int) => x*y,
//      (x:Int,y:Int) => x+y
//    )
//    /*
//      (初始值)1*1 => 1 , 1*2 => 2
//      (初始值)1*3 => 3 , 3*4 => 12
//      (初始值)1 + 2 + 12 => 15
//     */
//
//    println(value)

//    val rdd19 =sc.makeRDD("hello,world").map((_,1)).countByKey().foreach(println)
//    // map 内部可以通过模式匹配 进行拆分 ，必须使用 大括号
//    sc.makeRDD(Array(('a',1),('b',2))).map{case (k,v) => (v,k)}.collect().foreach(println)
//
//    val rdd20 = sc.makeRDD(Array((1,(2,3)),(2,(2,3)),(3,(2,3))))
//    rdd20.flatMap{case (a,(b,c)) => List(a,b,c)}.collect().foreach(println)

//    val rdd21 = sc.makeRDD(1 to 100)
//    rdd21.sample(false,0.2,10).foreach(println)
//
//    val rdd22 =sc.makeRDD("hello,world").map((_,1)).groupByKey().map(t=>(t._1,t._2.sum)).foreach(println)

//    val rdd23 = sc.makeRDD(Array((1,2),(1,3),(2,3),(2,4),(3,6),(3,8)),3)
    // 0:(1,2)(1,3) 1:(2:3)(2:4) 2:(3,6)(3,8)
    // 0分区 max(2,3) => 3 , (初始值)0 + 3 = 3 => (1,3)
//    rdd23.aggregateByKey(0)(math.max(_,_),_+_).foreach(println)

//    val rdd24 = sc.makeRDD(Array(('a',2),('a',3),('b',3),('b',4),('c',6),('c',8)),3)
//
//    rdd24.foldByKey(0)(_+_).sortByKey(true,1).foreach(println)
//
//    rdd24.foldByKey(0)(_+_).sortBy(_._1,true,1).foreach(println)

//      val rdd25 = sc.makeRDD(Array(('a',1),('b',2)))
//      val rdd26 = sc.makeRDD(Array(('a',10),('c',20)))

    // join 内连接
    //  rdd25.join(rdd26).map(t=>(t._1,math.max(t._2._1,t._2._2))).foreach(println)
    // 外连接
//    rdd25.leftOuterJoin(rdd26).map(t=>(t._1,math.max(t._2._1,t._2._2.getOrElse(0)))).foreach(println)

//    val rdd27 = sc.makeRDD(Array(('a',1),('a',2),('b',2),('b',3)))
//    val rdd28 = sc.makeRDD(Array(('a',10),('a',20),('b',22),('b',33)))
//    // 各 rdd 内部先聚合 然后再基于key 合并
//    rdd27.cogroup(rdd28).foreach(println)
//
//    rdd27.union(rdd28).groupByKey().foreach(println)
//
//    val rdd29 = sc.parallelize(1 to 3)
//    val rdd30 = sc.parallelize(3 to 5)
//    rdd29.cartesian(rdd30).foreach(println) // rdd29 * rdd30 构建笛卡尔集
//    rdd29.zip(rdd30).foreach(println) // 基于下标构建拉链

    // 每个分区执行一次 shell 命令，且该命令必须存储在 本地，而不是 hdfs （需要注意权限，路径)
//    val rdd31 = sc.makeRDD(Array(1,2,3),2)
//    rdd31.pipe("/Users/huhao/software/virtual_space/tmp/doecho.sh").collect().foreach(println)

//    val rdd32 = sc.parallelize(1 to 100,5)
//    // coalesce -> false 只在map 节点进行分区压缩，不发生shuffle,当为 true 时，等效于 repartition
//    rdd32.filter(_%2 !=0).coalesce(2,false).mapPartitionsWithIndex((idx,iter)=>Iterator(idx+":"+iter.mkString("|"))).foreach(println)
//    // 1:41|43|45|47|49|51|53|55|57|59|61|63|65|67|69|71|73|75|77|79|81|83|85|87|89|91|93|95|97|99
//    // 0:1|3|5|7|9|11|13|15|17|19|21|23|25|27|29|31|33|35|37|39
//
//    // 会发生shufle
//    rdd32.filter(_%2 !=0).repartition(2).mapPartitionsWithIndex((idx,iter)=>Iterator(idx+":"+iter.mkString("|"))).foreach(println)
//    // 1:3|7|11|15|19|23|27|31|35|39|43|47|51|55|59|63|67|71|75|79|83|87|91|95|99
//    // 0:1|5|9|13|17|21|25|29|33|37|41|45|49|53|57|61|65|69|73|77|81|85|89|93|97

//    val rdd33 = sc.makeRDD(Array((1,'a'),(2,'b'),(3,'c'),(4,'d')),2)
//    rdd33.mapPartitionsWithIndex((idx,iter) => Iterator(idx+":"+iter.mkString("|"))).foreach(println)
//
//    // 重新分区的同是进行顺序排序，且只能进行顺序排序
//    val rdd34 = rdd33.repartitionAndSortWithinPartitions(new Partitioner {
//      override def numPartitions: Int = 2
//      override def getPartition(key: Any): Int = if (key.toString.toInt % 3==0) 0 else 1
//    })
//
//    rdd34.mapPartitionsWithIndex((idx,iter) => Iterator(idx+":"+iter.mkString("|"))).foreach(println)

    // 将各分区的数据组合成数组返回
//    val rdd35 = sc.parallelize(1 to 50,4).mapPartitionsWithIndex((idx,iter) => Iterator(idx+":"+iter.mkString("|"))).foreach(println)

    // 只对 value 进行操作，默认还是返回 kv
//    val rdd36 = sc.makeRDD(Array((1,'a'),(2,'b'))).mapValues(_.toUpper).foreach(println)

    val rdd37 = sc.makeRDD(1 to 100000).filter(_%2 != 0).map(_+"100")
    rdd37.cache()
    println(rdd37.collect().mkString("|").substring(0,10))
    println(rdd37.collect().mkString("|").substring(0,10))








  }catch{
    case ex:Exception => println(ex.getCause)
  }finally {
    if(!sc.isStopped){
      sc.stop()
    }
  }



}
