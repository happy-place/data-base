package com.big.data.hbase.copy;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

/**
 * TableMapper<KEYOUT, VALUEOUT> extends  Mapper <ImmutableBytesWritable, Result, KEYOUT, VALUEOUT> {
 * 1.从HBase表逐行读取数据,然后以Result形式返回;
 * 2.默认 Mapper 的输入KV类型已经固定,唯一需要自定义的是输出KV类型
 *
 * @author Administrator
 */

public class HTableReadMapper extends TableMapper<ImmutableBytesWritable, Put>{
@Override
    protected void map(ImmutableBytesWritable key, Result value, Context context)
            throws IOException, InterruptedException {
        // 1.筛选特定条件的表记录
        boolean flag = false;
        Put put = null;

        Cell[] cells = value.rawCells();
        // 创建Put

        for (Cell cell : cells) {
            byte[] family = CellUtil.cloneFamily(cell);
            // 模拟通过 mr 筛选数据
            if ("info".equals(Bytes.toString(family))) {
                byte[] qualifier = CellUtil.cloneQualifier(cell);
                if ("name".equals(Bytes.toString(qualifier))) {
                    put = new Put(key.get());
                    put.add(cell);
                    flag = true;
                } else if ("color".equals(Bytes.toString(qualifier))) {
                    put = new Put(key.get());
                    // 默认 mr 程序对指定类型数据进行加工
                    String upperColor = Bytes.toString(CellUtil.cloneValue(cell)).toUpperCase();
                    put.add(family, qualifier, Bytes.toBytes(upperColor));
                    flag = true;
                }
            }
        }

        // 多次写出与一次写出效果一样，应为每次写出直接就序列化了
        if (flag) {
            context.write(key, put);
        }
    }
}
         
