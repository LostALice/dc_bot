"""import socket,struct

mac = "00-d8:61:c8:ed:39"
asd = ()
print(len(asd))

def wol(mac):
    a = b""
    for m in mac.split(":"):
        a += struct.pack("B",int(m,16))
    magic = b"\xff" * 6 + a * 16

    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    soc.sendto(magic,("192.168.0.255",9))
    return soc.close()

wol(mac)
"""

a = ()

b = [_ for _ in a]

print(type(b),b)
