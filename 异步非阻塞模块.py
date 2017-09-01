import socket
import select

class Request(object):
    """
    封装socket对象，使每次循环时创建的socket对象能对应它的req_info字典，
    方便其利用字典拿到对应的host信息等
    """
    def __init__(self, sock, info):
        self.sock = sock
        self.info = info

    def fileno(self):
        return self.sock.fileno()


class AsyncRequest(object):
    def __init__(self):
        self.sock_list = []
        self.conns = []

    def add_request(self, req_info):
        """
        创建请求
         req_info: {'host': 'www.baidu.com', 'port': 80, 'path': '/'},
        :return:
        """
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect((req_info['host'], req_info['port']))
        except BlockingIOError as e:
            pass

        obj = Request(sock, req_info)
        self.sock_list.append(obj)
        self.conns.append(obj)

    def run(self):
        """
        开始事件循环,检测：连接成功？数据是否返回？
        :return:
        """
        while True:
            # select.select([socket对象,])
            # 可是任何对象，对象一定要有fileno方法，实际上执行的是对象.fileno()
            # select.select([request对象,])
            r, w, e = select.select(self.sock_list, self.conns, [], 0.05)
            # w,是否连接成功
            for obj in w:
                # 检查obj:request对象
                # socket, {'host': 'www.baidu.com', 'port': 80, 'path': '/'},
                data = "GET %s http/1.1\r\nhost:%s\r\n\r\n" % (obj.info['path'], obj.info['host'])
                obj.sock.send(data.encode('utf-8'))
                #连接成功后从列表中删除此obj对象，避免重复连接
                self.conns.remove(obj)
            # 数据返回，接收到数据
            for obj in r:
                response = obj.sock.recv(8096)
                #函数名加括号运行对应的回调函数
                obj.info['callback'](response)
                #相应的为避免重复接收移除已经接收成功的对象
                self.sock_list.remove(obj)

            # 所有请求已经返回
            if not self.sock_list:
                break


if __name__ == '__main__':
    #指定回调函数，可以在屏幕输出，也可以写入文件、数据库等
    def callback_fun1(response):
        print(response)

    def callback_fun2(response):
        pass
        # with open ......

    url_list = [
        {'host': 'www.baidu.com', 'port': 80, 'path': '/', 'callback': callback_fun1},
        {'host': 'www.cnblogs.com', 'port': 80, 'path': '/index.html', 'callback': callback_fun2},
        {'host': 'www.bing.com', 'port': 80, 'path': '/', 'callback': callback_fun1},
    ]

    obj = AsyncRequest()
    for item in url_list:
        obj.add_request(item)

    obj.run()
