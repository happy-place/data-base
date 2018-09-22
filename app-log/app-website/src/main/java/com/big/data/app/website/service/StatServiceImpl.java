package com.big.data.app.website.service;

import com.big.data.app.website.dao.StatMapper;
import com.big.data.app.website.domain.StatBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 统计服务
 */
@Service("statService")
public class StatServiceImpl implements StatService {

    @Autowired
    StatMapper statMapper;

    public List<StatBean> findThisWeekNewUsers(String sdk34734) {
        return statMapper.findThisWeekNewUsers(sdk34734);
    }
}
