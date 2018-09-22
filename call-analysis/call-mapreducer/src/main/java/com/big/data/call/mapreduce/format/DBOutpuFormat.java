package com.big.data.call.mapreduce.format;

import com.big.data.call.mapreduce.kv.impl.AnalysisValue;
import com.big.data.call.mapreduce.kv.impl.CombineDimension;
import com.big.data.call.mapreduce.kv.impl.ContactDimension;
import com.big.data.call.mapreduce.kv.impl.DateDimension;
import com.big.data.call.mapreduce.util.SQLUtil;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.output.FileOutputCommitter;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

;

public class DBOutpuFormat extends OutputFormat<CombineDimension,AnalysisValue>{

    private String contactsDimensionTab = null;
    private String dateDimensionTab = null;
    private String callTab = null;

    public DBOutpuFormat() {
        this.contactsDimensionTab = "tb_dimension_contacts";
        this.dateDimensionTab = "tb_dimension_date";
        this.callTab = "tb_call";
    }

    @Override
    public RecordWriter<CombineDimension, AnalysisValue> getRecordWriter(TaskAttemptContext context)
            throws IOException, InterruptedException {
        return new DBWriter(contactsDimensionTab,dateDimensionTab,callTab);
    }

    @Override
    public void checkOutputSpecs(JobContext context) throws IOException, InterruptedException {

    }

    @Override
    public OutputCommitter getOutputCommitter(TaskAttemptContext context) throws IOException, InterruptedException {
        String name = context.getConfiguration().get(FileOutputFormat.OUTDIR);
        Path output = name == null ? null : new Path (name);
        return new FileOutputCommitter (output, context);
    }

    private class DBWriter extends RecordWriter<CombineDimension, AnalysisValue>{
        private String contactsDimensionTab ;
        private String dateDimensionTab ;
        private String callTab;

        public DBWriter(String contactsDimensionTab, String dateDimensionTab, String callTab) {
            this.contactsDimensionTab = contactsDimensionTab;
            this.dateDimensionTab = dateDimensionTab;
            this.callTab = callTab;
        }

        @Override
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

                SQLUtil.insertOrUpdate (callTab,colMap,criteriaMap);

            } catch (SQLException e) {
                e.printStackTrace ();
            }
        }

        @Override
        public void close(TaskAttemptContext context) throws IOException, InterruptedException {

        }
    }


}
