types = {
  "stone": (153, 151, 142),
  "dirt": (74, 42, 37),
  "red wool": (240,34,20)
}
class block:
  def __init__(self,x,y,color):
    self.x = x
    self.y = y
    self.color = color
    self.prevcolor = color
  def changecolor(self,type):
    try: 
      self.color = types[type]
      self.prevcolor = self.color
      
    except KeyError:
      return 0
  