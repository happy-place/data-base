package com.big.data.storm.wc;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import java.util.Map;

/**
 * 接收 WordCountSpout 发送的数据，切分，然后抛给WordCountBolt: Mapper
 */
public class WordCountSplitBolt extends BaseRichBolt {

    private static final long serialVersionUID = 1L;
    private OutputCollector collector;

    @Override
    public void execute(Tuple input) {
        // 1 获取传递过来的一行数据
        String line = input.getString(0);
        // 2 截取
        String[] arrWords = line.split(" ");

        // 3 发射
        for (String word : arrWords) {
            collector.emit(new Values(word, 1));
        }
    }

    @SuppressWarnings("rawtypes")
    @Override
    public void prepare(Map arg0, TopologyContext arg1, OutputCollector collector) {
        this.collector = collector;
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("word", "num"));
    }
}


