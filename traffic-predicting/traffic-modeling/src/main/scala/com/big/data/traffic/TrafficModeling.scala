package com.big.data.traffic

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

import java.io.{File, PrintWriter}
import java.text.SimpleDateFormat
import java.util.{Calendar, Date}

import org.apache.spark.mllib.classification.LogisticRegressionWithLBFGS
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable.ArrayBuffer

/**
  * 前端输入待预测卡口 id ，获取当前时间作为入参
  * 从内置卡口关系映射表中获取待预测卡口的关联卡口集合
  * 从redis 提取目标卡口和其关联卡口当天的全部聚合数据 (ynd_monitorId,hm,speedAndCnt) (key,field,value)
  * 以当前时间为基准，倒退到1h前，取4min位窗口长度，1min为滑动长度，每个窗口前3min构建DataX(自变量)，后1min构建DataY(应变量)，其中DataX 也会包含目标卡口信息
  * 按上述规则按 3：2 比例将 1h 内数据拆分为训练集 和 测试集，数据依据平均车速十位数分等级归类
  * 通过训练集训练模型，用模型处理测试集，得到（预测值，实际值）集合，进而可以评价模型准确度，高于预设值，则保存到 hdfs,并将索引维护到redis
  *
  *
  *
  */

object TrafficModeling {
  def main(args: Array[String]): Unit = {
    val writer = new PrintWriter(new File("model_training.txt"))
    //配置spark
    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("TrafficModeling")
    val sc = new SparkContext(sparkConf)
    //配置redis
    val dbIndex = 1
    val jedis = RedisUtil.pool.getResource
    jedis.select(dbIndex)
    //想要对哪个监测点进行建模
    val monitorIDs = List("0005", "0015")
    //找到目标监测点它的相关监测点数据
    val relationIDs = Map(
      "0005" -> Array("0003", "0004", "0005", "0006", "0007"),
      "0015" -> Array("0013", "0014", "0015", "0016", "0017"))

    //获取redis中的实时数据
    val temp = monitorIDs.map(monitorID => {
      //包含目标监测点数据,得到一个Array
      val monitorRealtionList = relationIDs.get(monitorID).get
      //处理时间（key, field, value） --> (yyyyMMdd_monitor_id, HHmm, speed_count)
      val currentDate = Calendar.getInstance().getTime
      val ymdSDF = new SimpleDateFormat("yyyyMMdd")
      val hmSDF = new SimpleDateFormat("HHmm")

      val currentDateString = ymdSDF.format(currentDate)
      //根据"相关监测点”,取得当日所有相关监测点车辆速度和车辆数目的信息
      val relationInfo = monitorRealtionList.map(monitorID => (monitorID, jedis.hgetAll(currentDateString + "_" + monitorID)))

      //使用多少小时内的数据进行建模
      val hours = 1
      //本地特征向量
      val dataTrain = ArrayBuffer[LabeledPoint]()
      //特征因子(留个疑问：该因子是否需要每次for循环清空)
      val dataX = ArrayBuffer[Double]()
      //结果因子
      val dataY = ArrayBuffer[Double]()
      //将时间拉回到2小时之前,i的单位为分钟
      for (i <- Range(60 * hours, 2, -1)) {
        dataX.clear()
        dataY.clear()
        //60, 59, 58, 3
        for (index <- 0 to 2) {
          //当前毫秒数 - 1小时之前的毫秒数 + 1小时之前的毫秒数后的0分钟，1分钟，2分钟，3分钟
          //（第3分钟操作作为有监督学习的结果向量）
          val oneMoment = currentDate.getTime - 60 * i * 1000 + 60 * index * 1000
          //格式化历史时间1507 field
          val oneHM = hmSDF.format(new Date(oneMoment))
          //取出相关数据，封装到特征因子中
          for ((k, v) <- relationInfo) {
            //如果已经得到了两个小时前的数据，并且index已经向后滚动到了2
            //"0005" -> Array("0003", "0004", "0005", "0006", "0007"),
            if (k == monitorID && index == 2) { // 因变量
              //index==2时， 下一分钟该数据放置于dataY中
              val nextMoment = oneMoment + 60 * 1 * 1000
              val nextHM = hmSDF.format(new Date(nextMoment))

              //线性滤波
              if (v.containsKey(nextHM)) {  // 有数据上报缺失的点整个 X(0，1，2) = Y(3) 的组合被排除
                val speedAndCount = v.get(nextHM).split("_")
                val valueY = speedAndCount(0).toDouble / speedAndCount(1).toDouble
                dataY += valueY
              }
            }

            //将index等于0~2的情况的数据放置于dataX中 ，自变量 (此处将目标卡口车速也当做因变量入参，因为自身车速才是最大影响因素)
            if (v.containsKey(oneHM)) {
              val speedAndCount = v.get(oneHM).split("_")
              val valueX = speedAndCount(0).toDouble / speedAndCount(1).toDouble
              dataX += valueX
            } else {
              // 有数据上报缺失的点平均车速赋默认值
              dataX += -1.0
            }
          }
        }
        //组装数据，有DataY 缺失的 4min 组个被剔除
        if (dataY.toArray.length == 1) {
          val label = dataY.toArray.head
          //车速情况：0~15   30~60，按十位数划分等级
          val labelPoint = LabeledPoint(if (label.toInt / 10 < 10) label.toInt / 10 else 10, Vectors.dense(dataX.toArray))
          dataTrain += labelPoint
        }
      }
      //打印一下封装好的数据集
      dataTrain.foreach(println(_))
      //将数据集转为RDD
      val rddData = sc.parallelize(dataTrain)
      val randomSplits = rddData.randomSplit(Array(0.8, 0.2), 11L) // 训练集 : 测试集 = 3：2，11l随机数种
      val trainDataRDD = randomSplits(0)
      val testDataRDD = randomSplits(1)

      if (!rddData.isEmpty()) {
        //使用训练集训练模型
        //先学极限，导数，微分，积分，牛顿迭代法，拟牛顿迭代法，LBFGS
        val model = new LogisticRegressionWithLBFGS().setNumClasses(6).run(trainDataRDD) // [0~60) 总共 6各等级
        //评估模型
        val predictionAndLabels = testDataRDD.map {
          case LabeledPoint(label, features) =>
            val prediction = model.predict(features)
            (prediction, label)
        }
        //得到当前监测点的model评估值
        val metrics = new MulticlassMetrics(predictionAndLabels)
        val accuracy = metrics.accuracy
        //评估值范围：0.0~1.0，值越大，model一般越好
        println("\n\n\n评估值：" + accuracy+"\n\n\n")
        writer.write("评估值：" + accuracy)

        //保存模型
        if (accuracy > 0.0) {
          val hdfsPath = "hdfs://localhost:9000/traffic/model/" + monitorID + "_" + new SimpleDateFormat("yyyyMMddHHmm").format(currentDate)
          model.save(sc, hdfsPath)
          jedis.hset("model", monitorID, hdfsPath)
        }
      }
      null
    })
    //释放资源
    RedisUtil.pool.returnResource(jedis)
    sc.stop
    writer.close()
  }
}
