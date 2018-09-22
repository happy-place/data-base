package com.big.data.spark.graphx.test

import org.apache.spark.graphx.{Edge, Graph, VertexId}
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/23
  * Desc: 
  *
  */
object CreateGraph {

  // 泛型函数
  def doPrint[VD,ED](graph:Graph[VD,ED]):Unit={
    println("--------------------------")
    // 遍历三元组RDD
    graph.triplets.foreach{ t=>
      val srcId = t.srcId
      val srcAttr = t.srcAttr
      val dstId = t.dstId
      val dstAttr = t.dstAttr
      val edgeAttr = t.attr
      println(s"$srcId [$srcAttr] -> $edgeAttr -> $dstId [$dstAttr]")
    }
  }


  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[4]").setAppName(getClass.getSimpleName)
    val sc = new SparkContext(conf)

    try{
      // 定义点的RDD VertexId 为long类型，描述点ID,(String,String) 代表VD 为点的属性，在此案例中第一个为姓名，第二个为职业
      val vertexRDD:RDD[(VertexId,(String,String))] = sc.makeRDD(Array((3L,("rxin","stu")),(5L,("franklin","prof")),(7L,("jgonzal","pst.doc")),(2L,("istoica","prof"))))

      // 定义边的RDD Edge[srcId,dstId,VertexId]
      val edgeRDD:RDD[Edge[String]] = sc.makeRDD(Array(Edge(5l,3l,"Advisor"),Edge(3l,7l,"Collab"),Edge(5l,7l,"PI"),Edge(2l,5l,"Colleague")))

      // 方案1：基于 点RDD 和 边RDD 创建 图
      val graph = Graph(vertexRDD,edgeRDD)
      doPrint(graph)
      /*
        2 [(istoica,prof)] -> Colleague -> 5 [(franklin,prof)]
        5 [(franklin,prof)] -> PI -> 7 [(jgonzal,pst.doc)]
        5 [(franklin,prof)] -> Advisor -> 3 [(rxin,stu)]
        3 [(rxin,stu)] -> Collab -> 7 [(jgonzal,pst.doc)]
       */

      // 方案2: 基于边构建图
      val graph2 = Graph.fromEdges(edgeRDD,"mygraph")
      doPrint(graph2)
      /*
        2 [mygraph] -> Colleague -> 5 [mygraph]
        3 [mygraph] -> Collab -> 7 [mygraph]
        5 [mygraph] -> PI -> 7 [mygraph]
        5 [mygraph] -> Advisor -> 3 [mygraph]
       */

      // 方案3：基于边元组创建图
      val edgeTripletRDD = edgeRDD.map(t=> (t.srcId,t.dstId))
      val graph3 = Graph.fromEdgeTuples(edgeTripletRDD,"mygraph2")
      doPrint(graph3)
      /*
        2 [mygraph2] -> 1 -> 5 [mygraph2]
        5 [mygraph2] -> 1 -> 3 [mygraph2]
        5 [mygraph2] -> 1 -> 7 [mygraph2]
        3 [mygraph2] -> 1 -> 7 [mygraph2]
       */

      // 过滤掉 职业为 prof 的顶点，构建子图
      val newVertexRDD = graph.vertices.filter(_._2._2!="prof")
      val subGraph = Graph(newVertexRDD,edgeRDD)
      doPrint(subGraph)
      /*
        2 [null] -> Colleague -> 5 [null]
        3 [(rxin,stu)] -> Collab -> 7 [(jgonzal,pst.doc)]
        5 [null] -> Advisor -> 3 [(rxin,stu)]
        5 [null] -> PI -> 7 [(jgonzal,pst.doc)]
       */

    }finally {
      if(!sc.isStopped){
        sc.stop()
      }
    }
  }






}
