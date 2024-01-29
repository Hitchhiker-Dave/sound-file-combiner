#Mostly Abandoned Reference Code: https://www.scivision.dev/playing-sounds-from-numpy-arrays-in-python/
#Pygame Reference Doc (sound array): https://www.pygame.org/docs/ref/sndarray.html?highlight=sound%20array
#Pygame Reference Doc (mixer): https://www.pygame.org/docs/ref/mixer.html
#was trying to merge two songs bit by bit using logical commands like AND, OR, XOR
import pygame
import random
from time import sleep

fs = 8000 # Hz, affects audio quality somewhat

pygame.mixer.pre_init(fs, size=-16, channels=1) #not sure what size effects
pygame.mixer.init()

effect = pygame.mixer.Sound("guitar rift 1.wav")
effect_digitized = pygame.sndarray.array(effect) #turn sound file into a valid pygame sound array
#once the effect is digitized I can start messing around with the arrays

#Effect distortion goes here
'''for i in range(len(effect_digitized)):
    effect_digitized[i] = effect_digitized[i] * random.uniform(-1, 1)'''

print(len(effect_digitized))
song_length = (len(effect_digitized)) / 10000 # Figure out how to find song length, either that or have a way to detect the way the song is playing and 
                                                #have the program sleep until the song is over

sound = pygame.sndarray.make_sound(effect_digitized) #use sound array to play a sound

sound.play()

sleep(song_length) # NOTE: Since sound playback is async, allow sound playback to start before Python exits