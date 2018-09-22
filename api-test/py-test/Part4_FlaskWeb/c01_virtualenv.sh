#!/bin/sh

# File > New > Module > Python > Django(先使用现成 python2.7 环境创建，稍后再切换为虚拟环境) Part4_FlaskWeb

# 安装 虚拟环境
pip install virtualenv

# 查看版本 16.0.0
virtualenv --version

cd venv

'''
直接使用 git clone https 报错 Unknown SSL protocol
huhao:~ huhao$ git clone https://github.com/miguelgrinberg/flasky.git
Cloning into 'flasky'...
fatal: unable to access 'https://github.com/miguelgrinberg/flasky.git/': Unknown SSL protocol error in connection to github.com:-9836
'''
# 尝试将 https改成git 正常
git clone git://github.com/miguelgrinberg/flasky.git

# 存储目录规划错误，删除
cd flasky
git rm ./* -r -f
cd ..
rm -rf flasky
cd ../

# 拷贝到 Part4_Flaskweb 目录下，落盘为项目名称 flasky
git clone git://github.com/miguelgrinberg/flasky.git
# 下载并重命名
git clone git://github.com/miguelgrinberg/flasky.git git_flasky



# 进入git目录
cd flasky

# 检出第一章
git checkout 1a
# HEAD is now at 613ae49 Chapter 1: initial version (1a)

virtualenv venv
'''
直接在 flasky 目录 创建虚拟环境
huhao:flasky huhao$ virtualenv venv
New python executable in /Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_Flaskweb/flasky/venv/bin/python
Installing setuptools, pip, wheel...done.
'''

# 激活venv 这个虚拟环境
source venv/bin/activate
'''
huhao:flasky huhao$ source venv/bin/activate  <<< 进入虚拟环境
(venv) huhao:flasky huhao$  <<<< 当前就处于虚拟环境中
(venv) huhao:flasky huhao$ deactivate   <<< 退出虚拟环境
huhao:flasky huhao$  <<< 返回全局环境
(venv) huhao:flasky huhao$ pip install flask
'''

# 工作结束，关闭虚拟环境
deactivate

'''
(venv) huhao:flasky huhao$ pip install flask   <<< 虚拟环境中安装 flask
(venv) huhao:flasky huhao$ python   <<< 虚拟环境中启动 python
Python 2.7.14rc1 (v2.7.14rc1:c707893f9c, Aug 26 2017, 14:20:52)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import flask   <<< 导入flask 模块
>>>
'''

# 将 venv 中的 python2.7 环境暴露到公共shell 环境
vim /etc/profile
alias pyenv2="/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/flasky/venv/bin/python2.7"
alias pipenv2="/Users/huhao/software/idea_proj/data-base/api-test/py-test/Part4_FlaskWeb/flasky/venv/bin/pip2.7"
source /etc/profile

# 将 vene 中的 python2.7 注册到 SDK 环境中
# File > Project Structure > SDK > 点击 '+' 添加 python sdk > 定位到指定 venv/bin/python2.7 文件即可

# 将本项目的环境切换为虚拟环境
# File > Project Structure > Modules > 选中当前模块 Part4_FlaskWeb > Modules SDK 下拉选选择配置好的 data-base/venv 环境



