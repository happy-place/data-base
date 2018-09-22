package com.big.data.commerce.common

/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/5/29
  * Desc: 
  *
  */

  /**
    * 数量：100
    *
    * @param user_id      用户的ID[1 - 100]
    * @param username     用户的名称[user + id]
    * @param name         用户的姓名[name + id]
    * @param age          用户的年龄[1 - 60]
    * @param professional 用户的职业[profess + [1 - 100]
    * @param city         用户所在的城市[1 - 10]
    * @param sex          用户的性别[male,female]
    */
  case class UserInfo(user_id: Int,
                      username: String,
                      name: String,
                      age: String,
                      professional: String,
                      city: String,
                      sex: String)

  /**
    * 数量：100
    *
    * @param product_id   商品的ID[1 - 100]
    * @param product_name 商品的名称[product + id]
    * @param extend_info  是否为自营商品 [0,1]
    */
  case class ProductInfo(product_id: Int,
                         product_name: String,
                         extend_info: String)

  /**
    * 100个用户 => 每个用户10个Session => 每个Session100以内随机Action  ("search", "click", "order", "pay")不能同时出现
    *
    * @param date               Session发生的日期yyyy-MM-dd
    * @param user_id            用户的ID[1 - 100]
    * @param session_id         sessionde唯一标识UUID
    * @param page_id            用户点击的页面[1 - 10]
    * @param action_time        行为发生的具体时间yyyy-MM-dd hh:mm:ss
    * @param search_keyword     搜索的关键字，从("火锅", "蛋糕", "重庆辣子鸡", "重庆小面", "呷哺呷哺", "新辣道鱼火锅", "国贸大厦", "太古商场", "日本料理", "温泉")
    * @param click_category_id  点击的物品的类别ID[1 - 100]
    * @param click_product_id   点击的物品ID类[1 - 100]
    * @param order_categroy_ids 下单的物品的类别ID[1 - 100]
    * @param order_product_ids  下单的物品ID[1 - 100]
    * @param pay_product_ids    支付的物品ID[1 - 100]
    * @param pay_categroy_ids   支付的物品的类别的ID[1 - 100]
    * @param city_id            行为发生的城市[1 - 10]
    */
  case class UserVisitAction(date: String,
                             user_id: Int,
                             session_id: String,
                             page_id: String,
                             action_time: String,
                             search_keyword: String,
                             click_category_id: String,
                             click_product_id: String,
                             order_categroy_ids: String,
                             order_product_ids: String,
                             pay_product_ids: String,
                             pay_categroy_ids: String,
                             city_id: String)

