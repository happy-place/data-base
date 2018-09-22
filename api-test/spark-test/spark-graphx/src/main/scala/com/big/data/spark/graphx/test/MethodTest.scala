package com.big.data.spark.graphx.test

import org.apache.spark.graphx._
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/23
  * Desc: 
  *
  */
object MethodTest {

  // 泛型函数
  def doPrint[VD, ED](graph: Graph[VD, ED]): Unit = {
    println("--------------------------")
    // 遍历三元组RDD
    graph.triplets.foreach { t =>
      val srcId = t.srcId
      val srcAttr = t.srcAttr
      val dstId = t.dstId
      val dstAttr = t.dstAttr
      val edgeAttr = t.attr
      println(s"源点：$srcId [$srcAttr] -> 边属性： $edgeAttr ->目标：$dstId [$dstAttr]")
    }
  }


  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown", "true").setMaster("local[4]").setAppName(getClass.getSimpleName)
    val sc = new SparkContext(conf)

    try {
      // 声明边RDD
      val edgeRDD = sc.makeRDD(Array(
        Edge(2l, 1l, 7),
        Edge(2l, 4l, 2),
        Edge(3l, 2l, 4),
        Edge(3l, 6l, 3),
        Edge(4l, 1l, 1),
        Edge(5l, 2l, 2),
        Edge(5l, 3l, 8),
        Edge(5l, 6l, 3)
      ))

      // 声明 顶点
      val vertexRDD = sc.makeRDD(Array(
        (1l, ("Alice", 28)),
        (2l, ("Bob", 27)),
        (3l, ("Charlie", 65)),
        (4l, ("David", 42)),
        (5l, ("Ed", 55)),
        (6l, ("Fran", 50))
      ))

      val graph = Graph(vertexRDD, edgeRDD)
      doPrint(graph)

      // 基本信息接口
      // 边个数
      val numEdges = graph.numEdges
      // 顶点个数
      val numVertices = graph.numVertices
      // 入度
      val inDegrees = graph.inDegrees
      // 出度
      val outDegrees = graph.outDegrees
      //inDegrees + outDegrees
      val degress = graph.degrees
      // 全部边
      val edges = graph.edges
      // 全部顶点
      val vertices = graph.vertices
      // 全部三元组
      val triplets = graph.triplets

      // 转换操作 对全部顶点进行遍历转换
      val transformGraph1 = graph.mapVertices{
        case (vid,(name,age)) => s"${vid}:${name}_${age}"
      }
      doPrint(transformGraph1)

      // 对全部边进行遍历转换
      val transformGraph2 = graph.mapEdges{
        e => e.srcId+" -> "+e.attr+" -> "+e.dstId
      }
      doPrint(transformGraph2)

      // 对全部三元组进行遍历
      val transformGraph3 =graph.mapTriplets{ trip =>
        trip.srcId +" -> "+trip.attr +" -> "+trip.dstId
      }
      doPrint(transformGraph3)

      // 边方向翻转
      val reversedGraph = graph.reverse
      doPrint(reversedGraph)

//      def subgraph(
      // epred : scala.Function1[org.apache.spark.graphx.EdgeTriplet[VD, ED], scala.Boolean] = { /* compiled code */ }, Edge(2l, 1l, 7)
      // vpred : scala.Function2[org.apache.spark.graphx.VertexId, VD, scala.Boolean] = { /* compiled code */ } (1l, ("Alice", 28))
      // ) : org.apache.spark.graphx.Graph[VD, ED]
      val sub = graph.subgraph(epred=(et) => et.attr > 5,vpred = (vertex,attr) => attr._2 > 50)
      doPrint(sub)

      // 声明边RDD
      val edgeRDD2 = sc.makeRDD(Array(
        Edge(1l, 2l, 7),
        Edge(2l, 4l, 2),
        Edge(2l, 3l, 4),
        Edge(3l, 6l, 3),
        Edge(4l, 1l, 1),
        Edge(5l, 2l, 2),
        Edge(5l, 3l, 8),
        Edge(5l, 6l, 12)
      ))

      // 声明 顶点
      val vertexRDD2 = sc.makeRDD(Array(
        (1l, ("Alice", 28)),
        (2l, ("Bob", 27)),
        (3l, ("Charlie", 65)),
        (4l, ("David", 42)),
        (5l, ("Ed", 55)),
        (6l, ("Fran", 50))
      ))

      // 取两个图的相较的边，构建的新图进行打印输出，如果边属性不一致，已前者的属性为准
      val graph2 = Graph(vertexRDD2,edgeRDD2)
      val intersectGraph = graph.mask(graph2)
      doPrint(intersectGraph)


      val edgeRDD3 = sc.makeRDD(Array(
        Edge(1l, 2l, 7),
        Edge(2l, 4l, 5),
        Edge(2l, 3l, 4),
        Edge(3l, 6l, 3),
        Edge(4l, 1l, 1),
        Edge(5l, 2l, 2),
        Edge(5l, 3l, 8),
        Edge(5l, 6l, 12),
        Edge(2l, 4l, 5)
      ))

      // 声明 顶点
      val vertexRDD3 = sc.makeRDD(Array(
        (1l, ("Alice", 28)),
        (2l, ("Bob", 27)),
        (3l, ("Charlie", 65)),
        (4l, ("David", 42)),
        (5l, ("Ed", 55)),
        (6l, ("Fran", 50))
      ))

      val graph3 = Graph(vertexRDD3,edgeRDD3.repartition(1))
      graph3.edges.mapPartitionsWithIndex((index,iter)=> Iterator(index+":"+iter.mkString("|"))).foreach(println)

      // 将图中 通分区内，相同起止点 边 进行收集聚合操作
      val edgeGroup = graph3.groupEdges(_+_)
      doPrint(edgeGroup)

      // 顶点关联操作
      // 将外部顶点的rdd 与 当前图 相同顶点的 rdd 进行join (内连接)
      val newVertex = sc.makeRDD(Array((1l, 28)))
      val newGraph = graph3.joinVertices(newVertex)((vid,attr,newAttr) =>(attr._1+newAttr,attr._2))
      doPrint(newGraph)

      // 将外部顶点的rdd 与 当前图 相同顶点的 rdd 进行join (外连接)，未匹配上的可以赋默认值
      val newGraph2 = graph3.outerJoinVertices(newVertex)((vid,attr,newAttr) =>(attr._1+newAttr.getOrElse(22),attr._2))
      doPrint(newGraph2)

      // 收集顶点周围邻居，方向，入度
      graph.collectNeighbors(EdgeDirection.In).collect().foreach(t=> println(t._1 + "\t"+t._2.mkString("|")))

      // 聚合指向顶点的边的其他顶点，由边想当前顶点发消息，统计最大的源顶点，然后输出
      val aggGraph = graph.aggregateMessages[(String,Int)](
        ctx=> ctx.sendToDst(ctx.srcAttr), // 各边将想目标顶点，发送源顶点的消息
        (x,y) => if (x._2 >=y._2) x else y // 比较源顶点，取最大值
      )
      aggGraph.foreach(println)


    } finally {
      if (sc.isStopped) {
        sc.stop()
      }
    }

  }


}
