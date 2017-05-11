# Msg sended must have:
# 	1-type
# 	2-id
# 	3-src_ip
# 	4-dst_ip
# 	5-src_gps
from Environment import *
import time, threading, math
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

		self.hello()

	def add_neighbour(self, node):
		self.Immediate_Neighbours[node] = [0,0,0]

	def hello(self):
		# print(self.IP,'send hello')
		for node_ip in self.Immediate_Neighbours:
			# send(ip, msg)
			msg = {'type' : 'hello', 'id' : self.msg_id ,
					'src_ip' : self.IP, 'dst_ip' : node_ip,
					'src_gps' : self.GPS_Location}
			self.msg_id += 1
			self.Environment.send(self.IP, node_ip, msg)
		threading.Timer(1, self.hello).start()

	def receive(self, sender_ip, msg):
		# First save src_gps and send ACK
		self.GPS_Map[msg['src_ip']] = msg['src_gps']
		if msg['type'] != 'ACK':		
			self.send_ACK(sender_ip, msg)

		if msg['type'] == 'hello':
			if(sender_ip not in self.Immediate_Neighbours):
				self.Immediate_Neighbours[sender_ip] = [0,0,0]
			return
		
		elif msg['type'] == 'gps_reply' and msg['dst_ip'] != self.IP:
			# Forward the msg
			self.send_msg(msg)
		
		# If have wanted gps reply else forward
		elif msg['type'] == 'gps_request' and msg['dst_ip'] != self.IP:
			if(msg['dst_ip'] in self.GPS_Map):
				rlp_msg = {'type' : 'gps_reply','id':self.msg_id,
						'src_ip' : self.IP, 'dst_ip' : msg['src_ip'],
						'src_gps' : self.GPS_Location, 
						'rpl_ip': msg['dst_ip'],
						'rpl_gps':self.GPS_Map[msg['dst_ip']]}
				self.msg_id += 1
				self.send_msg(rlp_msg)
				return
			# Forward the msg
			self.send_msg_test(msg)

		# Reply with my location
		elif msg['type'] == 'gps_request':
			rlp_msg = {'type' : 'gps_reply','id':self.msg_id,
						'src_ip' : self.IP, 'dst_ip' : msg['src_ip'],
						'src_gps' : self.GPS_Location, 
						'rpl_ip': self.IP,
						'rpl_gps':self.GPS_Location}
			self.msg_id += 1
			self.send_msg(rlp_msg)
		
		# Update GPS Map with received location
		elif msg['type'] == 'gps_reply':
			self.GPS_Map[msg['rpl_ip']] = msg['rpl_gps']
		
		elif msg['type'] == 'ACK':
			# Update time for msg[src_ip]
			return

	def send_ACK(self, node_ip, received_msg):
		msg = {'type' : 'ACK', 'id': received_msg['id'] ,
				'src_ip' : self.IP, 'dst_ip' : node_ip, 'src_gps' : self.GPS_Location}
		self.Environment.send(self.IP, node_ip, msg)

	def send_msg(self, msg):
		if(msg['dst_ip'] not in self.GPS_Map):
			self.send_msg_test(msg)
			return
		# This message was send before or not
		f = False
		if msg['src_ip'] in self.sended_msgs:
			for i in self.sended_msgs[msg['src_ip']]:
				if(i == msg['id']):
					return
		else:
			self.sended_msgs[msg['src_ip']] = []
		self.sended_msgs[msg['src_ip']].append(msg['id'])

		# 1- determine possible neighbor
		possible_nodes = []
		ang = 0
		while(len(possible_nodes) == 0):
			ang += 45
			for node_ip in self.Immediate_Neighbours:
				if(self.in_region(self.GPS_Map[msg['dst_ip']], self.GPS_Map[node_ip], ang)):
					possible_nodes.append(node_ip)
			print("******************",possible_nodes)
		
		# 2- choose one neighbor to send msg to
		for node_ip in possible_nodes:
			self.Environment.send(self.IP, node_ip, msg)
		
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

	def in_region(self, dest_gps, gps, ang = 45):

		m = (dest_gps[1] - self.GPS_Location[1]) / (dest_gps[0] - self.GPS_Location[0]-0.0000000000000001)
		angle = math.atan(m)

		p = self.rotate_point(gps[:], angle)
		# print(p)

		m = p[1] / (p[0]+0.0000000001)
		angle = math.degrees(math.atan(m))
		if(angle<= ang and angle >= -1*ang):
			return True
		return False

	def rotate_point(self, p, angle):
		s = math.sin(angle)
		c = math.cos(angle)

		# translate point back to origin:
		p[0] -= self.GPS_Location[0]
		p[1] -= self.GPS_Location[1]

		# rotate point
		xnew = p[0] * c + p[1] * s
		ynew = -1* p[0] * s + p[1] * c
		
		# xnew = xnew + cx
		# ynew = ynew + cy
		return [xnew,ynew]