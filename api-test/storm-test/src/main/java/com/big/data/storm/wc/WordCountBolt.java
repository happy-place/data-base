package com.big.data.storm.wc;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

import java.util.HashMap;
import java.util.Map;

/**
 *  统计汇总 ;Reducer
 */
public class WordCountBolt extends BaseRichBolt {

    private static final long serialVersionUID = 1L;
    private Map<String, Integer> map = new HashMap<String, Integer>();

    @Override
    public void execute(Tuple input) {

        // 1 获取传递过来的数据
        String word = input.getString(0);
        Integer num = input.getInteger(1);

        // 2 累加单词
        if (map.containsKey(word)) {
            Integer count = map.get(word);
            map.put(word, count + num);
        } else {
            map.put(word, num);
        }

        System.err.println(Thread.currentThread().getId() + "  word:" + word + "  num:" + map.get(word));
    }

    @SuppressWarnings("rawtypes")
    @Override
    public void prepare(Map arg0, TopologyContext arg1, OutputCollector collector) {

    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer arg0) {
        // 不输出
    }
}
