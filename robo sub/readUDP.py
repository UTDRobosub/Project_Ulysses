import socket

HOST = '' 
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", PORT))

while (1):
	 data, addr = s.recvfrom(1024)
	 li = []
	 li= data.split()
	 print(li)
