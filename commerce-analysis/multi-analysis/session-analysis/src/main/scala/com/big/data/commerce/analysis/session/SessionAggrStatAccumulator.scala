package com.big.data.commerce.analysis.session

import org.apache.spark.util.AccumulatorV2

import scala.collection._

class SessionAggrStatAccumulator extends AccumulatorV2[String,mutable.HashMap[String,Int]]{

  private val aggrStatMap = mutable.HashMap[String,Int]()

  override def isZero: Boolean = {
    aggrStatMap.isEmpty
  }

  override def copy(): AccumulatorV2[String, mutable.HashMap[String, Int]] = {
    val newacc = new SessionAggrStatAccumulator
    aggrStatMap.synchronized{
      newacc.aggrStatMap ++= this.aggrStatMap
    }
    newacc
  }

  override def reset(): Unit = {
    aggrStatMap.clear()
  }

  override def add(v: String): Unit = {
    if(!aggrStatMap.contains(v)){
      aggrStatMap += (v -> 0)
    }
    aggrStatMap.update(v,aggrStatMap(v) + 1)
  }

  override def merge(other: AccumulatorV2[String, mutable.HashMap[String, Int]]): Unit = {
    other match {
      case acc:SessionAggrStatAccumulator => {

        (this.aggrStatMap /: acc.value){ case (map,(k,v)) =>
          map += (k -> (v + map.getOrElse(k,0)))
        }

      }
    }
  }

  override def value: mutable.HashMap[String, Int] = {
    aggrStatMap
  }
}
