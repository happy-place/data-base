package com.big.data.app.website.controller;

import com.big.data.app.website.domain.StatBean;
import com.big.data.app.website.service.StatService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 统计分析类
 */
@Controller
@RequestMapping("/stat")
public class StatController {

    @Resource(name="statService")
    private StatService ss ;

    /**
     * 统计每周每天新增用户数
     */
    @RequestMapping("/week1")
    @ResponseBody
    public Map<String, Object> stat3() {

        // 1 查询每周每天新增用户数
        List<StatBean> list = ss.findThisWeekNewUsers("sdk34734");
        Map<String,Object> map = new HashMap<String,Object>();

        String[] xlabels = new String[list.size()] ;
        long[] newUsers = new long[list.size()];

        // 2 将查询结果复制给数组
        for(int i = 0 ; i < list.size() ; i ++){
            xlabels[i] = list.get(i).getDate();
            newUsers[i] = list.get(i).getCount();
        }

        // 3 把数组复制给map集合
        map.put("date",xlabels);
        map.put("count", newUsers);

        return map ;
    }
}
