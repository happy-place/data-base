package com.big.data.test.test3_phoneFlow.text_as_key;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

//  Mapper 中FlowBean最作为OutKey时,必须实现Comparable接口,如果仅作为OutValue输出,则可不实现Comparable接口
public class FlowBean implements Writable {
        
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

    public void write(DataOutput out) throws IOException {
        out.writeUTF(phoneNum);
        out.writeLong(upflow);
        out.writeLong(downflow);
        out.writeLong(totalflow);
    }

    public void readFields(DataInput in) throws IOException {
        phoneNum = in.readUTF();
        upflow = in.readLong();
        downflow = in.readLong();
        totalflow = in.readLong();
    }
        
 //  public  int  compareTo(FlowBean o) {
//    return  totalflow >o.getTotalflow()?-1:1;
//  }
                
}
         
