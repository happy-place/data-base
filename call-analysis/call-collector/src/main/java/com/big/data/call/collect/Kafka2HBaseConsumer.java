package com.big.data.call.collect;


import com.big.data.call.common.PropertiesUtil;
import kafka.consumer.Consumer;
import kafka.consumer.ConsumerConfig;
import kafka.consumer.ConsumerIterator;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;
import kafka.serializer.Decoder;
import kafka.serializer.StringDecoder;
import kafka.utils.VerifiableProperties;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.LinkedBlockingQueue;


/**
 * 接收flume传送给kafka的call-log主题的消息,写入hbase表
 */
public class Kafka2HBaseConsumer {

    private static Log LOG = LogFactory.getLog (Kafka2HBaseConsumer.class);

    private HBaseDao hbaseDao = null;

    private String callerFamily = null;


    /**
     * 1).会阻塞,无超时
     * 尾部插入,如果没有空间可存,会阻塞
     * put: Inserts the specified element at the tail of this queue, waiting if necessary for space to become available.
     * <p>
     * 头部取出,如果没有元素可取,会阻塞
     * take: Retrieves and removes the head of this queue, waiting if necessary until an element becomes available.
     * <p>
     * 2).会阻塞,有超时
     * 尾部插入,如果无空间,会阻塞至有空间或超时
     * offer: Inserts the specified element at the tail of this queue, waiting if necessary up to the specified wait
     * time for space to become available.
     * <p>
     * 3).取而不出,如果没有返回null
     * peek: Retrieves, but does not remove, the head of this queue, or returns null if this queue is empty.
     * 移除:
     * remove: Removes a single instance of the specified element from this queue,if it is present
     * <p>
     * 3).不会阻塞
     * 头部取出,如果没有返回null
     * poll: Retrieves and removes the head of this queue, or returns null if this queue is empty.
     */
    private LinkedBlockingQueue queue = null;

    public Kafka2HBaseConsumer() {
        hbaseDao = new HBaseDao ();
        callerFamily = PropertiesUtil.get ("hbase.properties", "caller.family");
        queue = new LinkedBlockingQueue ();
    }

    private void getMsgFromKafka() throws InterruptedException {

        ConsumerConfig consumerConfig = new ConsumerConfig (PropertiesUtil.getProperties ("kafka.properties", null));
        ConsumerConnector connector = Consumer.createJavaConsumerConnector (consumerConfig);

        Map<String, Integer> fetchSettings = new HashMap<> ();

        String topic = "calllog";
        Integer parallelLevel = new Integer (1);
        fetchSettings.put (topic, parallelLevel);

        Decoder<String> keyDecoder = new StringDecoder (new VerifiableProperties ());
        Decoder<String> valDecoder = new StringDecoder (new VerifiableProperties ());

        Map<String, List<KafkaStream<String, String>>> messageStreams = connector.createMessageStreams (fetchSettings, keyDecoder, valDecoder);

        KafkaStream<String, String> kafkaStream = messageStreams.get (topic).get (0);

        ConsumerIterator<String, String> iterator = kafkaStream.iterator ();

        // 通过队列均衡负载
        while (iterator.hasNext ()) {
            String msg = iterator.next ().message ();
            queue.put (msg);
            LOG.info ("--> put msg:["+msg+"] into queue...");
        }
    }

    private void putMsgToHBase() {
        while (true) {
            try {
                String callerLog = String.valueOf (queue.take ());
                hbaseDao.put (callerFamily, callerLog);
                LOG.info ("<<< take msg: ["+callerLog+"] from queue...");
            } catch (Exception e) {
                e.printStackTrace ();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // 创建 kafka消费者
        Kafka2HBaseConsumer consumer = new Kafka2HBaseConsumer ();
        // 先启动消费端 kafka consumer -> hbase
        Thread hbaseThread = new Thread (()->{
            consumer.putMsgToHBase ();
        });
        hbaseThread.start ();
        // 再启动接收端 kafka Producer -> channel -> kafka consumer
        consumer.getMsgFromKafka ();

    }

}
