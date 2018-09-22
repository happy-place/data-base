package com.big.data.call.mapreduce.kv.impl;

import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 +-------------------+--------------+------+-----+---------+-------+
 | Field             | Type         | Null | Key | Default | Extra |
 +-------------------+--------------+------+-----+---------+-------+
 | id_date_contact   | varchar(255) | NO   | PRI | NULL    |       |
 | id_date_dimension | int(11)      | NO   |     | NULL    |       |
 | id_contact        | int(11)      | NO   |     | NULL    |       |
 | call_sum          | int(11)      | NO   |     | NULL    |       |
 | call_duration_sum | int(11)      | NO   |     | NULL    |       |
 +-------------------+--------------+------+-----+---------+-------+
 */
public class CombineDimension implements WritableComparable {

    private String id;

    private ContactDimension contactDimension = new ContactDimension();

    private DateDimension dateDimension  = new DateDimension();

    public CombineDimension() {
        super();
    }

    public String getId() {
        return this.id;
    }

    public void setAll(ContactDimension contactDimension,DateDimension dateDimension) {
        this.contactDimension = contactDimension;
        this.dateDimension = dateDimension;
        this.id = dateDimension.getId ()+"_"+contactDimension.getId ();
    }

    public void setId(String id) {
        this.id = id;
    }

    public ContactDimension getContactDimension() {
        return contactDimension;
    }

    public void setContactDimension(ContactDimension contactDimension) {
        this.contactDimension = contactDimension;
    }

    public DateDimension getDateDimension() {
        return dateDimension;
    }

    public void setDateDimension(DateDimension dateDimension) {
        this.dateDimension = dateDimension;
    }

    public Map<String, Object> getCriteriaMap() {
        Map<String,Object> criteriaMap = new HashMap<> ();

        criteriaMap.put("id_date_contact", "'"+this.id+"'");

        return criteriaMap;
    }

    public Map<String, Object> getColMap() {
        Map<String,Object> colMap = new HashMap<> ();

        colMap.putAll (this.contactDimension.getColMap ());
        colMap.putAll (this.dateDimension.getColMap ());

        return colMap;
    }

    public int compareTo(Object o) {
        CombineDimension obj = (CombineDimension)o;
        int result = this.contactDimension.compareTo (obj.contactDimension);
        if(result ==0 ){
            result = this.dateDimension.compareTo (obj.dateDimension);
        }
        return result;
    }

    public void write(DataOutput out) throws IOException {
        out.writeUTF (id);
        this.contactDimension.write (out);
        this.dateDimension.write (out);
    }

    public void readFields(DataInput in) throws IOException {
        this.id = in.readUTF ();
        this.contactDimension.readFields (in);
        this.dateDimension.readFields (in);
    }
}
