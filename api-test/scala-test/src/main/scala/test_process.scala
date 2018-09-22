
/**
  * Author: Huhao <huhao1@cmc.com>
  * Date: 2018/8/6
  * Desc: 
  *  进程操作符
  */
import sys.process._

object test_process {
  def main(args: Array[String]): Unit = {
    val path = "/Users/huhao/Desktop/1.txt"

    val code = s"rm -rf ${path}" !

    print(code)
  }
}

