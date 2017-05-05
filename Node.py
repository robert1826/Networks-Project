# Msg sended must have:
# 	1-type
# 	2-id
# 	3-src_ip
# 	4-dst_ip
# 	5-src_gps
from Environment import *
class Node:
	# Environment = None
	# IP = None # my ip
	# GPS_Location = None # my gps
	# GPS_Map = {} # map[node_ip] => its gps
	# Immediate_Neighbours = {} # map[node_ip] => (t1, t2, t3)
	# sended_msgs = {} # map[node_ip] => list of msg id(id1,id2...) to prevent resend the same msg again


	def __init__(self, env, ip, gps):
		self.Environment = env
		self.IP = ip
		self.GPS_Location = gps
		self.msg_id = 0
		self.Immediate_Neighbours = {}
		self.sended_msgs = {}
		self.GPS_Map = {}
		self.sended_msgs[ip] = [0]


	def hello(self):
		for node_ip in self.Immediate_Neighbours:
			# send(ip, msg)
			msg = {'type' : 'hello', 'id' : self.msg_id ,
					'src_ip' : self.IP, 'dst_ip' : node_ip,
					'src_gps' : self.GPS_Location}
			self.msg_id += 1
			self.Environment.send(self.IP, node_ip, msg)

	def receive(self, sender_ip, msg):
		# First save src_gps and send ACK
		self.GPS_Map[msg['src_ip']] = msg['src_gps']
		if msg['type'] != 'ACK':		
			self.send_ACK(sender_ip, msg)

		if msg['type'] == 'hello':
			return
		
		elif (msg['type'] == 'gps_request' or msg['type'] == 'gps_replay') and msg['dst_ip'] != self.IP:
			# Forward the msg
			self.send_msg_test(msg)

		elif msg['type'] == 'gps_request':
			rlp_msg = {'type' : 'gps_reply','id':msg['id'],
						'src_ip' : self.IP, 'dst_ip' : msg['src_ip'],
						'src_gps' : self.GPS_Location}
			self.Environment.send(self.IP, msg['src_ip'], rlp_msg)
		elif msg['type'] == 'ACK':
			# Update time for msg[src_ip]
			return

	def send_ACK(self, node_ip, received_msg):
		msg = {'type' : 'ACK', 'id': received_msg['id'] ,
				'src_ip' : self.IP, 'dst_ip' : node_ip, 'src_gps' : self.GPS_Location}
		self.Environment.send(self.IP, node_ip, msg)

	def send_msg(self, msg):
		# 1- determine possible neighbor
		# 2- choose one neighbor to send msg to
		# 3- wait for reply
		return 0

	def send_msg_test(self, msg):
		f = False
		if msg['src_ip'] in self.sended_msgs:
			for i in self.sended_msgs[msg['src_ip']]:
				if(i == msg['id']):
					return
		else:
			self.sended_msgs[msg['src_ip']] = []
		self.sended_msgs[msg['src_ip']].append(msg['id'])
		for node_ip in self.Immediate_Neighbours:
			self.Environment.send(self.IP, node_ip, msg)

	def request_gps(self, dst_ip):
		msg = {'type' : 'gps_request','id':self.msg_id,
				'src_ip' : self.IP, 'dst_ip' : dst_ip,
				'src_gps' : self.GPS_Location}
		self.msg_id += 1
		self.send_msg_test(msg)