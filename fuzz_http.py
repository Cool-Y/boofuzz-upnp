#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
from boofuzz import *

def check_service():
    target_ip = "192.168.2.2"
    port = 5000
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((target_ip,int(port)))
        print(target_ip)
        s.shutdown(2)
        print('{0} is open'.format(port))
        return True
    except:
        print('{0} is close'.format(port))
        return False

def main():
    #session = Session(
    #    target=Target(
    #        connection=SocketConnection("192.168.2.2", 5000 , proto='tcp')
    #    ),
    #)

    session = Session()
    target=Target(connection=SocketConnection("192.168.2.2", 5000, proto='tcp'))
    target.procmon = instrumentation.External(pre=None, post=check_service, start=reset_target, stop=None)
    session.add_target(target)

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_group("Method", ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
        s_delim(" ", name='space-1')
        s_string("/index.html", name='Request-URI')
        s_delim(" ", name='space-2')
        s_string('HTTP/1.1', name='HTTP-Version')
        s_static("\r\n", name="Request-Line-CRLF")
    s_static("\r\n", "Request-CRLF")

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":
    main()
