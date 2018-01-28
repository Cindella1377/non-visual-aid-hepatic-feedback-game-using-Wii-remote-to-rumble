import cwiid
from datetime import datetime
from datetime import timedelta
import random
import time

print 'Press 1 + 2 on ze Wiimote now...'
wm = None
i = 2
while not wm:
    try:
        wm = cwiid.Wiimote()
    except:
        if (i > 10):
            quit()
            break
        print 'Error opening Wiimote connection!'
        print 'attempt ' + str(i)
        i += 1

wm.rpt_mode = cwiid.RPT_BTN
print(wm.state)

for i in range(8):
    wm.led = i
    if i % 2:
        wm.rumble = False
    else:
        wm.rumble = True
    time.sleep(0.01)
wm.rumble = False

print('Press the \"B\" button when you feel a rumble.\nReady, set, RUMBLE!')

def the_rumble():
    interval_to_start = random.uniform(3,10)
    time.sleep(interval_to_start)
    print('interval_to_start: ' + str(interval_to_start))
    wm.led = 1
    wm.rumble = 1
    t0 = datetime.now()
    time.sleep(0.1)
    wm.rumble = 0
    print('t0: ' + str(t0))
    return t0

def millis(dt0, dt1):
    dt = dt1 - dt0
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

def main():
    t0 = the_rumble()
    print('t0 in \'main\': ' + str(t0))
    lost = None
    while lost == None:
        if (wm.state['buttons'] & cwiid.BTN_B):
            print 'Button B pressed'
            t1 = datetime.now()
            print('t1: ' + str(t1))
            print('t0: ' + str(t0))
            if (millis(t0, t1) < 500):
                print 'Good job!'
                main()
            else:
                print '************ Game over! ***********'
                lost = True
                quit()
                break

main()
