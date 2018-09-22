package com.big.data.test.zk;

import org.apache.zookeeper.*;
import org.apache.zookeeper.ZooDefs.Ids;

import java.io.IOException;
import java.util.Date;
import java.util.List;

/**
 * 需要先创建 /servers 节点
 * create /servers 'data'
 *
 */

public class ServicePublisher{
    // 创建静态客户端,在阻塞状态,循环开启main线程,能节省资源
    private static ZooKeeper zkClient = null;
    private static String connectString = "localhost:2181";
    private static int sessionTimeout = 2000;

    static {
        try {
            zkClient = new ZooKeeper(connectString, sessionTimeout, new Watcher() {

                public void process(WatchedEvent event) {
                    System.out.println(event.getPath() + "-->" + event.getType());
                }
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 通过传参解决方法选区问题,(@Test 方法不能传参)
    public static void main(String[] args) {
        try {
            if (args.length == 0) {
                System.out.println("please input args ...");
                return;  // 未传任何参数直接退出
            } else if (args.length > 1) {
                publish(args[0], args[1]);  // 发布服务
            } else {
                unpublish(args[0]);  // 取消发布
            }

        } catch (Exception e) {

            try {
                List<String> children = zkClient.getChildren("/servers", false);

                if (children == null || children.size() == 0) {
                    zkClient.close();
                }

            } catch (Exception e1) {
            }

        }

    }

    private static void unpublish(String node) throws InterruptedException, KeeperException {
        zkClient.delete("/servers/" + node, -1);
        info("/servers/" + node);
    }

    // 只能在永久节点下创建子节点,临时节点不能创建子节点
    private static void publish(String node, String data) throws KeeperException, InterruptedException {

        String path = zkClient.create("/servers/" + node, data.getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL_SEQUENTIAL);

        info(node, data);

        Thread.sleep(Long.MAX_VALUE);

    }

    private static void info(String... msg) {
        if (msg.length == 2) {
            System.out.println(new Date() + " >>>> " + msg[0] + "[ " + msg[1] + " ] has already published ...");
        } else {
            System.out.println(new Date() + " >>>> " + msg[0] + " ] has already unpublished ...");
        }
    }


}
         
