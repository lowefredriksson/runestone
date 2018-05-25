import http.client
import socket
from bluetooth import *
from Tkinter import *




class GUI(Frame):

    def __init__(self,window=None):
        Frame.__init__(self, window)
        self.grid()

        self.fnameLabel = Label(window, text="First Name")
        self.fnameLabel.grid()

        self.fnameEntry = Entry(window,show=None)
        self.fnameEntry.grid()

        self.lnameLabel = Label(window, text="Last Name")
        self.lnameLabel.grid()

        self.lnameEntry = Entry(window)
        self.lnameEntry.grid()

        self.submitButton = Button(self.buttonClick,text = 'connect',width = 10,height = 2)
		self.submitButton.grid()
		
        self.submitButton.grid()


    def buttonClick(self, event):
        """ handle button click event and output text from entry area"""
        var = StringVar()
		var = e.get()
#	t.insert('insert',payload)

if __name__ == "__main__":
    guiFrame = GUI()
    guiFrame.mainloop()



window = Tk()
window.title('HTTPClient')
window.geometry('200x200')
#e = Entry(window,show=None)
#e.pack()
#var = StringVar()

#b = Button(window,text = 'connect',width = 10,height = 2, command = self.buttonClick)
#b.pack()

conn = http.client.HTTPConnection("localhost:8080")

payload = '{"temperature":"good","humidity":"bad","drop-off":"fix","carge":"yes"}'

headers = {
	'content-type': "application/json",
	}
	
#def buttonClick(self):
#	var = e.get()
#	t.insert('insert',payload)
	
t = Text(window,height=2)
t.pack()


conn.request("POST", "/robotData", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
window.mainloop()
''''
# Example of how to create the client socket and send json to the robot. 
	#((author Antti bluetooth connection
	client_socket=BluetoothSocket( RFCOMM )
	client_socket.connect(("B0:B4:48:78:4F:45", 3))
	env = conn.recv(1024)
	print "send action to robot",payload
	client_socket.send(payload)
	client_socket.close()
#getEnvorimentData()
'''

	
	
#def getEnvorimentData():
	



