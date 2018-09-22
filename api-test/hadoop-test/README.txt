MAC 配置免密登录
vi ~/.ssh/config
----------------------------------------
Host cssor_server  #别名，域名缩写
   HostName localhost  #完整的域名
   User huhao  #登录该域名使用的账号名
   PreferredAuthentications publickey  #有些情况或许需要加入此句，优先验证类型ssh
   IdentityFile ~/.ssh/id_rsa #私钥文件的路径
----------------------------------------

hdfs namenode -format
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.6.0-cdh5.7.0.jar pi 3 1024