#!/usr/bin/env python

import threading
import time
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer

from arduino import Arduino


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




FILE = 'index.html'
PORT = 8080

global ard
ard = Arduino()
try:
    ard.configure_serial('/dev/tty.usbmodem1451')
except:
    print "Serial port configuration failed, moving ahead"
ard.start()

global d
d = 0;

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        global d

        """Handle a post request by returning the square of the number."""
        # poll arduino here
        #length = int(self.headers.getheader('content-length'))        
        #data_string = self.rfile.read(length)
        
        try:
            #result = int(data_string) ** 2
            packet = ard.get_packet()
        except:
            packet = (512,512,1,0)
        
        # result = "0,0"
        print packet;
        g_keys = pygame.event.get()

        d = 0;

        #for i in range(0, my_joystick.get_numbuttons()):
        #  if (my_joystick.get_button(i)):
        #    if(i==3):
        #      d = 1;
        #    if(i==1):
        #      d = -1;
        
        for i in range(0, my_joystick.get_numaxes()):
                if (my_joystick.get_axis(i)):
                  if(i==3):
                    d = -my_joystick.get_axis(i);

        packet = (512, 512 + (d*512), packet[2], packet[3]);
        #print(packet, d, "analog")

        result = "%i,%i,%i,%i" % (packet)  
        self.wfile.write(result)


def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    try:
        open_browser()
        start_server()
    except:
        ard.keepAlive = False
        ard.join()