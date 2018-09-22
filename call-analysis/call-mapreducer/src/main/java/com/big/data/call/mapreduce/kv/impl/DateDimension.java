package com.big.data.call.mapreduce.kv.impl;

import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 +-------+---------+------+-----+---------+----------------+
 | Field | Type    | Null | Key | Default | Extra          |
 +-------+---------+------+-----+---------+----------------+
 | id    | int(11) | NO   | PRI | NULL    | auto_increment |
 | year  | int(11) | NO   |     | NULL    |                |
 | month | int(11) | NO   |     | NULL    |                |
 | day   | int(11) | NO   |     | NULL    |                |
 +-------+---------+------+-----+---------+----------------+
 */
public class DateDimension implements WritableComparable{

    private String id;
    private Integer year;
    private Integer month;
    private Integer day;

    public DateDimension() {
        super();
    }

    public void setAll(String id, Integer year, Integer month, Integer day) {
        this.id = id;
        this.year = year;
        this.month = month;
        this.day = day;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getYear() {
        return year;
    }

    public void setYear(Integer year) {
        this.year = year;
    }

    public Integer getMonth() {
        return month;
    }

    public void setMonth(Integer month) {
        this.month = month;
    }

    public Integer getDay() {
        return day;
    }

    public void setDay(Integer day) {
        this.day = day;
    }

    public Map<String, Object> getColMap() {
        Map<String,Object> colMap = new HashMap<> ();

        colMap.put ("year","'"+year+"'");
        colMap.put ("month","'"+month+"'");
        colMap.put ("day","'"+day+"'");

        return colMap;
    }

    public int compareTo(Object o) {
        DateDimension obj = (DateDimension)o;
        int result = this.toString ().compareTo (obj.toString ());
        return result;
    }

    public void write(DataOutput out) throws IOException {
        out.writeUTF (id);
        out.writeInt (year);
        out.writeInt (month);
        out.writeInt (day);
    }

    public void readFields(DataInput in) throws IOException {
        id = in.readUTF ();
        year = in.readInt ();
        month = in.readInt ();
        day = in.readInt ();
    }

    public String toString() {
        return "DateDimension{" +
                "id='" + id + '\'' +
                ", year=" + year +
                ", month=" + month +
                ", day=" + day +
                '}';
    }
}
