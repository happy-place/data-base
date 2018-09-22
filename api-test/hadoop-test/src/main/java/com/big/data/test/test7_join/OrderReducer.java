package com.big.data.test.test7_join;


import org.apache.commons.beanutils.BeanUtils;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class OrderReducer extends Reducer<OrderBean, OrderBean, OrderBean, NullWritable> {

    private List<OrderBean> orders = new ArrayList<OrderBean>();
    private String goodsName = null;

    @Override
    protected void reduce(OrderBean key, Iterable<OrderBean> iter, Context context)
            throws IOException, InterruptedException {

        for (OrderBean orderBean : iter) {
            OrderBean tmp = new OrderBean();
            System.out.println(orderBean.getOrderId()+"\t"+orderBean.getGoodsId()+"\t"+orderBean.getGoodsName()+"\t"+orderBean.getAmount());
            if ("null".equals(orderBean.getOrderId())) {
                goodsName = orderBean.getGoodsName();
            } else {
                try {

                    BeanUtils.copyProperties(tmp, orderBean);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                orders.add(tmp);
            }
        }

        for (OrderBean orderBean : orders) {
            orderBean.setGoodsName(goodsName);
            context.write(orderBean, NullWritable.get());
        }

        orders.clear();
    }

}
         

