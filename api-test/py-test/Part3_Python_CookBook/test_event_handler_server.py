#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2018/7/21'
Info:
        
"""
import os,traceback
import select,socket,time
from concurrent.futures import ThreadPoolExecutor

# 事件驱动基类
class EventHandler:
	def fileno(self):
		# 必须被继承才能调用
		raise NotImplemented('must implement')
	
	# 判断时候接受请求，还是发出相应 （事件类型)
	def wants_to_receive(self):
		return False
	
	def handle_receive(self):
		pass
	
	def wants_to_send(self):
		return False
	
	def handle_send(self):
		pass

# 注册事件驱动
def event_loop(handlers):
	while True:
		# 分别提取接受，发送类型驱动器
		wants_recv = [h for h in handlers if h.wants_to_receive()]
		wants_send = [h for h in handlers if h.wants_to_send()]
		# 先处理接受，再处理发送
		can_recv,can_send,_ = select.select(wants_recv,wants_send,[])
		for h in can_recv:
			h.handle_receive()
		for h in can_send:
			h.handle_send()


def start_server():
	# 组织需要注册的驱动器
	handlers = [UDPTimeServer(('',14000)),UDPEchoServer(('',15000))]
	# 注册驱动器，开始轮询监听
	event_loop(handlers)


# 继承驱动器基类，创建 UDP驱动程序
class UDPServer(EventHandler):
	def __init__(self,address):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind(address)
	
	# 获取文件句柄
	def fileno(self):
		return self.sock.fileno()
	
	# 接收类型
	def wants_to_receive(self):
		return True

# 继承UDPServer 驱动器，进一步，处理数据接受函数
class UDPTimeServer(UDPServer):
	def handle_receive(self):
		msg,addr = self.sock.recvfrom(1)
		self.sock.sendto(msg,addr)

# 继承UDPServer 驱动器，进一步，处理数据接受函数
class UDPEchoServer(UDPServer):
	def handle_receive(self):
		msg,addr = self.sock.recvfrom(8192)
		self.sock.sendto(msg,addr)

'''

TCP例子的关键点是从处理器中列表增加和删除客户端的操作。 对每一个连接，一个新的处理器被创建并加到列表中。当连接被关闭后，
每个客户端负责将其从列表中删除。 如果你运行程序并试着用Telnet或类似工具连接，它会将你发送的消息回显给你。
并且它能很轻松的处理多客户端连接。
'''

class TCPServer(EventHandler):
	def __init__(self, address, client_handler, handler_list):
		'''
		:param address: 监听地址
		:param client_handler: 处理请求的处理器
		:param handler_list: 待轮询处理器集合
		'''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		self.sock.bind(address)
		self.sock.listen(1)
		self.client_handler = client_handler
		self.handler_list = handler_list
	
	def fileno(self):
		return self.sock.fileno()
	
	def wants_to_receive(self):
		# 一直开启接收模型
		return True
	
	def handle_receive(self):
		client, addr = self.sock.accept()
		# 处理器集合中注册客户端处理器
		self.handler_list.append(self.client_handler(client, self.handler_list))

class TCPSender(EventHandler):
	def __init__(self, sock, handler_list):
		self.sock = sock
		self.handler_list = handler_list
		self.outgoing = bytearray()
	
	def fileno(self):
		return self.sock.fileno()
	
	def close(self):
		self.sock.close()
		# Remove myself from the event loop's handler list
		self.handler_list.remove(self)
	
	def wants_to_send(self):
		# outgoing 中储备消息，就发送，否则拒绝发送
		return True if self.outgoing else False
	
	def handle_send(self):
		# 消息发送完，清空发送完的消息
		nsent = self.sock.send(self.outgoing)
		self.outgoing = self.outgoing[nsent:]


class TCPReceiverSender(TCPSender):
	def wants_to_receive(self):
		# 一直接受消息
		return True
	
	def handle_receive(self):
		# 接受消息后返回
		data = self.sock.recv(8192)
		if not data:
			self.close()
		else:
			self.outgoing.extend(data)


def start_server2():
	handlers = []
	handlers.append(TCPServer(('',16000),TCPReceiverSender,handlers))
	event_loop(handlers)
	
	
'''
实际上所有的事件驱动框架原理跟上面的例子相差无几。实际的实现细节和软件架构可能不一样， 但是在最核心的部分，都会有一个轮询的循环来检查活动socket，并执行响应操作。

事件驱动I/O的一个可能好处是它能处理非常大的并发连接，而不需要使用多线程或多进程。 也就是说，select() 调用（或其他等效的）能监听大量的socket并响应它们中任何一个产生事件的。
 在循环中一次处理一个事件，并不需要其他的并发机制。

事件驱动I/O的缺点是没有真正的同步机制。 如果任何事件处理器方法阻塞或执行一个耗时计算，它会阻塞所有的处理进程。 调用那些并不是事件驱动风格的库函数也会有问题，
同样要是某些库函数调用会阻塞，那么也会导致整个事件循环停止。

'''

class ThreadPoolHandler(EventHandler):
	def __init__(self, nworkers):
		if os.name == 'posix':
			self.signal_done_sock, self.done_sock = socket.socketpair()
		else:
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.bind(('127.0.0.1', 0))
			server.listen(1)
			self.signal_done_sock = socket.socket(socket.AF_INET,
			                                      socket.SOCK_STREAM)
			self.signal_done_sock.connect(server.getsockname())
			self.done_sock, _ = server.accept()
			server.close()
		
		self.pending = []
		self.pool = ThreadPoolExecutor(nworkers)
	
	def fileno(self):
		return self.done_sock.fileno()
	
	# Callback that executes when the thread is done
	def _complete(self, callback, r):
		self.pending.append((callback, r.result()))
		self.signal_done_sock.send(b'x')
	
	# Run a function in a thread pool
	def run(self, func, args=(), kwargs={},*,callback):
		r = self.pool.submit(func, *args, **kwargs)
		r.add_done_callback(lambda r: self._complete(callback, r))
	
	def wants_to_receive(self):
		return True
	
	# Run callback functions of completed work
	def handle_receive(self):
		# Invoke all pending callback functions
		for callback, result in self.pending:
			callback(result)
			self.done_sock.recv(1)
		self.pending = []

def fib(n):
	if n < 2:
		return 1
	else:
		return fib(n - 1) + fib(n - 2)

class UDPFibServer(UDPServer):
	def handle_receive(self):
		msg, addr = self.sock.recvfrom(128)
		n = int(msg)
		pool.run(fib, (n,), callback=lambda r: self.respond(r, addr))
	
	def respond(self, result, addr):
		self.sock.sendto(str(result).encode('ascii'), addr)

if __name__ == '__main__':
	pool = ThreadPoolHandler(16)
	handlers = [ pool, UDPFibServer(('',16000))]
	event_loop(handlers)


def start_server3():
	# 创建总容量为16 的线程池 ThreadPoolHandler
	pool = ThreadPoolHandler(16)
	# 将线程池 和 UDF 服务端点存入轮询hanldler 队列
	handlers = [ pool, UDPFibServer(('',16000))]
	event_loop(handlers)

	
if __name__=="__main__":
	try:
		# start_server2()
		start_server3()
		pass
	except:
		traceback.print_exc()
	finally:
		os._exit(0)




