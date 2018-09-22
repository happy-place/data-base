package com.big.data.traffic

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import java.util.Properties

object PropertyUtil {
  val properties = new Properties()

  try{
    val inputStream = ClassLoader.getSystemResourceAsStream("kafka.properties")
    properties.load(inputStream)
  }catch {
    case ex: Exception => println(ex)
  }finally {}

  def getProperty(key: String): String = {
    properties.getProperty(key)
  }
}

object PropertyUtil2 {

  val properties = new Properties()

  def apply(fileName:String) ={
    PropertyUtil2.properties.load(ClassLoader.getSystemResourceAsStream(fileName))
    PropertyUtil2
  }

//  try{
//    val inputStream = ClassLoader.getSystemResourceAsStream("kafka.properties")
//    properties.load(inputStream)
//  }catch {
//    case ex: Exception => println(ex)
//  }finally {}

  def getProperty(key: String): String = {
    properties.getProperty(key)
  }

}