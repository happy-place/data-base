package com.big.data.storm.pv;


import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;

public class PVMain {

    public static void main(String[] args) {
        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("PVSpout", new PVSpout(), 1);
        builder.setBolt("PVBolt1", new PVBolt1(), 4).shuffleGrouping("PVSpout");
        builder.setBolt("PVSumBolt", new PVSumBolt(), 1).shuffleGrouping("PVBolt1");

        Config conf = new Config();

        conf.setNumWorkers(2);

        if (args.length > 0) {
            try {
                StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("pvtopology", conf, builder.createTopology());
        }
    }
}
