package com.big.data.call.mapreduce.job;

import com.big.data.call.mapreduce.kv.impl.CombineDimension;
import com.big.data.call.mapreduce.kv.impl.ContactDimension;
import com.big.data.call.mapreduce.kv.impl.DateDimension;
import org.apache.commons.lang.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.IntWritable;

import java.io.IOException;

public class LogMapper extends TableMapper<CombineDimension, IntWritable> {

    private static Log LOG = LogFactory.getLog (LogMapper.class);

    private static String callerFamily = null;
    private static String calleeFamily = null;
    private static String callerFlag = null;
    private static String calleeFlag = null;

    static{
        callerFamily = "caller";
        calleeFamily = "callee";
        callerFlag = "1";
        calleeFlag = "0";
    }

    private CombineDimension keyOut = new CombineDimension();
    private IntWritable valueOut = new IntWritable();

    private ContactDimension caller = new ContactDimension ();
    private ContactDimension callee = new ContactDimension ();

    private DateDimension dateDimension = new DateDimension ();

    /**
     * put: partitionCode_beforePhone_callTime_afterPhone_duration_flag
     * 0?_16756356329_20101010092345_18256376789_0200_1
     * -----------------------------------------------------------------
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(ImmutableBytesWritable key, Result value, Context context)
            throws IOException, InterruptedException {

        String rowkey = Bytes.toString (value.getRow ());

        String[] fields = rowkey.split ("_");

        String flag = fields[5];

        // 只统计主叫记录,基于此记录能同时追踪到主叫和被叫用户,能有效减轻mapper压力
        if(StringUtils.equals (calleeFlag,flag)){
            return ;
        }

        String callerPhone = fields[1];

        String callTime = fields[2];

        String calleePhone = fields[3];
        Integer duration = Integer.parseInt (fields[4]);

        valueOut.set (duration);

        byte[] callerFamilyBytes = Bytes.toBytes ("caller");

        byte[] callerNamesBytes = Bytes.toBytes ("callerName");

        Cell columnLatestCell = value.getColumnLatestCell (callerFamilyBytes, callerNamesBytes);

        byte[] value1 = columnLatestCell.getValue ();

        String callerName = Bytes.toString (value1);
        String calleeName = Bytes.toString (value.getColumnLatestCell (Bytes.toBytes (callerFamily), Bytes.toBytes ("calleeName")).getValue ());

        String callerId = callerFlag+"_"+callerPhone;
        String calleeId = calleeFlag+"_"+calleePhone;

        caller.setAll (callerId,callerPhone,callerName);
        callee.setAll (calleeId,calleePhone,calleeName);

        Integer year = Integer.parseInt (callTime.substring (0,4));
        Integer month = Integer.parseInt (callTime.substring (4,6));
        Integer day = Integer.parseInt (callTime.substring (6,8));

        // 1).按年统计
        String toYearId = year+"_-1_-1";
        dateDimension.setAll (toYearId,year,-1,-1);

        keyOut.setAll (caller,dateDimension);
        context.write (keyOut,valueOut);

        keyOut.setAll (callee,dateDimension);
        context.write (keyOut,valueOut);

        // 2).按月统计
        String toMonthId = year+"_"+month+"_-1";
        dateDimension.setAll (toMonthId,year,month,-1);

        keyOut.setAll (caller,dateDimension);
        context.write (keyOut,valueOut);

        keyOut.setAll (callee,dateDimension);
        context.write (keyOut,valueOut);

        // 3).按日统计
        String toDayId = year+"_"+month+"_"+day;
        dateDimension.setAll (toDayId,year,month,day);

        keyOut.setAll (caller,dateDimension);
        context.write (keyOut,valueOut);

        keyOut.setAll (callee,dateDimension);
        context.write (keyOut,valueOut);

    }


}
