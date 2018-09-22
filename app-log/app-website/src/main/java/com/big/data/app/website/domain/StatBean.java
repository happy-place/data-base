package com.big.data.app.website.domain;
/**
 * 统计信息
 */
public class StatBean {
    //统计日期
    private String date ;
    //统计数量
    private long count ;

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }
}

