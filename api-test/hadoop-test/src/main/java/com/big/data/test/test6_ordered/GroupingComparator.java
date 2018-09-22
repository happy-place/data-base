package com.big.data.test.test6_ordered;

import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;


public class GroupingComparator extends WritableComparator {

    public GroupingComparator() {
        super(Goods.class, true);
    }

    @Override
    public int compare(WritableComparable a, WritableComparable b) {

        Goods goods1 = (Goods) a;
        Goods goods2 = (Goods) b;

        return goods1.getOrderId().compareTo(goods2.getOrderId());
    }

}
         
