
import pygame
from pygame.locals import *

pygame.init()
pygame.joystick.init()

my_joystick = None
joystick_names = []

        # Enumerate joysticks
for i in range(0, pygame.joystick.get_count()):
  joystick_names.append(pygame.joystick.Joystick(i).get_name())
  print joystick_names

if (len(joystick_names) > 0):
  my_joystick = pygame.joystick.Joystick(0)
  my_joystick.init()

max_joy = max(my_joystick.get_numaxes(), 
                      my_joystick.get_numbuttons(), 
                      my_joystick.get_numhats())

print(max_joy);
def check_button(self, p_button):
  if (self.my_joystick):
    if (p_button < self.my_joystick.get_numbuttons()):
      return self.my_joystick.get_button(p_button)
  return False

while (True):
  g_keys = pygame.event.get()

  for i in range(0, my_joystick.get_numbuttons()):
    if (my_joystick.get_button(i)):
      print(i, "True", "\n");                
    #else:
      #print(i, "False", "\n");
