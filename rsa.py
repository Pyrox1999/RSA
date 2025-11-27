import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

pygame.mixer.music.load("song.mp3") #Eric Matyas
pygame.mixer.music.play(-1)

level=-1
target=""
message=""
message2=""
gemacht=False

def encode(target: str):
    global message, message2

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    message = target.encode("utf-8")

    wrapped_plain = "\n".join(target[i:i+20] for i in range(0, len(target), 20))

    message2  = "Plaintext:\n" + wrapped_plain + "\n\n"
    message2 += "Your message in Bytes:\n" + str(message) + "\n\n"

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    ciphertext_str = str(ciphertext)
    wrapped_cipher = "\n".join(ciphertext_str[i:i+50] for i in range(0, len(ciphertext_str), 50))

    message2 += "Encoded message:\n" + wrapped_cipher + "\n\n"

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def draw():
    global level, target,message,message2
    screen.clear()
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Text to encode:", center=(400, 130), fontsize=24, color=(250, 250, 255))
        screen.draw.text(target, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        screen.draw.text(str(message2), center=(400, 280), fontsize=24, color=(255, 255, 0))

def on_key_down(key, unicode=None):
    global level, target
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        target = ""
    elif key == keys.RETURN and level == 1:
        level = 2
    elif unicode and key != keys.RETURN and level==1:
        target += unicode

def update():
    global level,gemacht,target,message,message2
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    if level==0:
        target=""
        message=""
        message2=""
        gemacht=False
    if level==2:
        if not gemacht:
            encode(target)
            gemacht=True
        if keyboard.space:
            level=0

pgzrun.go()
