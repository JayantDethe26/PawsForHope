from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL 
from datetime import datetime 
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'PawsForHope'
mysql = MySQL(app)





@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        Username = userDetails['Username']
        Password= userDetails['Password']
        Email= userDetails['Email']
        Gender= userDetails['Gender']
        Birthdate= userDetails['Birthdate']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO `Registrations`(`Username`, `Password`,`Email`, `Gender`, `Birthdate`) VALUES (%s,%s,%s,%s,%s)",(Username,Password,Email,Gender,Birthdate))

        mysql.connection.commit()

        cur.close()
        return render_template('login.html')
    


@app.route('/login_process', methods=['GET', 'POST'])
def login_process():
    if request.method == 'POST':
        username = request.form['un']
        password = request.form['psw']

        cur = mysql.connection.cursor()
        cur.execute("SELECT Username FROM registrations WHERE Username = %s AND Password = %s", (username, password))
        x = cur.fetchone()

        cur.close()

        if x:
            session['Username'] = x[0]
            return render_template('display.html')
        else:
            return 'Invalid username/password'

    return render_template('display.html')





@app.route("/dogselling", methods=['POST'])
def dogselling():
    print("The /dogselling route is being triggered.")

    if request.method == 'POST':
        userDetails = request.form
        image = userDetails['image']
        Breed = userDetails['breed']
        Age = userDetails['age']
        Height = userDetails['height']
        Disease = userDetails['disease']
        Reason = userDetails['reason']
        Contact = userDetails['contact']
        Cost =  userDetails['cost']

        cur = mysql.connection.cursor()
       
        
        cur.execute("INSERT INTO `dogs_sell`(`Image`, `Breed`, `Age`, `Height`, `Disease`, `Reason`, `ContactNo`,`Cost`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)", (image, Breed, Age, Height, Disease, Reason,Contact,Cost))
        
        mysql.connection.commit()
        cur.close()

        return render_template('dogs.html')





        
@app.route("/showdogs", methods=['POST'])
def showdogs():
    cur = mysql.connection.cursor()
    x = request.form.get('Breed')
    cur.execute("SELECT Image, Breed, Age, Height, Disease, Reason, ContactNo, Cost FROM dogs_sell where Breed= %s",(x,))
    dogs = cur.fetchall()
    cur.close()
    return render_template('dog-buy-page.html', dogs=dogs)



@app.route("/catselling", methods=['POST'])
def catselling():
    print("The /catselling route is being triggered.")

    if request.method == 'POST':
        userDetails = request.form
        image = userDetails['image']
        Breed = userDetails['breed']
        Age = userDetails['age']
        Height = userDetails['height']
        Disease = userDetails['disease']
        Reason = userDetails['reason']
        Contact = userDetails['contact']
        Cost =  userDetails['cost']

        cur = mysql.connection.cursor()
       
        
        cur.execute("INSERT INTO `cats_sell`(`Image`, `Breed`, `Age`, `Height`, `Disease`, `Reason`, `ContactNo`,`Cost`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)", (image, Breed, Age, Height, Disease, Reason,Contact,Cost))
        
        mysql.connection.commit()
        cur.close()

        return render_template('cats.html')


@app.route("/showcats", methods=['POST'])
def showcats():
    cur = mysql.connection.cursor()
    x = request.form.get('Breed')
    cur.execute("SELECT Image, Breed, Age, Height, Disease, Reason, ContactNo, Cost FROM cats_sell where Breed= %s",(x,))
    cats = cur.fetchall()
    cur.close()
    return render_template('cat-buy-page.html', cats=cats)



@app.route("/ngo_regist", methods=['POST'])
def ngo_regist():
    

    if request.method == 'POST':
        userDetails = request.form
        Name = userDetails['ngo-name']
        Password = userDetails['Password']
        Email = userDetails['Email']
        Website = userDetails['website']
        Location = userDetails['location']
        Contact = userDetails['contact']
        Mission = userDetails['mission']
        

        cur = mysql.connection.cursor()
       
        
        cur.execute("INSERT INTO `ngo_registerations`(`Name`, `Password`, `Email`, `Website`, `Location`,`Contact`,`Mission`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (Name,Password,Email,Website,Location,Contact,Mission))
        
        mysql.connection.commit()
        cur.close()

        return render_template('ngo-login.html')



@app.route('/ngo_login_process', methods=['GET', 'POST'])
def ngo_login_process():
    if request.method == 'POST':
        Name = request.form['ngo-name']
        Password = request.form['psw']

        cur = mysql.connection.cursor()
        cur.execute("SELECT Name FROM ngo_registerations WHERE Name = %s AND Password = %s", (Name, Password))
        x = cur.fetchone()

        cur.close()

        if x:
            session['Name'] = x[0]
            return render_template('ngo-homepage.html')
        else:
            return 'Invalid username/password'

    return render_template('ngo-homepage.html')


@app.route("/showngos")
def showngos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name,Email,Website,Location,Contact,Mission FROM ngo_registerations")
    ngos = cur.fetchall()
    cur.close()
    return render_template('ngo-listings.html', ngos=ngos)


featured_pets = [
    {
        'name': 'Buddy',
        'breed': 'Labrador Retriever',
        'age': 3,
        'image': 'images/home/golden-retriever.jpg'
    },
    {
        'name': 'Luna',
        'breed': 'Maine Coon',
        'age': 2,
        'image': 'images/home/siamese.jpg'
    },
    # Add more pet data as needed
]





@app.route('/')
def home():
    return render_template('home.html', featured_pets=featured_pets)

@app.route('/ngo_register')
def ngo_register():
    return render_template('ngo-register.html')

@app.route('/ngo_login')
def ngo_login():
    return render_template('ngo-login.html')

@app.route('/ngo_displaypage')
def ngo_displaypage():
    return render_template('ngo-displaypage.html')


@app.route('/ngo_homepage')
def ngo_homepage():
    return render_template('ngo-homepage.html')


@app.route('/ngo_adoption')
def ngo_adoption():
    return render_template('ngo-adoption.html')


@app.route('/ngo_donation')
def ngo_donation():
    return render_template('ngo-donation.html')

@app.route('/ngo_education')
def ngo_education():
    return render_template('ngo-education.html')

@app.route('/ngo_volunteer')
def ngo_volunteer():
    return render_template('ngo-volunteer.html')

@app.route('/ngo_rescue')
def ngo_rescue():
    return render_template('ngo-rescue.html')


@app.route("/regist")
def regist():
    return render_template('register.html')


@app.route("/login_prossess")
def login_prossess():
    return render_template('display.html')



@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/display")
def display():
    return render_template('display.html')



@app.route("/dogs")
def dogs():
    return render_template('dogs.html')



@app.route("/cats")
def cats():
    return render_template('cats.html')




@app.route("/dog-sell")
def dogsell():
    return render_template('dog-sellingpage.html')


@app.route('/dog-sellingpage')
def dog_selling_page():
    return render_template('dog-sellingpage.html')


@app.route("/cat-sell")
def catsell():
    return render_template('cats-sellingpage.html')


@app.route('/cats-sellingpage')
def cats_selling_page():
    return render_template('cats-sellingpage.html')


if __name__ == "__main__":
    app.run(debug=True)