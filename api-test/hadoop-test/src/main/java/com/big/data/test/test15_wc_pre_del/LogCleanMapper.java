package com.big.data.test.test15_wc_pre_del;

import java.io.IOException;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class LogCleanMapper extends Mapper<LongWritable, Text, LongWritable, Text>{

	@Override
	protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		String lineValue = value.toString();
		
		String[] splitsStrings = lineValue.split("\t");
		
		if(splitsStrings.length < 30){
			context.getCounter("Web Counter ", "Length < 30").increment(1L);
			return;
		}
		
		String url = splitsStrings[1];
		if(StringUtils.isBlank(url)){
			context.getCounter("Web Counter ", "Url is Blank").increment(1L);
			return;
		}
		
		String provinceIdValueString = splitsStrings[23];
		if(StringUtils.isBlank(provinceIdValueString)){
			context.getCounter("Web Counter ", "ProvinceId is Blank").increment(1L);
			return;
		}
		
		int provinceId = Integer.MAX_VALUE;
		try {
			provinceId = Integer.parseInt(provinceIdValueString);
		} catch (Exception e) {
			return;
		}
		
		if(Integer.MAX_VALUE == provinceId){
			return;
		}
		
		context.write(key, value);	
		
	}
	
}
