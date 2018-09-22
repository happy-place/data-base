package com.big.data.app.client;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by atguigu on 2017/11/10
 */
public class UploadUtil {

    /**
     * 上传日志
     */
    public static void upload(String json) throws Exception {

        try{
            // 1 设置请求的URL
            URL url = new URL("http://localhost:8080/app_logs/coll/index");// 生产地址
//            URL url = new URL("http://localhost:8080/coll/index");// 测试地址


            // 2 获取连接
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            // 2.1 设置请求方式为post
            conn.setRequestMethod("POST");

            // 2.2 允许上传数据
            conn.setDoOutput(true);

            // 2.3 时间头用来供server进行时钟校对的
            conn.setRequestProperty("clientTime",System.currentTimeMillis() + "");

            // 2.4 设置请求的头信息,设置内容类型
            conn.setRequestProperty("Content-Type", "application/json");

            // 3 获取输出流
            OutputStream out = conn.getOutputStream();
            // 3.1 向输出流里面写数据
            out.write(json.getBytes());
            out.flush();
            // 3.2 关闭资源
            out.close();

            // 4 获取响应码
            int code = conn.getResponseCode();
            System.out.println(code);
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }

}
