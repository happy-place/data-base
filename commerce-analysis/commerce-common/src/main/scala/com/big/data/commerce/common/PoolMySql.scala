package com.big.data.commerce.common

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import java.sql.{DriverManager, PreparedStatement, ResultSet}

import org.apache.commons.pool2.impl.{DefaultPooledObject, GenericObjectPool}
import org.apache.commons.pool2.{BasePooledObjectFactory, PooledObject}

trait QueryCallback{
  def process(rs:ResultSet)
}

// 代表我的一个mysql实例
class MySqlProxy(url:String,username:String,password:String){

  private val mysqlClient = DriverManager.getConnection(url,username,password)

  /**
    * 增删改
    * @return
    */
  def executeUpdate(sql:String,params:Array[Any]): Int ={
    var returnCode = 0
    var pstmt :PreparedStatement = null

    try{

      mysqlClient.setAutoCommit(false)
      pstmt = mysqlClient.prepareStatement(sql)

      if(params != null && params.length >0){
        for(i <- 0 until params.length){
          pstmt.setObject(i+1,params(i))
        }
      }

      returnCode = pstmt.executeUpdate()
      mysqlClient.commit()
    }catch {
      case e:Exception => e.printStackTrace()
    }
    returnCode
  }

  /**
    * 查询
    * @param sql
    * @param params
    * @param queryCallback
    */
  def executeQuery(sql:String,params:Array[Any],queryCallback: QueryCallback): Unit ={
    var pstmt :PreparedStatement = null
    var rs:ResultSet = null

    try{
      pstmt = mysqlClient.prepareStatement(sql)

      if(params != null && params.length >0){
        for(i <- 0 until params.length){
          pstmt.setObject(i+1,params(i))
        }
      }
      rs = pstmt.executeQuery()
      queryCallback.process(rs)
    }catch {
      case e:Exception => e.printStackTrace()
    }
  }

  /**
    * 批量执行增删改
    * @param sql
    * @param paramList
    * @return
    */
  def executeBatch(sql:String,paramList:Array[Array[Any]]):Array[Int]={
    var returnCode:Array[Int] = null
    var pstmt :PreparedStatement = null

    try{

      mysqlClient.setAutoCommit(false)
      pstmt = mysqlClient.prepareStatement(sql)

      if(paramList != null && paramList.length >0){
        for(params <- paramList){
          for(i <- 0 until params.length){
            pstmt.setObject(i+1,params(i))
          }
          pstmt.addBatch()
        }
      }

      returnCode = pstmt.executeBatch()
      mysqlClient.commit()
    }catch {
      case e:Exception => e.printStackTrace()
    }
    returnCode
  }

}


class MySqlProxyFactory(url:String,username:String,password:String) extends BasePooledObjectFactory[MySqlProxy]{

  override def create(): MySqlProxy = new MySqlProxy(url,username,password)

  override def wrap(t: MySqlProxy): PooledObject[MySqlProxy] = new DefaultPooledObject[MySqlProxy](t)
}

object PoolMySql {

  Class.forName("com.mysql.jdbc.Driver")

  private var pool :GenericObjectPool[MySqlProxy] = null

  def apply():GenericObjectPool[MySqlProxy] ={

    if(this.pool == null){
      this.synchronized{
        val url = ConfigManager.config.getString("jdbc.url")
        val username = ConfigManager.config.getString("jdbc.user")
        val password = ConfigManager.config.getString("jdbc.password")

        val mySqlProxyFactory = new MySqlProxyFactory(url,username,password)

        this.pool = new GenericObjectPool[MySqlProxy](mySqlProxyFactory)
      }
    }

    this.pool
  }

}

