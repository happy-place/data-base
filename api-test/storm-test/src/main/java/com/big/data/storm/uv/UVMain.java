package com.big.data.storm.uv;


import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;

public class UVMain {

    public static void main(String[] args) {

        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("UVSpout", new UVSpout(), 1);
        builder.setBolt("UVBolt1", new UVBolt1(), 4).shuffleGrouping("UVSpout");
        builder.setBolt("UVSumBolt", new UVSumBolt(), 1).shuffleGrouping("UVBolt1");
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

            cluster.submitTopology("uvtopology", conf, builder.createTopology());
        }
    }
}
