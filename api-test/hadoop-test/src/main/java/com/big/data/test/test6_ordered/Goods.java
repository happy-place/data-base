package com.big.data.test.test6_ordered;


import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class Goods implements WritableComparable<Goods> {

    private String orderId;
    private String goodName;
    private double price;

    public Goods() {
        super();
    }

    public Goods(String orderId, String goodName, double price) {
        super();
        this.orderId = orderId;
        this.goodName = goodName;
        this.price = price;
    }

    public void set(String orderId, String goodName, double price) {
        this.orderId = orderId;
        this.goodName = goodName;
        this.price = price;
    }

//    @Override
    public int compareTo(Goods o) {

        int result = orderId.compareTo(o.orderId);

        if (result == 0) {
            result = price > o.getPrice() ? -1 : 1;
        }

        return result;
    }

//    @Override
    public void readFields(DataInput in) throws IOException {
        orderId = in.readUTF();
        goodName = in.readUTF();
        price = in.readDouble();
    }

//    @Override
    public void write(DataOutput out) throws IOException {
        out.writeUTF(orderId);
        out.writeUTF(goodName);
        out.writeDouble(price);
    }

    @Override
    public String toString() {
        return orderId + "\t" + goodName + "\t" + price;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getGoodName() {
        return goodName;
    }

    public void setGoodName(String goodName) {
        this.goodName = goodName;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

}
         
