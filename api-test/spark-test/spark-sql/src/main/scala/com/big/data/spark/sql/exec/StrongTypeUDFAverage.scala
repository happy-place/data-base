package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.expressions.Aggregator
import org.apache.spark.sql.{Encoder, Encoders, SparkSession}

// UDF 函数入参类型
case class Employee(name: String, salary: Double)
// UDF 函数中间计算需要用到的 缓冲数据结构
case class Average(var sum: Double, var count: Long)

// Aggregator[Employee, Average, Double] Double 为最终输出结果类型
object StrongTypeUDFAverage extends Aggregator[Employee, Average, Double] {
  // 定义一个数据结构，保存工资总数和工资总个数，初始都为0
  def zero: Average = Average(0, 0L)

  // 分区内部累加
  def reduce(buffer: Average, employee: Employee): Average = {
    buffer.sum += employee.salary
    buffer.count += 1
    buffer
  }

  // 分区间聚合
  def merge(b1: Average, b2: Average): Average = {
    b1.sum += b2.sum
    b1.count += b2.count
    b1
  }

  // 计算输出
  def finish(reduction: Average): Double = reduction.sum / reduction.count

  // 设定之间值类型的编码器，要转换成case类
  // Encoders.product是进行scala元组和case类转换的编码器
  def bufferEncoder: Encoder[Average] = Encoders.product

  // 设定最终输出值的编码器
  def outputEncoder: Encoder[Double] = Encoders.scalaDouble
}

object StrongTypeUDFAverageTest extends App {

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()

  import spark.implicits._

  val ds = spark.read.json("hdfs://localhost:9000/tmp/sparl/df/in/json/employee.json").as[Employee]
  ds.show()

  // 注册UDF 输出 结果的 别名
  val averageSalary = StrongTypeUDFAverage.toColumn.name("average_salary")
  val result = ds.select(averageSalary)
  result.show()

}