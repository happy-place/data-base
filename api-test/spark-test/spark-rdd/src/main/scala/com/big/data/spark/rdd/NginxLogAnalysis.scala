package com.big.data.spark.rdd

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

import scala.util.matching.Regex

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/6/19
  * Desc: 
  *
  */
object NginxLogAnalysis {
  // IP 过滤正则表达式
  val IPPattern = "((?:(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d)))\\.){3}(?:25[0-5]|2[0-4]\\d|((1\\d{2})|([1-9]?\\d))))".r

  val VideoPattern = "([0-9]+).mp4".r

  val timePattern = ".*(2017):([0-9]{2}):[0-9]{2}:[0-9]{2}.*".r

  val httpSizePattern = ".*\\s(200|206|304)\\s([0-9]+)\\s.*".r // ".r 能够避免使用转义符"

  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[*]")
    val sparkContext = new SparkContext(sparkConf)

    val logRDD = sparkContext.textFile("/Users/huhao/software/idea_proj/data-base/api-test/spark-test/spark-rdd/src/main/resources/cdn.txt")

    /*
    6.1计算独立IP数主要是两步
    1. 从每行日志中筛选出IP地
    2. 去除重复的IP得到独立IP数
     */
    ipAnalysis(logRDD)

    /*
    6.2	统计每个视频独立IP数
    有时我们不但需要知道全网访问的独立IP数，更想知道每个视频访问的独立IP数
     */
    videoAnalysis(logRDD)

    /*
    6.3	统计一天中每个小时间的流量
    有时我想知道网站每小时视频的观看流量，看看用户都喜欢在什么时间段过来看视频
     */
    flowAnalysis(logRDD)

    sparkContext.stop()

  }

  def isMatch(pattern: Regex, target: String) = {
    target match {
      case pattern(_*) => true
      case _ => false
    }
  }

  def ipAnalysis(rdd: RDD[String]): Unit = {
    rdd.map {
      line => (IPPattern.findFirstIn(line).get, 1) // 每行可能包含多个匹配的Ip,为安全起见,取第一个,并添加计数纬度
    }.reduceByKey(_ + _) // 累计次数
      .sortBy(_._2, false) // 基于出现次数降序排序
      .take(10) // 取前10位
      .foreach(println) // 遍历输出
  }

  def videoAnalysis(rdd: RDD[String]): Unit = {
    // _.matches(".*([0-9]+)\\.mp4.*")  直接对照字符串过滤
    rdd.filter(isMatch(".*([0-9]+)\\.mp4.*".r,_)) // 过滤出包含视频名称的记录,相当于日志清洗
      .map { line => (VideoPattern.findFirstIn(line).get , IPPattern.findFirstIn(line).get) } // 遍历解析,获取(video,ip)集合
      .groupByKey() // 基于k 分组,返回的元组的 _2 是可迭代对象
      .map(t => (t._1, t._2.toSet.size)) // 去重
      .sortBy(_._2, false) // 访问量排序
      .take(10) // 取top10
      .foreach(println) // 输出
  }

  def flowAnalysis(rdd: RDD[String]): Unit = {
    /*
     *  ipAnalysis 和 videoAnalysis 取的都是 top10,由于take(10),存在,已经进行了分区间的排序,因此直接foreach(println)输出,是全局有序的
     *  而flowAnalysis 是全部输出,无需take操作,就需要造sortBy 中指定分区数,避免区内有序,区间无序的尴尬(即数据分段有序,段与段间无序),指定
     *  分区数为1,相当于在全局内进行排序
     */
    val sumRdd = rdd.filter(isMatch(httpSizePattern, _)) // 过滤出响应成功的记录
      .filter(isMatch(timePattern, _)) // 过滤出指定年份记录
      .map {
      line => {
        val httpSizePattern(code, size) = line // 基于已有的正则表达式创建解析函数
        val timePattern(year, hour) = line
        (hour, size.toLong) // 返回(时,响应长度)
      }
    }.reduceByKey(_ + _) // 基于k聚合
      .sortBy(_._2, false,1)
      .foreach {
        t => println("( "+ t._1 + " ," + (t._2/(1024*1024*1024)) +"GB )")
      }

  }

}
