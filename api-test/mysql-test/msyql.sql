-- 时间间隔
SELECT datediff('2008-12-30','2008-12-29') from dual;

-- mysql 整数封装成时间戳
-- WHERE UNIX_TIMESTAMP(updated_at) <=({updated_at} - (24-{hour})*3600) AND UNIX_TIMESTAMP(updated_at)> ({updated_at}-24*3600)"









