from flask import Flask, render_template, request
import json, requests
from battle import bracketBattle1, winnersR1, bracketBattle2, winnersR2, bracketBattle3, winnerR3, finalBattle, ultimateWinner
from ppp import get_data
import pygal


app = Flask('app')

currSymbols =[]

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/edu')
def education():
  return render_template("education.html")

@app.route('/exp')
def experience():
  return render_template("experience.html")
  
@app.route('/pyportfolio')
def pyport():
  return render_template("pyportfolio.html")

@app.route('/robots')
def game():
    battles = bracketBattle1()
    round1 = winnersR1()
    round2 = bracketBattle2()
    winners_R2 = winnersR2()
    list3 = bracketBattle3()
    winner_R3 = winnerR3()
    finalist = finalBattle()
    ultimate_Winner = ultimateWinner()
    return render_template("robobracketbattle.html",battles=battles, round1 = round1, round2=round2, winners_R2 = winners_R2, list3=list3, winner_R3=winner_R3, finalist=finalist,ultimate_Winner=ultimate_Winner)
  
@app.route('/bigmac')
def big_mac():
  data = get_data()

  #Currencies for each country, hard coded country codes. work later on this. 
  symbol1 = data[0]['currencies']['CAD']['symbol']
  symbol2 = data[3]['currencies']['INR']['symbol']
  symbol3 = data[6]['currencies']['UAH']['symbol']
  symbol4 = data[9]['currencies']['TRY']['symbol']

  currSymbols.append(symbol1)
  currSymbols.append(symbol2)
  currSymbols.append(symbol3)
  currSymbols.append(symbol4)

  bar_chart = pygal.Bar()
  bar_chart.title = 'Purchasing Power of various countries'
  bar_chart.add(data[0]['country_name'], data[0]['dollar_ppp'])
  bar_chart.add(data[3]['country_name'], data[3]['dollar_ppp'])
  bar_chart.add(data[6]['country_name'], data[6]['dollar_ppp'])
  bar_chart.add(data[9]['country_name'], data[9]['dollar_ppp'])
  bar_chart.render_to_file('static/images/ppp_chart.svg') 
  
  return render_template("bigmac.html",data=data, currSymbols = currSymbols)


filename = "bmidata.json"
@app.route('/bmi', methods = ['POST', 'GET'])
def bmical():
  filename = "bmi_log.json" #sidney - I added this so the log in BMI would work
  bmidata = []
  bmi = ''
  if request.method == 'POST' and 'weight' in request.form and 'height' in request.form:
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    bmi = round((weight / ((height / 100) ** 2)), 2)
    bmidata.append(bmi)
    with open(filename, 'w') as jsonFile:
      jsonFile.write(json.dumps(bmidata, indent=3))
  return render_template("Bmi.html", bmi=bmi)

filename = "weather.json"

#My Api Id is c17856fae46dcfdee7fb3ae1a4301558
@app.route('/weather', methods = ['GET', 'POST'])
def city_weather():
  list_cityWeatherData = []   # create an empty list to store the api data.
  Temp = ''
  celsius = ''
  if request.method == 'POST' and 'city' in request.form:
    city = request.form.get('city')  #storing the form value to a variable
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},CA&appid=c17856fae46dcfdee7fb3ae1a4301558'
    res = requests.get(url).json()

    #writing data to json file
    list_cityWeatherData.append(res)
    with open(filename, 'w') as jsonFile:
      jsonFile.write(json.dumps(list_cityWeatherData, indent=3))
    
    Temp = res.get('main', {}).get('temp') 

  # Temp = list_cityWeatherData['main']['temp'] 
    celsius = round((Temp - 273.15), 0) #converting temperature to degree celcius
  else:
    celsius = {}
  return render_template("weather.html",Temp = celsius)

app.run(host='0.0.0.0', port=8080)




















