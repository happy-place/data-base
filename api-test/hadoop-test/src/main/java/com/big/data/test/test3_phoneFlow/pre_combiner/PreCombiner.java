package com.big.data.test.test3_phoneFlow.pre_combiner;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

// map-task 节点提前进行局部汇总
public class PreCombiner extends Reducer<Text, FlowBean, Text, FlowBean> {

    private FlowBean v = new FlowBean();

    @Override
    protected void reduce(Text key, Iterable<FlowBean> iter, Context context)
            throws IOException, InterruptedException {

        long sumUpflow = 0;
        long sumDowmflow = 0;

        for (FlowBean flowBean : iter) {
            sumUpflow += flowBean.getUpflow();
            sumDowmflow += flowBean.getDownflow();
        }

        v.set(key.toString(), sumUpflow, sumDowmflow);

        context.write(key, v);

    }

}
         
