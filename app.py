
from flask import Flask,flash
from flask import Blueprint, render_template, url_for,request,redirect


from flask_sqlalchemy import SQLAlchemy



from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer,ListTrainer
import os


from googletrans import Translator
translator = Translator()




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasesqlite.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class databasesqlite(db.Model):
   
   name = db.Column(db.String(100),primary_key = True)
   pwd = db.Column(db.String(50),primary_key=True)
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

    cursor=databasesqlite.query.filter_by(name=name);
    print(cursor)
    if cursor:
        return render_template('sampleNLP.html')
    else:
        return render_template('create-account.html')


@app.route('/signup',methods=["POST"])
def signup_post():

        account = databasesqlite(request.form['name'], request.form['pwd'],request.form['email'],request.form['no'])
         
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
    # print(userText) 
    # result=translator.translate(str(userText), dest='en')
    # userText1=result.text
    # print(userText1)
    response = str(english_bot.get_response(userText))


    # response=translator.translate(response, dest=result.src)

    return str(response)

if __name__ == "__main__":
    db.create_all()
    
    app.run(host='0.0.0.0')