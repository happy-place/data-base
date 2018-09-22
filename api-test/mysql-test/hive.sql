-- 时间戳转换为指定格式输出
select uid,uname,countrycode,from_unixtime(reg_time,'yyyy-MM-dd') reg,from_unixtime(last_login_time,'yyyy-MM-dd') last_login  , from_unixtime(last_update_time,'yyyy-MM-dd') last_update from t_cl_user_daily where dt in ('20180616','20180618') and uid ='811052691999948800';


insert overwrite local directory "./gold_sum.tsv" row format delimited fields terminated by '\t' lines terminated by '\n'  select dt,sum(delta) from dataReport.finance_cl_user_finan_logs where action >=100 and action <=199 and action%2 = 1 and action not in (117,105) group by dt order by dt;

# 第一张：汇总 income 每天用户消费金额 》》 表名：kewl_income_sum_daily
# >> [uid,country,dt,sum_money,sum_gold] 插入20180701 分区的数据 ↓↓↓↓↓↓

select uid,country,sum(money) as sum_money,sum(gold) as sum_gold from income where dt='20180701' group by uid,country;


# 第二张：汇总 kewl_income_sum_daily 历史30天 sum_money，sum_gold 累计求和 》》表名： kewl_income_sum_30
# >>[uid,country,dt,sum_money30,sum_gold30] 插入20180701 分区的数据 ↓↓↓↓↓↓

select uid,country,sum(sum_money) as sum_money30,sum(sum_gold) as sum_gold30 from kewl_income_sum_daily  where dt >= regexp_replace(date_sub(concat(substring('20180701',0,4),'-',substring('20180701',5,2),'-',substring('20180701',7,2)),29),'-','') and dt <='20180701'
group by uid,country;


# 第三张：汇总 kewl_income_sum_30 历史30天内，max_sum_money30 和 max_sum_gold30 的最大值 》》表名：kewl_income_max_sum_30
# >>[uid,country,dt,max_sum_money30,max_sum_gold30] 插入20180701 分区的数据 ↓↓↓↓↓↓

select uid,country,max(sum_money30) as max_sum_money30,max(sum_gold30) as max_sum_gold30 from kewl_income_sum_30 where dt >= regexp_replace(date_sub(concat(substring('20180701',0,4),'-',substring('20180701',5,2),'-',substring('20180701',7,2)),29),'-','') and dt <='20180701'
group by uid,country;