package com.big.data.app.website.service;

import com.big.data.app.website.domain.StatBean;

import java.util.List;

/**
 * Service
 */
public interface StatService {

    List<StatBean> findThisWeekNewUsers(String appid);
}
