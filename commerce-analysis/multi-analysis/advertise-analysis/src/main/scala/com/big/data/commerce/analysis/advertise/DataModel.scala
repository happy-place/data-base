package com.big.data.commerce.analysis.advertise

case class AdvertiseRealTime(timestamp:Long,
                             province:Int,
                             city:Int,
                             userid:Int,
                             adid:Int)

/**
  * 广告黑名单
  * @author wuyufei
  *
  */
case class AdBlacklist(userid:Long)

/**
  * 用户广告点击量
  * @author wuyufei
  *
  */
case class AdUserClickCount(date:String,
                            userid:Long,
                            adid:Long,
                            clickCount:Long)


case class AdStat(date:String,
                  province:Int,
                  city:Int,
                  adid:Long,
                  clickCount:Long)


case class AdProvinceTop3(date:String,
                  province:Int,
                  adid:Int,
                  clickCount:Long)

case class AdClickTrend(date:String,
                        hour:String,
                        minute:String,
                        adid:Int,
                        clickCount:Long)

