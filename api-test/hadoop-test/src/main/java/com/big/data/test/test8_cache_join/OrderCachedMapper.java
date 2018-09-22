package com.big.data.test.test8_cache_join;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

public class OrderCachedMapper extends
        Mapper<LongWritable, Text, OrderCachedBean, OrderCachedBean> {

    private OrderCachedBean bean = new OrderCachedBean();

    private Map<String, String> pdMap = new HashMap<String, String>();

    @SuppressWarnings("deprecation")
    @Override
    protected void setup(Context context) throws IOException,
            InterruptedException {
        URI cache = context.getCacheFiles()[0];

        Configuration conf = context.getConfiguration();

        FileSystem fs = FileSystem.get(conf);

        FSDataInputStream fis = fs.open(new Path(cache));

        BufferedReader reader = new BufferedReader(new InputStreamReader(fis));

        String line = null;

        while (!StringUtils.isEmpty(line = reader.readLine())) {
            String[] fields = line.split(" ");
            pdMap.put(fields[0], fields[1]);
        }

    }

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] fields = line.split(" ");

        bean.setOrderId(fields[0]);
        bean.setGoodsId(fields[1]);
        bean.setGoodsName(pdMap.get(fields[1]));
        bean.setAmount(Integer.parseInt(fields[2]));

        context.write(bean, bean);

    }

}
         
