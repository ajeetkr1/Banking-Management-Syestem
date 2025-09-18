from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
from Captcha_test import generate_captcha
from PIL import Image,ImageTk
import time,random
from table_creation import generate
from email_test import sendopen_acnmsg,otp_pswd
import sqlite3
from tkinter import ttk
import re
generate()
def show_date_time():
    dt=time.strftime('%A %d-%b-%Y %r')
    date_time_label.configure(text=dt,bg='#1ddb80')
    date_time_label.after(1000,show_date_time)  #ms (1sec)

list_imgs=['logo1.webp','logo2.png','logo3.webp','logo4.jpg','logo5.jpeg','logo6.jpg','logo7.png','logo8.jpeg','logo9.png']
def img_animation():
    index=random.randint(0,8)
    img=Image.open(list_imgs[index]).resize((250,100))
    imgtk=ImageTk.PhotoImage(img,master=root)
    logo_lbl=Label(root,image=imgtk)
    logo_lbl.place(relx=0,rely=0)
    logo_lbl.image=imgtk
    logo_lbl.after(1000,img_animation)

root=Tk()
root.state('zoomed')
root.configure(bg="#1ddb80")

title_label=Label(root,text='Banking Automation',bg="#1ddb80",fg='blue',font=('Arial',45,'bold','underline'))
title_label.pack()

date_time_label=Label(root,font=('Arial',15,'bold'),bg='pink')
date_time_label.pack(pady=1)
show_date_time()

img=Image.open('logo1.webp').resize((250,100))
imgtk=ImageTk.PhotoImage(img,master=root)

logo_lbl=Label(root,image=imgtk)
logo_lbl.place(relx=0,rely=0)
img_animation()

footer_labl=Label(root,font=('Arial',12,'bold'),fg='blue',bg="#1ddb80",text='Created By \n AJEET KUMAR')
footer_labl.pack(side='bottom')

code_captcha=generate_captcha()

def main_screen():
    def refresh_captcha():
        global code_captcha
        code_captcha=generate_captcha()
        captcha_value_lbl.configure(text=code_captcha)

    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#1ddb80")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)

    
    

  #  scroll_text()   # start scrolling



    def forgot():
        frm.destroy()
        forgot_screen()

    def Login():
        utype=accntype_cb.get()
        uacn=accno_Entry.get()
        upass=pswd_Entry.get()

        ucaptcha=captcha_e.get()
        global code_captcha            
        code_captcha=code_captcha.replace(' ','')

        if utype=='ADMIN':
            if uacn=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login',"Invalid Captcha")
            elif len(uacn)==0 or len(upass)==0:
                messagebox.showerror('Login',"Please Enter Account No/password")            
            else:
                messagebox.showerror('Login','Wrong Password')
        else:   
            
            if code_captcha==ucaptcha:

                conobj=sqlite3.connect(database='bank.sqlite')
                curboj=conobj.cursor()
                query='select * from accounts where acc_accno=? and acn_pswd=?'
                curboj.execute(query,(uacn,upass))
                row=curboj.fetchone() 
                if row==None:
                    messagebox.showerror('Login',"Invalid Account No/password")                                    
                else:
                    frm.destroy()
                    User_screen(row[0],row[1])                                   
            else:
                messagebox.showerror('Login',"Account No/password/Invalid Captcha")
                
    
    accntype_lbl=Label(frm,text='Account Type',font=('Arial',19,'bold'),bg='#1ddb80')
    accntype_lbl.place(relx=.3,rely=.1)

    accntype_cb=Combobox(frm,values=['USER','ADMIN'],font=('Arial',18,'bold'))
    accntype_cb.current(0)
    accntype_cb.place(relx=.45,rely=.1)

    accno_lbl=Label(frm,text='Account No',font=('Arial',19,'bold'),bg='#1ddb80')
    accno_lbl.place(relx=.3,rely=.2)

    accno_Entry=Entry(frm,font=('Arial',19,'bold'),bd=5)
    accno_Entry.place(relx=.45,rely=.2)
    accno_Entry.focus()

    pswd_lbl=Label(frm,text='Password',font=('Arial',19,'bold'),bg='#1ddb80')
    pswd_lbl.place(relx=.3,rely=.3)

    pswd_Entry=Entry(frm,font=('Arial',19,'bold'),bd=5,show='*')
    pswd_Entry.place(relx=.45,rely=.3)

    captcha_lbl=Label(frm,text='Captcha',font=('Arial',19,'bold'),bg='#1ddb80')
    captcha_lbl.place(relx=.3,rely=.4)

    captcha_value_lbl=Label(frm,text=code_captcha,fg='green',font=('Arial',19,'bold'))
    captcha_value_lbl.place(relx=.45,rely=.4)

    refsh_butn=Button(frm,text='🔄',bg='#1ddb80',font=('Arial',13 ,'bold'),command=refresh_captcha)
    refsh_butn.place(relx=.55,rely=.4)

    captcha_e=Entry(frm,font=('Arial',19,'bold'),bd=5)
    captcha_e.place(relx=.45,rely=.5)

    login_butn=Button(frm,text='Login',command=Login,width=14,fg='yellow',bg="#EA5CB4",bd=2,font=('Arial',14,'bold'))
    login_butn.place(relx=.5,rely=.6)

    forgot_butn=Button(frm,text='Forgot Password',command=forgot,fg='yellow',bg='#EA5CB4',width=14,bd=2,font=('Arial',14,'bold'))
    forgot_butn.place(relx=.5,rely=.7)

def forgot_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='light green')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)

    def back():
        frm.destroy()
        main_screen()

    def frgt_butn():
        uemail=email_Entry.get()
        uacn=acc_fgt_Entry.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curboj=conobj.cursor()
        query='select * from accounts where acc_accno=?' 
        curboj.execute(query,(uacn,))
        torow=curboj.fetchone()
        if torow==None:
            messagebox.showerror("Forgot Password",'Account does not Exist')
        else:
            if uemail==torow[3]:
                otp=random.randint(1000,9999)
                otp_pswd(uemail,otp)
                messagebox.showinfo('Forgot','otp sent to registered Email,kindly verify')
                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curboj=conobj.cursor()
                            query='select acn_pswd from accounts where acc_accno=?'
                            curboj.execute(query,(uacn,))   

                            messagebox.showinfo('Forget Password',f"Your Account password is {curboj.fetchone()[0]}")
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Forgot Password",'Invalid otp')

                otp_e=Entry(frm,font=('Arial',19,'bold'),bd=5)
                otp_e.place(relx=.4,rely=.6)
                otp_e.focus()

                verify_butn=Button(frm,text='Verify',command=verify_otp,bg='pink',bd=5,font=('Arial',13,'bold'))
                verify_butn.place(relx=.5,rely=.7)
            else:
                messagebox.showerror('Forgot Password',"Email doesn't matched")

    back_butn=Button(frm,text='Home Page',command=back,bg='pink',bd=5,font=('Arial',13,'bold'))
    back_butn.place(relx=.02,rely=.02)

    acc_fgt_lbl=Label(frm,text='Account No',font=('Arial',19,'bold'),bg='light green')
    acc_fgt_lbl.place(relx=.3,rely=.3)

    acc_fgt_Entry=Entry(frm,font=('Arial',19,'bold'),bd=5)
    acc_fgt_Entry.place(relx=.45,rely=.3)
    acc_fgt_Entry.focus()

    email_lbl=Label(frm,text='Enter Email',font=('Arial',19,'bold'),bg='light green')
    email_lbl.place(relx=.3,rely=.4)

    email_Entry=Entry(frm,font=('Arial',19,'bold'),bd=5)
    email_Entry.place(relx=.45,rely=.4)
 
    submit_butn=Button(frm,text='Submit',command=frgt_butn,bg='pink',bd=5,font=('Arial',15,'bold'))
    submit_butn.place(relx=.53,rely=.5)

def admin_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#b0b1b5")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)

    def logout():
        frm.destroy()
        main_screen()

    logout_butn=Button(frm,text='Logout',command=logout,width=11,bg="#d81515",fg="#95eb2d",bd=5,font=('Arial',15,'bold'))
    logout_butn.place(relx=.04,rely=.8)

    wlc_lbl=Label(frm,text='ADMIN SCREEN',fg="#E313CE",bg="#b0b1b5",font=('Ariat',35,'bold'))
    wlc_lbl.place(relx=.4,rely=.05)

    def open():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#94c4e3")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Account Open Screen',bg='#94c4e3',font=('Arial',19,'bold'))
        t_lbl.pack()

        def openAccnt():

            uname=openacc_name_Entry.get()
            uemail=openacc_email_Entry.get()
            umob=openacc_no_Entry.get()
            uadhar=openacc_adhar_Entry.get()
            uadrs=openacc_addrs_Entry.get()
            udob=openacc_dob_Entry.get()
            upswd=generate_captcha()
            upswd=upswd.replace(' ','')
            ubal=0
            uopendate=time.strftime("%A %d-%b-%Y")
            ugender=gender_type_cb.get()
            unominee=openacc_nominee_Entry.get()

            # Empty Validation
            if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadrs)==0 or len(udob)==0 or len(ugender)==0 or len(unominee)==0:
                messagebox.showerror('Open Account','Empty fields are not allowed')
                return
            
            # Email Validation
            match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+",uemail)
            if match==None:
                messagebox.showerror('Open Account','kindly check format of email')
                return
            
            # mob validation
            mob=re.fullmatch('[0-9]{10}',umob)
            if mob==None:
                messagebox.showerror('Open Account','kindly check format of phone number')
                return

            #Adhar validation
            adhar=re.fullmatch('[0-9]{12}',uadhar)
            if adhar==None:
                messagebox.showerror('Open Account','kindly check format of Adhar number')
                return

            conobj=sqlite3.connect(database='bank.sqlite')
            curboj=conobj.cursor()
            query='insert into accounts values (null,?,?,?,?,?,?,?,?,?,?,?)'
            curboj.execute(query,(uname,upswd,uemail,umob,uadhar,uadrs,udob,ubal,uopendate,ugender,unominee))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curboj=conobj.cursor()
            curboj.execute("select max(acc_accno) from accounts")
            uaccn=curboj.fetchone()[0]
            conobj.close()
            sendopen_acnmsg(uemail,uname,uaccn,upswd)

            messagebox.showinfo('Account Opened',"Accounts open and details sends to your email")
            frm.destroy()
            admin_screen()

        openacc_name_lbl=Label(ifrm,text='Name',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_name_lbl.place(relx=.04,rely=.2)

        openacc_name_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_name_Entry.place(relx=.19,rely=.2)

        openacc_email_lbl=Label(ifrm,text='Email Id',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_email_lbl.place(relx=.04,rely=.35)

        openacc_email_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_email_Entry.place(relx=.19,rely=.35)

        openacc_no_lbl=Label(ifrm,text='Phone No',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_no_lbl.place(relx=.04,rely=.5)

        openacc_no_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_no_Entry.place(relx=.19,rely=.5)

        openacc_adhar_lbl=Label(ifrm,text='Adhar No',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_adhar_lbl.place(relx=.04,rely=.65)

        openacc_adhar_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_adhar_Entry.place(relx=.19,rely=.65)

        openacc_dob_lbl=Label(ifrm,text='D-O-B',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_dob_lbl.place(relx=.51,rely=.2)

        openacc_dob_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_dob_Entry.place(relx=.65,rely=.2)

        gender_type_lbl=Label(ifrm,text='Gender',bg='#94c4e3',font=('Arial',17,'bold'))
        gender_type_lbl.place(relx=.51,rely=.35)

        gender_type_cb=Combobox(ifrm,values=['MALE','FEMALE'],width=17,font=('Arial',16,'bold'))
        gender_type_cb.current(0)
        gender_type_cb.place(relx=.65,rely=.35)

        openacc_addrs_lbl=Label(ifrm,text='Address',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_addrs_lbl.place(relx=.51,rely=.5)

        openacc_addrs_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_addrs_Entry.place(relx=.65,rely=.5)

        openacc_nominee_lbl=Label(ifrm,text='Nominee',bg='#94c4e3',font=('Arial',17,'bold'))
        openacc_nominee_lbl.place(relx=.51,rely=.65)

        openacc_nominee_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        openacc_nominee_Entry.place(relx=.65,rely=.65)

        open_accn_butn=Button(ifrm,text='Open Account',command=openAccnt,fg='yellow',bg="#e04fbe",bd=5,font=('Arial',14,'bold'))
        open_accn_butn.place(relx=.45,rely=.82)

    def close():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#94c4e3")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Account Close Screen',font=('Arial',19,'bold'),bg='#94c4e3')
        t_lbl.pack()

        def close_acc():
            uacn=accno_Entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acc_accno=?'
            curobj.execute(query,(uacn,))
            torow=curobj.fetchone()
            if len(uacn)==0:
                    messagebox.showerror("Close Account","Please Enter Account NO/password")
                    return
            if torow==None:
                messagebox.showerror("Close Account","ACN does not exist")
                
            else:
                clo_pswd='admin'
                pswd=pswd_Entry.get()
                if len(pswd)==0:
                    messagebox.showerror("Close Account","Please Enter Password")
                    return
                if clo_pswd==pswd:                 
                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    query='delete from accounts where acc_accno=?'
                    curobj.execute(query,(uacn,))
                         
                    messagebox.showinfo('Close Account',"Account Closed")
                    conobj.commit()
                    conobj.close()
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Close Account","Wrong Password")
                
        accno_lbl=Label(ifrm,text='Account No',bg="#94c4e3",font=('Arial',17,'bold'))
        accno_lbl.place(relx=.25,rely=.2)

        accno_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        accno_Entry.place(relx=.49,rely=.2)
        accno_Entry.focus()

        pswd_lbl=Label(ifrm,text='Admin Password',bg="#94c4e3",font=('Arial',17,'bold'))
        pswd_lbl.place(relx=.25,rely=.34)

        pswd_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        pswd_Entry.place(relx=.49,rely=.34)            

        ac_close_butn=Button(frm,text='Close Account',command=close_acc,fg='yellow',bg="#1238B4",width=14,bd=2,font=('Arial',14,'bold'))
        ac_close_butn.place(relx=.48,rely=.7)

    def view():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="light green")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Account Details Screen',font=('Arial',19,'bold'),bg='light green')
        t_lbl.pack()

        tree = ttk.Treeview(ifrm, columns=("A","B","C","D","E","F","G","H","I","J","K"), show="headings")
        tree.heading("A", text="ACN0.")
        tree.heading("B", text="NAME")
        tree.heading("C", text="Email")
        tree.heading("D", text="MOB")        
        tree.heading("E", text="Adhar")
        tree.heading("F", text="Address")
        tree.heading("G", text="DOB")
        tree.heading("H", text="Balance")
        tree.heading("I", text="Gender")        
        tree.heading("J", text="OPEN DATE")
        tree.heading("K", text="Nominee")       

        tree.column("A", width=100,anchor="center")
        tree.column("B", width=150,anchor="center")
        tree.column("C", width=200,anchor="center")
        tree.column("D", width=100,anchor="center")
        tree.column("E", width=100,anchor="center")
        tree.column("F", width=100,anchor="center")
        tree.column("G", width=100,anchor="center")
        tree.column("H", width=100,anchor="center")
        tree.column("I", width=100,anchor="center")
        tree.column("J", width=100,anchor="center")
        tree.column("K", width=100,anchor="center")
        
        
        tree.place(relx=.01,rely=.1,relwidth=.98,relheight=.87) 

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select acc_accno,acn_name,acn_email,acn_mob,acn_adhar,acn_addrs,acn_dob,acn_bal,acn_gender,acn_opendate,acn_nominee from accounts'
        curobj.execute(query)
        for tup in curobj.fetchall():
            tree.insert("", "end", values=tup)
        conobj.close()

    Open_accn_butn=Button(frm,text='Open Account',command=open,fg="#c2ff0b",bg="#5387e7",bd=5,font=('Arial',15,'bold'))
    Open_accn_butn.place(relx=.04,rely=.23)

    close_accn_butn=Button(frm,text='Close Account',command=close,fg="#53ef0a",bg="#6e5f97",bd=5,font=('Arial',15,'bold'))
    close_accn_butn.place(relx=.04,rely=.43)

    view_accn_butn=Button(frm,text='View Account',command=view,fg="#eded93",bg="#a380f0",bd=5,font=('Arial',15,'bold'))
    view_accn_butn.place(relx=.04,rely=.62)

def User_screen(uacn,uname):
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#E6E9D0")
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.8)

    conobj=sqlite3.connect(database='bank.sqlite')
    curboj=conobj.cursor()
    query='select * from accounts where acc_accno=?'
    curboj.execute(query,(uacn,))
    row=curboj.fetchone()
    conobj.close()

    def logout():
        frm.destroy()
        main_screen()

    def check_datails():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#eeee5f")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Account Details Screen',font=('Arial',19,'bold'),bg='#eeee5f')
        t_lbl.pack()

        acn_details_lbl=Label(ifrm,text=f'Account Number\t=\t{row[0]}',font=('Arial',19,'bold'),bg="#eeee5f")
        acn_details_lbl.place(relx=.2,rely=.2)

        userBal_details_lbl=Label(ifrm,text=f'Account Balance\t=\t{row[8]}',font=('Arial',19,'bold'),bg="#eeee5f")
        userBal_details_lbl.place(relx=.2,rely=.3)

        Adhar_details_lbl=Label(ifrm,text=f'Adhar Number\t=\t{row[5]}',font=('Arial',19,'bold'),bg="#eeee5f")
        Adhar_details_lbl.place(relx=.2,rely=.4)

        DOb_details_lbl=Label(ifrm,text=f'Date of Birth\t=\t{row[7]}',font=('Arial',19,'bold'),bg="#eeee5f")
        DOb_details_lbl.place(relx=.2,rely=.5)

        Dateopen_details_lbl=Label(ifrm,text=f'Open Date\t=\t{row[9]}',font=('Arial',19,'bold'),bg="#eeee5f")
        Dateopen_details_lbl.place(relx=.2,rely=.6)


    def user_update():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#eeee5f")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Account Details Update Screen',font=('Arial',19,'bold'),bg='#eeee5f')
        t_lbl.pack()

        def user_update():
            uname=update_name_Entry.get()
            upswd=update_pswd_Entry.get()
            uemail=update_email_Entry.get()
            umob=update_no_Entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curboj=conobj.cursor()
            query='update accounts set acn_name=?,acn_pswd=?,acn_email=?,acn_mob=? where acc_accno=?'

            curboj.execute(query,(uname,upswd,uemail,umob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update",'Details Updated')
            frm.destroy()
            User_screen(uacn,uname)


        update_name_lbl=Label(ifrm,text='Name',bg="#eeee5f",font=('Arial',17,'bold'))
        update_name_lbl.place(relx=.3,rely=.2)

        update_name_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        update_name_Entry.place(relx=.45,rely=.2)
        update_name_Entry.insert(0,row[1])

        update_pswd_lbl=Label(ifrm,text='Password',bg="#eeee5f",font=('Arial',17,'bold'))
        update_pswd_lbl.place(relx=.3,rely=.35)

        update_pswd_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        update_pswd_Entry.place(relx=.45,rely=.35)
        update_pswd_Entry.insert(0,row[2])

        openacc_no_lbl=Label(ifrm,text='Mobile No',bg="#eeee5f",font=('Arial',17,'bold'))
        openacc_no_lbl.place(relx=.3,rely=.5)

        update_no_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        update_no_Entry.place(relx=.45,rely=.5)
        update_no_Entry.insert(0,row[4])

        update_email_lbl=Label(ifrm,text='Email ID',bg="#eeee5f",font=('Arial',17,'bold'))
        update_email_lbl.place(relx=.3,rely=.65)

        update_email_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        update_email_Entry.place(relx=.45,rely=.65)
        update_email_Entry.insert(0,row[3])

        user_update_butn=Button(frm,text='Update Details',width=14,fg='yellow',command=user_update,bg="#388feb",bd=5,font=('Arial',15,'bold'))
        user_update_butn.place(relx=.54,rely=.79)

    def user_deposit():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#eeee5f")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Amount Deposit Screen',bg="#eeee5f",font=('Arial',19,'bold'))
        t_lbl.pack()

        def amnt_submit():
            umnt=float(depo_amnt_Entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curboj=conobj.cursor()
            query='update accounts set acn_bal=acn_bal+? where acc_accno=?'

            curboj.execute(query,(umnt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f'{umnt}Deposited')
            frm.destroy()
            User_screen(uacn,uname)

        depo_amnt_lbl=Label(ifrm,text='Enter Amount',bg="#eeee5f",font=('Arial',17,'bold'))
        depo_amnt_lbl.place(relx=.27,rely=.2)

        depo_amnt_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        depo_amnt_Entry.place(relx=.5,rely=.2)
        depo_amnt_Entry.focus()

        depo_butn=Button(ifrm,text='Submit',width=14,command=amnt_submit,fg='yellow',bg="#388feb",bd=5,font=('Arial',15,'bold'))
        depo_butn.place(relx=.4,rely=.79)

    def user_withdraw():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#eeee5f")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Amount Withdraw Screen',font=('Arial',19,'bold'),bg='#eeee5f')
        t_lbl.pack()

        def withdraw_submit():
            umnt=float(withdraw_amnt_Entry.get())
            wpswd=wdrd_pswd_Entry.get()
            if row[8]>=umnt and wpswd==row[2]:                
                
                conobj=sqlite3.connect(database='bank.sqlite')
                curboj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal-? where acc_accno=?'

                curboj.execute(query,(umnt,uacn,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f'{umnt}Amount withdrawl')
                frm.destroy()
                User_screen(uacn,uname)
                
            elif row[8]<=umnt:
                messagebox.showerror('withdraw','Insufficient Balance')
            if len(wpswd)==0:
                messagebox.showerror("Close Account","Please Enter password")
                
            elif wpswd!=row[2]:
                messagebox.showerror('withdraw','Wrong password')
                return
                        
            

        withdraw_amnt_lbl=Label(ifrm,text='Withdraw Amount',bg="#eeee5f",font=('Arial',17,'bold'))
        withdraw_amnt_lbl.place(relx=.24,rely=.2)

        withdraw_amnt_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        withdraw_amnt_Entry.place(relx=.5,rely=.2)
        withdraw_amnt_Entry.focus()

        wdrw_pswd_lbl=Label(ifrm,text='Enter Password',bg="#eeee5f",font=('Arial',17,'bold'))
        wdrw_pswd_lbl.place(relx=.24,rely=.35)

        wdrd_pswd_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        wdrd_pswd_Entry.place(relx=.5,rely=.35)

        depo_butn=Button(ifrm,text='Submit',width=14,command=withdraw_submit,fg='yellow',bg="#388feb",bd=5,font=('Arial',15,'bold'))
        depo_butn.place(relx=.4,rely=.79)

    def user_transfer():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg="#eeee5f")
        ifrm.place(relx=.25,rely=.2,relwidth=.7,relheight=.7)

        t_lbl=Label(ifrm,text='Amount Transfer Screen',font=('Arial',19,'bold'),bg='#eeee5f')
        t_lbl.pack()

        def tnsfr_butn():
            upswd=tnsfr_pswd_Entry.get()
            toacn=tnsfr_to_Entry.get()
            uamt=float(tnsfr_amnt_Entry.get())
                       
            conobj=sqlite3.connect(database='bank.sqlite')
            curboj=conobj.cursor()
            query='select * from accounts where acc_accno=?' 
            curboj.execute(query,(toacn,))
            torow=curboj.fetchone()
            if len(toacn)==0:
                messagebox.showerror("Transfer",'Please Enter Account Number')
            elif torow==None:
                messagebox.showerror("Transfer",'Account Number Not Exist')
            else:                
                if row[8]>=uamt and row[2]==upswd:
                    conobj=sqlite3.connect(database='bank.sqlite')
                    curboj=conobj.cursor()
                    query1='update accounts set acn_bal=acn_bal-? where acc_accno=?'
                    query2='update accounts set acn_bal=acn_bal+? where acc_accno=?' 
                    curboj.execute(query1,(uamt,uacn))
                    curboj.execute(query2,(uamt,toacn))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Transfer",'Balance Transferred')
                    frm.destroy()
                    User_screen(uacn,uname)
                    
                elif row[8]<=uamt:
                    messagebox.showerror("Transfer",'Insufficient Balance')
                elif len(upswd)==0:
                    messagebox.showerror('Transfer','please Enter Password')
                else:                    
                    messagebox.showerror("Transfer",'Incorrect Password')
                        
        tnsfr_to_lbl=Label(ifrm,text='Enter Account No',bg="#eeee5f",font=('Arial',17,'bold'))
        tnsfr_to_lbl.place(relx=.24,rely=.2)

        tnsfr_to_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        tnsfr_to_Entry.place(relx=.5,rely=.2)
        tnsfr_to_Entry.focus()

        tnsfr_amnt_lbl=Label(ifrm,text='Tranfer Amount',bg="#eeee5f",font=('Arial',17,'bold'))
        tnsfr_amnt_lbl.place(relx=.24,rely=.32)

        tnsfr_amnt_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        tnsfr_amnt_Entry.place(relx=.5,rely=.32)

        tnsfr_pswd_lbl=Label(ifrm,text='Enter Password',bg="#eeee5f",font=('Arial',17,'bold'))
        tnsfr_pswd_lbl.place(relx=.24,rely=.44)

        tnsfr_pswd_Entry=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        tnsfr_pswd_Entry.place(relx=.5,rely=.44)

        transfer_butn=Button(ifrm,text='Submit',width=14,command=tnsfr_butn,fg='yellow',bg="#388feb",bd=5,font=('Arial',15,'bold'))
        transfer_butn.place(relx=.4,rely=.79)

    user_logout_butn=Button(frm,text='Logout',command=logout,width=14,fg="#eded93",bg="#d81515",bd=5,font=('Arial',15,'bold'))
    user_logout_butn.place(relx=.04,rely=.9)

    wlc_lbl=Label(frm,text='WELCOME',fg="blue",bg="#E6E9D0",font=('Arial',35,'bold'))
    wlc_lbl.place(relx=.48,rely=.09)

    wlc_lbl=Label(frm,text=f'Hi,{uname}',fg='blue',bg="#E6E9D0",font=('Arial',25,'bold'))
    wlc_lbl.place(relx=.05,rely=.03)

    user_details_butn=Button(frm,text='Personal Details',width=14,command=check_datails,fg="#c2ff0b",bg="#5387e7",bd=5,font=('Arial',15,'bold'))
    user_details_butn.place(relx=.04,rely=.15)

    user_update_butn=Button(frm,text='Update Details',width=14,command=user_update,fg="#53ef0a",bg="#6e5f97",bd=5,font=('Arial',15,'bold'))
    user_update_butn.place(relx=.04,rely=.3)

    user_deposit_butn=Button(frm,text='Deposit Amount',command=user_deposit,width=14,fg="#eded93",bg="#a380f0",bd=5,font=('Arial',15,'bold'))
    user_deposit_butn.place(relx=.04,rely=.45)

    user_withdraw_butn=Button(frm,text='Withdraw Amount',command=user_withdraw,width=14,fg="#53ef0a",bg="#6e5f97",bd=5,font=('Arial',15,'bold'))
    user_withdraw_butn.place(relx=.04,rely=.6)

    user_transfer_butn=Button(frm,text='Transfer Amount',command=user_transfer,width=14,fg="#eded93",bg="#a380f0",bd=5,font=('Arial',15,'bold'))
    user_transfer_butn.place(relx=.04,rely=.75)


main_screen()
root.mainloop()