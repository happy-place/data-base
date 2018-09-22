 #!/usr/bin/env bash

# go2infc 原本就有 python2.7 环境，需要安装pip2.7
alias go2infc="ssh 10.47.200.3"
# go127 只有 python2.6，需要安装 python2.7 和 pip2.7
alias go127="ssh 10.47.200.127"
# go203 原先只有python2.6环境，通过tar包成功安装 python2.7, 然后再补 pip2.7
alias go203="ssh 10.47.200.203"

######  一、 go2infc 基于已有python2.7 创建虚拟环境
# 1）检查当前 pip 版本，不符合要求
 pip --version
# pip 9.0.3 from /usr/lib/python2.6/site-packages (python 2.6)

# 2) 升级失败 SSL 协议被封
 sudo pip install -U pip 升级失败

# 3) 成功检查到 python2.7 环境
python2.7
#Python 2.7.6 (default, Feb 10 2014, 12:41:37)
#[GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
#Type "help", "copyright", "credits" or "license" for more information.
#>>>

# 4) 使用现有 旧pip,安装 virtualenv
 pip install virtualenv

# 5) 创建虚拟环境目录 并 开放权限
 sudo mkdir /usr/local/penv2.7
 sudo chmod 755 /usr/local/penv2.7

# 6) 基于现有的 python2.7 安装 虚拟环境，出现如下提示，即说明成功安装了整套 python2.7 环境到  /usr/local/penv2.7 目录
sudo virtualenv penv2.7 --python=python2.7
#New python executable in /usr/local/penv27/bin/python2.7
#Also creating executable in /usr/local/penv27/bin/python
#Installing setuptools, pip, wheel...done.

# 7) 激活虚拟环境 并查看 pip 版本
source /usr/local/penv2.7/bin/activate
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ pip --version
#pip 18.0 from /usr/local/penv27/lib/python2.7/site-packages/pip (python 2.7)
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ exit()

# 8）注销虚拟环境命令 (慎用)
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ deactivate

# 9）配置别名
sudo vim /etc/profile
alias python2.7="/usr/local/penv2.7/bin/python2.7"
alias pip2.7="/usr/local/penv2.7/bin/pip2.7"
source /etc/profile

#10) 测试
#pip2.7 install flask
#  Downloading https://files.pythonhosted.org/packages/00/a4/cd587b2b19f043b65bf33ceda2f6e4e6cdbd0ce18d01a52b9559781b1da6/Flask-Script-2.0.6.tar.gz (43kB)
#    100% |████████████████████████████████| 51kB 138kB/s
#Collecting Flask (from flask-script)



###### 二、 go127 从无到有创建 python2.7 pip2.7 环境
# 经过多方测试，发现直接 在2.6.32-573.el6.x86_64 机器上 基于源码安装 Python2.7 都会失败，目前唯一对策是，拷贝 go2infc
# 已经成功安装的penv2.7环境到 go127 上，期待能够正常运行，或至少能够成功运行 python2.7 环境
#[huhao1@bi-infoc-txygz3-2 ~]$ uname -a
#Linux bi-infoc-txygz3-2 2.6.32-573.el6.x86_64 #1 SMP Thu Jul 23 15:44:03 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux

# 1) go2infc 机器上打包现有的 python2.7 环境,并通过 rz 命令 传送到本地
sudo tar -zcvf penv2.7.tar.gz /usr/local/penv2.7
rz /usr/local/penv2.7.tar.gz

# 2）从本地将 penv2.7.tar.gz 发送到 go127
# 经测试 sz -b 命令传送文件会出现乱码，每次都传送失败，改用 nc 启动 tcp服务传送
# 接受端执行 curl httpbin.org/ip 获取，其外网地址
curl httpbin.org/ip
{
  "origin": "118.89.34.125"
}
# 接收端先开启 nc 接受服务  (监听随意指定的8003端口，将接受的文件保存为penv2.7.tar.gz）
nc -l 8003 > penv2.7.tar.gz
# 发送端开始发送
nc 118.89.34.125 8003 < penv2.7.tar.gz
# 接受端成功接受后，会自动退出nc服务，解压，并移动到 /usr/local 目录
tar -zxvf penv2.7.tar.gz
sudo mv penv2.7 /usr/local/

# 3）安装virtualenv
pip install virtualenv

# 4）激活拷贝过来的 虚拟环境，发现直接进入了虚拟环境命令行，并可成功使用 python2.7 环境，但pip2.7 不能正常使用
source /usr/local/penv2.7/bin/activate
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ pthon2.7
#(penv27) Python 2.7.6 (default, Feb 10 2014, 12:41:37)
#(penv27) [GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
#(penv27) Type "help", "copyright", "credits" or "license" for more information.
#(penv27) >>>
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ pip --version
#Traceback (most recent call last):
#  File "/usr/local/penv27/bin/pip2.7", line 7, in <module>
#    from pip._internal import main
#  File "/usr/local/penv2.7/lib/python2.7/site-packages/pip/_internal/__init__.py", line 2, in <module>
#    from __future__ import absolute_import

# 5）重新回到了 go2infc 当初安装pip2.7 的环境
# 创建新虚拟环境目录
sudo mkdir /usr/local/penv27
sudo chmod 755 /usr/local/penv27

# 6) 基于现有的 python2.7 环境，重新再/usr/local/penv27 目录下安装一套新的python2.7,pip2.7环境
sudo virtualenv penv2.7 --python=/usr/local/penv2.7/bin/python2.7
#New python executable in /usr/local/penv27/bin/python2.7
#Also creating executable in /usr/local/penv27/bin/python
#Installing setuptools, pip, wheel...done.

# 7) 激活虚拟环境 并查看 pip 版本 Ctrl+D 退出
source /usr/local/penv2.7/bin/activate
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ pip --version
#pip 18.0 from /usr/local/penv27/lib/python2.7/site-packages/pip (python 2.7)
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ exit()

# 8）配置别名
sudo vim /etc/profile
alias python2.7="/usr/local/penv27/bin/python2.7"
alias pip2.7="/usr/local/penv27/bin/pip2.7"
source /etc/profile

# 9）测试 （大功告成）
#pip2.7 install flask
#  Downloading https://files.pythonhosted.org/packages/00/a4/cd587b2b19f043b65bf33ceda2f6e4e6cdbd0ce18d01a52b9559781b1da6/Flask-Script-2.0.6.tar.gz (43kB)
#    100% |████████████████████████████████| 51kB 138kB/s
#Collecting Flask (from flask-script)



######  一、 go203 参照 go127 从无到有 安装pip2.7失败，线上机器已经存在的 pip 不存在 re 模块
# 1）参照 go127 1~4）操作成功拷贝现有  penv2.7.tar.gz 解压到 /usr/local
# 2）下载 源码,成功安装
wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
tar -jxvf Python-2.7.3.tar.bz2
./configure
cd Python-2.7.3
make all
sudo make install
python2.7
#Python 2.7.3 (default, Feb 10 2014, 12:41:37)
#[GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
#Type "help", "copyright", "credits" or "license" for more information.
#>>>

# 3) 接下来情况与go2infc 一致了
# 创建新虚拟环境目录
sudo mkdir /usr/local/penv27
sudo chmod 755 /usr/local/penv27

# 4) 基于现有的 python2.7 环境，重新再/usr/local/penv27 目录下安装一套新的python2.7,pip2.7环境
sudo virtualenv penv2.7 --python=/usr/local/penv2.7/bin/python2.7
#New python executable in /usr/local/penv27/bin/python2.7
#Also creating executable in /usr/local/penv27/bin/python
#Installing setuptools, pip, wheel...done.

# 5) 激活虚拟环境 并查看 pip 版本 Ctrl+D 退出
source /usr/local/penv2.7/bin/activate
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ pip --version
#pip 18.0 from /usr/local/penv27/lib/python2.7/site-packages/pip (python 2.7)
#(penv27) [huhao1@bi-infoc-txygz3-2 penv27]$ exit()

# 6）配置别名
sudo vim /etc/profile
alias python2.7="/usr/local/penv27/bin/python2.7"
alias pip2.7="/usr/local/penv27/bin/pip2.7"
source /etc/profile

# 7）测试 （大功告成）
#pip2.7 install flask
#  Downloading https://files.pythonhosted.org/packages/00/a4/cd587b2b19f043b65bf33ceda2f6e4e6cdbd0ce18d01a52b9559781b1da6/Flask-Script-2.0.6.tar.gz (43kB)
#    100% |████████████████████████████████| 51kB 138kB/s
#Collecting Flask (from flask-script)

# 8) pip 批量安装依赖
    # 自动将项目使用到的依赖，记录到指定文件
    pip freeze requirements.txt
    # 安装依赖清单，恢复环境
    pip install -r equirements.txt
