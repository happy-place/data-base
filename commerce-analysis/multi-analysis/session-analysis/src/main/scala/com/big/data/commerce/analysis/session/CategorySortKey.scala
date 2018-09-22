package com.big.data.commerce.analysis.session

/**
  * 主要用于根据业务规则来排序
  */
case class CategorySortKey(val clickCount:Int,
                           val orderCount:Int,
                           val payCount:Int) extends Ordered[CategorySortKey]{

  /** Result of comparing `this` with operand `that`.
    *
    * Implement this method to determine how instances of A will be sorted.
    *
    * Returns `x` where:
    *
    *   - `x < 0` when `this < that`
    *
    *   - `x == 0` when `this == that`
    *
    *   - `x > 0` when  `this > that`
    *
    */
  override def compare(that: CategorySortKey): Int = {

    if((this.clickCount - that.clickCount) !=0){
      return (this.clickCount - that.clickCount)
    } else if((this.orderCount - that.orderCount) !=0){
      return (this.orderCount - that.orderCount)
    } else if((this.payCount - that.payCount) !=0){
      return (this.payCount - that.payCount)
    } else
      0
  }
}
