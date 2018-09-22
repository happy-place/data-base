package com.big.data.test.test7_join;


import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class OrderMapper extends Mapper<LongWritable, Text, OrderBean, OrderBean> {

    private OrderBean bean = new OrderBean();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split(" ");

        if (fields.length == 3) {
            bean.setOrderId(fields[0]);
            bean.setGoodsId(fields[1]);
            bean.setGoodsName("null");
            bean.setAmount(Integer.parseInt(fields[2]));
        } else if (fields.length == 2) {
            bean.setOrderId("null");
            bean.setGoodsId(fields[0]);
            bean.setGoodsName(fields[1]);
            bean.setAmount(-1);
        }

//        System.out.println(bean.getOrderId()+"\t"+bean.getGoodsId()+"\t"+bean.getGoodsName()+"\t"+bean.getAmount());
        context.write(bean, bean);

    }

}
         

