import pygame
import random
import block as b
import math
import saveload
pygame.init()
music = 'c418.mp3'
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)
(width, height) = (480, 360)
background_colour = (0,0,255)
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
zoom = 1
for i in range(amount):
  currentbloc = b.block(x,y,(random.randint(0,255),255,0))
  if x < width:  
    x+=10
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
while running:
  #print("Zoom: "+str(zoom),end='\r')
  pygame.display.flip()
  screen.fill(background_colour)
  (mouseX, mouseY) = pygame.mouse.get_pos()
  for block in blocks:  
    if math.sqrt((((block.x+scx)-mouseX)*((block.x+scx)-mouseX))+((((block.y+scy)-mouseY)*((block.y+scy)-mouseY)))) < 5:
      block.color = (255,0,0)
    else:
      block.color = block.prevcolor
    pygame.draw.rect(screen,block.color,(block.x+scx,block.y+scy,10+zoom,10+zoom))
  #pygame.draw.rect(screen,(255,0,0),(mouseX,mouseY,10,10))
  keys = pygame.key.get_pressed() 
  clock.tick()
  text = "FPS: " + str(clock.get_fps()) #get fps
  textsurface = myfont.render(text, False, (0, 20, 0))
  screen.blit(textsurface, (0, 0))
  text = "BLOCK: " + str(currentblockcolor) #get block
  textsurface = myfont.render(text, False, (0, 20, 0))
  screen.blit(textsurface, (0, 20))
  text = "CURRENT SAVE FILE: " + str(savefile) #get savefile
  textsurface = myfont.render(text, False, (0, 20, 0))
  screen.blit(textsurface, (0, 40))
  text = "CURRENT SAVE FILE: " + str(savefile) #get savefile
  textsurface = myfont.render(currentstatus, False, (0, 20, 0))
  screen.blit(textsurface, (0, height-20))
  
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
  if keys[pygame.K_9]:
    textsurface = myfont.render("Saving...", False, (0, 20, 0))
    screen.blit(textsurface, (0, height-20))
    saveload.save("save1.mcsave",blocks)
    currentstatus = "Saved..."
  if keys[pygame.K_8]:
    textsurface = myfont.render("Loading..", False, (0, 20, 0))
    screen.blit(textsurface, (0, height-20))
    blocks = saveload.read("save1.mcsave")
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
                if math.sqrt((((block.x+scx)-mouseX)*((block.x+scx)-mouseX))+((((block.y+scy)-mouseY)*((block.y+scy)-mouseY)))) < 10:
                  block.changecolor(currentblockcolor)
            except AttributeError:
                pass
      
    

