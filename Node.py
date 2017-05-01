class Node:
	Environment = None
	IP = None # my ip
	GPS_Location = None # my gps
	GPS_Map = {} # map[node_ip] => its gps
	Immediate_Neighbours = {} # map[node_ip] => (t1, t2, t3)


	def __init__(env, ip, gps):
		self.Environment = env
		self.IP = ip
		self.GPS_Location = gps

	def hello():
		for node_ip in Immediate_Neighbours:
			# send(ip, msg)
			msg = {'type' : 'hello', 'src_ip' : self.IP, 'dst_ip' : node_ip, 'src_gps' : self.GPS_Location}
			Environment.send(node_ip, msg) 

	def request_gps(dst_ip):


	def receive(msg):
		# check ip
		if msg['type'] == 'gps_request' and msg['dst_ip'] != self.IP:
			ip = request_gps(msg['dst_ip'])
			
		if msg['dst_ip'] != self.IP:
			return
		if msg['type'] == 'hello':
			self.GPS_Location[msg['src_ip']] = msg['src_gps']
		if msg['type'] == 'gps_request':
			msg = {'type' : 'gps_reply', 'src_ip' : self.IP, 'dst_ip' : msg['src_ip'], 'src_gps' : self.GPS_Location}
			self.Environment.send(msg['src_ip'], msg)
