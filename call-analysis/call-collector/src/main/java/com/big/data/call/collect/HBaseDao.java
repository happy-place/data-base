package com.big.data.call.collect;

import com.big.data.call.common.PropertiesUtil;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.text.DecimalFormat;
import java.util.Date;
import java.util.Map;

public class HBaseDao {

    private static Log LOG = LogFactory.getLog (HBaseDao.class);

    private Configuration conf = null;

    private HBaseAdmin hadmin = null;
    private HTable hTable = null;

    private String nameSpace = null;
    private String htabName = null;

    private String[] colFamilies = null;

    private static boolean inited = false;

    public HBaseDao() {
        this.conf = HBaseConfiguration.create ();

        this.nameSpace = PropertiesUtil.get ("hbase.properties","nameSpace");
        this.htabName = PropertiesUtil.get ("hbase.properties","tableName");
        this.colFamilies = PropertiesUtil.get ("hbase.properties","families").split (",");

        try {
            hadmin = new HBaseAdmin(conf);
            hTable = new HTable (conf,Bytes.toBytes (htabName));
        } catch (IOException e) {
            e.printStackTrace ();
        }

    }

    public void initCheck() {
        try {
            if(!inited) {
                createNameSpace ();
                createTable ();
                inited = true;
            }
        } catch (IOException e) {
            e.printStackTrace ();
        }
    }

    private void createNameSpace() throws IOException {
        NamespaceDescriptor[] nsArr = hadmin.listNamespaceDescriptors ();

        if(nsArr!=null){
            for(NamespaceDescriptor nsd: nsArr){
                if(nameSpace.equals (nsd.getName ())){
                    LOG.info (">>> "+nameSpace+"\t"+nsd.getName ()+" is already existed ...");
                    return;
                }
            }
        }

        NamespaceDescriptor nsDesc = NamespaceDescriptor.create (nameSpace)
                                        .addConfiguration ("creator","Huhao")
                                        .addConfiguration ("createTime", new Date (System.currentTimeMillis ()).toString ())
                                        .build ();

        hadmin.createNamespace (nsDesc);

        LOG.info (">>> "+nameSpace+" has already created ...");
    }

    private void createTable() throws IOException {
        if(hadmin.tableExists (htabName)){
            LOG.info (">>> HTable: "+htabName+" is already existed ...");
            return;
        }

        HTableDescriptor hTableDescriptor = new HTableDescriptor(TableName.valueOf (htabName));
        // 添加需要协处理器帮助建表代码
        hTableDescriptor.addCoprocessor ("com.big.data.call.collect.HBaseCoprocessor");

        for(String cf:colFamilies){
            hTableDescriptor.addFamily (new HColumnDescriptor (Bytes.toBytes (cf.trim ())));
        }

        new DecimalFormat (PropertiesUtil.get ("hbase.properties","regionCode.format"));

        hadmin.createTable (hTableDescriptor, HBaseUtil.genPartitionKeys ());

        LOG.info (">>> HTable: "+htabName+" has already created ...");
    }

    /**
     * msg: callerPhone,calleePhone,callTime,duration,flag,callerName,calleeName
     * eg: 16756356329,18256376789,2010-10-10 09:23:45,0200,曹红恋,冯怜云
     * -------------------------------------------------------------------------
     * put: partitionCode_beforePhone_callTime_afterPhone_duration_flag
     *      0?_16756356329_20101010092345_18256376789_0200_1
     */
    public void put(String family,String callLog) throws IOException {

        initCheck();

        Map<String, Object> putMap = HBaseUtil.preparePut (family, callLog);

        String rowkey = putMap.get ("rowkey").toString ();

        Map<String,Object> cellMap = (Map<String,Object>) putMap.get ("cellMap");

        Put put = HBaseUtil.getRowPut (rowkey, family, cellMap);

        hTable.put (put);

        LOG.info (">>> "+callLog+" has already put ...");
    }

}
