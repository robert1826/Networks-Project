from Node import *
class Environment:
	Nodes = {}	# map[node_id] => Node

	def send(self, sender_ip, receiver_ip, msg):
		self.Nodes[receiver_ip].receive(sender_ip, msg)


if __name__ == '__main__':
	env = Environment()

	# 1-2
	# |
	# 3-4
	n1 = Node(env, 1 , 1)
	n2 = Node(env, 2 , 2)
	n3 = Node(env, 3 , 3)
	n4 = Node(env, 4 , 4)
	env.Nodes[1] = n1
	env.Nodes[2] = n2
	env.Nodes[3] = n3
	env.Nodes[4] = n4

	n1.Immediate_Neighbours[2] = [0,0,0]
	n1.Immediate_Neighbours[3] = [0,0,0]

	n2.Immediate_Neighbours[1] = [0,0,0]

	n3.Immediate_Neighbours[1] = [0,0,0]
	n3.Immediate_Neighbours[4] = [0,0,0]

	n4.Immediate_Neighbours[3] = [0,0,0]

	n1.hello()

	print(n1.GPS_Map)
	print(n2.GPS_Map)
	print(n3.GPS_Map)
	print(n4.GPS_Map)
	print()
	n1.request_gps(4)
	print(n1.GPS_Map)
	print(n2.GPS_Map)
	print(n3.GPS_Map)
	print(n4.GPS_Map)