package com.big.data.test.test7_join;


import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class OrderBean implements WritableComparable<OrderBean> {

    private String orderId;
    private String goodsId;
    private String goodsName;
    private int amount;

    public OrderBean() {
        super();
    }

    public OrderBean(String orderId, String goodsId, String goodsName,
                     int amount) {
        super();
        this.orderId = orderId;
        this.goodsId = goodsId;
        this.goodsName = goodsName;
        this.amount = amount;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getGoodsId() {
        return goodsId;
    }

    public void setGoodsId(String goodsId) {
        this.goodsId = goodsId;
    }

    public String getGoodsName() {
        return goodsName;
    }

    public void setGoodsName(String goodsName) {
        this.goodsName = goodsName;
    }

    public int getAmount() {
        return amount;
    }

    public void setAmount(int amount) {
        this.amount = amount;
    }

    @Override
    public String toString() {
        return orderId + "\t" + goodsId + "\t" + goodsName + "\t" + amount;
    }

//    @Override
    public int compareTo(OrderBean o) {

        int result = goodsId.compareTo(o.getGoodsId());
        if (result == 0) {
            result = amount > o.getAmount() ? -1 : 1;
        }
        return result;
    }

//    @Override
    public void readFields(DataInput in) throws IOException {
        orderId = in.readUTF();
        goodsId = in.readUTF();
        goodsName = in.readUTF();
        amount = in.readInt();
    }

//    @Override
    public void write(DataOutput out) throws IOException {
        out.writeUTF(orderId);
        out.writeUTF(goodsId);
        out.writeUTF(goodsName);
        out.writeInt(amount);
    }
}
         
