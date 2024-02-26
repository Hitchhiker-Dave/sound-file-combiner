#Mostly Abandoned Reference Code: https://www.scivision.dev/playing-sounds-from-numpy-arrays-in-python/
#Pygame Reference Doc (sound array): https://www.pygame.org/docs/ref/sndarray.html?highlight=sound%20array
#Pygame Reference Doc (mixer): https://www.pygame.org/docs/ref/mixer.html
#was trying to merge two songs bit by bit using logical commands like AND, OR, XOR
import pygame
import random
import math
from time import sleep

fs = 16000 # Hz, affects audio quality somewhat and sound durration calculations; also the bigger it is the longer it takes to sort through the array

pygame.mixer.pre_init(fs, size=-16, channels=1) #not sure what size effects
pygame.mixer.init()

effect1 = pygame.mixer.Sound("binary babble (modulated).wav")
effect2 = pygame.mixer.Sound("Brown Noise for 2 Minutes.wav")
effect3 = pygame.mixer.Sound("heartbeats-61(new).wav")
effect4 = pygame.mixer.Sound("droning_of_the_damned.wav")

effect_digitized1 = pygame.sndarray.array(effect1) #turn sound file into a valid pygame sound array
effect_digitized2 = pygame.sndarray.array(effect2) #turn sound file into a valid pygame sound array
effect_digitized3 = pygame.sndarray.array(effect2) #turn sound file into a valid pygame sound array
effect_digitized4 = pygame.sndarray.array(effect3) #turn sound file into a valid pygame sound array
effect_digitized5 = pygame.sndarray.array(effect4) #turn sound file into a valid pygame sound array
new_digitized_effect = None
#once the effect is digitized I can start messing around with the arrays``

array_length = 0 #only update array up to the smallest sound file's index
if len(effect_digitized1) <= len(effect_digitized2):
    new_digitized_effect = effect_digitized1
else:
    new_digitized_effect = effect_digitized2

array_length = len(new_digitized_effect)

#Effect distortion goes here; never multiply the value by more then one to prevent hearing damage; maybe multiply the result by 0.x for safety
print("Compiling Song")
for i in range(array_length):
    sound_progress = i/array_length
    lerp_progress = math.sqrt(sound_progress)
    log_progress = math.log2(math.pow(sound_progress, 11) + 1)
    main_degridation = 1 / (math.pow(sound_progress, 4) + 1)
    modulation = random.random() * random.randint(-1,1)

    #main part- combine the brown static and binary babble for a general unease + (effect_digitized2[i][0] + effect_digitized2[i][1] * sound_progress * 0.9))
    main = ((effect_digitized1[i][0] + effect_digitized1[i][1] + effect_digitized2[i][0] + effect_digitized2[i][1]) * 0.75 ) * ((main_degridation) + ( modulation * (log_progress)) )*0.75
    new_digitized_effect[i][0] = main * 0.5
    new_digitized_effect[i][1] = main * 0.5

    #gradual bass static distortion
    bass = ( (new_digitized_effect[i][0] + new_digitized_effect[i][1]) * (effect_digitized3[i][0] + effect_digitized3[i][1]) * (modulation) * (sound_progress *0.75) ) * 0.5

    new_digitized_effect[i][0] += bass * 0.6
    new_digitized_effect[i][1] += bass * 0.6

    #Heartbeat
    heartbeat = ((effect_digitized4[i][0] + effect_digitized4[i][1]) * (modulation) * (lerp_progress)) 

    new_digitized_effect[i][0] += heartbeat *0.75
    new_digitized_effect[i][1] += heartbeat *0.75
    
    #deep gradual background scream/droning
    #drone = (((effect_digitized4[i][0] + effect_digitized4[i][1]) * 0.5) * (lerp_progress * 0.75))
    new_digitized_effect[i][0] += (effect_digitized5[i][0] * (1 + (modulation / 10))) * (lerp_progress) * 0.5
    new_digitized_effect[i][1] += (effect_digitized5[i][1] * (1 + (modulation / 10))) * (lerp_progress) * 0.5


song_length = (len(effect_digitized1)) / fs #divide the length of the array by the frequency to always get the correct length

sound = pygame.sndarray.make_sound(new_digitized_effect) #use sound array to play a sound

print("Song Compiled")

sound.play()

sleep(song_length) # NOTE: Since sound playback is async, allow sound playback to start before Python exits
print("end")