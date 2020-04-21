import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
window.configure(bg ="#606569 ")
window.title("ATTENDENCE MANAGEMENT SYTEM WITH FACE RECOGNITIION")
window.geometry(str(window.winfo_screenwidth())+"x"+str(window.winfo_screenheight()))

message = tk.Label(window, text="ATTENDENCE MANAGEMENT SYTEM WITH FACE RECOGNITIION",fg="white" ,bg="#606569 ",height=3,font=('times', 25))
message.pack()

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="white"  ,bg="blue",font=('times', 15, ' bold ') )
lbl.place(x=100, y=200)

txt = tk.Entry(window,width=20  ,fg="white"  ,bg="blue",font=('times', 15, ' bold '))
txt.place(x=400, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="white"  ,bg="blue",height=2 ,font=('times', 15, ' bold '))
lbl2.place(x=100, y=300)

txt2 = tk.Entry(window,width=20  ,fg="white"  ,bg="blue",font=('times', 15, ' bold ')  )
txt2.place(x=400, y=315)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="blue",height=2 ,font=('times', 15, ' bold underline '))
lbl3.place(x=100, y=400)

message = tk.Label(window, text="" ,fg="white"  ,bg="blue",width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
message.place(x=400, y=400)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="white"  ,bg="blue",height=2 ,font=('times', 15, ' bold  underline'))
lbl3.place(x=100, y=500)

message2 = tk.Label(window, text="" ,fg="white"  ,bg="blue",activeforeground = "green",width=30  ,height=8,font=('times', 15, ' bold '))
message2.place(x=400, y=500)

def show_today_attendence():
    def open_file():
        clicked_item = mylist.curselection()
        path = mylist.get(clicked_item)
        with open(path) as file:
            reader = csv.reader(file)
            for row in reader:
                open_file_label.configure(text = row)
    root = tk.Tk()
    root.configure(bg = "#606569")
    root.geometry("650x650")
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack( side = "left", fill = "y" )

    mylist = tk.Listbox(root,bg = "blue" , fg = "white" , yscrollcommand = scrollbar.set,selectmode = "extended" )
    Paths=[os.path.join("Attendance",f) for f in os.listdir("Attendance")]

    for line in Paths:
        mylist.insert("end", line)

    mylist.pack(side = "left", fill = "both" )
    scrollbar.config( command = mylist.yview )

    open_btn = tk.Button(root, text="open",bg = "blue" ,fg="white" ,command = open_file,width = 20 ,height=1 ,font=('times', 14))
    open_btn.pack()

    open_file_label = tk.Label(root, text="",justify = "center",fg = "white",bg = "blue",font=('times', 14))
    open_file_label.place(x=200, y=50)

    root.mainloop()

def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text= res)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def TakeImages():
    Id=(txt.get())
    name=(txt2.get())
    if ():
        message.configure(text = "input error")

    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                #incrementing sample number
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #Write the count of the images
                cv2.putText(img,str(sampleNum),(10,100),1,3,(0,255,0),2)
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds
            if (cv2.waitKey(100) & 0xFF == ord('q')):
                break
            # break if the sample number is morethan 100
            elif sampleNum>200:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        if os.path.exists("StudentDetails/StudentDetails.csv"):
            with open('StudentDetails/StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
        else:
             with open('StudentDetails/StudentDetails.csv', 'w', newline='') as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC,delimiter=';', quotechar='*')
                    writer.writerow(["Id","Name"])
                    writer.writerow(row)
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)

def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Image Trained"+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    Ids=[]

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    df=pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    while True:
        ret, im =cam.read()
        im = cv2.flip(im,1)
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf > 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+" "+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
            else:
                Id='Unknown'
                tt=str(Id)
            if(conf < 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
            cv2.putText(im,str(tt),(x,y+h), font, 1,(0,255,0),1)
            cv2.putText(im,"confidence:"+str(int(conf))+"%",(x,y+h+30), font,1,(0,255,255),1)
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')

        cv2.imshow('im',im)
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second = timeStamp.split(":")
    fileName="Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text= res)

clearButton = tk.Button(window, text="Clear", command=clear  ,fg="white"  ,bg="blue",width = 20 ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=650, y=200)

clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="white"  ,bg="blue" ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=650, y=300)

takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue" ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=950, y=200)

trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="blue"  ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=950, y=250)

trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="white"  ,bg="blue"  ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=950, y=300)

show_attendence = tk.Button(window, text="Today's Attendance", command=show_today_attendence  ,fg="white"  ,bg="blue"  ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
show_attendence.place(x=950, y=350)

quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="blue"  ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=950, y=400)

copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Abdullah")
copyWrite.configure(state="disabled"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=600)

window.mainloop()