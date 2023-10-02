import socket

hosts = ['www.uc.edu', 'www.google.com', 'www.bing.com']

print('Working from host:' + socket.getfqdn())

for h in hosts:
	print(socket.gethostbynae(h))
