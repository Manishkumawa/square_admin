


import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os

import json
myconn = mysql.connector.connect(host =os.getenv("HOST"),user = os.getenv("USER"),passwd = os.getenv("PASSWORD") ,database = os.getenv("DATABASE"))

print(myconn)
curr = myconn.cursor()


def insert_into_data(insurare ,datas ,created_at):


    

    sql = "insert into square_insurance.pdf_text_extract(insurare ,datas, created_at ) values(%s ,%s,%s)"


    value =(insurare,datas,created_at)

    curr.execute(sql,value)

    myconn.commit()




def is_existed(insurare ,datas ,created):

    sql = "select * from square_insurance.pdf_text_extract where datas =%s"
    val =  (datas,)

    curr.execute(sql,val)

    result = curr.fetchall()
    if result is not None:
        return True
    else:
        return False 
    




def select_data():

    sql = "select id ,insurare ,datas ,created_at ,updated_at from square_insurance.pdf_text_extract"

    curr.execute(sql)

    result = curr.fetchall()

    
    
    if result is not None:
        return result
    else:
        return result
    

    
    
    








