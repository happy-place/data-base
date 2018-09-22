package com.big.data.storm.pv;


import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichSpout;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Map;

public class PVSpout implements IRichSpout {

    private static final long serialVersionUID = 1L;
    private SpoutOutputCollector collector;
    private BufferedReader reader;

    @SuppressWarnings("rawtypes")
    @Override
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        this.collector = collector;

        try {
            reader = new BufferedReader(new InputStreamReader(new FileInputStream("./api-test/storm-test/logs/website.log"), "UTF-8"));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void close() {

        try {
            if (reader != null) {
                reader.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void activate() {

    }

    @Override
    public void deactivate() {

    }

    private String str;

    @Override
    public void nextTuple() {

        try {
            while ((str = reader.readLine()) != null) {

                collector.emit(new Values(str));

                Thread.sleep(500);
            }
        } catch (Exception e) {

        }
    }

    @Override
    public void ack(Object msgId) {
    }


    @Override
    public void fail(Object msgId) {

    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("log"));
    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
