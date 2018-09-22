hive 安装

1.下载 http://mirror.bit.edu.cn/apache/hive/hive-1.2.2/apache-hive-1.2.2-bin.tar.gz
  准备  mysql-connector-java-5.1.27-bin.jar

2. 解压
 tar -zxvf apache-hive-1.2.2-bin.tar.gz /Users/huhao/software/

3. 释放自定义配置文件
cd /Users/huhao/software
mv apache-hive-1.2.2-bin hive-1.2.2
cd hive-1.2.2/conf

cp hive-default.xml.template hive-site.xml
cp hive-env.sh.template hive-env.sh
cp hive-exec-log4j.properties.template  hive-exec-log4j.properties
cp hive-log4j.properties.template hive-log4j.properties

4.修改配置
vim hive-site.xml
-------------------------------------------------------------------
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
<property>
	<name>hive.metastore.warehouse.dir</name>
	<value>hdfs://localhost:9000/apps/hive/warehouse</value>
</property>

</property>
	<name>hive.exec.scratchdir</name>
  	<value>/tmp/hive</value>
</property>

<property>
    <name>hive.downloaded.resources.dir</name>
    <value>/Users/huhao/software/hive-1.2.2/tmp/${hive.session.id}_resources</value>
</property>

<property>
    <name>hive.server2.logging.operation.log.location</name>
    <value>/Users/huhao/software/hive-1.2.2/tmp/huhao/operation_logs</value>
</property>

<property>
 	<name>javax.jdo.option.ConnectionDriverName</name>
 	<value>com.mysql.jdbc.Driver</value>
</property>

<property>
	<name>javax.jdo.option.ConnectionURL</name>
 	<value>jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true</value>
</property>

<property>
	<name>javax.jdo.option.ConnectionUserName</name>
	<value>root</value>
</property>

<property>
	<name>javax.jdo.option.ConnectionPassword</name>
	<value>root</value>
</property>

</configuration>
-------------------------------------------------------------------

vim hive-env.sh
-------------------------------------------------------------------
export HADOOP_HOME=/Users/huhao/software/hadoop-2.7.2
export HIVE_CONF_DIR=/Users/huhao/software/hive-1.2.2/conf
export HIVE_AUX_JARS_PATH=/Users/huhao/software/hive-1.2.2/extlib
-------------------------------------------------------------------

5.配置环境
sudo vim /etc/profile  ~/.bash_profile ~/.bashrc
-------------------------------------------------------------------
# hive
HIVE_HOME=/Users/huhao/software/hive-1.2.2
HIVE_CONF_DIR=$HIVE_HOME/conf
HIVE_AUX_JARS_PATH=$HIVE_HOME/extlib
PATH=$PATH:$HIVE_HOME/bin
export HIVE_HOME HIVE_CONF_DIR HIVE_AUX_JARS_PATH PATH
-------------------------------------------------------------------

6。初始化目录
mkdir /Users/huhao/software/hive-1.2.2/extlib
chmod 777 /Users/huhao/software/hive-1.2.2/extlib

hdfs dfs -mkdir -p /apps/hive/warehouse
hdfs dfs -mkdir /tmp/hive

hdfs dfs -chmod 777 /apps/hive/warehouse
hdfs dfs -chmod 777 /tmp/hive

cp mysql-connector-java-5.1.27-bin.jar /Users/huhao/software/hive-1.2.2/lib

7.初始化 schema
schematool -initSchema -dbType mysql

8.查看 mysql hive 数据库是否被创建

9.命令行 hive
