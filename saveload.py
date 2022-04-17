import block
types = {
  "stone": (153, 151, 142),
  "dirt": (74, 42, 37)
}
def save(file,data):
  try:
    inv_map = {v: k for k, v in types.items()}
    with open(file,'x') as f:
      for blocks in data:
        f.write(str(blocks.x))
        f.write('\n')
        f.write(str(blocks.y))
        f.write('\n')
        f.write(str(blocks.color))
        f.write('\n')
  except FileExistsError:
    with open(file,'w') as f:
      for blocks in data:
        f.write(str(blocks.x))
        f.write('\n')
        f.write(str(blocks.y))
        f.write('\n')
        f.write(str(blocks.color))
        f.write('\n')
def read(file):
  print("Getting File")
  try:
    with open(file,'r') as f:
      print("File opend")
      g = f.readlines()
      a = 0
      blocks = []
      print(len(g))
      for i in range(len(g)-1):
        x = int(g[a])
        y = int(g[a+1])
        color = str(g[a+2])
        #ccolor = tuple(map(int, color.split(', ')))
        ccolor = eval(color)
        #print(ccolor)
        cblock = block.block(x,y,ccolor)
        blocks.append(cblock)
        if a!=len(g)-3:
          a+=3
        else:
          break
        
      return blocks
  except KeyError:
    print("an execption occure")
      
