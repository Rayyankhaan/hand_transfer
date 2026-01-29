import socket
import zlib

def build_frame(data):
    payload = data
    length = len(payload).to_bytes(2, 'big')
    crc = zlib.crc32(payload).to_bytes(4, 'big')
    return b'HG' + length + payload + crc

def send(ip, data):
    s = socket.socket()
    s.connect((ip, 9000))
    s.send(build_frame(data))
    s.close()

def receive():
    s = socket.socket()
    s.bind(("", 9000))
    s.listen(1)
    conn, _ = s.accept()
    frame = conn.recv(4096)
    conn.close()
    return frame
