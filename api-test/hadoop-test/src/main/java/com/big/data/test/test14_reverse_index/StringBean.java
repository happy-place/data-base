package com.big.data.test.test14_reverse_index;


import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class StringBean implements WritableComparable<StringBean> {

    private String target;
    private String path;
    private int hint;

    
    public void write(DataOutput out) throws IOException {
        out.writeUTF(target);
        out.writeUTF(path);
        out.writeInt(hint);
    }

    public void readFields(DataInput in) throws IOException {
        target = in.readUTF();
        path = in.readUTF();
        hint = in.readInt();
    }

    public int compareTo(StringBean o) {
        int result = o.getTarget().compareTo(target);
        if (result == 0) {
            result = hint > o.getHint() ? -1 : 1;
        }
        return result;
    }

    public StringBean() {
        super();
    }

    public StringBean(String target, String path, int hint) {
        super();
        this.target = target;
        this.path = path;
        this.hint = hint;
    }

    public String getTarget() {
        return target;
    }

    public void setTarget(String target) {
        this.target = target;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public int getHint() {
        return hint;
    }

    public void setHint(int hint) {
        this.hint = hint;
    }

    @Override
    public String toString() {
        return target + "\t" + path + "\t" + hint;
    }

}
         
