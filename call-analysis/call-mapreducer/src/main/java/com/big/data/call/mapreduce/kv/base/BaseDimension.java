package com.big.data.call.mapreduce.kv.base;

import org.apache.hadoop.io.WritableComparable;

import java.util.Map;

public abstract  class BaseDimension implements WritableComparable{

    abstract String getId();

    abstract void setId(String id);

    abstract Map<String,Object> getColMap();

}
