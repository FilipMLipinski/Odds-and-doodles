import tkinter as tk
import numpy as np

f = open("zeros_ones_twos.txt", "w")

window = tk.Tk()

pixels = 50

pixel_list = np.zeros([pixels, pixels])
count = 0

def paint(event):
   python_green = "#476042"
   if(event.x in range(0, pixels) and event.y in range(0, pixels)):
	   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
	   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
	   canvas.create_oval( x1, y1, x2, y2, fill = python_green )
	   pixel_list[event.y][event.x] = 1

def clear_board(event):
	if(event.char == 'q'):
		f.close()
		window.destroy()
	else:
		canvas.delete("all")
		save_image(event.char)
		for i in range(0, pixels):
			pixel_list[i].fill(0)

def save_image(k):
	if(k in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
		iterator = pixel_list.flat
		for val in iterator:
			f.write("{},".format(val))
		f.write("{}\n".format(k))
		global count
		count+=1
		print("{} was added, count = {}".format(k, count))

	else:
		print("not an integer")

def print_list(event):
	print(pixel_list)


canvas = tk.Canvas(window, 
	bg="white", 
	width=pixels, 
	height=pixels)

canvas.pack()
canvas.bind("<B1-Motion>", paint)

window.bind("<Key>", clear_board)
window.bind("<Button-3>", print_list)

tk.mainloop()