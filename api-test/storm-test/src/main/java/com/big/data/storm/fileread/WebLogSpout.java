package com.big.data.storm.fileread;


import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichSpout;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.Map;

public class WebLogSpout implements IRichSpout {

    private static final long serialVersionUID = 1L;

    private BufferedReader br;
    private SpoutOutputCollector collector = null;
    private String str = null;

    @Override
    public void nextTuple() {
        // 循环调用的方法
        try {
            while ((str = this.br.readLine()) != null) {
                // 发射出去
                collector.emit(new Values(str));

//				Thread.sleep(3000);
            }
        } catch (Exception e) {

        }
    }

    @SuppressWarnings("rawtypes")
    @Override
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        // 打开输入的文件
        try {
            this.collector = collector;
            this.br = new BufferedReader(new InputStreamReader(new FileInputStream("./api-test/storm-test/logs/website.log"), "UTF-8"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        // 声明输出字段类型
        declarer.declare(new Fields("log"));
    }

    @Override
    public void ack(Object arg0) {

    }

    @Override
    public void activate() {

    }

    @Override
    public void close() {

    }

    @Override
    public void deactivate() {

    }

    @Override
    public void fail(Object arg0) {

    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
