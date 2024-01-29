import psycopg2
from psycopg2 import sql
import os

def getcon():


    try:
        con= psycopg2.connect(
        host= os.getenv("HOST"),
        database =os.getenv("DATABASE"),
        user= os.getenv("USER"),
        password= os.getenv("PASSWORD"),
        port=os.getenv("DB_PORT")
        )
        cur=con.cursor()
        print("success",cur)
        return con, cur

    except (Exception, psycopg2.Error):
        print("invalid")
        return None, None
    


def insert_data(con, cur, url: str, random_letters: str):    
    try:
            insert_query = sql.SQL("INSERT INTO short_url (long_url, converted_short_url) VALUES (%s, %s)")
            cur.execute(insert_query, (url, random_letters))
            con.commit()

            return "Data saved successfully"

    except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into the table:", error)


    finally:
            cur.close()
            con.close()

    

def searchall(con,cur,random_letters):
        try:
                query=sql.SQL("Select * from short_url where converted_short_url ='{}'".format(random_letters))
                cur.execute(query)
                result=cur.fetchall()
                con.commit()     
                print(len(result))       
                return result

           
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into the table:", error)


        
    
 