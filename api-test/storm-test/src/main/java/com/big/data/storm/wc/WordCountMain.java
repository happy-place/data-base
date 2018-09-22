package com.big.data.storm.wc;


import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;

public class WordCountMain {

    public static void main(String[] args) {
        // 1、准备一个TopologyBuilder
        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("WordCountSpout", new WordCountSpout(), 1);
        builder.setBolt("WordCountSplitBolt", new WordCountSplitBolt(), 2).shuffleGrouping("WordCountSpout");
        builder.setBolt("WordCountBolt", new WordCountBolt(), 4).fieldsGrouping("WordCountSplitBolt", new Fields("word"));

        // 2、创建一个configuration，用来指定当前topology 需要的worker的数量
        Config conf = new Config();
        conf.setNumWorkers(2);

        // 3、提交任务 -----两种模式 本地模式和集群模式
        if (args.length > 0) {
            try {
                // 4 分布式提交
                StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            // 5 本地模式提交
            LocalCluster localCluster = new LocalCluster();
            localCluster.submitTopology("wordcounttopology", conf, builder.createTopology());
        }
    }
}
