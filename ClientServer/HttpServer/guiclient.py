import http.client
import socket
from bluetooth import *

import tkinter as tk


#connection 


conn = http.client.HTTPConnection("localhost:8080")

payload = '{"temperature":"good","humidity":"bad","drop-off":"fix","carge":"yes"}'

headers = {
	'content-type': "application/json",
	}

#GUI
window = tk.Tk()
window.title('my window')
window.geometry('200x100')

var = tk.StringVar()
var2 = tk.StringVar()
e = tk.Entry(window,show=None)
e.pack()
l = tk.Label(window, textvariable=var, bg='gray', font=('Arial', 12), width=50,
             height=2)
#l = tk.Label(window, text='OMG! this is TK!', bg='green', font=('Arial', 12), width=15, height=2)
l.pack()

l2 = tk.Label(window, textvariable=var2, bg='white', font=('Arial', 12), width=50,
             height=2)
l2.pack()

on_hit = False
def hit_me():
	global on_hit
	if on_hit == False:
		on_hit = True
		payload = e.get()
		conn.request("POST", "/robotData", payload, headers)
		var.set("The request have send to server : "+payload)
		res = conn.getresponse()
		data = res.read()
		var2.set(data)
	else:
		on_hit = False
		var.set('')

b = tk.Button(window, text='hit me', width=15,
              height=2, command=hit_me)
b.pack()


window.mainloop()
