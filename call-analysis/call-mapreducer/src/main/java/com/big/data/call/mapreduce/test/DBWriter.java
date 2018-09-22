package com.big.data.call.mapreduce.test;

import com.big.data.call.mapreduce.kv.impl.AnalysisValue;
import com.big.data.call.mapreduce.kv.impl.CombineDimension;
import com.big.data.call.mapreduce.kv.impl.ContactDimension;
import com.big.data.call.mapreduce.kv.impl.DateDimension;
import com.big.data.call.mapreduce.util.SQLUtil;

import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

public class DBWriter {
        private String contactsDimensionTab = "tb_dimension_contacts";
        private String dateDimensionTab = "tb_dimension_date";

        public DBWriter() {}

        public void write(CombineDimension key, AnalysisValue value) throws IOException, InterruptedException {
            ContactDimension contactDimension = key.getContactDimension ();
            DateDimension dateDimension = key.getDateDimension ();

            try {
                
                String contactId = SQLUtil.getOrInsertGet (contactsDimensionTab, contactDimension.getId (), contactDimension.getColMap ());
                contactDimension.setId (contactId);

                String dateId = SQLUtil.getOrInsertGet (dateDimensionTab, dateDimension.getId (), dateDimension.getColMap ());
                dateDimension.setId (dateId);

                Map<String,Object> colMap = new HashMap<> ();

                colMap.put ("id_date_contact","'"+key.getId ()+"'");
                colMap.put ("id_date_dimension",dateDimension.getId ());
                colMap.put ("id_contact_dimension",contactDimension.getId ());

                colMap.put ("call_sum",value.getCallCount ());
                colMap.put ("call_duration_sum",value.getDurationCount ());

                Map<String,Object> criteriaMap = new HashMap<> ();
                criteriaMap.put ("id_date_contact","'"+key.getId ()+"'");

                SQLUtil.insertOrUpdate ("tb_call",colMap,criteriaMap);

            } catch (SQLException e) {
                e.printStackTrace ();
            }
        }

    }