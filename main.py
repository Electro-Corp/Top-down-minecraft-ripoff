import pygame
import random
import block as b
import math
import saveload
s = None
pygame.init()
music = 'c418.mp3'
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)
(width, height) = (500, 300)
background_colour = (0, 0, 255)
pygame.display.set_caption('MC RIPOFF Alpha 0.1')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
running = True
myfont = pygame.font.SysFont('Sans Serif', 30)
scx = 0
scy = 0
"""Create blocks"""
blocks = []
amount = 1000
x = 0
y = 0
zoom = 50.0
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
"""MAIN MENU"""
img = pygame.image.load('mc.png')
imgx = 50
imgy = 230
savefile = "save1.mcsave"
currentblockcolor = "stone"
currentstatus = ""
""" SERVER CLIENT STUFF """
def connect():
	global s
	import socket
	HOST = str(input("Connect to: "))
	if HOST == "0":
		HOST = "192.168.86.31"
	PORT = int(input("Port: "))
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((HOST, PORT))
	except ConnectionRefusedError:
		print("Error, server refused. Check IP and port!")
		s = None
def sendblocks():
		global blocks
		global s
		data = bytearray([0xAA] * 30000)
		
		i = 0
		
		for block in blocks:
			if(i < len(data)):
				data[i] = 0xDA
				i += 1
				data[i] = 0xFA
				i += 1
				#print(block.x)
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
		
		s.sendall(data)	
while running:

    #print("Zoom: "+str(zoom),end='\r')
    pygame.display.flip()
    screen.fill(background_colour)
    (mouseX, mouseY) = pygame.mouse.get_pos()
    blocksren = 0
    if(s):
    	blockdata = s.recv(30000)
    	
    	inblock = False
    	if(blockdata):
    		#print("data recived. parsing!")
    		_b = []
	    	x = 0
	    	y = 0
	    	color = [0,0,0]
	    	for i in range(len(blockdata)):
	    		if(blockdata[i] == 0xCA):
	    			sendblocks()
	    			break
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
			    	except: 
			    		pass
			    	if(blockdata[i] == 0xdb):
			    		inblock = False
			    		currentbloc = b.block(x, y, tuple(color))
			    		#print(f"Block recived, X: {x}, Y: {y}, Color: {color}")
			    		_b.append(currentbloc)
           
	    	#print(blockdata)
	    	#print(blocks)
	    	if(len(_b) > 100):
	    	    blocks = _b
   # print(f"Current ammount of blocks: {len(blocks)}")
    for block in blocks:
        newx = (block.x + scx)
        newy = (block.y + scy)
        if math.sqrt((((newx) - mouseX) * ((newx) - mouseX)) +
                     ((((newy) - mouseY) * ((newy) - mouseY)))) < 5:
            block.color = (255, 0, 0)
        else:
            block.color = block.prevcolor
        if newx < width + 1 and newx > 0 - 1 and newy < height + 1 and newy > 0 - 1:
            blocksren = blocksren + 1
            rect = pygame.draw.rect(
                screen, block.color,
                (block.x + scx, block.y + scy, 10, 10)).inflate_ip(zoom, zoom)

        #else:
        #    blocksren = blocksren - 1

        #rect = pygame.Rect(newx, newy, 10, 10)
        #rect.inflate_ip(zoom, zoom)
        #pygame.draw.rect(screen, block.color, rect)
        #rect.inflate_ip(zoom,zoom)

        #rect.inflate_ip(zoom, zoom)
    #pygame.draw.rect(screen,(255,0,0),(mouseX,mouseY,10,10))
    keys = pygame.key.get_pressed()
    clock.tick()
    text = "FPS: " + str(clock.get_fps())  #get fps
    textsurface = myfont.render(text, False, (0, 20, 0))
    screen.blit(textsurface, (0, 0))
    text = "BLOCK: " + str(currentblockcolor)  #get block
    textsurface = myfont.render(text, False, (0, 20, 0))
    screen.blit(textsurface, (0, 20))
    text = "CURRENT SAVE FILE: " + str(savefile)  #get savefile
    textsurface = myfont.render(text, False, (0, 20, 0))
    screen.blit(textsurface, (0, 40))
    text = "BLOCKS RENDERED: " + str(
        blocksren)  #get how many blocks are currently rendered
    textsurface = myfont.render(text, False, (0, 20, 0))
    screen.blit(textsurface, (0, 60))
    text = "BLOCKS TOTAL: " + str(len(blocks))  #get how many blocks are currently rendered
    textsurface = myfont.render(text, False, (0, 20, 0))
    screen.blit(textsurface, (0, 80))
    text = "CURRENT SAVE FILE: " + str(savefile)  #get savefile
    textsurface = myfont.render(currentstatus, False, (0, 20, 0))
    screen.blit(textsurface, (0, height - 20))
    """Image"""
    #screen.blit(img, (imgx, imgy))
    if keys[pygame.K_UP]:
        scy += 10
    if keys[pygame.K_DOWN]:
        scy -= 10
    if keys[pygame.K_LEFT]:
        scx += 10
    if keys[pygame.K_RIGHT]:
        scx -= 10
    """diffent block types"""
    if keys[pygame.K_1]:
        currentblockcolor = "stone"
    if keys[pygame.K_2]:
        currentblockcolor = "dirt"
    if keys[pygame.K_3]:
        currentblockcolor = "red wool"
    if keys[pygame.K_c]:
    	connect()
    """SAVE/LOAD"""
    if keys[pygame.K_9]:

        textsurface = myfont.render("Saving...", False, (0, 20, 0))
        screen.blit(textsurface, (0, height - 20))
        savefile = input("Save file: ")
        saveload.save(savefile, blocks)
        currentstatus = "Saved..."
    if keys[pygame.K_8]:
        textsurface = myfont.render("Loading..", False, (0, 20, 0))
        screen.blit(textsurface, (0, height - 20))
        savefile = input("Load: ")
        blocks = saveload.read(savefile)
        currentstatus = "Loaded..."
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONUP:
        #   for block in blocks:
        #     if math.sqrt((((block.x+scx)-mouseX)*((block.x+scx)-mouseX))+((((block.y+scy)-mouseY)*((block.y+scy)-mouseY)))) < 10:
        #       block.changecolor(currentblockcolor)
        if pygame.mouse.get_pressed()[0]:
            try:
                for block in blocks:
                    if math.sqrt((((block.x + scx) - mouseX) *
                                  ((block.x + scx) - mouseX)) +
                                 ((((block.y + scy) - mouseY) *
                                   ((block.y + scy) - mouseY)))) < 10:
                        block.changecolor(currentblockcolor)
                        
            except AttributeError:
                pass
        	
   
