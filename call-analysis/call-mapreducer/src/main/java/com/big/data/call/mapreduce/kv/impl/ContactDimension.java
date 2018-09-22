package com.big.data.call.mapreduce.kv.impl;

import org.apache.hadoop.io.WritableComparable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;


/**
 +-----------+--------------+------+-----+---------+----------------+
 | Field     | Type         | Null | Key | Default | Extra          |
 +-----------+--------------+------+-----+---------+----------------+
 | id        | int(11)      | NO   | PRI | NULL    | auto_increment |
 | telephone | varchar(255) | NO   |     | NULL    |                |
 | name      | varchar(255) | NO   |     | NULL    |                |
 +-----------+--------------+------+-----+---------+----------------+
 */
public class ContactDimension implements WritableComparable{

    private String id;
    private String telephone;
    private String name;

    public ContactDimension() {
        super();
    }

    public void setAll(String id, String telephone, String name) {
        this.id = id;
        this.telephone = telephone;
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setTelephone(String telephone) {
        this.telephone = telephone;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Map<String, Object> getColMap() {
        Map<String,Object> colMap = new HashMap<> ();

        colMap.put ("telephone","'"+telephone+"'");
        colMap.put ("name","'"+name+"'");

        return colMap;
    }

    public int compareTo(Object o) {
        ContactDimension obj = (ContactDimension)o;
        int result = this.toString ().compareTo (obj.toString ());
        return result;
    }

    public void write(DataOutput out) throws IOException {
        out.writeUTF (id);
        out.writeUTF (telephone);
        out.writeUTF (name);
    }

    public void readFields(DataInput in) throws IOException {
        id = in.readUTF ();
        telephone = in.readUTF ();
        name = in.readUTF ();
    }

    public String toString() {
        return "ContactDimension{" +
                "id='" + id + '\'' +
                ", telephone='" + telephone + '\'' +
                ", name='" + name + '\'' +
                '}';
    }
}
