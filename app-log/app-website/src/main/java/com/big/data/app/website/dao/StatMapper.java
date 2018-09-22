package com.big.data.app.website.dao;


import com.big.data.app.website.domain.StatBean;

import java.util.List;

/**
 * BaseDao接口
 */
public interface StatMapper<T> {

    List<StatBean> findThisWeekNewUsers(String appid);
}
