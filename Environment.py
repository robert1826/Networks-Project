from Node2 import *
import time
class Environment:
	Nodes = {}	# map[node_id] => Node
	links = []
	Transfer_time = 0.5

	def __init__(self, n):
		n += 1
		for i in range(1,n):
			self.Nodes[i] = Node(self, i, [i,i])
		
		for i in range(0,n):
			self.links.append([])
		for i in range(0,n):
			for j in range(0,n):
				self.links[i].append([])

	def send(self, sender_ip, receiver_ip, msg):
		self.links[sender_ip][receiver_ip].append(msg)
		if( len(self.links[sender_ip][receiver_ip]) == 1):
			threading.Timer(self.Transfer_time, self.send_sim,[sender_ip, receiver_ip]).start()
		

	def send_sim(self, sender_ip, receiver_ip):
		if( len(self.links[sender_ip][receiver_ip]) > 0):
			msg = self.links[sender_ip][receiver_ip][0]
			del self.links[sender_ip][receiver_ip][0]
			
			if(msg['type'] != 'hello' and msg['type'] != 'ACK'):
				print(sender_ip,'send',msg['type'],'to',receiver_ip)
			self.Nodes[receiver_ip].receive(sender_ip, msg)

		if( len(self.links[sender_ip][receiver_ip]) > 0):
			threading.Timer(self.Transfer_time, self.send_sim,[sender_ip, receiver_ip]).start()


if __name__ == '__main__':
	env = Environment(5)

	# 1---2
	# |	   \
	# 3-----4
	#		|
	# 		5
	
	# print(len(env.links),len(env.links[0]),len(env.links[0][0]))

	env.Nodes[1].GPS_Location = [0,0]
	env.Nodes[2].GPS_Location = [4,-5]
	env.Nodes[3].GPS_Location = [0,-10]
	env.Nodes[4].GPS_Location = [10,-10]
	env.Nodes[5].GPS_Location = [10,-20]

	env.Nodes[1].add_neighbour(2)
	env.Nodes[1].add_neighbour(3)
	env.Nodes[2].add_neighbour(4)
	env.Nodes[3].add_neighbour(4)
	env.Nodes[4].add_neighbour(5)

	time.sleep(3)

	
	print("********************"*2,"Reqest GPS")
	env.Nodes[1].request_gps(4)

	time.sleep(5)
	for i in env.Nodes:
		print(env.Nodes[i].GPS_Map)

	print("********************"*2,"Send Data")
	env.Nodes[1].send_data(4,50)
