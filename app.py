
from flask import Flask,flash
from flask import Blueprint, render_template, url_for,request,redirect


from flask_sqlalchemy import SQLAlchemy



from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer,ListTrainer
import os


from googletrans import Translator
translator = Translator()


# import demoji
# demoji.download_codes()


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasesqlite.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class databasesqlite(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   pwd = db.Column(db.String(50))
   email=db.Column(db.String(50))
   no=db.Column(db.String(50))
   
   def __init__(self, name, pwd,email,no):
        self.name = name
        self.pwd = pwd
        self.email = email
        self.no = no

    

english_bot = ChatBot('Bot',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
   
],
trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)


for file in os.listdir('data'):
    convData = open('data/' + file).readlines()
    english_bot.train(convData)


@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login',methods=["POST"])
def login_post():
    name=request.form['name']
    password=request.form['pwd']

    cursor=databasesqlite.query.filter_by(name=name,pwd=password).all()
    if cursor:
        nam=name
        return render_template('sampleNLP.html',name=name)
    else:
        return render_template('create-account.html')


@app.route('/signup',methods=["POST"])
def signup_post():

        account = databasesqlite(request.form['name'], request.form['pwd'],request.form['email'],request.form['no'])
        user= databasesqlite.query.filter_by(name=request.form['name']).first()
        if user:
            print("user already existed")
            return render_template('create-account.html')
        else:
            db.session.add(account)
            db.session.commit()
            return render_template('index.html')
        

@app.route('/chatbot')
def chatbot():

    return render_template('sampleNLP.html')


@app.route('/signup')
def signup():
    return render_template('create-account.html')



@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(userText) 
    # result=translator.translate(str(userText), dest='en')
    # userText1=result.text
    # print(userText1)
    response = str(english_bot.get_response(userText))


    # response=translator.translate(response, dest=result.src)

        
    return str(response)

if __name__ == "__main__":
    db.create_all()
    
    app.run(host='127.0.0.1')