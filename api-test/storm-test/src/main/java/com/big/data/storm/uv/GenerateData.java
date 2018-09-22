package com.big.data.storm.uv;


import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Random;

public class GenerateData {

    public static void main(String[] args) {
        // 创建文件
        File logFile = new File("./api-test/storm-test/logs/website-uv.log");
        // 判断文件是否存在
        if (!logFile.exists()) {
            try {
                logFile.createNewFile();
            } catch (IOException e) {

                e.printStackTrace();
            }
        }

        Random random = new Random();

        // 1 网站名称
        String[] hosts = {"www.atguigu.com"};
        // 2 会话id
        String[] session_id = {"ABYH6Y4V4SCVXTG6DPB4VH9U123", "XXYH6YCGFJYERTT834R52FDXV9U34",
                "BBYH61456FGHHJ7JL89RG5VV9UYU7", "CYYH6Y2345GHI899OFG4V9U567", "VVVYH6Y4V4SFXZ56JIPDPB4V678"};
        // 3 访问网站时间
        String[] time = {"2017-08-07 08:40:50", "2017-08-07 08:40:51", "2017-08-07 08:40:52", "2017-08-07 08:40:53",
                "2017-08-07 09:40:49", "2017-08-07 10:40:49", "2017-08-07 11:40:49", "2017-08-07 12:40:49"};
        // 3 访问网站时间
        String[] ip = {"192.168.1.101", "192.168.1.102", "192.168.1.103", "192.168.1.104", "192.168.1.105",
                "192.168.1.106", "192.168.1.107", "192.168.1.108"};

        StringBuffer sb = new StringBuffer();

        for (int i = 0; i < 30; i++) {
            sb.append(hosts[0] + "\t" + session_id[random.nextInt(5)] + "\t" + time[random.nextInt(8)] + "\t"
                    + ip[random.nextInt(8)] + "\n");
        }

        // 写数据
        try {
            FileOutputStream fs = new FileOutputStream(logFile);

            fs.write(sb.toString().getBytes());
            fs.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
