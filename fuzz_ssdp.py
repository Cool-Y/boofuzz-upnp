#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
from boofuzz import *
from boofuzz import instrumentation
import socket

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

def reset_target():
    print(1)

def main():
    # session = Session(
    #     target=Target(
    #         connection=SocketConnection("239.255.255.250", 1900, proto='udp')
    #         # netmon=Remote_NetworkMonitor("192.168.2.2", 5000, proto='tcp'))
    #     ),
    # )
    session = Session()
    target=Target(connection=SocketConnection("127.0.0.1", 1900, proto='udp',bind=('192.168.2.1', 17972)))
    target.procmon = instrumentation.External(pre=None, post=check_service, start=reset_target, stop=None)
    session.add_target(target)

    s_initialize(name="SSDP")
    with s_block("Request-Line"):
        s_group("Method", ['M-SEARCH'])
        s_delim(" ", name='space-1')
        s_string("*", name='Request-URI')
        s_delim(" ", name='space-2')
        s_string('HTTP/1.1', name='HTTP-Version')
        s_static("\r\n", name="CRLF1")
        s_string('HOST:239.255.255.250:1900', name='HOST')
        s_static("\r\n", name="CRLF2")
        s_string('ST:ssdp:all', name='ST')
        s_static("\r\n", name="CRLF3")
        s_string('MX:2', name='MX')
        s_static("\r\n", name="CRLF4")
        s_string('HMAN:"ssdp:discover', name='MAN')
        s_static("\r\n", name="CRLF5")
    s_static("\r\n", "Request-CRLF")

    session.connect(s_get("SSDP"))
    session.fuzz()


if __name__ == "__main__":
    main()
