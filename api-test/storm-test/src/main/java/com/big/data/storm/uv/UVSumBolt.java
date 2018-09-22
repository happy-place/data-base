package com.big.data.storm.uv;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

import java.util.HashMap;
import java.util.Map;

public class UVSumBolt extends BaseRichBolt {
    private static final long serialVersionUID = 1L;
    private Map<String, Integer> map = new HashMap<String, Integer>();

    @SuppressWarnings("rawtypes")
    @Override
    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {

    }

    @Override
    public void execute(Tuple input) {
        // 1 获取传递过来的数据
        String ip = input.getString(0);
        Integer num = input.getInteger(1);

        // 2 累加单词，对 ip 进行归类存储，相当于 计算 UV
        if (map.containsKey(ip)) {
            Integer count = map.get(ip);
            map.put(ip, count + num);
        } else {
            map.put(ip, num);
        }

        System.err.println(Thread.currentThread().getId() + "  ip:" + ip + "  num:" + map.get(ip));
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {

    }
}
