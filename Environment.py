from Node import *
import time
class Environment:
	Nodes = {}	# map[node_id] => Node

	def send(self, sender_ip, receiver_ip, msg):
		print(sender_ip,'send',msg['type'],'to',receiver_ip)
		self.Nodes[receiver_ip].receive(sender_ip, msg)


if __name__ == '__main__':
	env = Environment()

	# 1-2
	# |
	# 3-4
	for i in range(1,5):
		env.Nodes[i] = Node(env, i, [i,i])

	env.Nodes[1].GPS_Location = [0,0]
	env.Nodes[2].GPS_Location = [10,2]
	env.Nodes[3].GPS_Location = [0,-10]
	env.Nodes[4].GPS_Location = [-10,-10]

	env.Nodes[1].add_neighbour(2)
	env.Nodes[1].add_neighbour(3)
	env.Nodes[3].add_neighbour(4)

	time.sleep(3)

	for i in env.Nodes:
		print(env.Nodes[i].GPS_Map)
	print()
	env.Nodes[1].request_gps(4)
	for i in env.Nodes:
		print(env.Nodes[i].GPS_Map)

	for i in env.Nodes:
		print(env.Nodes[i].GPS_Location)