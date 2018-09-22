package com.big.data.test.test3_phoneFlow.bean_as_key;

import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

// Mapper中FlowBean最作为OutKey时,必须实现Comparable接口,如果仅作为OutValue输出,则可不实现Comparable接口
public class FlowBean implements WritableComparable<FlowBean> {
 
    private String phoneNum;
    private long upflow;
    private long downflow;
    private long totalflow;
 

    public FlowBean() {
        super();
    }
 

    public FlowBean(String phoneNum, long upflow, long downflow, long totalflow) {
        super();
        this.phoneNum = phoneNum;
        this.upflow = upflow;
        this.downflow = downflow;
        this.totalflow = totalflow;
    }

    public void set(String phoneNum, long upflow, long downflow) {
        this.phoneNum = phoneNum;
        this.upflow = upflow;
        this.downflow = downflow;
        this.totalflow = upflow + downflow;
    }
 

    public String getPhoneNum() {
        return phoneNum;
    }
 

    public void setPhoneNum(String phoneNum) {
        this.phoneNum = phoneNum;
    }
 

    public long getUpflow() {
        return upflow;
    }
 

    public void setUpflow(long upflow) {
        this.upflow = upflow;
    }
 

    public long getDownflow() {
        return downflow;
    }
 

    public void setDownflow(long downflow) {
        this.downflow = downflow;
    }
 

    public long getTotalflow() {
        return totalflow;
    }
 

    public void setTotalflow(long totalflow) {
        this.totalflow = totalflow;
    }
 

    @Override
    public String toString() {
        return "phoneNum=" + phoneNum + "\tupflow=" + upflow + "\tdownflow="
                + downflow + "\ttotalflow=" + totalflow;
    }
 

//    @Override
    public void write(DataOutput out) throws IOException {
        out.writeUTF(phoneNum);
        out.writeLong(upflow);
        out.writeLong(downflow);
        out.writeLong(totalflow);
    }
 

//    @Override
    public void readFields(DataInput in) throws IOException {
        phoneNum = in.readUTF();
        upflow = in.readLong();
        downflow = in.readLong();
        totalflow = in.readLong();
    }
//
//    @Override
//    public boolean equals(Object o) {
//        if (this == o) return true;
//        if (o == null || getClass() != o.getClass()) return false;
//        FlowBean flowBean = (FlowBean) o;
//        return flowBean.phoneNum == this.phoneNum;
//    }
//
//    @Override
//    public int hashCode() {
//        return Objects.hash(this.phoneNum);
//    }

    // 通过 WriteableComparable 接口的compareTo 方法判定 key 是否一致
    public int compareTo(FlowBean o) {
        return this.phoneNum.hashCode() - o.phoneNum.hashCode();
    }
 
}
 

