package com.big.data.test.test6_ordered;


import com.big.data.test.test5_locationPartition.FlowBean;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Partitioner;


public class IdPartitioner extends Partitioner<Goods, Goods> {

    @Override
    public int getPartition(Goods key, Goods value, int numReduceTasks) {

        int partition = key.getOrderId().hashCode() % numReduceTasks;

        return partition;
    }

}
         

