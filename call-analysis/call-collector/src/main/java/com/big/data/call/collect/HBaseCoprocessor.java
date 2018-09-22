package com.big.data.call.collect;


import com.big.data.call.common.PropertiesUtil;
import org.apache.commons.lang.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Durability;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.coprocessor.BaseRegionObserver;
import org.apache.hadoop.hbase.coprocessor.ObserverContext;
import org.apache.hadoop.hbase.coprocessor.RegionCoprocessorEnvironment;
import org.apache.hadoop.hbase.regionserver.wal.WALEdit;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class HBaseCoprocessor extends BaseRegionObserver {

    private static Log LOG = LogFactory.getLog (HBaseCoprocessor.class);

    private HBaseDao hBaseDao = null;

    private String callerFamily = null;

    public HBaseCoprocessor() {
        hBaseDao = new HBaseDao ();
        callerFamily = PropertiesUtil.get ("hbase.properties", "caller.family");
        LOG.info (">>> HBaseCoprocessor has been inited...");
    }

    /**
     * msg: callerPhone,calleePhone,callTime,duration,flag,callerName,calleeName
     * eg: 16756356329,18256376789,2010-10-10 09:23:45,0200,曹红恋,冯怜云
     * -------------------------------------------------------------------------
     * put: partitionCode_beforePhone_callTime_afterPhone_duration_flag
     * 0?_16756356329_20101010092345_18256376789_0200_1
     */
    @Override
    public void postPut(ObserverContext<RegionCoprocessorEnvironment> e, Put put, WALEdit edit, Durability durability)
            throws IOException {
        super.postPut (e, put, edit, durability);

        String currentTableName = e.getEnvironment ().getRegion ().getRegionInfo ().getTable ().getNameAsString ();

        String targetTableName = PropertiesUtil.get ("hbase.properties", "tableName");

        String callerFlag = PropertiesUtil.get ("hbase.properties", "caller.flag");
        String calleeFlag = PropertiesUtil.get ("hbase.properties", "callee.flag");

        if (!StringUtils.equals (currentTableName, targetTableName)) {
            return;
        }

        String rowkey = Bytes.toString (put.getRow ());
        String[] fields = rowkey.split ("_");
        String flag = fields[5];

        if (!StringUtils.equals (flag, callerFlag)) {
            return;
        }

        String callerPhone = fields[1];
        String callTime = fields[2];
        String calleePhone = fields[3];
        String duration = fields[4];

        String callerName = Bytes.toString (CellUtil.cloneValue (put.get (Bytes.toBytes (callerFamily), Bytes.toBytes ("callerName")).get (0)));
        String calleeName = Bytes.toString (CellUtil.cloneValue (put.get (Bytes.toBytes (callerFamily), Bytes.toBytes ("calleeName")).get (0)));

        String newLog = new StringBuilder (callerPhone).append (",").append (calleePhone).append (",")
                .append (callTime).append (",").append (duration).append (",")
                .append (calleeFlag).append (",").append (callerName).append (",").append (calleeName).toString ();

//         方案1: 直接使用 HBaseDao 完成数据插入
        hBaseDao.put ("callee", newLog);
        LOG.info (">>> postPut by HBaseCoprocessor...");

//        方案2: 手动封装put,完成数据插入
//        String phoneNumber = calleePhone;
//        String beforePhone = calleePhone;
//        String afterPhone = callerPhone;
//
//        String regionCode = HBaseUtil.getRegionCode (phoneNumber, callTime);
//
//        String newRowKey = new StringBuilder (regionCode).append ("_").append (beforePhone).append ("_")
//                            .append (callTime).append ("_").append (afterPhone).append ("_")
//                            .append (duration).append ("_").append (flag).toString ();
//
//        Map<String, Object> cellMap = HBaseUtil.preparePut (calleeFamily, newLog);
//
//        Put newPut = HBaseUtil.getRowPut (newRowKey, calleeFamily, cellMap);
//
//        HTableInterface hTable = e.getEnvironment ().getTable (TableName.valueOf (targetTableName));
//        hTable.put (newPut);
//        hTable.close ();

    }


}
