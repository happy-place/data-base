package com.big.data.call.collect;


import com.big.data.call.common.PropertiesUtil;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.util.Bytes;

import java.text.DecimalFormat;
import java.util.*;


public class HBaseUtil {

    private static Integer regionNum = -1;
    private static DecimalFormat regionCodeFormat = null;
    private static String callerFamily = null;
    private static String calleeFamily = null;
    private static String callerFlag = null;
    private static String calleeFlag = null;

    static{
        regionNum = Integer.parseInt (PropertiesUtil.get ("hbase.properties","regions"));
        regionCodeFormat = new DecimalFormat (PropertiesUtil.get ("hbase.properties","regionCode.format"));

        callerFamily = PropertiesUtil.get ("hbase.properties","caller.family");
        calleeFamily = PropertiesUtil.get ("hbase.properties","callee.family");

        callerFlag = PropertiesUtil.get ("hbase.properties","caller.flag");
        calleeFlag = PropertiesUtil.get ("hbase.properties","callee.flag");
    }

    /**
     *
     * @param family
     * @param callLog
     * @return : Map<String,Object> >> keySet {"rowkey","family","cellMap"}
     */
    public static Map<String,Object> preparePut(String family,String callLog){

        Map<String,Object> putMap = new HashMap<String,Object> ();

        String[] fields = callLog.split (",");

        String callerPhone = fields[0];
        String calleePhone = fields[1];
        String callTime = HBaseUtil.simpleDateStr(fields[2]);
        String duration = fields[3];
        String flag = family.equals (callerFamily)?callerFlag:calleeFlag;
        String callerName = fields[5];
        String calleeName = fields[6];

        String markedPhone = family.equals (callerFamily) ? callerPhone : calleePhone;

        String regionCode = HBaseUtil.getRegionCode (markedPhone, callTime);

        String beforePhone = family.equals (callerFamily)?callerPhone:calleePhone;
        String afterPhone = family.equals (callerFamily)?calleePhone:callerPhone;

        String rowkey = new StringBuilder (regionCode).append ("_").append (beforePhone).append ("_")
                .append (callTime).append ("_").append (afterPhone).append ("_")
                .append (duration).append ("_").append (flag).toString ();

        Map<String,Object> cellMap = new HashMap<String,Object> ();

        cellMap.put ("callerPhone",callerPhone);
        cellMap.put ("calleePhone",calleePhone);
        cellMap.put ("callTime",callTime);
        cellMap.put ("duration",duration);
        cellMap.put ("flag",flag);
        cellMap.put ("callerName",callerName);
        cellMap.put ("calleeName",calleeName);

        putMap.put ("rowkey",rowkey);
        putMap.put ("family",family);
        putMap.put ("cellMap",cellMap);

        return putMap;
    }

    /**
     * 通行多cell插入
     * @param rowkey
     * @param family
     * @param cellMap
     * @return
     */
    public static Put getRowPut(String rowkey,String family,Map<String,Object> cellMap){

        byte[] cf = Bytes.toBytes (family);
        byte[] row = Bytes.toBytes (rowkey);

        Put put = new Put(row);

        for(Map.Entry<String,Object> entry : cellMap.entrySet ()){
            byte[] qualifier = Bytes.toBytes (entry.getKey ().toString ());
            byte[] value = Bytes.toBytes (entry.getValue ().toString ());
            put.add (cf,qualifier,value);
        }

        return put;
    }

    /**
     * 基于手机号前4位,通行时间前6位 取或(特征并集),然后对分区数取余,格式化为"00" 格式,作为分区标识输出
     * @param phoneNum
     * @param timeStr
     * @return
     */
    public static String getRegionCode(String phoneNum,String timeStr){
        int left = Integer.parseInt (phoneNum.substring (0,4));
        int right = Integer.parseInt (timeStr.substring (0,6));
        String regionCode = regionCodeFormat.format ((left ^ right) % regionNum);
        return regionCode;
    }

    /**
     * 基于配置文件指定分区数,和默认规则创建分区键数组,在创建表时使用.
     * @param
     * @return partitionKeysArr:  hadmin.createTab(tabName,partitionKeysArr)
     */
    public static byte[][] genPartitionKeys(){
        List<String> tempList = new ArrayList<String> ();

        for(int i=0;i<regionNum;i++){
            tempList.add (regionCodeFormat.format (i)+"|");
        }

        TreeSet<byte[]> treeSet = new TreeSet(Bytes.BYTES_COMPARATOR);

        for(String keys:tempList){
            treeSet.add (Bytes.toBytes (keys));
        }

        byte[][] splitkeys = new byte[treeSet.size ()][];

        int i = 0;

        for(byte[] key : treeSet){
            splitkeys[i++] = key;
        }

        return splitkeys;
    }

    public static String simpleDateStr(String timeStr){
        return timeStr.replaceAll ("-","").replaceAll (":","");
    }

}
