package com.big.data.spark.sql.exec

import org.apache.spark.SparkConf
import org.apache.spark.sql.expressions.{MutableAggregationBuffer, UserDefinedAggregateFunction}
import org.apache.spark.sql.types._
import org.apache.spark.sql.{Row, SparkSession}

object WeakTypeUDFAverage extends UserDefinedAggregateFunction {
  // 聚合函数 入参类型
  def inputSchema: StructType = StructType(StructField("inputColumn", DoubleType) :: Nil)
  // 聚合函数完成计算需要的 缓冲区
  def bufferSchema: StructType = {
    StructType(StructField("sum", DoubleType) :: StructField("count", LongType) :: Nil)
  }
  // 返回值的数据类型
  def dataType: DataType = DoubleType
  // 对于相同的输入是否一直返回相同的输出。
  def deterministic: Boolean = true
  // 初始化
  def initialize(buffer: MutableAggregationBuffer): Unit = {
    // 存工资的总额
    buffer(0) = 0D
    // 存工资的个数
    buffer(1) = 0L
  }
  // 相同Executor间的数据合并。
  def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    if (!input.isNullAt(0)) {
      buffer(0) = buffer.getDouble(0) + input.getDouble(0)
      buffer(1) = buffer.getLong(1) + 1
    }
  }
  // 不同Executor间的数据合并
  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1(0) = buffer1.getDouble(0) + buffer2.getDouble(0)
    buffer1(1) = buffer1.getLong(1) + buffer2.getLong(1)
  }
  // 计算最终结果
  def evaluate(buffer: Row): Double = buffer.getDouble(0) / buffer.getLong(1)
}

object WeakTypeUDFAverageTest extends App{

  val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")

  val spark = SparkSession.builder().config(sparkconf).getOrCreate()

  // 注册函数
  spark.udf.register("WeakTypeUDFAverage", WeakTypeUDFAverage)

  val df = spark.read.json("hdfs://localhost:9000/tmp/sparl/df/in/json/employee.json")
  df.createOrReplaceTempView("employees")
  df.show()
  // +-------+------+
  // |   name|salary|
  // +-------+------+
  // |Michael|  3000|
  // |   Andy|  4500|
  // | Justin|  3500|
  // |  Berta|  4000|
  // +-------+------+

  val result = spark.sql("SELECT WeakTypeUDFAverage(salary) as average_salary FROM employees")
  result.show()
  // +--------------+
  // |average_salary|
  // +--------------+
  // |        3750.0|
  // +--------------+

}

