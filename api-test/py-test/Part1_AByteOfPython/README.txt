规划：https://www.zhihu.com/question/20702054
https://files.cnblogs.com/files/wangshide/A-Byte-of-Python3(中文版).pdf

1.7 值得考虑的一些东西
There are two ways of constructing a software design: one way is to make it so simple that there are obviously no deficiencies; the other is to make it so complicated that there are no obvious deficiencies. 有两种方式构建软件设计:一种是把软件做得很简单以至于明显找不到缺陷;另一种 是把它做得很复杂以至于找不到明显的缺陷。
——C. A. R. Hoare

Success in life is a matter not so much of talent and opportunity as of concentration and perseverance.
获得人生中的成功需要的专注与坚持不懈多过天才与机会。
——C. W. Wendte

 Unicode 是 ASCII 的超集。如果要严格使用 ASCII 编码的 字节流，可用 str.encode("ascii") 。更多细节，请访问在 StackOverflow 上的相关讨论。 默认所有的字符串的编码是 Unicode 。

换行
>>> a="aaaa\
... aaa"
>>> a

转义
>>> 'What\'s your name?'
"What's your name?"

保留3位精度
>>> '{0:.3}'.format(1/3)
'0.333'

定长居中
>>> '{0:^11}'.format('hello')
'   hello   '

运算符：
+ - * /
// 整除  5//3 = 1  % 取余
2**3 = 8 幂
2<<2 = 8 左移位 0010 -》 1000 ，3<<2 = 12 -》0011 -》 1100
8>>2 = 2 右位移 1000 -》 0010 ，12>>2 = 3 -》1100 -》 0011
2&3 = 2  位与 10 & 11 -》01
2|3 = 3  位或 10 | 11 -》11
5^3 = 6  非或 不同为1，相同为0，101^011 = 110
~5 = -6  ~x = -(x+1)
< <=,>,>=,==,!=,not,and,or 逻辑运算
a=2,a=a*3,a*=3 赋值


input("please enter a num: ")












