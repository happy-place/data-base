package com.big.data.test.test14_reverse_index;

import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;

public class GroupingComparator extends WritableComparator {
        
    public GroupingComparator() {
        super(StringBean.class, true);
    }
    
    // 自定义Bean对象作为分 Mapper 输出的key时,选取指定属性作为分组标识时,先在Bean的comparTo方法中设置多次排序
    // 被选定为分组标准的属性,必须作为最外层排序的条件,分组过程一旦检索到组块的边界,立即打包发射,不会遍历全部元素
    @Override
    public int compare(WritableComparable a, WritableComparable b) {
        StringBean bean1 = (StringBean) a;
        StringBean bean2 = (StringBean) b;
        return bean1.getTarget().compareTo(bean2.getTarget());
    }
    
}
         
