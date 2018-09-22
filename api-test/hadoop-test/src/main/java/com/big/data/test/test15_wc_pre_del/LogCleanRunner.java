package com.big.data.test.test15_wc_pre_del;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class LogCleanRunner extends Configured implements Tool{

	public static void main(String[] args) throws Exception {
		LogCleanRunner lc = new LogCleanRunner();
//		args = new String[]{"/weblog/20170725/2015082818", "/user/hive/warehouse/syllabus.db/track_log/date=20150828/hour=18"};
//		/user/hive/warehouse/syllabus.db/track_log/date=20150828/hour=18
		Tools.deleteFileInHDFS(args[1].substring(0, 57), args[1].substring(57));
    	int status = ToolRunner.run(lc.getConf(), lc, args);
    	System.exit(status);

	}
	
	 public int run(String[] args) throws Exception {
			Configuration conf = new Configuration();
	    	
	    	Job job = Job.getInstance(conf);
	    	job.setJarByClass(LogCleanRunner.class);
	    	
	    	Path inPath = new Path(args[0]);
	    	FileInputFormat.addInputPath(job, inPath);
	    	
	    	job.setMapperClass(LogCleanMapper.class);
	    	job.setMapOutputKeyClass(LongWritable.class);
	    	job.setMapOutputValueClass(Text.class);
	    	
	    	job.setReducerClass(LogCleanReducer.class);
	    	job.setOutputKeyClass(Text.class);
	    	job.setOutputValueClass(NullWritable.class);
	    	
	    	Path outPath = new Path(args[1]);
	    	FileOutputFormat.setOutputPath(job, outPath);
	    	
	    	boolean isSuccess = job.waitForCompletion(true);
	    	
	    	return isSuccess ? 0 : 1;
		}

}
