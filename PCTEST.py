import serial,time
from random import randint
U=serial.Serial("COM12",9600)
print(U.isOpen())
def r():
    return randint(0,31)
def getkey():
    print(1)
    return bytearray([40,r(),r(),r(),r(),r(),r(),r(),41])
prev=None
delay=1/60

def Uread():
    if U.in_waiting:
        return U.read(6)
    else:
        return b''
while 1:
    data=Uread()
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
            data=Uread()
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