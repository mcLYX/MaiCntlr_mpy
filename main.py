import mpr121,time,sys,micropython
from machine import I2C,Pin,UART
from random import randint
A=I2C(0,scl=Pin(5),sda=Pin(4))#SCL5 SDA4 FOR 32C3
B=mpr121.MPR121(A)

B.set_thresholds(7,0)
'''
B.set_thresholds(4,0,7)
B.set_thresholds(4,0,0)
B.set_thresholds(4,0,1)
B.set_thresholds(4,0,2)
'''
masks=[bytearray([0b00000000,0b00001100,0b00000001,0b00010010,0b00000000,0b00010000,0b00000010][::-1]),
       bytearray([0b00000000,0b00011000,0b00000011,0b00000010,0b00000001,0b00000000,0b00000100][::-1]),
       bytearray([0b00000001,0b00010000,0b00000110,0b00000010,0b00000010,0b00000000,0b00001000][::-1]),
       bytearray([0b00000011,0b00000000,0b00001100,0b00000100,0b00000100,0b00000000,0b00010000][::-1]),
       bytearray([0b00000110,0b00000000,0b00011000,0b00000100,0b00001000,0b00000001,0b00000000][::-1]),
       bytearray([0b00001100,0b00000001,0b00010000,0b00000100,0b00010000,0b00000010,0b00000000][::-1]),
       bytearray([0b00001000,0b00000010,0b00000000,0b00001101,0b00000000,0b00000100,0b00000000][::-1]),
       bytearray([0b00000000,0b00000110,0b00000000,0b00011010,0b00000000,0b00001000,0b00000001][::-1])]

delay=1/60
def r():
    return randint(0,31)

def getkey():
    r=B.touched()
    keydata=bytearray(9)
    for i in range(8):
        if r%2:
            for j in range(7):
                keydata[j+1]|=masks[-i-1][j]
        r>>=1
    keydata[0]=40
    keydata[-1]=41
    return keydata

c=Pin(2,Pin.PULL_DOWN)#按下Pin2则直连
if c.value():
    #print('ENTER DIRECT MODE!')
    print=lambda x:None
    Pin(12,Pin.PULL_UP).on()
    Pin(13,Pin.PULL_UP).on()
    micropython.kbd_intr(-1)
    #UART(0,9600)
    
    class U:
        def __init__():
            pass
        def read():
            return sys.stdin.buffer.read()
        def write(buf):
            sys.stdout.buffer.write(buf)
else:
    print('ENTER DETACHED MODE!')
    U=UART(1,9600,tx=8,rx=9)
print('test')
halt=0
prev=0
while 1:
    data=U.read()
    if data==b'{RSET}':
        halt=0
        print('RESET')
    elif data==b'{HALT}':
        halt=1
        print('HALT')
    elif data==b'{STAT}':
        halt=0
        print('TOUCH START')
        U.write(getkey())
        while 1:
            data=U.read()
            if data==b'{HALT}':
                halt=1
                print('HALT')
                break
            elif data:
                print('received:',data)
            now=getkey()
            if now!=prev:
                U.write(now)
                prev=now
                print(now)
                time.sleep(delay)
                U.write(now)
            time.sleep(delay)
    elif data:
        datac=bytearray(data)
        datac[0]=40
        datac[-1]=41
        U.write(datac)
        print('UNKNOWN CMD:',data,'try response:',datac)
        
    