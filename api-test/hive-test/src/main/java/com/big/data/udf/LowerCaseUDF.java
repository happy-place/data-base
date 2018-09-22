package com.big.data.udf;

import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public class LowerCaseUDF extends UDF {

    public Text evaluate(Text str){
      return  new Text(str.toString().toUpperCase());
    }

}
