package com.big.data.spark.rdd

import java.util
import org.apache.spark.util.AccumulatorV2
import org.apache.spark.{SparkConf, SparkContext}
import scala.collection.JavaConversions._

//  JavaConversions._ 内部自己转 JavaConvertors._ 手动转
/*
 *
 * Author: Huhao <huhao1@cmc.com>
 * Date: 2018/6/18
 * Desc:
 *
 */

class MyAccumulator extends AccumulatorV2[String,util.Set[String]]{
  // 各节点申请内存
  val _logArray:util.Set[String] = new util.HashSet[String]()

  // 判断是否为空
  override def isZero: Boolean = _logArray.isEmpty

  // 克隆
  override def copy(): AccumulatorV2[String, util.Set[String]] = {
    val newAcc = new MyAccumulator()
    // 拷贝过程需要上锁
    _logArray.synchronized{
      // addAll 是 javaAPI
      newAcc._logArray.addAll(this._logArray)
    }
    newAcc
  }

  // 重置
  override def reset(): Unit = _logArray.clear()

  // 添加元素
  override def add(v: String): Unit = _logArray.add(v)
  // 合并
  override def merge(other: AccumulatorV2[String, util.Set[String]]): Unit = {
    // 只运行通类型合并
    other match {
      case o:MyAccumulator => _logArray.addAll(other.value)
    }
  }

  // 安全输出累加器值
  override def value: util.Set[String] = java.util.Collections.unmodifiableSet(_logArray)
}




object TestAccumulatorTest extends App{

  val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[*]")
  val sc = new SparkContext(conf)

  try {
    // 1.使用系统自带累加器
      val acc = sc.accumulator(0)

    //  // 使用累加器时，控制为单分区
      val rdd = sc.parallelize(1 to 50,4)
      // transform 算子中使用 累加器时，必须在最后调用 action算子才能真正进行计算
      rdd.mapPartitions(iter=>{
        while(iter.hasNext){
          val it = iter.next()
          if(it%2==0){
            // 必须使用 线程安全的 add 方法进行累计，否则分布式计算会出现问题
            acc.add(1)
          }
        }
        iter
      }).count()

      // action 使用 累加器
      rdd.foreachPartition(iter=>{
        while(iter.hasNext){
          val it = iter.next()
          if(it%2==0){
            // 必须使用 线程安全的 add 方法进行累计，否则分布式计算会出现问题
            acc.add(1)
          }
        }
      })

      println(acc.value)

    // 2.使用自定义累加器
    // 创建累加器实例
    val myAccumulator = new MyAccumulator()
    // sc 中注册累加器
    sc.register(myAccumulator, "myAccumulator")
    val sum = sc.parallelize(Array("-1c", "2a", "3", "4b","5d","4","7c"), 3).filter(t => {
      val pattern = """^-?(\d+)"""
      /*
        ^ 以后面开头
        -? 可选的0~1 个负号
        \d+ 1~n 位整数
        ^-?(\d+) 整数
       */
      val flag = t.matches(pattern)
      if (!flag) {
        myAccumulator.add(t)  // >> 只收集 非整数类型 2a 和 4b
      }
      flag
    }).map(_.toInt).reduce(_ + _) // 1+3
    println(sum)
    for (v <- myAccumulator.value) {
      println(v)
    }

  }catch {
    case ex:Exception=> println(ex.getCause)
  }finally {
    if(!sc.isStopped){
      sc.stop()
    }
  }




}