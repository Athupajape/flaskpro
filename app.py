from flask import Flask,render_template,request,flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml
import os

app = Flask(__name__)
Bootstrap(app)

db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] ='DictCursor'
mysql=MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24) 

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:

            form = request.form
            name = form['name']
            age = form['age']
            
            cur = mysql.connection.cursor()
            
            cur.execute("INSERT INTO employee(name,age) VALUES(%s,%s)",(name,age))
            mysql.connection.commit()
            flash('Successfully implemented data','success')
        except:
            flash('Failed to insert data','danger')    
    return render_template('index.html')

@app.route('/employees')
def employees():
    cur=mysql.connection.cursor()
    result_value=cur.execute("SELECT * FROM employee")
    if result_value > 0:
        employees = cur.fetchall()
        
        return render_template('employees.html',employees=employees)




if __name__=="__main__":
    app.run(debug=True,port=5001)  


#session['username'] = employees[0]['name']    
 
#
#password=form['password']
#from werkzeug.security import generate_password_hash
#name = generate_password_hash(name)