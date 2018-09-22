#!/usr/bin/env bash

# 执行
cd flasky
git checkout 6a
#error: Your local changes to the following files would be overwritten by checkout:
#        hello.py
#Please commit your changes or stash them before you switch branches.
#Aborting

git diff
#diff --git a/hello.py b/hello.py
#index 83940c1..4b50d05 100644
#--- a/hello.py
#+++ b/hello.py
#@@ -24,3 +24,6 @@ def index():
# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html', name=name)
#+                          <<<< 相比线上代码，一下是多出的部分
#+if __name__=='__main__':
#+    app.run(debug=True)
#\ No newline at end of file

git diff
#diff --git a/hello.py b/hello.py
#index 83940c1..cb63ef3 100644
#--- a/hello.py
#+++ b/hello.py
#@@ -23,4 +23,4 @@ def index():
#
# @app.route('/user/<name>')
# def user(name):   <<<< 删过头了，在尾部留空白换行
#-    return render_template('user.html', name=name)
#+    return render_template('user.html', name=name)
#\ No newline at end of file

git checkout 6a   # 成功取回
#Previous HEAD position was db6e7d3 Chapter 3: Static files (3d)
#HEAD is now at 86622e9 Chapter 6: Email support with Flask-Mail (6a)


