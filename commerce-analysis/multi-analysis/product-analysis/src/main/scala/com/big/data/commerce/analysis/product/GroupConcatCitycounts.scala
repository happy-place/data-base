package com.big.data.commerce.analysis.product

import org.apache.spark.sql.Row
import org.apache.spark.sql.expressions.{MutableAggregationBuffer, UserDefinedAggregateFunction}
import org.apache.spark.sql.types.{DataType, StringType, StructField, StructType}

class GroupConcatCitycounts extends UserDefinedAggregateFunction{

  override def inputSchema: StructType = StructType(StructField("cityInfo",StringType) :: Nil)

  override def bufferSchema: StructType = StructType(StructField("bufferCityInfo",StringType):: Nil)

  override def dataType: DataType = StringType

  override def deterministic: Boolean = true

  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer(0) = ""
  }

  override def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    var bufferCityInfos = buffer.getString(0)

    val cityInfo = input.getString(0)

    if(!bufferCityInfos.contains(cityInfo)){

      bufferCityInfos += "|"

      bufferCityInfos += cityInfo
    }
    buffer.update(0,bufferCityInfos)

  }

  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    var bufferCityInfos = buffer1.getString(0)
    val bufferCityInfos2 = buffer2.getString(0)

    for(cityInfo <- bufferCityInfos2.split("\\|")){
      if(!bufferCityInfos.contains(cityInfo)){

        bufferCityInfos += "|"

        bufferCityInfos += cityInfo
      }
    }
    buffer1.update(0,bufferCityInfos)
  }

  override def evaluate(buffer: Row): Any = {
    buffer.getString(0)
  }
}
