package com.big.data.storm.fileread;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;

public class WebLogMain {

    public static void main(String[] args) {
        // 1 创建拓扑对象
        TopologyBuilder builder = new TopologyBuilder();

        // 2 设置Spout和bolt
        builder.setSpout("weblogspout", new WebLogSpout(), 1);
        builder.setBolt("weblogbolt", new WebLogBolt(), 1).shuffleGrouping("weblogspout");

        // 3 配置Worker开启个数
        Config conf = new Config();
        conf.setNumWorkers(4);

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
            localCluster.submitTopology("weblogtopology", conf, builder.createTopology());
        }
    }
}
