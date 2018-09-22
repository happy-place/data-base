package com.big.data.es;

import java.net.InetAddress;
import java.sql.SQLFeatureNotSupportedException;

import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.TransportAddress;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.junit.Test;
import org.nlpcn.es4sql.SearchDao;
import org.nlpcn.es4sql.exception.SqlParseException;
import org.nlpcn.es4sql.query.SqlElasticSearchRequestBuilder;

public class ESExplain {

    @Test
    public void parse() {

        // 1 设置连接的集群名称
        Settings settings = Settings.builder().put("cluster.name", "my-application").build();

        // 2 连接集群  settings
        TransportClient client = new PreBuiltTransportClient(settings);

        // 5.6.1 版本 api
        // client.addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("loalhost"), 9300));

        try {
            // 3.单机版连接 Settings.EMPTY
            client = new PreBuiltTransportClient(Settings.EMPTY).addTransportAddress(new TransportAddress(InetAddress.getByName("127.0.0.1"), 9300));
            String sql = "select sum(join_num),sum(num) from (select distinct ts,join_num,num from ndex where ts >='2018-06-28' and ts <= '2018-07-11' and pid = '8' and exp='live_99') tmp group by dt";
            System.out.println(new SearchDao(client).explain(sql).explain().explain());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }



}
