from datetime import timedelta
from flask import Flask
from flask_jsonpify import jsonify
import requests
import mysql.connector
import datetime


session = requests.session()
app = Flask(__name__)


mydb = mysql.connector.connect(
  host="db",
  user="test",
  password="test",
  database="lolmdr10_ws"
)

def username(id,password):

    mycursor = mydb.cursor()
    mycursor.execute('SELECT id FROM client where username = %s and password= %s',(id,password))
    myresult = mycursor.fetchone()
    return myresult[0]
    
    


@app.route("/information/<date>/<numberofnight>/<numberofroom>/<id>/<password>")
def filter(date,numberofnight,numberofroom,id,password):


    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

    print(date_time_obj)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DISTINCT(id) FROM hotel")
    myresult = mycursor.fetchall()
    
    Id=[x[0] for x in myresult]

    idSUr=[]
    for i in Id:
        mycursor = mydb.cursor()
        mycursor.execute("""SELECT * FROM chambre LEFT JOIN reservation ON chambre.id=reservation.chambre_id WHERE (reservation.chambre_id is NULL OR chambre.id is NULL) 
                            AND number_of_nights>= %s and chambre.departure_date= %s and chambre.hotel_id=%s """,(int(numberofnight),date_time_obj.date(),i))
        myresult = mycursor.fetchall()
        if len(myresult)>=int(numberofroom):
            idSUr.append(i)
        

    hotel=[]
    
    for i in idSUr:
        mycursor.execute('SELECT name FROM hotel where id = %s',(i,))
        myresult = mycursor.fetchall()
        for j in range(len(myresult)):
           hotel.append(f'Name:{myresult[0][0]} id:{i}')


    hotelsur={}
    for i in range(len(hotel)):
        hotelsur[str(i)]=hotel[i]
    hotelsur["max"]=len(hotel)-1


    return jsonify(hotelsur)

@app.route("/reservation/<date>/<numberofnight>/<numberofroom>/<hotelid>/<id>/<password>")
def reservation(date,numberofnight,numberofroom,hotelid,id,password):

    client_id=username(id,password)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id from hotel") 
    myresult = mycursor.fetchall()

    Hotelid=[]
    for x in myresult:
        Hotelid.append(x[0])

    if int(hotelid) not in Hotelid:
        return "False"


    departuredate = datetime.datetime.strptime(date, '%Y-%m-%d')

    mycursor = mydb.cursor()
    mycursor.execute("""SELECT * FROM chambre LEFT JOIN reservation ON chambre.id=reservation.chambre_id WHERE (reservation.chambre_id is NULL OR chambre.id is NULL) 
                        AND number_of_nights>= %s and chambre.departure_date= %s and chambre.hotel_id= %s 
                        ORDER BY number_of_nights ASC""",(int(numberofnight),departuredate.date(),hotelid))
    try:
        c=0
        result = mycursor.fetchall()
        if len(result)<int(numberofroom):
            return "False"
        arrivaldate=departuredate+timedelta(days=int(numberofnight))
        
        mycursor.execute("""select * from reservation where 
                            (departure_date <= %s and  %s <= arrival_date) 
                            or (  %s <= departure_date and departure_date <= %s) 
                            or ( %s <= arrival_date and arrival_date <=  %s)""",(departuredate.date(),departuredate.date(),departuredate.date(),arrivaldate.date(),departuredate.date(),arrivaldate.date()))
        adelete=mycursor.fetchall()
        for i in adelete:
            cancel(i[0],"","")
             
        for x in result:
            if c==int(numberofroom):
                break
            
            sql = """INSERT INTO reservation 
                    (hotel_id,chambre_id,departure_date,arrival_date,client_id) 
                    VALUES 
                    (%s,%s,%s,%s,%s)"""
            val = (hotelid,x[0],departuredate.date(),arrivaldate.date(),client_id)
            mycursor.execute(sql, val)
            mydb.commit()
            c+=1

    except TypeError:
        return "False"
    mydb.commit()
    return "True"

@app.route("/cancel/<idreserv>/<id>/<password>")
def cancel(idreserv,id,password):

    mycursor = mydb.cursor()

    try:
        sql = "DELETE FROM reservation WHERE id=%s"
        mycursor.execute(sql,(int(idreserv),))
        mydb.commit()
    except TypeError:
        return "False"
    
    mydb.commit()
    return "True"



if __name__ == "__main__":
    app.run(host="0.0.0.0",port="9999")