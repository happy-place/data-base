package com.big.data.test.test7_join;


import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;

public class GroupingComparator extends WritableComparator {

    public GroupingComparator() {
        super(OrderBean.class, true);
    }

    @Override
    public int compare(WritableComparable a, WritableComparable b) {

        OrderBean bean1 = (OrderBean) a;
        OrderBean bean2 = (OrderBean) b;

        return bean1.getGoodsId().compareTo(bean2.getGoodsId());
    }

}
         
