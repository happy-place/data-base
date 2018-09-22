package com.big.data.call.mapreduce.util;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * 读取 resources 目录下的.properties配置信息工具类
 */
public class PropertiesUtil {

    private static Properties prop = new Properties();
    private static InputStream is = null;


    /**
     * 获取装配kv属性的properties对象
     * @param propFile: properties文件存储位置
     * @param propKeys: 需要获取kv列表,为null时表明获取全部信息
     * @return
     */
    public static Properties getProperties(String propFile, List<String> propKeys){

        try {
            loadProp(propFile);
            if(propKeys==null){
                return prop;
            }else{
                for(String propKey:propKeys){
                    prop.setProperty (propKey,prop.getProperty (propKey));
                }
                release ();
            }
        } catch (Exception e) {
            e.printStackTrace ();
            release ();
        }
        return prop;
    }

    /**
     * 批量获取配置信息
     * @param propFile
     * @param propKeys
     * @return
     */
    public static Map<String, String> multiGet(String propFile,List<String> propKeys) {
        Map<String, String> outMap = null;
        try {
            loadProp(propFile);

            outMap = new HashMap<> ();

            for(String propKey:propKeys){
                outMap.put (propKey,prop.getProperty (propKey));
            }
        } catch (Exception e) {
            e.printStackTrace ();
        } finally {
            release ();
        }

        return outMap;
    }

    /**
     * 临时获取配置信息
     * @param propFile
     * @param propKey
     * @return
     */
    public static String get(String propFile, String propKey){
        try {
            loadProp(propFile);
        } catch (Exception e) {
            e.printStackTrace ();
        } finally {
            release ();
        }
        return prop.getProperty (propKey);
    }

    /**
     * 加载配置文件
     * @param propFile
     * @throws Exception
     */
    private static void loadProp(String propFile) throws Exception{
        prop.clear ();
        is = ClassLoader.getSystemResourceAsStream (propFile);
        prop.load (is);
    }

    /**
     * 程序正常退出,或虚拟机崩溃前都可以释放资源
     */
    private static void release(){
        if(is!=null){
            try {
                is.close ();
            } catch (IOException e) {
                e.printStackTrace ();
            }
        }
    }

}
