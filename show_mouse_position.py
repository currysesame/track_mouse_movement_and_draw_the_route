
import cv2 
import numpy as np
import copy
# read position and gyro

def draw_line_forward(blank_image0, x1, y1, x2, y2):
	cv2.line(blank_image0, (x1, y1), (x2, y2), (255, 0, 0), thickness=line_thickness)
	
def draw_line_backward(blank_image0, x1, y1, x2, y2):
	cv2.line(blank_image0, (x1, y1), (x2, y2), (80, 80, 80), thickness=line_thickness)


file = 'mouse_move.txt'
height = 300
width = 300
blank_image = np.zeros((height,width,3), np.uint8)
blank_image += 128
center_posi_x = 150
center_posi_y = 150
line_thickness = 3


diff_set_x = []
diff_set_y = []

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 25.0
out = cv2.VideoWriter('output.avi',fourcc, fps, (width, height))

with open(file, 'r') as f:
	content_list = f.read().splitlines()
	for i in range(len(content_list) - 1):
		x2 = content_list[i+1].split()[0]
		y2 = content_list[i+1].split()[1]
		x1 = content_list[i].split()[0]
		y1 = content_list[i].split()[1]

		diff_x = int(x2) - int(x1)
		diff_y = int(y2) - int(y1)
		diff_set_x.append(diff_x)
		diff_set_y.append(diff_y)

for i in range(len(diff_set_x)):
	blank_image0 = copy.copy(blank_image)
	x1 = center_posi_x
	y1 = center_posi_y
	
	# backward part

	if(i>0):
		x1 = center_posi_x
		y1 = center_posi_y
		x2 = x1 - diff_set_x[i-1]
		y2 = y1 - diff_set_y[i-1]
		draw_line_backward(blank_image0, x1, y1, x2, y2)

	for j in range(20):
		x1 = x2
		y1 = y2
		if(i-1-j>0):
			x2 = x1 - diff_set_x[i-2-j]
			y2 = y1 - diff_set_y[i-2-j]
			draw_line_backward(blank_image0, x1, y1, x2, y2)

	# forward part
	x1 = center_posi_x
	y1 = center_posi_y
	x2 = diff_set_x[i] + center_posi_x
	y2 = diff_set_y[i] + center_posi_y

	draw_line_forward(blank_image0, x1, y1, x2, y2)

	for j in range(20):
		x1 = x2
		y1 = y2
		if(i+1 + j<len(diff_set_x)):
			x2 = x1 + diff_set_x[i+1 + j]
			y2 = y1 + diff_set_y[i+1 + j]
			draw_line_forward(blank_image0, x1, y1, x2, y2)


	# object position

	cv2.circle(blank_image0,(center_posi_x, center_posi_y), 7, (80,127,255), -1)
	
	for j in range(1,7):
		vec_x = int(3*j*diff_set_x[i]/np.sqrt(diff_set_x[i]**2 + diff_set_y[i]**2 + 1e-6))
		vec_y = int(3*j*diff_set_y[i]/np.sqrt(diff_set_x[i]**2 + diff_set_y[i]**2 + 1e-6))
		arraw_x = vec_x + center_posi_x
		arraw_y = vec_y + center_posi_y

		cv2.circle(blank_image0,(arraw_x, arraw_y), 7-j, (80,127,255), -1)

	cv2.circle(blank_image0,(center_posi_x, center_posi_y), 3, (255,255,255), -1)
	
	for j in range(1,3):
		vec_x = int(3*j*diff_set_x[i]/np.sqrt(diff_set_x[i]**2 + diff_set_y[i]**2 + 1e-6))
		vec_y = int(3*j*diff_set_y[i]/np.sqrt(diff_set_x[i]**2 + diff_set_y[i]**2 + 1e-6))
		arraw_x = vec_x + center_posi_x
		arraw_y = vec_y + center_posi_y

		cv2.circle(blank_image0,(arraw_x, arraw_y), 3-j, (255,255,255), -1)

	# cv2.imshow('sss', blank_image0)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	out.write(blank_image0)


# Release everything if job is finished
out.release()
cv2.destroyAllWindows()


