ls /    查看
    [cluster, server, brokers, zookeeper, -s, admin, isr_change_notification, log_dir_event_notification]

ls2 /   详细查看
    [cluster, server, brokers, zookeeper, admin, isr_change_notification, log_dir_event_notification, server2, server10000000023, controller_epoch, servers, consumers, latest_producer_id_block, config, hbase]
    cZxid = 0x0
    ctime = Thu Jan 01 08:00:00 CST 1970
    mZxid = 0x0
    mtime = Thu Jan 01 08:00:00 CST 1970
    pZxid = 0x5cc
    cversion = 37
    dataVersion = 0
    aclVersion = 0
    ephemeralOwner = 0x0
    dataLength = 0
    numChildren = 15

ls /server watch
    对 /server 节点添加监控
delete /server
    删除 /server 节点并激活监控
    WATCHER::
    WatchedEvent state:SyncConnected type:NodeDeleted path:/server

create /server1 'd1' 默认创建 永久非自增节点
create -s /server2 'd2' 创建自增序列节点  》》  server10000000023
create -e /server3 'd3' 创建临时节点 》》 session 关闭，节点失效
delete /server 删除节点
set /server1 'dd1' 修改
get /server1 获取
stat /server2 查看详细状态
