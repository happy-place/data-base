package com.big.data.es;

import org.elasticsearch.action.admin.indices.mapping.put.PutMappingRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Requests;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;

import org.elasticsearch.common.transport.TransportAddress;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.XContentFactory;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.SearchHits;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.junit.Before;
import org.junit.Test;

import java.net.InetAddress;
import java.util.HashMap;
import java.util.Map;

public class ElasticSearchIKTest {

    private TransportClient client;

    @SuppressWarnings("unchecked")
    @Before
    public void getClient() throws Exception {

        // 1 连接集群时，设置连接集群的名称
        Settings settings = Settings.builder().put("cluster.name", "my-application").build();

        // 2 连接集群
        client = new PreBuiltTransportClient(settings);
        // 5.6.1 API
//        client.addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("loalhost"), 9300));

        // 2.单机版 或 指定连接机器的固定节点
        client = new PreBuiltTransportClient(Settings.EMPTY).addTransportAddress(new TransportAddress(InetAddress.getByName("localhost"), 9300));

        // 3 打印集群名称
        System.out.println(client.toString());
    }

    //创建索引(数据库)
    @Test
    public void createIndex() {
        //创建索引
        client.admin().indices().prepareCreate("blog4").get();
        //关闭资源
        client.close();
    }

    //创建使用ik分词器的mapping
    @Test
    public void createMapping() throws Exception {
        // 0.先删
        client.admin().indices().prepareDelete("blog4").get();

        // 1.创建index
        client.admin().indices().prepareCreate("blog4").get();

        // 2.设置mapping
        XContentBuilder builder = XContentFactory.jsonBuilder()
                .startObject()
                .startObject("article")
                .startObject("properties")
                .startObject("id")
                .field("type", "integer")
                .endObject()
                .startObject("title")
                .field("type", "keyword")  // 不会创建分词索引
                .endObject()
                .startObject("keywords")
                .field("type", "text")  // 会创建分词索引
                .field("analyzer","ik_smart")
                .endObject()
                .startObject("content")
                .field("type", "text")
                .field("analyzer","ik_smart")
                .endObject()
                .endObject()
                .endObject()
                .endObject();

        PutMappingRequest mapping = Requests.putMappingRequest("blog4").type("article").source(builder);
        client.admin().indices().putMapping(mapping).get();

        // 3.插入数据
        Map<String, Object> map1 = new HashMap<String, Object>();
        map1.put("id", "1");
        map1.put("title", "基于webservice发布接口");
        map1.put("keywords", "wsdl,soap,webservice");
        map1.put("content", "它提供灵活RESTful web接口");

        Map<String, Object> map2 = new HashMap<String, Object>();
        map2.put("id", "2");
        map2.put("title", "基于hbase发布接口");
        map2.put("keywords", "hmaster,hregionserver,region");
        map2.put("content", "它提供灵活稀疏存储");

        IndexResponse indexResponse1 = client.prepareIndex("blog4", "article", "1").setSource(map1).execute().actionGet();
        IndexResponse indexResponse2 = client.prepareIndex("blog4", "article", "2").setSource(map2).execute().actionGet();

        // 3 打印返回的结果
        System.out.println("index:" + indexResponse1.getIndex());
        System.out.println("type:" + indexResponse1.getType());
        System.out.println("id:" + indexResponse1.getId());
        System.out.println("version:" + indexResponse1.getVersion());
        System.out.println("result:" + indexResponse1.getResult());

        // 3 关闭资源
        client.close();
    }

    //创建文档,以map形式
    @Test
    public void createDocumentByMap() {

        HashMap<String, String> map = new HashMap<>();
        map.put("id1", "2");
        map.put("title2", "Lucene");
        map.put("content", "它提供了一个分布式的web接口");

        IndexResponse response = client.prepareIndex("blog4", "article", "3").setSource(map).execute().actionGet();

        //打印返回的结果
        System.out.println("结果:" + response.getResult());
        System.out.println("id:" + response.getId());
        System.out.println("index:" + response.getIndex());
        System.out.println("type:" + response.getType());
        System.out.println("版本:" + response.getVersion());

        //关闭资源
        client.close();
    }

    //词条查询
    @Test
    public void queryTerm() {

        SearchResponse response = client.prepareSearch("blog4").setTypes("article").setQuery(QueryBuilders.termQuery("content","提供")).get();

        //获取查询命中结果
        SearchHits hits = response.getHits();

        System.out.println("结果条数:" + hits.getTotalHits());

        for (SearchHit hit : hits) {
            System.out.println(hit.getSourceAsString());
        }
    }





}
