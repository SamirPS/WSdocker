from flask import Flask, session, redirect, url_for, request,render_template
import mysql.connector
import requests



app = Flask(__name__)

mydb = mysql.connector.connect(
  host="db",
  user="test",
  password="test",
  database="lolmdr10_ws"
)
def username(id,password):

    mycursor = mydb.cursor()

    try:
        mycursor.execute('SELECT id FROM client where username = %s and password= %s',(id,password))
        myresult = mycursor.fetchone()
        return myresult[0]
    except TypeError:
        return -1

@app.errorhandler(404) 
def invalid_route(e): 
    return redirect(url_for("login",url="index"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if username(request.form["username"],request.form['password'])==-1:
            return redirect(url_for('index'))
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for(request.args.get('url')))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/filter',methods=['GET', 'POST'])
def index():
    
    if 'username' in session and 'password' in session:
        if request.method=="GET":
            return '''
        <form method="post">
            <p> Date de début
            <p><input type="date" id="start" name="start" required>
            <p> Nombre de nuit
            <p><input type=number name=nbrofnight required >
            <p> Nombre de chambres 
            <p><input type=number name=nbrroom required >
            <p><input type=submit value=Login>
        </form>
    '''
        url=f'http://tomcat:8080/Hotel/services/A/information?rentaldate={request.form["start"]}&numberofnights={request.form["nbrofnight"]}&numberofrooms={request.form["nbrroom"]}&username={session["username"]}&password={session["password"]}'
        myget=requests.get(url)
        
        start = '<ns:return>'
        end = '</ns:return>'
        s = myget.text
        if "FOUND" in s.upper():
            return s
        
        c=(s.split(start))[1].split(end)[0]
        html=""
        try:
            nom=c.split("Name:")
            for i in nom :
                if i!="":
                    html+=f'<p>{i}'
                    
            return html
        except:
            return myget.text
        
    return redirect(url_for("login",url="index"))


@app.route('/reserv',methods=['GET', 'POST'])
def reserv():
    
    if 'username' in session and 'password' in session:
        if request.method=="GET":
            return '''
        <form method="post">
            <p> Date de début
            <p><input type="date" id="start" name="start" required>
            <p> Nombre de nuit
            <p><input type=number name=nbrofnight required >
            <p> Nombre de chambres 
            <p><input type=number name=nbrroom required >
            <p> Hotelid 
            <p><input type=number name=idhotel required >
            <p><input type=submit value=Login>
        </form>
    '''
        url=f'http://tomcat:8080/Hotel/services/A/reservation?rentaldate={request.form["start"]}&numberofnights={request.form["nbrofnight"]}&numberofrooms={request.form["nbrroom"]}&hotelid={request.form["idhotel"]}&username={session["username"]}&password={session["password"]}'
        myget=requests.get(url)
        mydb.commit()
        if "True" in myget.text:
            return "Reservation successful"
        return  f'Reservation error or the hotel {request.form["idhotel"]} is not available'
        
    return redirect(url_for("login",url="reserv"))

@app.route('/cancel',methods=['GET', 'POST'])
def cancel():
    
    if 'username' in session and 'password' in session:
        if request.method=="GET":
            mycursor = mydb.cursor()
            client_id=username(session["username"],session["password"])
            mycursor.execute('SELECT * FROM reservation where client_id=%s',(int(client_id),))
            myresult = mycursor.fetchall()
            s=[]
            for x in myresult:
                print(x)
                s.append(" ".join(str(i) for i in x))
            return render_template('cancelget.html',reserv=s)

        annulation=request.form.getlist('reservation')
        for i in annulation:
            id=i.split(" ")
            url=f'http://tomcat:8080/Hotel/services/A/cancel?id={id[0]}&username={session["username"]}&password={session["password"]}'
            myget=requests.get(url)
            
            if "False" in myget.text:
                return "False"
        mydb.commit()
        return "True"
        
    return redirect(url_for("login",url="cancel"))
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login',url="index"))



# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)