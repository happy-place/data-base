-- 调用     /usr/bin/hive -S -f dashboard.sql   -hivevar s3path='{s3path}'    -hivevar ts='{ts}'

set tez.queue.name=crontab;
use infoc_kewl;
create temporary table dash_board_now1(uid string,country string,pid string,exp string,ut string,reg_user string,ts string);
create temporary table dash_board_yesterday1(uid string,country string,pid string,exp string,ut string,reg_user string,ts string);

insert into dash_board_now1 select if(c1 is null,c2,c1) uid,c3 as country,c4 as pid,c5 as exp,c6 as ut,c7 as reg_user,"${hivevar:ts}" ts from (
  select json_tuple(json,"posid","aid","uid","c","pid","exp","ut","reg_user","ts") from prepareIdv where dt="${hivevar:cal_dt}"
) tmp1 where c0 not in ("8010","9010") and c0 is not null;

insert into dash_board_yesterday1 select if(c1 is null,c2,c1) uid,c3 as country,c4 as pid,c5 as exp,c6 as ut,c7 as reg_user,"${hivevar:ts}" ts from (
  select json_tuple(json,"posid","aid","uid","c","pid","exp","ut","reg_user","ts") from prepareIdv where dt="${hivevar:before1}"
) tmp1 where c0 not in ("8010","9010") and c0 is not null;

insert overwrite directory "${hivevar:s3path}/no_exp_date_product/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid),'",',    '"ts":"',ts,'",',   '"pid":"',pid,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,num,join_num from
(select ts,pid,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid) tmp1
left join
(select a.ts,a.pid,count(distinct a.uid) as join_num from ( select ts,uid,pid from dash_board_yesterday1 group by ts,uid,pid ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid) tmp where ts is not null and pid is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_product_country/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country),'",',    '"ts":"',ts,'",',   '"pid":"',pid,'",',    '"country":"',country,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,num,join_num from
(select ts,pid,country,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid,country) tmp1
left join
(select a.ts,a.pid,a.country,count(distinct a.uid) as join_num from( select ts,uid,pid,country from dash_board_yesterday1 group by ts,uid,pid,country ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid and tmp1.country = tmp2.country) tmp where ts is not null and pid is not null and country is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_product_reguser/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",reg_user),'",',    '"ts":"',ts,'",',   '"pid":"',pid,'",',    '"reg_user":"',reg_user,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.reg_user,num,join_num from
(select ts,pid,reg_user,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid,reg_user) tmp1
left join
(select a.ts,a.pid,a.reg_user,count(distinct a.uid) as join_num from( select ts,uid,pid,reg_user from dash_board_yesterday1 group by ts,uid,pid,reg_user ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.reg_user) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid and tmp1.reg_user = tmp2.reg_user) tmp where ts is not null and pid is not null and reg_user is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_product_country_reguser/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",reg_user),'",',    '"ts":"',ts,'",',   '"pid":"',pid,'",',    '"country":"',country,'",',    '"reg_user":"',reg_user,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.reg_user,num,join_num from
(select ts,pid,country,reg_user,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid,country,reg_user) tmp1
left join
(select a.ts,a.pid,a.country,a.reg_user,count(distinct a.uid) as join_num from( select ts,uid,pid,country,reg_user from dash_board_yesterday1 group by ts,uid,pid,country,reg_user ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.reg_user) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid and tmp1.country = tmp2.country and tmp1.reg_user = tmp2.reg_user) tmp where ts is not null and pid is not null and country is not null and reg_user is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_product_country_ut_reguser/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",ut,"_",reg_user),'",',       '"ts":"',ts,'",',   '"pid":"',pid,'",',    '"country":"',country,'",',   '"ut":"',ut,'",',    '"reg_user":"',reg_user,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.ut,tmp1.reg_user,num,join_num from
(select ts,pid,country,ut,reg_user,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid,country,ut,reg_user) tmp1
left join
(select a.ts,a.pid,a.country,a.ut,a.reg_user,count(distinct a.uid) as join_num from( select ts,uid,pid,country,ut,reg_user from dash_board_yesterday1 group by ts,uid,pid,country,ut,reg_user ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.ut,a.reg_user) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid and tmp1.country = tmp2.country and tmp1.ut = tmp2.ut and tmp1.reg_user = tmp2.reg_user) tmp where ts is not null and pid is not null and country is not null and ut is not null and reg_user is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_product_ut/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",ut),'",',    '"ts":"',ts,'",',   '"pid":"',pid,'",',    '"ut":"',ut,'",',     '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.ut,num,join_num from
(select ts,pid,ut,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid,ut) tmp1
left join
(select a.ts,a.pid,a.ut,count(distinct a.uid) as join_num from( select ts,uid,pid,ut from dash_board_yesterday1 group by ts,uid,pid,ut ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.ut) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid and tmp1.ut = tmp2.ut) tmp where ts is not null and pid is not null and ut is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_country_ut/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",country,"_",ut),'",',    '"ts":"',ts,'",',   '"country":"',country,'",',    '"ut":"',ut,'",',     '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.country,tmp1.ut,num,join_num from
(select ts,country,ut,count(distinct uid) as num from dash_board_yesterday1 group by ts,country,ut) tmp1
left join
(select a.ts,a.country,a.ut,count(distinct a.uid) as join_num from( select ts,uid,pid,country,ut from dash_board_yesterday1 group by ts,uid,pid,country,ut ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid group by a.ts,a.country,a.ut) tmp2
on tmp1.ts = tmp2.ts and tmp1.country = tmp2.country and tmp1.ut = tmp2.ut) tmp where ts is not null and country is not null and ut is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/no_exp_date_pid_country_ut/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",ut),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',   '"country":"',country,'",',    '"ut":"',ut,'",',     '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.ut,num,join_num from
(select ts,pid,country,ut,count(distinct uid) as num from dash_board_yesterday1 group by ts,pid,country,ut) tmp1
left join
(select a.ts,a.pid,a.country,a.ut,count(distinct a.uid) as join_num from( select ts,uid,pid,country,ut from dash_board_yesterday1 group by ts,uid,pid,country,ut ) as a join ( select ts,uid,pid from dash_board_now1 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.ut) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid = tmp2.pid and tmp1.country = tmp2.country and tmp1.ut = tmp2.ut) tmp where ts is not null and pid is not null and country is not null and ut is not null
) tmps where data !="\N";

create temporary table dash_board_now2(uid string,country string,pid string,exp string,ut string,reg_user string,ts string);
create temporary table dash_board_yesterday2(uid string,country string,pid string,exp string,ut string,reg_user string,ts string);

insert into dash_board_yesterday2
select uid,country,pid,new_exp as exp,ut,reg_user,ts from dash_board_yesterday1 lateral view explode(split(exp,","))
dash_board_yesterday_tmp as new_exp where new_exp!="" group by ts,uid,pid,ut,new_exp,country,reg_user;

insert into dash_board_now2
select uid,country,pid,new_exp as exp,ut,reg_user,ts from dash_board_now1 lateral view explode(split(exp,","))
dash_board_yesterday_tmp as new_exp where new_exp!="" group by ts,uid,pid,ut,new_exp,country,reg_user;

drop table dash_board_now1;
drop table dash_board_now1;

insert overwrite  directory "${hivevar:s3path}/has_exp_date_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",exp),'",',    '"ts":"',ts,'",',   '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.exp,num,join_num from
(select ts,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,exp) tmp1
left join
(select a.ts,a.exp,count(distinct a.uid) as join_num from ( select ts,uid,exp from dash_board_yesterday2 group by ts,uid,exp ) as a join ( select ts,uid,exp from dash_board_now2 group by ts,uid,exp ) as b on a.ts = b.ts and a.uid = b.uid and a.exp = b.exp group by a.ts,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.exp = tmp2.exp) tmp where ts is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_product_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",exp),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',   '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.exp,num,join_num from
(select ts,pid,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,pid,exp) tmp1
left join
(select a.ts,a.pid,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,exp from dash_board_yesterday2 group by ts,uid,pid,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid=tmp2.pid and tmp1.exp=tmp2.exp) tmp where ts is not null and pid is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_product_country_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",exp),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',   '"country":"',country,'",',   '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.exp,num,join_num from
(select ts,pid,country,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,pid,country,exp) tmp1
left join
(select a.ts,a.pid,a.country,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,country,exp from dash_board_yesterday2 group by ts,uid,pid,country,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid=tmp2.pid and tmp1.country=tmp2.country and tmp1.exp=tmp2.exp) tmp where ts is not null and pid is not null and country is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_product_reg_user_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",reg_user,"_",exp),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',   '"reg_user":"',reg_user,'",',   '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.reg_user,tmp1.exp,num,join_num from
(select ts,pid,reg_user,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,pid,reg_user,exp) tmp1
left join
(select a.ts,a.pid,a.reg_user,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,reg_user,exp from dash_board_yesterday2 group by ts,uid,pid,reg_user,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.reg_user,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid=tmp2.pid and tmp1.reg_user=tmp2.reg_user and tmp1.exp=tmp2.exp) tmp where ts is not null and pid is not null and reg_user is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_product_country_reg_user_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",reg_user,"_",exp),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',   '"country":"',country,'",',   '"reg_user":"',reg_user,'",',   '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.reg_user,tmp1.exp,num,join_num from
(select ts,pid,country,reg_user,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,pid,country,reg_user,exp) tmp1
left join
(select a.ts,a.pid,a.country,a.reg_user,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,country,reg_user,exp from dash_board_yesterday2 group by ts,uid,pid,country,reg_user,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.reg_user,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid=tmp2.pid and tmp1.country=tmp2.country and tmp1.reg_user=tmp2.reg_user and tmp1.exp=tmp2.exp) tmp where ts is not null and pid is not null and country is not null and reg_user is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_product_country_ut_reg_user_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",ut,"_",reg_user,"_",exp),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',   '"country":"',country,'",',   '"ut":"',ut,'",',   '"reg_user":"',reg_user,'",',   '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.ut,tmp1.reg_user,tmp1.exp,num,join_num from
(select ts,pid,country,ut,reg_user,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,pid,country,ut,reg_user,exp) tmp1
left join
(select a.ts,a.pid,a.country,a.ut,a.reg_user,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,country,ut,reg_user,exp from dash_board_yesterday2 group by ts,uid,pid,country,ut,reg_user,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.ut,a.reg_user,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid=tmp2.pid and tmp1.country=tmp2.country and tmp1.ut=tmp2.ut and tmp1.reg_user=tmp2.reg_user and tmp1.exp=tmp2.exp) tmp where ts is not null and pid is not null and country is not null and ut is not null and reg_user is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_ut_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",ut,"_",exp),'",',    '"ts":"',ts,'",',    '"ut":"',ut,'",',     '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.ut,tmp1.exp,num,join_num from
(select ts,ut,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,ut,exp) tmp1
left join
(select a.ts,a.ut,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,ut,exp from dash_board_yesterday2 group by ts,uid,pid,ut,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid group by a.ts,a.ut,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.ut=tmp2.ut and tmp1.exp=tmp2.exp) tmp where ts is not null and ut is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_country_ut_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",country,"_",ut,"_",exp),'",',    '"ts":"',ts,'",',    '"country":"',country,'",',    '"ut":"',ut,'",',     '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.country,tmp1.ut,tmp1.exp,num,join_num from
(select ts,country,ut,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,country,ut,exp) tmp1
left join
(select a.ts,a.country,a.ut,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,country,ut,exp from dash_board_yesterday2 group by ts,uid,pid,country,ut,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.country,a.ut,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.country=tmp2.country and tmp1.ut=tmp2.ut and tmp1.exp=tmp2.exp) tmp where ts is not null and country is not null and ut is not null and exp is not null
) tmps where data !="\N";

insert overwrite  directory "${hivevar:s3path}/has_exp_date_product_country_ut_exp/${hivevar:cal_dt}/" row format delimited fields terminated by "\\t"
select data from (
select concat(  '{',   '"id":"',concat(ts,"_",pid,"_",country,"_",ut,"_",exp),'",',    '"ts":"',ts,'",',    '"pid":"',pid,'",',    '"country":"',country,'",',    '"ut":"',ut,'",',     '"exp":"',exp,'",',    '"num":',num,',',  '"join_num":',join_num,   '}'  ) data from
(select tmp1.ts,tmp1.pid,tmp1.country,tmp1.ut,tmp1.exp,num,join_num from
(select ts,pid,country,ut,exp,count(distinct uid) as num from dash_board_yesterday2 group by ts,pid,country,ut,exp) tmp1
left join
(select a.ts,a.pid,a.country,a.ut,a.exp,count(distinct a.uid) as join_num from( select ts,uid,pid,country,ut,exp from dash_board_yesterday2 group by ts,uid,pid,country,ut,exp ) as a join ( select ts,uid,pid from dash_board_now2 group by ts,uid,pid ) as b on a.ts = b.ts and a.uid = b.uid and a.pid = b.pid group by a.ts,a.pid,a.country,a.ut,a.exp) tmp2
on tmp1.ts = tmp2.ts and tmp1.pid=tmp2.pid and tmp1.country=tmp2.country and tmp1.ut=tmp2.ut and tmp1.exp=tmp2.exp) tmp  where ts is not null and pid is not null and country is not null and ut is not null and exp is not null
) tmps where data !="\N";