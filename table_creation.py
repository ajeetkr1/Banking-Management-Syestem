import sqlite3

def generate():
    conobj=sqlite3.connect(database='bank.sqlite')
    curboj=conobj.cursor()
    query='''create table if not exists accounts(
    acc_accno integer primary key autoincrement,
    acn_name text,
    acn_pswd text,
    acn_email text,
    acn_mob text,
    acn_adhar text,
    acn_addrs text,
    acn_dob text,
    acn_bal float,
    acn_opendate text,
    acn_gender text,
    acn_nominee text)
    '''
    curboj.execute(query)
    conobj.close()