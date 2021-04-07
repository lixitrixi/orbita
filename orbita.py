import sys, math, numpy
import pygame
from pygame.locals import *

# colors
black = (0,0,0)
white = (250,250,250)
green = (57, 255, 20)

# optimization variables
slingshot_adjust = 0.1 # constant to make the slingshot more or less sensitive
G = 6.674 * (10 ** -5) # gravitational constant

def calcAcc(A, B): # returns acceleration of body toward attractor due to gravity
  dis = (A.pos[0]-B.pos[0], A.pos[1]-B.pos[1]) # position of A relative to B
  angle = math.atan(dis[1]/dis[0]) # angle between the objects
  force = G * ((A.mass * B.mass) / (math.hypot(dis[0], dis[1])**2)) # force of gravity between A and B

  acc = force/A.mass # calculate acceleration components

  accX = acc * math.cos(angle) * adjust(dis[0]) # get components of force
  accY = acc * abs(math.sin(angle)) * adjust(dis[1])
  return (accX, accY)

adjust = (lambda x: -1 if x > 0 else 1) # make sure negative vector components get a negative value

class Body(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self) # call sprite initializer
    self.pos = pygame.mouse.get_pos() # initialize body at cursor position
    self.radius = 20
    self.mass = self.radius * 10 ** 5
  
  def update(self, sprites):
    acc = (0,0)
    for body in [body for body in sprites if body.id != self.id]: # check all bodies except self
      acc = numpy.add(acc, calcAcc(self, body))

    self.velocity = numpy.add(self.velocity, acc)

    self.pos = numpy.add(self.pos, self.velocity)

  def change_size(self, amount):
    self.radius += amount
    self.mass = self.radius * 10 ** 5

# -------- Main Loop --------
def main():
  pygame.init()
  screen = pygame.display.set_mode((1600,1000))
  pygame.display.set_caption("Orbita")

  bodies = pygame.sprite.RenderPlain() # bodies currently in game
  clock = pygame.time.Clock()
  drawing = False

  while True:
    clock.tick(60)

    for event in pygame.event.get():
      if event.type == QUIT: sys.exit() # close game if user exits
      elif event.type == MOUSEBUTTONDOWN and event.button == 1:
        drawing = True
        newBody = Body() # create a new body at mouse position
      
      if drawing:
        if event.type == MOUSEBUTTONUP and event.button == 1: # add new body to bodies group and clean up
          bodyPos, mousePos = newBody.pos, pygame.mouse.get_pos()
          raw_dist = numpy.subtract(bodyPos, mousePos) # x and y distance components to mouse

          if math.hypot(raw_dist[0], raw_dist[1]) > 10:
            newBody.velocity = tuple(slingshot_adjust * numpy.array(raw_dist))
          else:
            newBody.velocity = (0,0) # if mouse is within a certain distance away, make body stationary

          newBody.id = len(bodies.sprites()) # give each body a unique id

          bodies.add(newBody)
          drawing = False

        elif event.type == MOUSEWHEEL:
          newBody.change_size(event.y)

    bodies.update(bodies.sprites())

    screen.fill(black)
    for body in bodies.sprites():
      pygame.draw.circle(screen, white, body.pos, body.radius, 8)
    
    if drawing:
      pygame.draw.line(screen, green, newBody.pos, pygame.mouse.get_pos(), 5) # draws slingshot
      pygame.draw.circle(screen, green, newBody.pos, newBody.radius, 8)
    pygame.display.flip()

main()
pygame.quit