package com.big.data.spark.graphx.test

import com.big.data.spark.graphx.test.CreateGraph.getClass
import org.apache.spark.graphx.{Edge, EdgeDirection, Graph, VertexId}
import org.apache.spark.{SparkConf, SparkContext}

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/24
  * Desc: 
  *
  */
object PregelTest extends App{

  val conf = new SparkConf().set("spark.streaming,stopGracefullyOnShutdown","true").setMaster("local[4]").setAppName(getClass.getSimpleName)
  val sc = new SparkContext(conf)

  try {

    // 声明边RDD
    val edgeRDD = sc.makeRDD(Array(
      Edge(2l, 1l, 7),
      Edge(2l, 4l, 2),
      Edge(3l, 2l, 4),
      Edge(3l, 6l, 3),
      Edge(4l, 1l, 1),
      Edge(2l, 5l, 2),
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

    // 研究 5 到其他点的最短距离
    val sourceId: VertexId = 5l
    //  初始化： 除目标点外，其余顶点全部初始化为整无穷大
    val initedGraph = graph.mapVertices((id, _) => if (id == sourceId) 0.0 else Double.PositiveInfinity)
    val resultGraph = initedGraph.pregel(Double.PositiveInfinity )(// 终止条件 vprog，累计到最大值才终止
       (id, dist, newDist) => {
        println(s"\n\ndestID:$id [oldVal:$dist,newVal:$newDist]");
        math.min(dist, newDist)
      }, // dst 节点最终将自身值 与 ，筛选出的最小的 srcAttr+attr 值进行比较，取较小值，然后更新给执行
      triplet => { // 默认 src 节点将 三元组信息发送给 dst 节点，复合比较条件，就表名发送 和 接受 成功，否则失败，，当某节点发送 和 接收消息全部失败，则进入钝化态，不参与下次迭代，否则继续擦怒下次迭代
        if (triplet.srcAttr + triplet.attr < triplet.dstAttr) {
          triplet.dstId
          println(s"${triplet.srcId} -> ${triplet.dstId} 发送成功 triplet.srcAttr + triplet.attr: ${triplet.srcAttr + triplet.attr} < triplet.dstAttr: ${triplet.dstAttr}")
          Iterator((triplet.dstId, triplet.srcAttr + triplet.attr))
        } else {
          Iterator.empty
        }
      },
      (a, b) => {
        println(s"src节点们，发送给dst的消息两两比较 (a:${a},)");
        math.min(a, b)
      } // 所有 src 发送过来的消息，先进行汇总，然后交给 (id,dist,newDist) => {math.min(dist,newDist)}, 进行最终合并更新
    )

    resultGraph.vertices.foreach(x=>println(s"vid:${x._1} [${x._2}]"))

  }finally {
    if(sc.isStopped){
      sc.stop()
    }
  }



}
