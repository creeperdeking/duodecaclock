import pygame
import time
from datetime import datetime
import math


class ClocDuodeca:
  

  def __init__(self):
    pygame.init()

    self.angleSmallClockHand = 0
    self.angleBigClockHand = 0

    self.positionBigClockHand = (0,0)
    self.positionSmallClockHand = (0,0)

    self.display_width = 600
    self.display_height = 600

    self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height), pygame.RESIZABLE)

    pygame.display.set_caption('Horloge Dudécamétrique')

    self.black = (0,0,0)
    self.background_color = (100,100,100)

    self.clock = pygame.time.Clock()
    self.crashed = False
    self.clockImg = pygame.image.load('data/fond_horloge.png')
    self.smallWatchHand = pygame.image.load('data/petite_aiguille.png')
    self.bigWatchHand = pygame.image.load('data/grande_aiguille.png')
    

    self.resizedClockImg = self.clockImg
    self.resizedSmallWatchHand = self.smallWatchHand
    self.resizedBigWatchHand = self.bigWatchHand
    self.rotatedClockImg = self.clockImg
    self.rotatedSmallWatchHand = self.smallWatchHand
    self.rotatedBigWatchHand = self.bigWatchHand
    self.updateImagesTransform()
    self.updateImagesSize()

    self.loop()


  def rot_center(self, image, angle):
      center = image.get_rect().center
      rotated_image = pygame.transform.rotate(image, angle)
      new_rect = rotated_image.get_rect(center = center)

      return rotated_image, new_rect
  

  def updateImagesSize(self):
      self.resizedClockImg = pygame.transform.smoothscale(self.clockImg, (self.display_width, self.display_width))
      self.resizedSmallWatchHand = pygame.transform.smoothscale(self.smallWatchHand, (self.display_width, self.display_width))

      self.resizedBigWatchHand = pygame.transform.smoothscale(self.bigWatchHand, (self.display_width, self.display_width))


  def updateImagesTransform(self):
      self.rotatedClockImg = self.resizedClockImg
      self.rotatedSmallWatchHand, self.positionSmallClockHand = self.rot_center(self.resizedSmallWatchHand, self.angleSmallClockHand - 90)

      self.rotatedBigWatchHand, self.positionBigClockHand = self.rot_center(self.resizedBigWatchHand, self.angleBigClockHand - 180)
  

  def updateClockHandsHandles(self):
      now = datetime.now()
      seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

      increment = 12
      tierceSinceMidnight = math.floor(seconds_since_midnight * (6./25.)*increment)/increment
      nbTiercesJour = 12**4
      nbTiercesHeure = 12**2
      self.angleBigClockHand = tierceSinceMidnight / nbTiercesJour * 360

      self.angleSmallClockHand = (tierceSinceMidnight / nbTiercesHeure * 360)
      

  def loop(self):
    crashed = False
    while not crashed:
        self.updateClockHandsHandles()
        self.updateImagesTransform()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.VIDEORESIZE:
                self.display_width = event.w
                self.display_height = event.h
                self.updateImagesSize()

        self.gameDisplay.fill(self.background_color)
        self.gameDisplay.blit(self.rotatedClockImg, (0,0))
        self.gameDisplay.blit(self.rotatedBigWatchHand, self.positionBigClockHand)
        self.gameDisplay.blit(self.rotatedSmallWatchHand, self.positionSmallClockHand)
        

        pygame.display.update()
        self.clock.tick(60)
        time.sleep(0.05)
    
    pygame.quit()


clockApp = ClocDuodeca()

