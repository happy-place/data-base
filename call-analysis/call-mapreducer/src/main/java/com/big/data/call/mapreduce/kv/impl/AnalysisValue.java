package com.big.data.call.mapreduce.kv.impl;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class AnalysisValue  implements Writable {

    private int callCount;
    private int durationCount;

    public void setAll(int callCount,int durationCount) {
        this.callCount = callCount;
        this.durationCount = durationCount;
    }

    public int getCallCount() {
        return callCount;
    }

    public void setCallCount(int callCount) {
        this.callCount = callCount;
    }

    public int getDurationCount() {
        return durationCount;
    }

    public void setDurationCount(int durationCount) {
        this.durationCount = durationCount;
    }

    public void write(DataOutput out) throws IOException {
        out.writeInt (callCount);
        out.writeInt (durationCount);
    }

    public void readFields(DataInput in) throws IOException {
        callCount = in.readInt ();
        durationCount = in.readInt ();
    }

    public String toString() {
        return "AnalysisValue{" +
                "callCount=" + callCount +
                ", durationCount=" + durationCount +
                '}';
    }
}
