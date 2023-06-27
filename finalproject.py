from flask import Flask, render_template, request, redirect, url_for
from flask import *
import mysql.connector
import boto3
from datetime import datetime
from itertools import product
current_date_time=datetime.now()
application= Flask(__name__)
application.secret_key='abcd'


db = mysql.connector.connect(
    host="project.cpdjhrsd9kzg.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Project123",
    database="finalprojectdb")

cursor = db.cursor(buffered=True)


@application.route('/', methods=['GET', 'POST'])
def home():
    
    return render_template("homeums.html")


#admin - Login
@application.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    message = ''
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        password = request.form['password']

        query = "SELECT * FROM admindetail WHERE admin_name = %s AND password = %s"
        values = (admin_name, password)
        cursor.execute(query, values)
        admin = cursor.fetchone()

        if admin:
            
            return redirect('/admindashboard')
        
        else:
            message = "Invalid credentials"
            print("Admin login failed. admin_name:", admin_name, "password:", password)
    return render_template('adminlogin.html', message=message)
         

#this is code for user register and  login

@application.route('/userregister', methods=['GET', 'POST'])
def userregister():
    message = ''
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        email_id = request.form['email_id']
        
        query = "SELECT * FROM userdetails WHERE user_id = %s AND password = %s AND email_id = %s"
        values = (user_id, password, email_id)
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if not result:
            query = "INSERT INTO userdetails (user_id, password, email_id) VALUES (%s, %s, %s)"
            values = (user_id, password, email_id)
            cursor.execute(query, values)
            db.commit()
            
            return redirect(url_for('userlogin', message=message))
            
        else:
            message = "User already exists"
            return render_template('userregister.html', message=message)
    
    return render_template('userregister.html', message=message)

@application.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    message=''
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        email_id = request.form['email_id']

        
        query = "SELECT * FROM userdetails WHERE user_id = %s AND password = %s AND email_id = %s"
        values = (user_id, password,email_id)
        cursor.execute(query, values)
        user = cursor.fetchone()
        
        if user:
            session['user_id']=user[0]
            return redirect(url_for('userdashboard'))
            
            
        else:
            message="Invalid User_id or Password or email_id"
            
            
            
    return render_template('userlogin.html',message=message)
@application.route('/userdashboard', methods=['GET', 'POST'])
def userdashboard():
    return render_template("userdashboard.html")


   
    



if __name__=='__main__':
    application.run(debug=True)
    
    
    application.run('0.0.0.0',7900)