from sys import exit
from logging import warning
from functools import partial
from signal import SIGINT, signal

def keyboardinterrupt_handler(camera):
    sigint_handler_partial = partial(sigint_handler, camera=camera) #use partial to give the camera argument to sigint_handler before running the signal function
    signal(SIGINT, sigint_handler_partial)

def sigint_handler(signal, stack_frame, camera): #the KeyboardInterrupt handler
    camera.close()
    warning('KeyboardInterrupt has been handled')
    exit()