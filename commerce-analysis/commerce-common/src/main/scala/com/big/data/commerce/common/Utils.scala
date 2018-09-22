package com.big.data.commerce.common

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import org.joda.time.format.DateTimeFormat

object Utils {

  val DATATIME_FORMAT = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss")

  def fullFill(time: String): String = {
    if (time.length == 1)
      "0" + time
    else
      time
  }

  def before(starttime:String, endtime:String):Boolean ={
    DATATIME_FORMAT.parseDateTime(starttime).isBefore(DATATIME_FORMAT.parseDateTime(endtime))
  }

  def after(starttime:String, endtime:String):Boolean ={
    before(endtime,starttime)
  }

  // 返回秒
  def getDateDuration(endtime:String, starttime:String):Long={
    (DATATIME_FORMAT.parseDateTime(endtime).getMillis - DATATIME_FORMAT.parseDateTime(starttime).getMillis) / 1000
  }

}

object NumberUtils {

  /**
    * 格式化小数
    * @param scale 四舍五入的位数
    * @return 格式化小数
    */
  def formatDouble(num:Double, scale:Int):Double = {
    val bd = BigDecimal(num)
    bd.setScale(scale, BigDecimal.RoundingMode.HALF_UP).doubleValue()
  }

}

