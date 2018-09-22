package com.big.data.call.mapreduce.test;

import com.big.data.call.mapreduce.kv.impl.AnalysisValue;
import com.big.data.call.mapreduce.kv.impl.CombineDimension;
import com.big.data.call.mapreduce.kv.impl.ContactDimension;
import com.big.data.call.mapreduce.kv.impl.DateDimension;
import com.big.data.call.mapreduce.util.SQLUtil;
import org.junit.Test;

import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

public class SQLTest {

    @Test
    public void getOrInsertGet(){

        Map<String,Object> map1 = new HashMap<> ();
        map1.put ("telephone","'18674257465'");
        map1.put ("name","'aa'");

        Map<String,Object> map2 = new HashMap<> ();
        map2.put ("year","'2017'");
        map2.put ("month","'08'");
        map2.put ("day","'23'");


        try {
            SQLUtil.getOrInsertGet("tb_dimension_contacts","01_18674257465",map1);
            SQLUtil.getOrInsertGet("tb_dimension_date","2017_08_23",map2);
        } catch (SQLException e) {
            e.printStackTrace ();
        }
    }

    // insertOrUpdate(String tableName,Map<String, Object> colMap,Map<String, Object> criteriaMap) throws SQLException {
    @Test
    public void insertOrUpdate(){

        CombineDimension combineDimension = new CombineDimension ();
        AnalysisValue analysisValue = new AnalysisValue ();
        analysisValue.setAll (10,100);

        ContactDimension contactDimension = new ContactDimension ();
        contactDimension.setAll ("01_18674257465","18674257465","aa");

        DateDimension dateDimension = new DateDimension ();
        dateDimension.setAll ("2017_08_23",2017,8,23);

        combineDimension.setAll (contactDimension,dateDimension);

        try {
            String contactId = SQLUtil.getOrInsertGet ("tb_dimension_contacts", contactDimension.getId (), contactDimension.getColMap ());
            String dataId = SQLUtil.getOrInsertGet ("tb_dimension_date", dateDimension.getId (), dateDimension.getColMap ());
            contactDimension.setId (contactId);
            dateDimension.setId (dataId);
        }catch (Exception r){
            r.printStackTrace ();
        }

        Map<String,Object> colMap = new HashMap<> ();

        colMap.put ("id_date_contact","'"+combineDimension.getId ()+"'");
        colMap.put ("id_date_dimension",dateDimension.getId ());
        colMap.put ("id_contact_dimension",contactDimension.getId ());

        colMap.put ("call_sum",analysisValue.getCallCount ());
        colMap.put ("call_duration_sum",analysisValue.getDurationCount ());

        Map<String,Object> criteriaMap = new HashMap<> ();
        criteriaMap.put ("id_date_contact","'"+combineDimension.getId ()+"'");

        try {
            SQLUtil.insertOrUpdate("tb_call", colMap, criteriaMap);
        } catch (SQLException e) {
            e.printStackTrace ();
        }
    }

    @Test
    public void insertOrUpdate2(){

        CombineDimension combineDimension1 = new CombineDimension();
        CombineDimension combineDimension2 = new CombineDimension ();
        CombineDimension combineDimension3 = new CombineDimension ();
        CombineDimension combineDimension4 = new CombineDimension ();

        AnalysisValue analysisValue1 = new AnalysisValue();
        AnalysisValue analysisValue2 = new AnalysisValue ();
        AnalysisValue analysisValue3 = new AnalysisValue ();
        AnalysisValue analysisValue4 = new AnalysisValue ();

        analysisValue1.setAll (10,100);
        analysisValue2.setAll (20,100);
        analysisValue3.setAll (30,100);
        analysisValue4.setAll (40,1000);

        ContactDimension contactDimension1 = new ContactDimension ();
        ContactDimension contactDimension2 = new ContactDimension();
        ContactDimension contactDimension3 = new ContactDimension ();

        contactDimension1.setAll ("01_18674257465","18674257465","aa");
        contactDimension2.setAll ("01_17674257465","17674257465","bb");
        contactDimension3.setAll ("01_19674257465","19674257465","cc");

        DateDimension dateDimension1 = new DateDimension();
        DateDimension dateDimension2 = new DateDimension ();
        DateDimension dateDimension3 = new DateDimension ();

        dateDimension1.setAll ("2017_08_23",2017,8,23);
        dateDimension2.setAll ("2017_08_-1",2017,8,-1);
        dateDimension3.setAll ("2017_-1_-1",2017,-1,-1);

        combineDimension1.setAll (contactDimension1,dateDimension1);
        combineDimension2.setAll (contactDimension2,dateDimension2);
        combineDimension3.setAll (contactDimension3,dateDimension3);
        combineDimension4.setAll (contactDimension2,dateDimension2);

        DBWriter dw = new DBWriter();

        try {
            dw.write (combineDimension1,analysisValue1);
            dw.write (combineDimension2,analysisValue2);
            dw.write (combineDimension3,analysisValue3);

            dw.write (combineDimension4,analysisValue4);
        } catch (IOException e) {
            e.printStackTrace ();
        } catch (InterruptedException e) {
            e.printStackTrace ();
        }

    }



}
