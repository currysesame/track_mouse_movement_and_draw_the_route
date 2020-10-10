
import win32api
from time import sleep

text_file = open("mouse_move.txt", "w")

savedpos = win32api.GetCursorPos()
count = 0
while(True):

    curpos = win32api.GetCursorPos()
    text_file.write(str(curpos[0]) + ' ' + str(curpos[1]) + ' \n')
    sleep(0.02)
    count += 1
    if(count == 300):
    	break

text_file.close()


