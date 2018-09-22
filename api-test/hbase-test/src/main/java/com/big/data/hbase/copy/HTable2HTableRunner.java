package com.big.data.hbase.copy;


import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
/**
 * Configured implements Configurable
 * Tool extends Configurable
 * 1.实现接口能够使用 hadoop 底层的高级特性,继承实现类,可以自动继承setConf,getConf方法
 *
 *  step1: 先创建 fruit_cp 表 hbase-shell> create 'fruit_cp','info'
 *  step2: yarn jar /Users/huhao/software/idea_proj/data-base/api-test/hbase-test/target/hbase-test-1.0-SNAPSHOT.jar com.big.data.hbase.copy.HTable2HTableRunner fruit fruit_cp
 *  step3: Hbase DNS 泛解析异常
 *      1.禁用DNS Server
 *          编辑etc/resolv.conf，把所有的DNS项（即形如 nameserver <ip>的行）都注释掉
 *      2.完善/etc/hosts文件
 *          将该文件中的所有ip与hostname的项都写正确
 *      3.调用命令dnsmasq
 *          brew install dnsmasq
 *          启动dnsmasq 反解析  MAC : sudo brew services start dnsmasq ，Linux: dnsmasq
 *      4.全部节点使用上述操作
 *  step4: 重新执行（依旧会报错），但可以正常执行
 *
 *
 *
 *
 *
 *
 *
 * @author Administrator
 */
public class HTable2HTableRunner extends Configured implements Tool {

    private static Log LOG = LogFactory.getLog(HTable2HTableRunner.class);

    private static Configuration conf;


    public int run(String[] args) throws Exception {
        // 1.获取Job实例,当本地的 hbase  或  hadoop 相关的 xml 配置需要覆盖集群配置时,创建job需要指定 conf
        Job job = Job.getInstance(conf);
        // 2.注册驱动类,提交yarn集群执行 mr 程序是必须的,若在本地运行则可随意
        job.setJarByClass(HTable2HTableRunner.class);

        /*3.org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil 新版本API,使用scan
         * org.apache.hadoop.hbase.mapred.TableMapReduceUtil 老版本API使用Columns
         */
        Scan scan = new Scan();

        // 4.设置使用缓存,但不设置缓存块
        scan.setCacheBlocks(false);
        // 每500条写提交写入一次
        scan.setCaching(500);

        // 5.注册 Mapper 类 Reader
        TableMapReduceUtil.initTableMapperJob(
                args[0],
                scan,
                HTableReadMapper.class,
                ImmutableBytesWritable.class,
                Put.class,
                job);
        // 6.注册Reducer驱动类 Wrirter
        TableMapReduceUtil.initTableReducerJob(
                args[1],
                HTableWriteReducer.class,
                job);

        // 7.提价Job
        boolean status = job.waitForCompletion(true);

        if (status) {
            LOG.info("HTable2HTableRunner has run " + status + ". >>>>>>>");
        } else {
            LOG.error("HTable2HTableRunner has run " + status + ". >>>>>>>");
        }

        return status ? 0 : 1;
    }

    public static void main(String[] args) throws Exception {

        // 1. mr 程序执行入口,创建驱动实体类
        HTable2HTableRunner runner = new HTable2HTableRunner();
        /*2. 调用HBaseConfiguration.create()时,框架会读取本地的 hbase -site.xml , hdfs -site.xml,core-site.xml配置
         * 并提交集群,完成对指定属性的覆盖
         */
        conf = HBaseConfiguration.create();
        runner.setConf(conf);
        // 3.ToolRunner 调用run方法实质底层在调用Tool接口的run()
        int code = ToolRunner.run(conf, runner, args);
        System.exit(code);
    }


}
         
