package com.big.data.call.mock;


import com.big.data.call.common.PropertiesUtil;

import java.io.*;
import java.text.DecimalFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

public class LogMocker {

    private static Map<String, String> contacts = new HashMap<String, String> ();
    private static List<String> phoneList = null;

    private static long startDate = -1L;
    private static long endDate = -1L;
    private static String calleeFlag = null;
    private static SimpleDateFormat callTimeFormat = null;
    private static DecimalFormat durationFormat = null;

    private static String logOutDir = null;

    private static FileOutputStream fos = null;
    private static OutputStreamWriter osw = null;
    private static BufferedWriter writer = null;

    private static File logFile = null;

    private static StringBuffer logInfo = new StringBuffer ();

    static {
        contacts.put ("15369468720", "李雁");
        contacts.put ("19920860202", "卫艺");
        contacts.put ("18411925860", "仰莉");
        contacts.put ("14473548449", "陶欣悦");
        contacts.put ("18749966182", "施梅梅");
        contacts.put ("19379884788", "金虹霖");
        contacts.put ("19335715448", "魏明艳");
        contacts.put ("18503558939", "华贞");
        contacts.put ("13407209608", "华啟倩");
        contacts.put ("15596505995", "仲采绿");
        contacts.put ("17519874292", "卫丹");
        contacts.put ("15178485516", "戚丽红");
        contacts.put ("19877232369", "何翠柔");
        contacts.put ("18706287692", "钱溶艳");
        contacts.put ("18944239644", "钱琳");
        contacts.put ("17325302007", "缪静欣");
        contacts.put ("18839074540", "焦秋菊");
        contacts.put ("19879419704", "吕访琴");
        contacts.put ("16480981069", "沈丹");
        contacts.put ("18674257265", "褚美丽");
        contacts.put ("18302820904", "孙怡");
        contacts.put ("15133295266", "许婵");
        contacts.put ("17868457605", "曹红恋");
        contacts.put ("15490732767", "吕柔");
        contacts.put ("15064972307", "冯怜云");

        phoneList = new ArrayList<String> (contacts.keySet ());
    }

    static {
        // 类加载路径 target/class

        Map<String, String> propMap = PropertiesUtil.multiGet ("log.properties", Arrays.asList (
                new String[]{"duration.decimal.format", "date.format", "start.date",
                        "end.date", "callee.flag", "log.outDir"}));

        durationFormat = new DecimalFormat (propMap.get ("duration.decimal.format"));

        callTimeFormat = new SimpleDateFormat (propMap.get ("date.format"));

        try {
            startDate = callTimeFormat.parse (propMap.get ("start.date")).getTime ();
            endDate = callTimeFormat.parse (propMap.get ("end.date")).getTime ();
        } catch (ParseException e) {
            e.printStackTrace ();
        }

        calleeFlag = propMap.get ("callee.flag");

        logOutDir = propMap.get ("log.outDir");

    }

    /**
     * 模拟从电信运营商路由器获取的通信日志
     * log: callerPhone,calleePhone,callTime,duration,flag,callerName,calleeName
     * eg: 16756356329,18256376789,2010-10-10 09:23:45,0200,曹红恋,冯怜云
     * --------------------------------------------------------------------------
     * callerPhone 主叫(16756356329)
     * calleePhone 被叫(18256376789)
     * callTimeStr 拨打时间(eg: 2010-10-10 09:23:45)
     * durationStr 通话时长(1~3600s)0000
     * flag: 1主叫,0被叫
     * callerName: 主叫人
     * calleeName: 被叫人
     */
    private static String prepareLog() {
        // 从已有联系人名单，随机取出联系人，构建主叫/被叫联系关系
        String callerPhone = phoneList.get (( int ) (Math.random () * phoneList.size ()));
        String calleePhone = null;

        while (true) {
            calleePhone = phoneList.get (( int ) (Math.random () * phoneList.size ()));
            if (!callerPhone.equals (calleePhone)) { // 主叫 被叫不一致就可以退出
                break;
            }
        }

        // 根据配置文件定制时间段，构建通话 开始 结束时间 callstart_time
        String callTimeStr = callTimeFormat.format (new Date (startDate + ( long ) (Math.random () * (endDate - startDate))));
        // 通话持续时间
        long duration = ( long ) (Math.random () * (60 * 60));

        String durationStr = durationFormat.format (duration == 0 ? 1 : duration);

        // 联系人
        String callerName = contacts.get (callerPhone);
        String calleeName = contacts.get (calleePhone);

        // 清空缓冲
        logInfo.delete (0,logInfo.length ());

        // 主叫电话,被叫电话,开始时间,持续时间,主被标识,主叫名称,被叫名称
        logInfo.append (callerPhone).append (",").append (calleePhone).append (",")
                .append (callTimeStr).append (",").append (durationStr).append (",")
                .append (calleeFlag).append (",").append (callerName).append (",").append (calleeName).append ("\r\n");

        return logInfo.toString ();
    }

    private static void printLog(String logInfo) throws IOException {
        // 刷写
     writer.write (logInfo);
        writer.flush ();
    }

    private static void prepareOutput(String[] args) throws IOException {
        logFile = new File ((args==null||args.length==0)?logOutDir:args[0]);

        if(logFile.exists ()){
            logFile.delete ();
        }
        // 输出流初始化阶段打开,异常退出时关闭,中间异常关闭,tail: call_log.csv: file truncated
        fos = new FileOutputStream (logFile);
        osw = new OutputStreamWriter (fos);
        writer = new BufferedWriter (osw);

    }

    private static void release(Closeable os) {
        if (os != null) {
            try {
                os.close ();
            } catch (IOException e) {
                e.printStackTrace ();
            }
        }
    }

    public static void main(String[] args) {
        try {
            // 基于配置，定义模拟数据输出目录，并初始化相应输出流
            prepareOutput (args);
            System.out.println("tail -f "+ logFile.getAbsolutePath());
            while (true) {
                // 每隔1s输出一条日志
                printLog (prepareLog ());
                Thread.sleep (1000);
            }
        } catch (Exception e) {
            e.printStackTrace ();
            release (fos);
            release (osw);
            release (writer);
        }
    }

}
