import mpr121,time
from machine import I2C,Pin,UART
from random import randint
A=I2C(1,scl=Pin(12),sda=Pin(13))
try:
    B=mpr121.MPR121(A)
    B.set_thresholds(1,1,0)
except:
    pass
'''
while 1:
    time.sleep(.05)
    r=str(bin(B.touched()))[2:]
    r=r.replace('0','  ')
    r=r.replace('1','##')
    print("|{:>24}|".format(r))
'''
delay=1/30
def r():
    return randint(0,31)
U=UART(1,9600)#TX10 RX9
print(U)
halt=0
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
        while 1:
            data=U.read()
            if data==b'{HALT}':
                halt=1
                print('HALT')
                break
            elif data:
                print('received:',data)
            U.write(bytearray([40,r(),r(),r(),r(),r(),r(),r(),41]))
            time.sleep(delay)
    elif data:
        datac=bytearray(data)
        datac[0]=40
        datac[-1]=41
        U.write(datac)
        print('UNKNOWN CMD:',data,'try response:',datac)
        
    