import tkinter as tk
import pickle as pkl
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def get_model():
	pickle_in = open("model_pickled.pickle", "rb")
	model = pkl.load(pickle_in)
	return model

my_model = get_model()

window = tk.Tk()
window.title("0,1,2 reader")
window.geometry("200x200")
pixels = 50

pixel_list = np.zeros([pixels, pixels])

def paint(event):
   python_green = "#476042"
   if(event.x in range(0, pixels) and event.y in range(0, pixels)):
	   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
	   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
	   canvas.create_oval( x1, y1, x2, y2, fill = python_green )
	   pixel_list[event.y][event.x] = 1

def clear_board():
	canvas.delete("all")
	for i in range(0, pixels):
		pixel_list[i].fill(0)
	pred_label.config(text="")

def print_list(event):
	print(pixel_list)

def predict():
	flattened = np.ravel(pixel_list)
	branched = flattened.reshape((1,pixels*pixels))
	x = pd.DataFrame(branched)
	prediction = my_model.predict(x)[0]
	pred_label.config(text="I see a {}".format(int(prediction)))


canvas = tk.Canvas(window, 
	bg="white", 
	width=pixels, 
	height=pixels)

canvas.pack()
canvas.bind("<B1-Motion>", paint)

pred_button = tk.Button(window, text="read", command=predict)
pred_button.pack()

pred_label = tk.Label(window, text="")
pred_label.pack()

reset_button = tk.Button(window, text="reset", command = clear_board)
reset_button.pack()

window.bind("<Button-3>", print_list)

tk.mainloop()