import tkinter   #Used to make GUI
import threading
import imutils
import time
import cv2
from PIL import Image, ImageTk #Used to show images in Tkinter window
from functools import partial

#The Images folder must be present within the same folder as this code

stream = cv2.VideoCapture("Clip.mp4") #Captures a video file so that you can read frames from the video clip. The video file must be saved in the same folder as the code with the name "Clip.mp4"
flag = True 

def play(speed): #To play the given clip at different speeds corresponding to different play buttons as soon as those buttons are clicked
    global flag
    print(f"Playing with speed {speed}.")
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read() #"grabbed" is the boolean variable which tells whether you have taken the frame or not and "frame" is the frame you have read from the stream
    if not grabbed: #If no frame is being read from the stream
        exit()
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = ImageTk.PhotoImage(image = Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)

    #Showing the text "Decision Pending" and make it blink
    if flag:
        canvas.create_text(134, 26, fill = "black", font = "Times 26 bold", text = "Decision Pending") 
    flag = not flag

def pending(decision):

    #Displyaing the "Decision Pending" image
    frame = cv2.cvtColor(cv2.imread("Images/Pending.jpg"), cv2.COLOR_BGR2RGB) 
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT) #Resizing the image
    frame = ImageTk.PhotoImage(image = Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)
    print("Decision Pending....")

    #Waiting for 1 second
    time.sleep(1.5)

    #Display the "Sponsor" image
    frame = cv2.cvtColor(cv2.imread("Images/Sponsor.png"), cv2.COLOR_BGR2RGB) 
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT) #Resizing the image
    frame = ImageTk.PhotoImage(image = Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)  
    print("Sponsor")

    #waiting for 1.5 seconds
    time.sleep(2.5)

    #Displaying the "Out"/"Not Out" image
    if decision == "out":
        decision_img = "Images/Out.png"
    else:
        decision_img = "Images/Not Out.png"
    frame = cv2.cvtColor(cv2.imread(decision_img), cv2.COLOR_BGR2RGB) 
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT) #Resizing the image
    frame = ImageTk.PhotoImage(image = Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image = frame, anchor = tkinter.NW)
    if decision == "out":
        print("Player is out!")
    else:
        print("Player is not out!")

def out(): #To display "Out" screen after "Give Out" button is pressed
    thread = threading.Thread(target = pending, args = ("out", )) #Creating the thread in which  the "target" argument takes the function as an input which needs to be called as soon as the thread is run. If the function written after "target=" takes up an argument then then that argument is written in the "args" argument. The "args" argument takes a tuple as an input, so, if there is just one arguemt you need to pass then just keep the second entry of the tuple as empty.
    thread.daemon = 1
    thread.start()
    print("Showing...")

def not_out(): #To display "Not Out" screen after "Give Not Out" button is pressed
    thread = threading.Thread(target = pending, args = ("not out", ))
    thread.daemon = 1
    thread.start()
    print("Showing...")

#Size of our main screen
SET_WIDTH = 612 
SET_HEIGHT = 368 

#Making the window
window = tkinter.Tk()   
window.title("Prem Bhugra Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("Images/Welcome.jpg"), cv2.COLOR_BGR2RGB) #COLOR_BGR2RGB implies that we want to keep the image as it is and do not want to add it to another color space
canvas = tkinter.Canvas(window, width = SET_WIDTH, height = SET_HEIGHT) #Creating the canvas
photo = ImageTk.PhotoImage(image = Image.fromarray(cv_img)) #Adding an image to the canvas
image_on_canvas = canvas.create_image(0, 0, ancho = tkinter.NW, image = photo) #Packing this image on canvas by setting its location as (0,0)
canvas.pack()

#Creating buttons
btn = tkinter.Button(window,text = "<< Previous (fast)", width = 50, command = partial(play, -25)) #The "command" argument runs the function written after "command=" when the respective button is pressed. The function written after "command=" should not have any argument, but here our "play function" does have the "speed" argument which has different values for different buttons. To resolve this issue, we use the "partial" fucntion.
btn.pack() 
btn = tkinter.Button(window,text = "<< Previous (slow)", width = 50, command = partial(play, -2))
btn.pack() 
btn = tkinter.Button(window, text = "Next (fast) >>", width = 50, command = partial(play, 25)) 
btn.pack() 
btn = tkinter.Button(window, text = "Next (slow) >>", width = 50, command = partial(play, 2))
btn.pack() 
btn = tkinter.Button(window, text = "Give Out", width = 50, command = out)
btn.pack() 
btn = tkinter.Button(window, text = "Give Not Out", width = 50, command = not_out)
btn.pack()

window.mainloop()

"""
This Third Umpiring System allows you to perform the following functions on the video clip you want to see:
1. Play the video in forward direction quickly.
2. Play the video in forward direction slowly.
3. Play the video in backward direction quickly.
4. Play the video in forward direction slowly.
5. Give your decision on whether the player is Out or Not Out.
6. Display the name of Sponsors before giving the decision.
"""