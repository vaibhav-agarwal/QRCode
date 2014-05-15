from Tkinter import *
import qrcode
import MySQLdb
import encoding as en
import decoding as de

db = MySQLdb.connect("localhost","root","test123","crypto" )
cursor = db.cursor()
#CREATE TABLE account(id int PRIMARY KEY , name VARCHAR(200) , balance VARCHAR(200));

def account():
    global root1,e
    root.destroy()
    root1=Tk()
    root1.resizable(width=FALSE, height=FALSE)
    frame = Frame(root1,width=300, height=200, bg="", colormap="new")
    w=Label(root1,text="Accounts")
    e = Entry(frame) 
    e.place(relx=.3 , rely=.2)
    m1 = Message(frame , text= "Enter the name",width=120)
    b1 = Button(frame, text="Search",height=2,width=15,command=searchname)
    b2 = Button(frame, text="Previous",height=2,width=15,command=restoremain)

    b1.place(relx=.3 , rely=.4)
    b2.place(relx=.3 , rely=.7)
    m1.place(relx=.35 , rely=.05)
    w.pack()  
    frame.pack()
    root1.mainloop()

def searchname():
    global root1,root2,e,top
    name=e.get()
    cursor.execute("SELECT * from account where name='"+str(name)+"';");
    b=cursor.fetchall()
    db.commit()
    if len(name)!=0 and len(b)>0:
        root1.destroy()
        root2=Tk()
        root2.resizable(width=FALSE, height=FALSE)
        frame = Frame(root2,width=300, height=200, bg="", colormap="new")
        w=Label(root2,text="Account Detail")
        m1 = Message(frame , text= "Name :",width=120)
        m2 = Message(frame , text= "Available Balance :",width=120)
        m3 = Message(frame , text=b[0][1],width=120)
        m4 = Message(frame , text=str(b[0][2]),width=120)
        
        m1.place(relx=.1 , rely=.05)
        m2.place(relx=.1 , rely=.3)
        m3.place(relx=.3 , rely=.05)
        m4.place(relx=.5 , rely=.3)
 
          
        b1 = Button(frame, text="Main Menu",height=2,width=15,command=restoremain)
        b1.place(relx=.3 , rely=.7)
        w.pack()  
        frame.pack()
        root2.mainloop()
    else:
        root1.withdraw()
        top = Toplevel()
        top.title("Message")
        msg = Message(top, text="Invalid Name" )
        msg.pack()
        button = Button(top, text="Dismiss", command=restore)
        button.pack()


def takeorder():
    global root,root3,quantity,menu
    root.destroy()
    root3=Tk()
    root3.resizable(width=FALSE, height=FALSE)
    frame = Frame(root3,width=300, height=450, bg="", colormap="new")
    w=Label(root3,text="Take Order")
    w.pack()
    menu={'Samosa___Rs.10':[0,10] ,'Sandwich___Rs.20':[0,20] , 'Tea___Rs.12':[0,12] ,'Burger___Rs.30':[0,30] , 'Patty___Rs.12':[0,12] , 'Coffee___Rs.18':[0,18] ,'Colddrink___Rs.30':[0,30]}
    quantity=[]
    count=0.12
    w1=Label(root3,text="Quantity")
    for i in menu:
        menu[i][0] = Variable()
        c = Checkbutton(root3, text=i, variable=menu[i][0])
        c.deselect()
        c.place(relx=0.1,rely=count+0.1)
        e=Entry(root3,width=3)
        e.insert(0,0)
        quantity.append(e)
        e.place(relx=0.6,rely=count+0.11)
        count+=0.1
    w1.place(relx=0.55,rely=0.1)
    b1 = Button(frame, text="Submit",height=2,width=15,command=submitchoice)
    b1.place(relx=.55 , rely=.9)
    b2 = Button(frame, text="Previous",height=2,width=15,command=restoremain)
    b2.place(relx=.1 , rely=.9)
    frame.pack()
    root3.mainloop()

def submitchoice():
    global quantity,menu,root3,root4,e,amount
    conforder=''
    count=0
    amount=0
    sno=1
    for i in menu:
        if menu[i][0].get()=='1':
            q=quantity[count].get()
            if int(q)>0:
                conforder+=str(sno)+'. '+i+"-----"+str(int(q)*menu[i][1])+'\n\n'
                amount+=int(q)*menu[i][1]
                sno+=1
        count+=1        
    root3.destroy()
    root4=Tk()
    root4.resizable(width=FALSE, height=FALSE)
    frame = Frame(root4,width=300, height=500, bg="", colormap="new")
    w=Label(root4,text="Confirm Order")
    w.pack()
    conforder+='\n\nTotal Amount :-----'+str(amount)
    m1 = Message(frame ,text=conforder,width=150)
    m1.place(relx=.1,rely=.1)
    m2 = Message(frame ,text='Enter Customer Name' ,width=150)
    m2.place(relx=.1,rely=.7)
    e=Entry(root4)
    e.place(relx=.1,rely=.8)
    b1 = Button(frame, text="Submit",height=2,width=15,command=makepayment)
    b1.place(relx=.55 , rely=.9)
    b2 = Button(frame, text="Previous",height=2,width=15,command=restoremain)
    b2.place(relx=.1 , rely=.9)
    
    frame.pack()
    root4.mainloop()           

def makepayment():
    global root4,e,amount,root5,top
    name=e.get()
    cursor.execute("SELECT * from account where name='"+str(name)+"';");
    b=cursor.fetchall()
    db.commit()
    if len(b)>0:
        pos=en.qrencode(name+str(amount)) 
        if pos!=1:
            text1='Your Transaction was not Successful!'
        else:
            pos=de.qrdecode()
            if pos!=1:
                  text1='Your Transaction was not Successful!'
            else:
                 balance=int(b[0][2])-amount 
                 cursor.execute("UPDATE account SET balance= "+str(balance)+" where name='"+name+"';")
                 db.commit() 
                 text1='Your Transaction was Successful !'
                 
        root4.destroy()
        root5=Tk()
        root5.resizable(width=FALSE, height=FALSE)
        frame = Frame(root5,width=200, height=200, bg="", colormap="new")
        msg = Message(frame, text=text1,width=150) 
        msg.place(relx=.1 , rely=.1)
        button = Button(frame, text="Close this box for Security", command=restoremain)
        button.place(relx=.1 , rely=.4)
        frame.pack()
        root5.mainloop()
    else:
        root4.withdraw()
        top = Toplevel()
        top.title("Message")
        msg = Message(top, text="Invalid Name" )
        msg.pack()
        button = Button(top, text="Dismiss", command=restore)
        button.pack()
        
def restore():
    global root1,root4,top
    top.destroy()
    try:
      root1.deiconify()
    except:
       root4.deiconify() 
def restoremain():
    global root2,root1,root3,root4,root5
    try:
        root5.destroy()
    except:
        try:
            root4.destroy()
        except:
            try:
                root3.destroy()
            except:
                try:
                    root2.destroy()
                except:
                    root1.destroy()
    mainmenu()
    
    
def cafeexit():
    global root
    root.destroy()


def mainmenu():
    global root
    root=Tk()
    root.resizable(width=FALSE, height=FALSE)
    frame = Frame(root,width=300, height=200, bg="", colormap="new")
    w=Label(root,text="JIIT Ca'fe Counter")
    b1 = Button(frame, text="Manage Accounts",height=2,width=15,command=account)
    b2 = Button(frame, text="Take Order",height=2,width=15,command=takeorder)
    b3 = Button(frame, text="Exit",height=2,width=15,command=cafeexit)
    w.pack()
    b1.place(relx=.1 , rely=.2)
    b2.place(relx=.55 , rely=.2)
    b3.place(relx=.3 , rely=.5)
    frame.pack()
    root.mainloop()

mainmenu()
db.close()
