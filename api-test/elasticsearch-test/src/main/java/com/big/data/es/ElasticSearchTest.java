package com.big.data.es;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.elasticsearch.action.admin.indices.create.CreateIndexResponse;
import org.elasticsearch.action.admin.indices.mapping.put.PutMappingRequest;
import org.elasticsearch.action.admin.indices.mapping.put.PutMappingResponse;
import org.elasticsearch.action.bulk.BulkItemResponse;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.bulk.BulkRequestBuilder;
import org.elasticsearch.action.bulk.BulkResponse;
import org.elasticsearch.action.delete.DeleteResponse;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.action.get.MultiGetItemResponse;
import org.elasticsearch.action.get.MultiGetResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.update.UpdateRequest;
import org.elasticsearch.action.update.UpdateResponse;
import org.elasticsearch.client.Requests;
import org.elasticsearch.client.Response;
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

import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import static org.elasticsearch.common.xcontent.XContentFactory.*;

public class ElasticSearchTest {


    private TransportClient client;

    @SuppressWarnings("unchecked")
    @Before
    public void getClient() throws Exception {

        // 1 设置连接的集群名称
        Settings settings = Settings.builder().put("cluster.name", "my-application").build();

        // 2 连接集群  settings
        client = new PreBuiltTransportClient(settings);

        // 5.6.1 版本 api
//        client.addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("loalhost"), 9300));

        // 3.单机版连接 Settings.EMPTY
        client = new PreBuiltTransportClient(Settings.EMPTY).addTransportAddress(new TransportAddress(InetAddress.getByName("127.0.0.1"), 9300));

        // 3 打印集群名称
        System.out.println(client.toString());
    }

    @Test
    public void createIndex_blog(){
        // 1 创建索引
        client.admin().indices().prepareCreate("blog").get();
        // 2 关闭连接
        client.close();
    }

    @Test
    public void deleteIndex(){
        // 1 删除索引
        client.admin().indices().prepareDelete("blog4").get();
        // 2 关闭连接
        client.close();
    }

    @Test
    public void createIndexByKV() throws UnknownHostException {
        // 1.直接基于kv对 插入数据

        // prepareIndex 中的 id 是 document 文档id 数据元数据范畴，setSource中的 id 为业务字段 id
        IndexResponse indexResponse1 = client.prepareIndex("blog", "article","1")
                .setSource("id", "1","name","Tony", "adresse", "USA").execute().actionGet();

        // id 在后
        IndexResponse indexResponse2 = client.prepareIndex("blog", "article", "2")
                .setSource("id", "2","name","Jack","adresse", "USA").execute().actionGet();

        // 3 打印返回的结果
        System.out.println("index:" + indexResponse1.getIndex());
        System.out.println("type:" + indexResponse1.getType());
        System.out.println("id:" + indexResponse1.getId());
        System.out.println("version:" + indexResponse1.getVersion());
        System.out.println("result:" + indexResponse1.getResult());

        // 4 关闭连接
        client.close();
    }

    @Test
    public void createIndexByJson() throws UnknownHostException {
        // 1 文档数据准备
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("id","1");
        jsonObject.put("title","基于Lucene的搜索服务器");
        jsonObject.put("content","它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口");

        // 2 创建文档
        IndexResponse indexResponse = client.prepareIndex("info", "article", "1")
                .setSource(jsonObject).execute().actionGet();

        // 3 打印返回的结果
        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("result:" + indexResponse.getResult());

        // 4 关闭连接
        client.close();
    }


    @Test
    public void createIndexByMap() {
        // 1 文档数据准备
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("id", "2");
        map.put("title", "基于webservice发布接口");
        map.put("content", "它提供灵活RESTful web接口");

        // 2 创建文档
        IndexResponse indexResponse = client.prepareIndex("info", "article", "2").setSource(map).execute().actionGet();

        // 3 打印返回的结果
        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("result:" + indexResponse.getResult());

        // 4 关闭连接
        client.close();
    }

    @Test
    public void createIndex() throws Exception {
        // 1 通过es自带的帮助类，构建json数据
        XContentBuilder builder = XContentFactory.jsonBuilder().startObject()
                .field("id", 3)
                .field("title", "依托HBase分布式存储")
                .field("content", "解决海量数据存储瓶颈问题。")
                .endObject();

        // 2 创建文档
        IndexResponse indexResponse = client.prepareIndex("info", "article", "3").setSource(builder).get();

        // 3 打印返回的结果
        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("result:" + indexResponse.getResult());

        // 4 关闭连接
        client.close();
    }




    @Test
    public void searchById() throws Exception {

        // 1 查询文档
        GetResponse response = client.prepareGet("info", "article", "1").get();

        System.out.println("index->"+response.getIndex());
        System.out.println("type->"+response.getType());
        System.out.println("version->"+response.getVersion());
        System.out.println("id->"+response.getId());
        System.out.println("isExists->"+response.isExists());
        System.out.println("isSourceEmpty->"+response.isSourceEmpty());
        System.out.println("source->"+response.getSource());


        // 2 打印搜索的结果
        System.out.println(response.getSourceAsString());

        Map<String,Object> map = response.getSourceAsMap();

        System.out.println("id ->"+map.get("id"));
        System.out.println("title ->"+map.get("title"));
        System.out.println("content ->"+map.get("content"));

        // 3 关闭连接
        client.close();
    }

    @Test
    public void multiGetById() {
        // 1 查询多个 index
        MultiGetResponse response = client.prepareMultiGet()
                .add("info", "article", "1")
                .add("info", "article", "2", "3")
                .add("blog", "article", "1").get();

        // 2 遍历返回的结果
        for(MultiGetItemResponse itemResponse:response){
            GetResponse getResponse = itemResponse.getResponse();

            // 如果获取到查询结果
            if (getResponse.isExists()) {
                String sourceAsString = getResponse.getSourceAsString();
                System.out.println(sourceAsString);
            }
        }

        // 3 关闭资源
        client.close();
    }

    @Test
    public void onlyUpdateExistedDoc() throws Throwable {

        // DOC[info:articla:5] 存在就执行更新，对已经存在的字段，直接进行更新，未存在字段执行插入
        // 1 创建更新数据的请求对象
        UpdateRequest updateRequest = new UpdateRequest();
        updateRequest.index("info");
        updateRequest.type("article");
        updateRequest.id("5");

        updateRequest.doc(XContentFactory.jsonBuilder().startObject()
                // 对没有的字段添加, 对已有的字段替换
                .field("title", "全部基于Lucene的搜索服务器")
                .field("content", "它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。大数据前景无限")
                .field("createDate", "2017-8-22").endObject());

        // 2 获取更新后的值
        UpdateResponse indexResponse = client.update(updateRequest).get();

        // 3 打印返回的结果
        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("create:" + indexResponse.getResult());

        // 4 关闭连接
        client.close();
    }

    @Test
    public void doUpsert() throws Exception {

        // 创建 插入对象
        IndexRequest indexRequest = new IndexRequest("blog", "article", "5")
                .source(XContentFactory.jsonBuilder().startObject().field("title", "搜索服务器")
                        .field("content","它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。Elasticsearch是用Java开发的，并作为Apache许可条款下的开放源码发布，是当前流行的企业级搜索引擎。设计用于云计算中，能够达到实时搜索，稳定，可靠，快速，安装使用方便。")
                        .endObject());

        // 执行插入
        IndexResponse indexResponse = client.index(indexRequest).get();
        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("found:" + indexResponse.getResult());

        client.close();
    }

    @Test
    public void deleteById() {

        // 1 删除文档数据
        DeleteResponse indexResponse = client.prepareDelete("blog", "article", "5").get();

        // 2 打印返回的结果
        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("found:" + indexResponse.getResult());

        // 3 关闭连接
        client.close();
    }

    @Test
    public void matchAllQuery() {

        // 1 执行查询
        SearchResponse searchResponse = client.prepareSearch("blog").setTypes("article")
                .setQuery(QueryBuilders.matchAllQuery()).get();

        // 2 打印查询结果
        SearchHits hits = searchResponse.getHits(); // 获取命中次数，查询结果有多少对象
        System.out.println("查询结果有：" + hits.getTotalHits() + "条");

        Iterator<SearchHit> iterator = hits.iterator();

        while (iterator.hasNext()) {
            SearchHit searchHit = iterator.next(); // 每个查询对象

            System.out.println(searchHit.getSourceAsString()); // 获取字符串格式打印
        }

        // 3 关闭连接
        client.close();
    }

    @Test
    public void queryByStringSplits() {
        // 1 条件查询 查询包含指定字段的 文档
        SearchResponse searchResponse = client.prepareSearch("info").setTypes("article")
                .setQuery(QueryBuilders.queryStringQuery("基于")).get();

        // 2 打印查询结果
        SearchHits hits = searchResponse.getHits(); // 获取命中次数，查询结果有多少对象
        System.out.println("查询结果有：" + hits.getTotalHits() + "条");

        Iterator<SearchHit> iterator = hits.iterator();

        while (iterator.hasNext()) {
            SearchHit searchHit = iterator.next(); // 每个查询对象

            System.out.println(searchHit.getSourceAsString()); // 获取字符串格式打印
        }

        // 3 关闭连接
        client.close();
    }

    @Test
    public void wildcardQuery() {

        // 1 通配符查询
        SearchResponse searchResponse = client.prepareSearch("info").setTypes("article")
                .setQuery(QueryBuilders.wildcardQuery("content", "*口*")).get();

        // 2 打印查询结果
        SearchHits hits = searchResponse.getHits(); // 获取命中次数，查询结果有多少对象
        System.out.println("查询结果有：" + hits.getTotalHits() + "条");

        Iterator<SearchHit> iterator = hits.iterator();

        while (iterator.hasNext()) {
            SearchHit searchHit = iterator.next(); // 每个查询对象
            System.out.println(searchHit.getSourceAsString()); // 获取字符串格式打印
        }

        // 3 关闭连接
        client.close();
    }

    @Test
    public void termQuery() {

        // 1 第一field查询
        SearchResponse searchResponse = client.prepareSearch("info").setTypes("article")
                .setQuery(QueryBuilders.termQuery("content", "口")).get();

        // 2 打印查询结果
        SearchHits hits = searchResponse.getHits(); // 获取命中次数，查询结果有多少对象
        System.out.println("查询结果有：" + hits.getTotalHits() + "条");

        Iterator<SearchHit> iterator = hits.iterator();

        while (iterator.hasNext()) {
            SearchHit searchHit = iterator.next(); // 每个查询对象

            System.out.println(searchHit.getSourceAsString()); // 获取字符串格式打印
        }

        // 3 关闭连接
        client.close();
    }

    @Test
    public void fuzzy() {

        // 1 模糊查询 lucene 可以被分词器切出来，但 luce 则不能
        SearchResponse searchResponse = client.prepareSearch("info").setTypes("article")
                .setQuery(QueryBuilders.fuzzyQuery("title", "lucene")).get();

        // 2 打印查询结果
        SearchHits hits = searchResponse.getHits(); // 获取命中次数，查询结果有多少对象
        System.out.println("查询结果有：" + hits.getTotalHits() + "条");

        Iterator<SearchHit> iterator = hits.iterator();

        while (iterator.hasNext()) {
            SearchHit searchHit = iterator.next(); // 每个查询对象

            System.out.println(searchHit.getSourceAsString()); // 获取字符串格式打印
        }

        // 3 关闭连接
        client.close();
    }

    @Test
    public void createMapping() throws Exception {
        // 1 创建索引
        CreateIndexResponse createIndexResponse = client.admin().indices().prepareCreate("blog2").get();

        System.out.println("isAcknowledged:" + createIndexResponse.isAcknowledged());
        System.out.println("isShardsAcknowledged:" + createIndexResponse.isShardsAcknowledged());
        System.out.println("index:" + createIndexResponse.index());

        // 2.设置mapping
        XContentBuilder builder = XContentFactory.jsonBuilder()
                .startObject()
                .startObject("article")
                .startObject("properties")
                .startObject("id") // 业务 id
                .field("type", "text")
                .endObject()
                .startObject("title")
                .field("type", "keyword")
                .endObject()
                .startObject("date")
                .field("type", "date")
                .endObject()
                .endObject()
                .endObject()
                .endObject();

        PutMappingRequest mapping = Requests.putMappingRequest("blog2").type("article").source(builder);

        PutMappingResponse putMappingResponse = client.admin().indices().putMapping(mapping).get();

        System.out.println("isAcknowledged:" + putMappingResponse.isAcknowledged());

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("id","1");
        jsonObject.put("title","基于Lucene的搜索服务器");
        jsonObject.put("date","2018-01-12");

        // 3.插入数据
        IndexResponse indexResponse = client.prepareIndex("blog2", "article", "1")
                .setSource(jsonObject).execute().actionGet();

        System.out.println("index:" + indexResponse.getIndex());
        System.out.println("type:" + indexResponse.getType());
        System.out.println("id:" + indexResponse.getId());
        System.out.println("version:" + indexResponse.getVersion());
        System.out.println("result:" + indexResponse.getResult());


        // 4 关闭资源
        client.close();
    }

    @Test
    public void bulkUpsert() throws IOException{

        client.admin().indices().prepareDelete("twitter").get();

        BulkRequestBuilder bulkRequest = client.prepareBulk();

        // 插入
        bulkRequest.add(client.prepareIndex("twitter", "tweet", "1")
                .setSource(XContentFactory.jsonBuilder()
                        .startObject()
                        .field("user", "kimchy")
                        .field("postDate", new Date())
                        .field("message", "trying out Elasticsearch")
                        .endObject()
                )
        );

        // 删除
        bulkRequest.add(client.prepareIndex("twitter", "tweet", "1")
                .setSource(XContentFactory.jsonBuilder().startObject()
                        .field("user", "Kimchy")
                        .endObject()
                )
        );

        // 测试删除 先插入再删除
        bulkRequest.add(client.prepareIndex("twitter", "tweet", "2")
                .setSource(XContentFactory.jsonBuilder()
                        .startObject()
                        .field("user", "kimchy")
                        .field("postDate", new Date())
                        .field("message", "another post")
                        .endObject()
                )
        );

        bulkRequest.add(client.prepareDelete("twitter", "tweet", "2"));

        BulkResponse bulkResponse = bulkRequest.get();

        if (bulkResponse.hasFailures()) {
            // process failures by iterating through each bulk response item
            System.out.println(bulkResponse.buildFailureMessage());
            Iterator<BulkItemResponse> iter = bulkResponse.iterator();
            while(iter.hasNext()){
                BulkItemResponse resp = iter.next();
                System.out.println(resp.getResponse().getResult());
            }
        }
    }


}
