import gmail
# Use your email and app_password
email_id="--"
app_pass="--"

def sendopen_acnmsg(uemail,uname,uacn,upass):
    con=gmail.GMail(email_id,app_pass)
    sub="Congratulations,Your Account is successfully Opened"
    
    utext=f"""Hello,{uname}
Welcome to SWISS Bank
Your Acc No is {uacn}
Your Pass is {upass}
Kindly change your password when you login first Time.

Thanks
SWISS BANK
Noida
    """
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)

def otp_pswd(uemail,otp):
    con=gmail.GMail(email_id,app_pass)
    sub='otp for password recovery'

    utext=f'''Your otp iS {otp} to recover password 
please don't share to anyone.


Thanks
SWISS BANK
    '''
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)