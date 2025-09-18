import random

def generate_captcha():
    
    a=str(random.randint(0,9))
    b=chr(random.randint(65,80))
    c=str(random.randint(0,9))
    d=chr(random.randint(96,122))
    captcha='  '+a+' '+b+' '+c+' '+d+' ' 
    return captcha