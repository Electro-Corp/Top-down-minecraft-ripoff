import socket
import os
import time
import block as b
import random
import sys
HOST = ''
PORT = int(sys.argv[1])
""" map data """
blocks = []
amount = 30000
x = 0
y = 0
zoom = 50.0
width = 256
height = 256
for i in range(amount):
    currentbloc = b.block(x, y, (random.randint(0, 255), 255, 0))
    if x < width:
        x += 10
    else:
        #print("Reached edge")
        x = 0
        y += 10
        #print("Y: "+str(y))
    blocks.append(currentbloc)
def parseblocks(conn):
	global blocks
	prevblock = blocks
	blockdata = conn.recv(30000)
	#global blocks
	inblock = False
	if(blockdata):
		#print("data recived. parsing!")
		blocks = []
		x = 0
		y = 0
		prevx = x
		prevy = y
		prevcolor = [0,0,0]
		color = [0,0,0]
		for i in range(len(blockdata)):
			if(blockdata[i] != 0xAA):
				if(not inblock):
					pass
		    			#print(f"Not inside block. weird. im at: {i} and am reading data {blockdata[i]}")
				"""
		    		0xFA = X data
		    		0xFB = Y data
		    		0xFC = color(1)
		    		0xFD = color(2)
		    		0xFF = color(3)
		    		"""
				if(blockdata[i] == 0xda):
					inblock = True
					#print("block!")
					
				#print(f"Inside block rn, i is {i}")
				try:
					if(blockdata[i] == 0xfa):
						i += 1
						x = blockdata[i]
					if(blockdata[i] == 0xfb):
						i += 1
						y = blockdata[i]
					if(blockdata[i] == 0xfc):
						i += 1
						color[0] = blockdata[i]
					if(blockdata[i] == 0xfd):
						i += 1
						color[1] = blockdata[i]
					if(blockdata[i] == 0xff):
						i += 1
						color[2] = blockdata[i]
				
					if(blockdata[i] == 0xdb):
						inblock = False
						currentbloc = b.block(x, y, tuple(color))
						prevx = x
						prevy = y
						prevcolor = color
						#print(f"Block recived, X: {x}, Y: {y}, Color: {color}")
						blocks.append(currentbloc)
				except:
					currentbloc = b.block(prevx+10, prevy+10, tuple(prevcolor))
					#print(f"Block recived, X: {x}, Y: {y}, Color: {color}")
					blocks.append(currentbloc)
	i = 0
	_b = []
	previ = 0
	for block in blocks:
		try:
			if(block == prevblock[i]):
				_b.append(prevblock[i])
				previ = i
			else:
				_b.append(block)
		except:
			_b.append(block)
	blocks = []	
	blocks = _b
	return blocks
def sendblocks(blocks):
		data = bytearray([0xAA] * 30000)
		i = 0
		for block in blocks:
			if(i < len(data)):
				data[i] = 0xDA
				i += 1
				data[i] = 0xFA
				i += 1
				if(block.x < 256):
					data[i] = block.x
				else:
					data[i] = 0xAA
				i += 1
				data[i] = 0xFB
				i += 1
				if(block.y < 256):
					data[i] = block.y
				else:
					data[i] = 0xAA
				i += 1
				data[i] = 0xFC
				i += 1
				data[i] = block.color[0]
				i += 1
				data[i] = 0xFD
				i += 1
				data[i] = block.color[1]
				i += 1
				data[i] = 0xFF
				i += 1
				data[i] = block.color[2]
				i += 1
				data[i] = 0xDB
				i += 1
		for i in range(len(connections)):
			#print(f"Sending data to {i}")
			connections[i].sendall(data)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	print("Server started...")
	s.bind((HOST,PORT))
	s.listen(2)
	connections = []
	while len(connections) != 2:
		conn, addr = s.accept()
		print(f"Server recived connection from : {conn} at {addr}")
		connections.append(conn)
	print(f"Connections length: {len(connections)}")
	print("Connections aquired")
	print("Sending map data")
	"""
	0xFA = X data
	0xFB = Y data
	0xFC = color(1)
	0xFD = color(2)
	0xFF = color(3)
    	"""
	e = open("log.txt","w")
	pc = 0
	sendblocks(blocks)
	"""while True:
		input("")
		sendblocks(blocks)
		connections[0].sendall(bytearray([0xCA]))
		e.write("Reciving data\n")
		blocks = parseblocks(connections[0])
	"""
	while True:
		#e.write(f"[LOOP {pc}]\n")
		#e.write("Sending read request to connection (0)\n")
		connections[0].sendall(bytearray([0xCA]))
		#e.write("Reciving data\n")
		blocks = parseblocks(connections[0])
		sendblocks(blocks)
		#e.write("Sending read request to connection (1)\n")
		connections[1].sendall(bytearray([0xCA]))
		#e.write("Reciving data (1)\n")
		blocks = parseblocks(connections[1])
		#e.write("Sending blocks\n")
		sendblocks(blocks)
		pc +=1
		    	
				
