package com.big.data.app.web;

import com.alibaba.fastjson.JSONObject;

import com.big.data.app.common.*;
import com.big.data.app.common.GeoInfo;
import com.big.data.app.utils.GeoUtil;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

/**
 * Created by atguigu on 2017/11/10
 */
@Controller
@RequestMapping("/coll")
public class CollectLogController {

    // 缓存地址信息
    private Map<String, GeoInfo> cache = new HashMap<String, GeoInfo>();


    @RequestMapping(value = "/index", method = RequestMethod.POST)
    @ResponseBody
    public AppLogEntity collect(@RequestBody AppLogEntity e, HttpServletRequest req) {

        // 1 修正服务器和客户端时间
        verifyTime(e, req);

        // 2 获取国家、省份和ip地址信息
        processIp(e, req);

        // 3 向Kafka发送消息
        sendMessage(e);

        return e;
    }

    // 修正时间
    private void verifyTime(AppLogEntity e, HttpServletRequest req) {

        // 1 获取服务器时间
        long myTime = System.currentTimeMillis();
        // 2 获取客户端时间
        long clientTime = Long.parseLong(req.getHeader("clientTime"));
        // 3 计算服务器和客户端时间差
        long diff = myTime - clientTime;

        // 4 根据时间差，修正日志中时间
        for (AppStartupLog log : e.getAppStartupLogs()) {
            log.setCreatedAtMs(log.getCreatedAtMs() + diff);
        }

        for (AppUsageLog log : e.getAppUsageLogs()) {
            log.setCreatedAtMs(log.getCreatedAtMs() + diff);
        }

        for (AppPageLog log : e.getAppPageLogs()) {
            log.setCreatedAtMs(log.getCreatedAtMs() + diff);
        }

        for (AppEventLog log : e.getAppEventLogs()) {
            log.setCreatedAtMs(log.getCreatedAtMs() + diff);
        }

        for (AppErrorLog log : e.getAppErrorLogs()) {
            log.setCreatedAtMs(log.getCreatedAtMs() + diff);
        }
    }

    /**
     * 处理ip client地址问题
     * @param e
     */
    private void processIp(AppLogEntity e, HttpServletRequest req) {

        // 1 获取客户端ip地址
        String clientIP = req.getRemoteAddr();

        // 2 从缓存中获取数据
        GeoInfo geoInfo = cache.get(clientIP);

        // 如果该客户端ip地址没有获取过国家和省份信息，则通过工具类获取；
        // 如果该客户端ip地址已经获取过国家和省份信息，则直接从缓存对象中获取
        if (geoInfo == null) {
            geoInfo = new GeoInfo();
            geoInfo.setCountry(GeoUtil.getCountry(clientIP));
            geoInfo.setProvince(GeoUtil.getProvince(clientIP));

            // 缓存数据
            cache.put(clientIP, geoInfo);
        }

        // 3 设置国家、省份和客户端ip地址信息
        for (AppStartupLog log : e.getAppStartupLogs()) {
            log.setCountry(geoInfo.getCountry());
            log.setProvince(geoInfo.getProvince());
            log.setIpAddress(clientIP);
        }
    }

    // 发送消息给发Kafka
    private void sendMessage(AppLogEntity e) {

        // 1 创建配置对象
        Properties props = new Properties();
        // 1.1 Kafka服务端的主机名和端口号
        props.put("bootstrap.servers", "localhost:9092");
        // 1.2 等待所有副本节点的应答
        props.put("acks", "all");
        // 1.3 消息发送最大尝试次数
        props.put("retries", 0);
        // 1.4 一批消息处理大小
        props.put("batch.size", 16384);
        // 1.5 请求延时
        props.put("linger.ms", 1);
        // 1.6 发送缓存区内存大小
        props.put("buffer.memory", 33554432);
        // 1.7 key序列化
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        // 1.8 value序列化
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        // 2 创建生产者
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);

        // 3 根据日志类型分别向5个主题发送消息
        sendSingleLog(producer, Constants.TOPIC_APP_STARTUP, e.getAppStartupLogs());
        sendSingleLog(producer, Constants.TOPIC_APP_ERRROR, e.getAppErrorLogs());
        sendSingleLog(producer, Constants.TOPIC_APP_EVENT, e.getAppEventLogs());
        sendSingleLog(producer, Constants.TOPIC_APP_PAGE, e.getAppPageLogs());
        sendSingleLog(producer, Constants.TOPIC_APP_USAGE, e.getAppUsageLogs());

        // 4 关闭生产者
        producer.close();
    }

    /**
     * 发送单个的log消息给kafka
     */
    private void sendSingleLog(KafkaProducer<String, String> producer, String topic, AppBaseLog[] logs) {

        for (AppBaseLog log : logs) {

            // 1 将bean对象转换为json
            String logMsg = JSONObject.toJSONString(log);

            // 2 创建待发送消息对象
            ProducerRecord<String, String> data = new ProducerRecord<String, String>(topic, logMsg);

            // 3 发送消息
            producer.send(data);
        }
    }

}

