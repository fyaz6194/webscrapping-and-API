#Please obey all rules and regulation of webpage for web scraping.

#!/usr/bin/python
import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, Response
import requests
from bs4 import BeautifulSoup
import sqlite3
from module1 import SQL
from array import *
import numpy as np
import json
import os
import platform
import _thread


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    
    return response
@app.route("/")
def redirect_api():
    return redirect("/api")
@app.route("/api", methods=['GET','POST']) #can use only POST method
def thread():
    #now = datetime.datetime.now()           
    #time_now = (now)

    #print(time_now)
    
    #return True
    userINput = request.form.get("") 
    USERID = request.form.get("USERID")
    PASS = request.form.get("PASS")
    APIKEY = request.form.get("APIKEY")
    PIP = request.remote_addr
    method = request.method
    response = GSTIN_V(userINput,USERID,PASS,APIKEY,PIP,method)
    return response
    response =  _thread.start_new_thread(GSTIN_V,(GSTIN,USERID,PASS,APIKEY,PIP,method))
    

def GSTIN_V(GSTIN_t,USERID_t,PASS_t,APIKEY_t,PIP_t,METHOD_t):
    if USERID_t == None or USERID_t == "" or PASS_t == None or PASS_t == "" or APIKEY_t == None or APIKEY_t == "":
        return jsonify({'msg':'authentication error(01).'})
    if GSTIN_t.isalnum() != True or USERID_t.isalnum() != True:
        return jsonify({'msg':'authentication error(1).'})
    if (PASS_t.replace("@","")).isalnum() != True:
        return jsonify({'msg':'authentication error(4).'})
    s = (APIKEY_t).replace("@","")
    s = s.replace("_","")
        #print(s)
    if s.isalnum() != True:
        return jsonify({'msg':'authentication error(5).'})
       
       
    userINput = GSTIN_t
    userINput = userINput.replace(" ", "").replace(",","")
    userINput = str(userINput.upper())
    pip = PIP_t
    USERID = USERID_t
    USERID = USERID.replace(" ", "").replace(",","")
    USERID = str(USERID)
    PASS = PASS_t
    PASS = PASS.replace(" ", "").replace(",","")
    PASS = str(PASS)
    APIKEY = APIKEY_t
    APIKEY = APIKEY.replace(" ", "").replace(",","")
    APIKEY = str(APIKEY)
        #print(str(USERID)+"     " + str(PASS) +"     " + str(APIKEY) )
    if USERID == None or USERID == "" or PASS == None or PASS == "" or APIKEY == None or APIKEY == "":
        return jsonify({'msg':'authentication error(01).'})
         #con_API = sqlite3.connect('APIKey.db')
         #db = con_API.cursor()
    if METHOD_t == 'POST':
        
        

        db_GSTIN = SQL("sqlite:///GSTIN_Check.db")
        db_API = SQL("sqlite:///APIKey.db")
        
        DB_auth = db_API.execute("select Userid,Password,API_Key FROM APIKEY Where Userid = :user_id", user_id = USERID)
        
          
        #print(DB_auth)
        #return "None"
        if len(DB_auth) == 0:
            return jsonify({'msg':'authentication error(04).'})
        DB_auth = DB_auth[0]        
        if USERID != DB_auth['Userid'] or PASS != DB_auth['Password'] or APIKEY != DB_auth['API_Key']:
            return jsonify({'msg':'authentication error(03).'})
                
        try:
            if len(userINput) == 15 and userINput.isalnum() == True:
                F2 = False
                F7 = False
                F11 = False
                F12 = False
                F13 = False
                F14 = False
                F15 = False
               
                if userINput[0:2].isdigit() == True:
                    F2 = True
                if userINput[2:7].isalpha() == True:
                    F7 = True
                if userINput[7:11].isdigit() == True:
                    F11 = True
                if userINput[11:12].isalnum() == True:
                    F12 = True
                if userINput[12:13].isalnum() == True:
                    F13 = True
                if userINput[13:14].isalpha() == True:
                    F14 = True
                if userINput[14].isalnum() == True:
                    F15 = True
                if F2 == True and F7 == True and F11 == True and F12 == True and F13 == True and F14 == True and F15 == True:
                   DB_GSTIN = db_GSTIN.execute("select Legal_Name, GSTIN, DOR, DOC, Address, CDate FROM GSTIN_Check Where GSTIN = :gstin", gstin = GSTIN)           
                   final_db_GSTIN = ""
                   if len(DB_GSTIN) > 0:
                       DB_GSTIN = DB_GSTIN[0]
                       
                       final_db_GSTIN = final_db_GSTIN + "{'Legal_Name':'" + DB_GSTIN['Legal_Name'] + "',"
                       final_db_GSTIN = final_db_GSTIN + "'GSTIN':'" + DB_GSTIN['GSTIN'] + "',"
                       final_db_GSTIN = final_db_GSTIN + "'DOR':'" + DB_GSTIN['DOR'] + "',"
                       final_db_GSTIN = final_db_GSTIN + "'DOC':'" + DB_GSTIN['DOC'] + "',"
                       final_db_GSTIN = final_db_GSTIN + "'Address':'" + DB_GSTIN['Address'] + "',"
                       #final_db_GSTIN = final_db_GSTIN + "'PIP':'" + DB_GSTIN('PIP') + "',"
                       final_db_GSTIN = final_db_GSTIN + "'ServerUpdateDate':'" + DB_GSTIN['CDate'] + "'}"
                       r_db = Response(final_db_GSTIN.replace("'","\""))
                       r_db.headers['server'] = ''
                       r_db.headers["Content-Type"] = "text/json; charset=utf-8"
                       return r_db
                   else:
                       
                       if platform.system() == "Windows":
                            response = os.system('') # website ping 
                       
                                             
                       if response != 0:
                            return jsonify({'msg':'Server Down(01).'})
                       r1 = requests.get('') # Authroised and apporve website provider for web scarping
                       r = BeautifulSoup(r1.text,'lxml')
                       #print(r)
                       result_th = []
                       result_td = []
                      
                       if len(r.findAll("", {""})) != 0: #website script for extraction of data
                           s= r.findAll("", {"": ""})[0].findAll("",{""})[0]
                           result_th = s.findAll("",{'':''})
                           result_td = s.findAll("",{'':''})
                           result_1 = []
                           result_2 = []
                           final_json = ""
                           final_data = []
                           Final_other_json = ""
                           #result_other_header = []
                           #result_other_data = []
                           count_comma = 0
                           
                       if len(result_td) == len(result_th) :
                            if len(result_td) != 0:
                                    Final_other_json = "{"
                                    #print(result_td)
                                    count = 0
                                    for i in range(len(result_td)):
                                        result_1.append(result_th[i].get_text().replace("\r","").replace("\n","").replace("\"",""))
                                        result_2.append(result_td[i].get_text().replace("\r","").replace("\n","").replace("\"",""))
                                    #for i in range(len(result_1)):
                                    #    print(result_1[i])
                                    #    print(result_2[i])
                                    for i in range(len(result_1)):
                                        if result_1[i].upper().replace(" ","") == "Legal Name of Business".upper().replace(" ", ""):
                                           #result_other_header.append("Legal_Name")
                                           #result_other_data.append(result_2[i].replace("'",""))
                                           Final_other_json = Final_other_json + " 'Legal_Name':'" + result_2[i].replace("'","") + "'"
                                           count = count + 1
                                          
                                        elif result_1[i].upper().replace(" ","") == "GSTIN/UIN".upper().replace(" ", ""):
                                            #result_other_header.append("GSTIN")
                                            #result_other_data.append(result_2[i].replace("'",""))
                                            Final_other_json = Final_other_json + "'GSTIN':'" + result_2[i].replace("'","") + "'"
                                            count = count + 1
                                        elif result_1[i].upper().replace(" ","") == "Date of registration".upper().replace(" ", ""):
                                            #result_other_header.append("DOR")
                                            #result_other_data.append(result_2[i].replace("'",""))
                                            
                                            Final_other_json = Final_other_json + "'DOR':'" + result_2[i].replace("'","") + "'"
                                            count = count + 1
                                        elif result_1[i].upper().replace(" ","") == "Date of Cancellation".upper().replace(" ", ""):
                                            #result_other_header.append("DOC")
                                            #result_other_data.append(result_2[i].replace("'",""))
                                            
                                            Final_other_json = Final_other_json + "'DOC':'" + result_2[i].replace("'","") + "'"
                                            count = count + 1
                                        elif result_1[i].upper().replace(" ","") == "State Jurisdiction".upper().replace(" ", ""):
                                            #result_other_header.append("Address")
                                            #result_other_data.append(result_2[i].replace("'",""))
                                            
                                            Final_other_json = Final_other_json + "'Address':'" + result_2[i].replace("'","") + "'"
                                            count = count + 1
                                        if count > 0:
                                            Final_other_json = Final_other_json + ","
                                            count = count - 1
                                            #print(Final_other_json)
                                        
                                        if i == (len(result_1) - 1):
                                            
                                            #result_other_header.append("PIP")
                                            #result_other_data.append(str(request.remote_addr))
                                            now_date = datetime.datetime.now()
                                            #print(now_date)
                                            Final_other_json = Final_other_json + "'ServerUpdateDate':'" + str(now_date)  + "'}"
                                            #print(Final_other_json)
                                        
                                    
                                    
                                    #print(Final_other_json)
                                    
                                    
                                    
                                    #Final_result_array = []
                                    #if len(result_other_data) == len(result_other_header):                                
                                     #   for x in range(len(result_other_data)):
                                      #      Final_result_array.append([result_other_header[x - 1]])
                                    
                                   # Final_result = np.array(Final_result_array).tolist()
                                    #print(Final_result)
                                    Final = ""
                                    Final = str(Final_other_json).replace("'","\"")
                                    #print(Final)
                                    Final_json2 =  json.loads(Final)
                                    #print(Final_json2['GSTIN'])
                                    json_GSTIN = Final_json2['GSTIN']
                                    json_Legal_Name = Final_json2['Legal_Name']
                                    json_DOR = Final_json2['DOR']
                                    json_DOC = Final_json2['DOC']
                                    json_Address = Final_json2['Address']
                                    if json_GSTIN == "" and json_GSTIN != len(json_GSTIN.replace(" ","")):
                                        return jsonify({'msg':'Program error(04).'})
                                    try:
                                     db_GSTIN.execute("INSERT INTO GSTIN_Check(GSTIN, Legal_Name, DOR, DOC, Address, PIP) VALUES(:GSTIN, :Legal_Name, :DOR, :DOC, :Address, :PIP)", GSTIN = json_GSTIN, Legal_Name = json_Legal_Name, DOR = json_DOR, DOC = json_DOC, Address = json_Address, PIP = PIP_t )           
                                    except (Exception):
                                        return jsonify({'msg':'Program error(05).'})

                                   
                                    
                                    
                                    #for y in range(len(Final_result)):
                                    #    print(Final_result_array[y])
                                        
                                    print()
                                    print()
                                    #print(result_other_all)
                                    
                                    #print("hello")
                                    r_nondb = Response(Final_other_json.replace("'","\""))
                                    r_nondb.headers['server'] = ''
                                    r_nondb.headers["Content-Type"] = "text/json; charset=utf-8"
                                    return r_nondb
                                    
                                   
                                    #for i in range(len(result_1)):
                                     #   if i == 0:
                                     #       final_json = "{" + ('"' + result_1[i] + '"' + ":" +'"'+ result_2[i] + '",')
                                     #   elif i == (len(result_1) - 1):
                                     #       final_json = final_json + ('"' + result_1[i] + '"' + ":" +'"'+ result_2[i] +'"}')
                                     #   else:
                                     #       final_json = final_json + ('"' + result_1[i] + '"' + ":" +'"'+ result_2[i] +'",')
                                    #for i in range(len(result_1)):
                                            #   final_data = final_data + ('' + result_1[i] + '' + ":" +''+ result_2[i] +'')
                                    #r = Response(final_json)
                                    #r.headers['server'] = ''
                                    #r.headers["Content-Type"] = "text/json; charset=utf-8"
                                    #return r                           
                            else:
                                 return jsonify({'msg':'Program error(03).'})
                       else:
                             return jsonify({'msg':'GSTIN Provider site error(01).'})
                       

                
                else:
                    return jsonify({'msg':'GSTIN IS NOT VALID. Code:02'})
            else:
                return jsonify({'msg':'GSTIN IS NOT VALID. Code:01'})
        except (AttributeError,NameError,RuntimeError, TypeError):
            return jsonify({'error':'Error(2) in connection.'})
        
    else:
        return jsonify({'error':'Error(1) in connection.'})


    

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5000)
           




