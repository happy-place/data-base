package com.big.data.test.test3_phoneFlow.bean_as_key;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class TotalFlowReducer extends
        Reducer<FlowBean, FlowBean, FlowBean, NullWritable> {
        
    private FlowBean v = new FlowBean();

    @Override
    protected void reduce(FlowBean key, Iterable<FlowBean> iter, Context context)
            throws IOException, InterruptedException {
        
        long sumUpflow = 0;
        long sumDowmflow = 0;
        
        for (FlowBean flowBean : iter) {
            sumUpflow += flowBean.getUpflow();
            sumDowmflow += flowBean.getDownflow();
        }
        
        v.set(key.getPhoneNum(), sumUpflow, sumDowmflow);
        System.out.println(v);
        context.write(v, NullWritable.get());

    }
        
}
         
