import pyaudio
import numpy as np
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

maxValue = 2**16
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=2,rate=48000,
              input=True, frames_per_buffer=1024)
last_grab=time.time()-.75
audioTotalL = 0
audioTotalR = 0
cutDirection = 1
playTime=time.time()-10
play = False

# print(__name__)

# def main():
#     time.sleep(5)
#     keyboard.press(Key.space)
#     keyboard.release(Key.space)
#     print('press space bar')
#
# if __name__ == '__main__':
#     main()

def pressPlay():
    global play
    print('from press play')
    play = True
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    keyboard.press('l')
    keyboard.release('l')

def cut(direction):
    global cutDirection
    if direction == 1:
        if direction != cutDirection:
            print('from inside 1 Left')
            keyboard.press('%s' % direction)
            keyboard.release('%s' % direction)
            cutDirection = direction
    else:
        if direction != cutDirection:
            keyboard.press('%s' % direction)
            keyboard.release('%s' % direction)
            print('from inside 2 Right')
            cutDirection = direction

while True:
    data = np.fromstring(stream.read(1024 ,exception_on_overflow = False),dtype=np.int16)
    dataL = data[0::2]
    dataR = data[1::2]
    peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
    peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue
    audioTotalL += peakL
    audioTotalR += peakR
    if time.time()-playTime > 10 and play == False:
        print('hello world')
        playTime=time.time()
        pressPlay()
    if time.time()-last_grab > .75:
        last_grab=time.time()
        if audioTotalL > audioTotalR:
            cut(1)
        elif audioTotalL < audioTotalR:
            cut(2)
        audioTotalL = 0
        audioTotalR = 0
    else:
        continue
