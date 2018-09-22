package com.big.data.test.zk;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import java.util.Date;
import java.util.List;

public class ServiceSubscriber{
    // 阻塞状态 使用静态属性,只生成一次客户端
    private static ZooKeeper zkClient = null;
    private static String connectString = "localhost:2181";
    private static int sessionTimeout = 2000;

    static {
        try {
            // 启动时刻,初始化客户端,并注册监听时间
            zkClient = new ZooKeeper(connectString, sessionTimeout, new Watcher() {
//                @Override
                public void process(WatchedEvent event) {
                    System.out.println(event.getState() + "-->" + event.getPath());
                    try {
                        // 轮询监听
                        monitor();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws KeeperException, InterruptedException {
        try {
            subscribe();  // main 方法阻塞于此
        } finally {
            zkClient.close();  // 最终关闭
        }
    }

    // 订阅服务
    private static void subscribe() throws KeeperException, InterruptedException {
        // 此处只获取一次,然后阻塞进程,但不注册监听事件
        List<String> children = zkClient.getChildren("/servers", false);

        doBiz(children);

        Thread.sleep(Long.MAX_VALUE);
    }

    // 客户端执行业务
    private static void doBiz(Object obj) {
        System.out.println(new Date() + " >>> client has already online for " + obj);
    }

    // 监听时间
    private static void monitor() throws KeeperException, InterruptedException {
        // 监听/servers 节点下的子节点数量变化
        List<String> children = zkClient.getChildren("/servers", true);

        System.out.println(new Date() + " >>> " + children);
    }

}

