package com.big.data.traffic

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import redis.clients.jedis.{JedisPool, JedisPoolConfig}

object RedisUtil {
  //配置redis
  val host = "localhost"
  val port = 6379
  val timeout = 30000

  val config = new JedisPoolConfig
  config.setMaxTotal(200)
  config.setMaxIdle(50)
  config.setMinIdle(8)

  config.setMaxWaitMillis(10000)
  config.setTestOnBorrow(true)
  config.setTestOnReturn(true)

  //连接扫描
  config.setTestWhileIdle(true)
  //两次扫描的时间间隔
  config.setTimeBetweenEvictionRunsMillis(25000)
  //每次扫描的对象数目
  config.setNumTestsPerEvictionRun(10)
  //一个对象至少停留在idle中的时间
  config.setMinEvictableIdleTimeMillis(60000)
  //连接池
  lazy val pool = new JedisPool(config, host, port, timeout)
  //回收资源
  lazy val hook = new Thread{
    override def run() = {
      pool.destroy()
    }
  }
  sys.addShutdownHook(hook)
}