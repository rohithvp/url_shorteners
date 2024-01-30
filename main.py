import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse 
from fastapi.templating import Jinja2Templates
import random
import string
import db

import uvicorn

app = FastAPI() 

templates = Jinja2Templates(directory="templates")

urls = {"abc" : "https://google.com/", "xyz" : "https://facebook.com/", "def" :"http://dinamalar.com/"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


@app.post("/result",response_class=HTMLResponse)
def result( request: Request, url= Form(...)): 
    global urls
    random_letters= "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
    short_url= "http://192.168.49.2:30032/"+random_letters
    print(short_url)
    urls[random_letters] = url
    con, cur = db.getcon()  
    
    try:
        c=db.searchall(con=con,cur=cur,random_letters=random_letters)
        length=len(c)
        if length==0:
            result = db.insert_data(con=con, cur=cur, url=url, random_letters=random_letters)
            print("print",len(c),c)
            print("Updated",result)
            return templates.TemplateResponse("result.html", context={"request": request, "url": short_url})
        else:
            print(" ss")
            return templates.TemplateResponse("result.html", context={"request": request, "url": short_url})

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        con.close()
        
    

@app.get("/{short_url}")
def redirect(short_url : str):
    print(short_url)
    print(urls)
    return RedirectResponse(url = urls[short_url])


if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)            