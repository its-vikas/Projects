import requests
import json
import os
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
print("Hello")

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class City(db.Model):
    __tablename__='weather'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

    def __init__(self,name):
        self.name=name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
    cities=City.query.all()
    print(cities)
    old_city=City.query.get(2)
    db.session.delete(old_city)
    db.session.commit()
    weather_data = []
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=Metric&appid=e17aeb5fc72066992e736c0a9ee96263'
    for city in cities:
        print(city.name)
        data=requests.get(url.format(city.name),verify=False).json()
        #result=json.dumps(data,indent=4)
        #print(result)
        weather={
            'city':city.name,
            'temp':data['main']['temp'],
            'description':data['weather'][0]['description'],
            'humidity':data['main']['humidity'],
            'icon':data['weather'][0]['icon'],
            'speed':data['wind']['speed']
        }
        weather_data.append(weather)
        print(weather_data)

    return render_template('weath.html', weather_data=weather_data)
if __name__=='__main__':
    app.run(debug=True)
