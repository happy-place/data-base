package com.big.data.storm.pv;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import java.util.Map;

public class PVBolt1 implements IRichBolt {

    private static final long serialVersionUID = 1L;
    private OutputCollector collector;
    private long pv = 0;

    @SuppressWarnings("rawtypes")
    @Override
    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;
    }

    @Override
    public void execute(Tuple input) {
        // 获取传递过来的数据
        String logline = input.getString(0);

        // 截取出sessionid
        String session_id = logline.split("\t")[1];

        // 根据会话id不同统计pv次数
        if (session_id != null) {
            pv++;
        }

        // 提交
        collector.emit(new Values(Thread.currentThread().getId(), pv));

        System.err.println("threadid:" + Thread.currentThread().getId() + "  pv:" + pv);
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("thireadID", "pv"));

    }

    @Override
    public void cleanup() {

    }

    @Override
    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
