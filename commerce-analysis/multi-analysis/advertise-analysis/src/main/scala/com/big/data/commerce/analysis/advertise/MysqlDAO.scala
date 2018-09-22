package com.big.data.commerce.analysis.advertise

import java.sql.ResultSet

import com.big.data.commerce.common.{PoolMySql, QueryCallback}

import scala.collection.mutable.ArrayBuffer

//广告黑名单 DAO
object AdBlackListDAO{

  def findAll(): Array[Int] ={

    val array = ArrayBuffer[Int]()

    val sql = "select * from ad_blacklist"

    val mysqlPool = PoolMySql()
    val client = mysqlPool.borrowObject()

    client.executeQuery(sql,null,new QueryCallback {
      override def process(rs: ResultSet): Unit = {
        while (rs.next()){
          array += rs.getInt(1)
        }
      }
    })

    mysqlPool.returnObject(client)
    array.toArray
  }

  /**
    * 批量插入广告黑名单用户
    *
    * @param adBlacklists
    */
  def insertBatch(adBlacklists: Array[AdBlacklist]) {
    val sql = "INSERT INTO ad_blacklist VALUES(?)"

    val paramsList = new ArrayBuffer[Array[Any]]()

    for (adBlacklist <- adBlacklists) {
      val params: Array[Any] = Array(adBlacklist.userid)
      paramsList += params
    }
    val mySqlPool = PoolMySql()
    val client = mySqlPool.borrowObject()
    client.executeBatch(sql, paramsList.toArray)
    mySqlPool.returnObject(client)
  }

}

/**
  * 用户广告点击量DAO实现类
  *
  */
object AdUserClickCountDAO {

  def updateBatch(adUserClickCounts: Array[AdUserClickCount]) {
    val mySqlPool = PoolMySql()
    val client = mySqlPool.borrowObject()

    // 首先对用户广告点击量进行分类，分成待插入的和待更新的
    val insertAdUserClickCounts = ArrayBuffer[AdUserClickCount]()
    val updateAdUserClickCounts = ArrayBuffer[AdUserClickCount]()

    val selectSQL = "SELECT count(*) FROM ad_user_click_count WHERE date=? AND userid=? AND adid=? "

    for (adUserClickCount <- adUserClickCounts) {

      val selectParams: Array[Any] = Array(adUserClickCount.date, adUserClickCount.userid, adUserClickCount.adid)
      client.executeQuery(selectSQL, selectParams, new QueryCallback {
        override def process(rs: ResultSet): Unit = {
          if (rs.next() && rs.getInt(1) > 0) {
            updateAdUserClickCounts += adUserClickCount
          } else {
            insertAdUserClickCounts += adUserClickCount
          }
        }
      })
    }

    // 执行批量插入
    val insertSQL = "INSERT INTO ad_user_click_count VALUES(?,?,?,?)"
    val insertParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adUserClickCount <- insertAdUserClickCounts) {
      insertParamsList += Array[Any](adUserClickCount.date, adUserClickCount.userid, adUserClickCount.adid, adUserClickCount.clickCount)
    }

    client.executeBatch(insertSQL, insertParamsList.toArray)

    // 执行批量更新

    // 突然间发现，（不好意思），小bug，其实很正常，不要太以为然
    // 作为一个课程，复杂的业务逻辑
    // 如果你就是像某些课程，来一个小案例（几个课时），不会犯什么bug
    // 但是真正课程里面讲解企业实际项目中复杂的业务需求时，都很正常，有个小bug

    val updateSQL = "UPDATE ad_user_click_count SET clickCount=clickCount + ? WHERE date=? AND userid=? AND adid=?"
    val updateParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adUserClickCount <- updateAdUserClickCounts) {
      updateParamsList += Array[Any](adUserClickCount.clickCount, adUserClickCount.date, adUserClickCount.userid, adUserClickCount.adid)
    }

    client.executeBatch(updateSQL, updateParamsList.toArray)

    mySqlPool.returnObject(client)
  }

  /**
    * 根据多个key查询用户广告点击量
    *
    * @param date   日期
    * @param userid 用户id
    * @param adid   广告id
    * @return
    */
  def findClickCountByMultiKey(date: String, userid: Long, adid: Long): Int = {
    val mySqlPool = PoolMySql()
    val client = mySqlPool.borrowObject()
    val sql = "SELECT clickCount FROM ad_user_click_count " +
      "WHERE date=? " +
      "AND userid=? " +
      "AND adid=?"

    var clickCount = 0
    val params = Array[Any](date, userid, adid)
    client.executeQuery(sql, params, new QueryCallback {
      override def process(rs: ResultSet): Unit = {
        if (rs.next()) {
          clickCount = rs.getInt(1)
        }
      }
    })
    mySqlPool.returnObject(client)
    clickCount
  }
}

object AdStatDAO{

  def updateBatch(adStats: Array[AdStat]) {

    val mySqlPool = PoolMySql()
    val client = mySqlPool.borrowObject()


    // 区分开来哪些是要插入的，哪些是要更新的
    val insertAdStats = ArrayBuffer[AdStat]()
    val updateAdStats = ArrayBuffer[AdStat]()

    val selectSQL = "SELECT count(*) " +
      "FROM ad_stat " +
      "WHERE date=? " +
      "AND province=? " +
      "AND city=? " +
      "AND adid=?"

    for (adStat <- adStats) {

      val params = Array[Any](adStat.date, adStat.province, adStat.city, adStat.adid)

      client.executeQuery(selectSQL, params, new QueryCallback {
        override def process(rs: ResultSet): Unit = {
          if (rs.next() && rs.getInt(1) > 0) {
            updateAdStats += adStat
          } else {
            insertAdStats += adStat
          }
        }
      })
    }

    // 对于需要插入的数据，执行批量插入操作
    val insertSQL = "INSERT INTO ad_stat VALUES(?,?,?,?,?)"

    val insertParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adStat <- insertAdStats) {
      insertParamsList += Array[Any](adStat.date, adStat.province, adStat.city, adStat.adid, adStat.clickCount)
    }

    client.executeBatch(insertSQL, insertParamsList.toArray)

    // 对于需要更新的数据，执行批量更新操作
    val updateSQL = "UPDATE ad_stat SET clickCount=? " +
      "WHERE date=? " +
      "AND province=? " +
      "AND city=? " +
      "AND adid=?"

    val updateParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adStat <- updateAdStats) {
      updateParamsList += Array[Any](adStat.clickCount, adStat.date, adStat.province, adStat.city, adStat.adid)
    }

    client.executeBatch(updateSQL, updateParamsList.toArray)

    mySqlPool.returnObject(client)
  }

}

object AdProvinceTop3DAO{

  def updateBatch(adProvinceTop3s: Array[AdProvinceTop3]) {
    val mySqlPool = PoolMySql()
    val client = mySqlPool.borrowObject()


    // 先做一次去重（date_province）
    val dateProvinces = ArrayBuffer[String]()

    for (adProvinceTop3 <- adProvinceTop3s) {

      val key = adProvinceTop3.date + "_" + adProvinceTop3.province

      if (!dateProvinces.contains(key)) {
        dateProvinces += key
      }
    }

    // 根据去重后的date和province，进行批量删除操作
    val deleteSQL = "DELETE FROM ad_province_top3 WHERE date=? AND province=?"

    val deleteParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (dateProvince <- dateProvinces) {

      val dateProvinceSplited = dateProvince.split("_")
      val date = dateProvinceSplited(0)
      val province = dateProvinceSplited(1)

      val params = Array[Any](date, province)
      deleteParamsList += params
    }

    client.executeBatch(deleteSQL, deleteParamsList.toArray)

    // 批量插入传入进来的所有数据
    val insertSQL = "INSERT INTO ad_province_top3 VALUES(?,?,?,?)"

    val insertParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adProvinceTop3 <- adProvinceTop3s) {
      insertParamsList += Array[Any](adProvinceTop3.date, adProvinceTop3.province, adProvinceTop3.adid, adProvinceTop3.clickCount)
    }

    client.executeBatch(insertSQL, insertParamsList.toArray)

    mySqlPool.returnObject(client)
  }

}


object AdClickTrendDAO {

  def updateBatch(adClickTrends: Array[AdClickTrend]) {

    val mySqlPool = PoolMySql()
    val client = mySqlPool.borrowObject()

    // 区分出来哪些数据是要插入的，哪些数据是要更新的
    // 提醒一下，比如说，通常来说，同一个key的数据（比如rdd，包含了多条相同的key）
    // 通常是在一个分区内的
    // 一般不会出现重复插入的

    // 但是根据业务需求来
    // 各位自己在实际做项目的时候，一定要自己思考，不要生搬硬套
    // 如果说可能会出现key重复插入的情况
    // 给一个create_time字段

    // j2ee系统在查询的时候，直接查询最新的数据即可（规避掉重复插入的问题）

    val updateAdClickTrends = ArrayBuffer[AdClickTrend]()
    val insertAdClickTrends = ArrayBuffer[AdClickTrend]()

    val selectSQL = "SELECT count(*) " +
      "FROM ad_click_trend " +
      "WHERE date=? " +
      "AND hour=? " +
      "AND minute=? " +
      "AND adid=?"

    for (adClickTrend <- adClickTrends) {

      val params = Array[Any](adClickTrend.date, adClickTrend.hour, adClickTrend.minute, adClickTrend.adid)
      client.executeQuery(selectSQL, params, new QueryCallback {
        override def process(rs: ResultSet): Unit = {
          if (rs.next() && rs.getInt(1) > 0) {
            updateAdClickTrends += adClickTrend
          } else {
            insertAdClickTrends += adClickTrend
          }
        }
      })

    }

    // 执行批量更新操作
    val updateSQL = "UPDATE ad_click_trend SET clickCount=? " +
      "WHERE date=? " +
      "AND hour=? " +
      "AND minute=? " +
      "AND adid=?"

    val updateParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adClickTrend <- updateAdClickTrends) {
      updateParamsList += Array[Any](adClickTrend.clickCount, adClickTrend.date, adClickTrend.hour, adClickTrend.minute, adClickTrend.adid)
    }

    client.executeBatch(updateSQL, updateParamsList.toArray)

    // 执行批量更新操作
    val insertSQL = "INSERT INTO ad_click_trend VALUES(?,?,?,?,?)"

    val insertParamsList: ArrayBuffer[Array[Any]] = ArrayBuffer[Array[Any]]()

    for (adClickTrend <- insertAdClickTrends) {
      insertParamsList += Array[Any](adClickTrend.date, adClickTrend.hour, adClickTrend.minute, adClickTrend.adid, adClickTrend.clickCount)
    }

    client.executeBatch(insertSQL, insertParamsList.toArray)
    mySqlPool.returnObject(client)
  }

}
