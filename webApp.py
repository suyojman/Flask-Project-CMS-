from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from data import Articles
import mysql.connector
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

app=Flask(__name__)

#config Mysql
mydb=mysql.connector.connect(
	host='localhost',
	user='root',
	passwd="",
	database="myflaskapp"
	)

Articles=Articles()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/article')
def article():
	return render_template('article.html',articles=Articles) 

class RegisterForm(Form):
	name=StringField('Name',[validators.Length(min=1,max=50)])
	username = StringField('Username',[validators.Length(min=4,max=25)])
	password=PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm',message="Password do not match")
		])
	confirm=PasswordField('Confirm Password')

@app.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm(request.form)
	if request.method =='POST'and form.validate():
		name=form.name.data
		username=form.username.data
		password=form.password.data

		mycursor=mydb.cursor()
		mycursor.execute("INSERT INTO user(name,username,password)VALUES(%s,%s,%s)",(name,username,password))

		mydb.commit()

		mycursor.close()

		flash('You are now registered !!','success')
		return redirect(url_for('login'))

	return render_template('register.html',form=form)	

@app.route('/login',methods=['GET','POST'])
def login():
	session.pop('user',None)
	print('Hello World')
	if request.method=='POST':
		session.pop('user',None)
		username=request.form['username']
		password=request.form['password']
		
		print(password)
		mycursor=mydb.cursor(buffered=True)
		print("SELECT * FROM user WHERE username= '"+username+"'")
		mycursor.execute("SELECT username,password,name FROM user WHERE username= '"+username+"'")
		result=mycursor.fetchone()
		print(result)
		if result==None:
			flash('Please enter valid username and password!!','error')
			return redirect(url_for('login'))
		elif (password)==result[1] and (username)==result[0]:
			session['user']=request.form['username']
			name=result[2]
			return render_template('dashboard.html',value=result[2],title='dash')
	
	return render_template('login.html')

@app.route('/article/<string:id>')
def articles(id):
	return render_template('articles.html',id=id) 



@app.route('/logout')
def logout():
	flash('Sucessfully Logged Out!!','success')
	session.pop('user',None)
	return redirect(url_for('login'))

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True)