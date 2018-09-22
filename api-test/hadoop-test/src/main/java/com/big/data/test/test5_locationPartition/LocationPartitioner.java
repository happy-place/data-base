package com.big.data.test.test5_locationPartition;


import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Partitioner;


public class LocationPartitioner extends Partitioner<Text, FlowBean> {

    @Override
    public int getPartition(Text key, FlowBean value, int numReduceTasks) {

        int result = 4;

        String prefix = key.toString().substring(0, 3);

        if ("136".equals(prefix)) {
            result = 0;
        } else if ("137".equals(prefix)) {
            result = 1;
        } else if ("138".equals(prefix)) {
            result = 2;
        } else if ("139".equals(prefix)) {
            result = 3;
        }

        return result;
    }

}
         

