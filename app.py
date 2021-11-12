from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import datetime

app = Flask(__name__)
api = Api(app)

"""First Day of the Year is 0"""
callendars = [
 {"year":2021, "name":"PL", "holidays":[1,2,10,11,303,306,307]},
 {"year":2022, "name":"PL", "holidays":[1,2,10,11,303,306,307]},
 {"year":2021, "name":"GS", "holidays":[3]},
 {"year":2022, "name":"GS", "holidays":[3]}
]

parser = reqparse.RequestParser()
parser.add_argument("days", type=int)
parser.add_argument("date")
parser.add_argument("type")

def pickupCallendar(year, name):
  for callendar in callendars:
    if (callendar["year"]==year and callendar["name"]==name):
      return callendar
  return []

def join2Callendars(callendarFirst, callendarSecond):
  setFirst = set(callendarFirst)
  setSecond = set(callendarSecond)
  inSecondOnly = setSecond - setFirst
  return callendarFirst + list(inSecondOnly)

def joinCallendars(callendarNames, year, callendarTypes):
  joinCallendar = []
  for callendarName in callendarNames:
    for callendarType in callendarTypes:
      joinCallendar = join2Callendars(joinCallendar, pickupCallendar(year, callendarName)[callendarType])
  return joinCallendar

def countDate(year, dayOfTheYear):
  dateFirstDayOfTheYear = datetime.datetime.strptime("01-01-"+year,"%d-%m-%Y")
  return dateFirstDayOfTheYear + datetime.timedelta(days=dayOfTheYear) 

def countDayOfTheYear(date):
  dateFirstDayOfTheYear = datetime.datetime.strptime("01-01-"+str(date.year),"%d-%m-%Y")
  return (date - dateFirstDayOfTheYear).days+1

def addWorkingDays(date, days, callendarNames):
  dateBegin = datetime.datetime.strptime(date,"%d-%m-%Y")
  dateDayOfTheYear = int(countDayOfTheYear(dateBegin))
  dateDayOfTheYearAfterDays = dateDayOfTheYear+days
  daysAbs = abs(days)
  while (daysAbs > 0): 
    """print("("+str(days)+") "+str(dateBegin))"""
    """if not(dateDayOfTheYear in pickupCallendar(dateBegin.year, "PL")["holidays"]):"""
    if not(dateDayOfTheYear in joinCallendars(callendarNames, dateBegin.year, ["holidays"])):
      daysAbs = daysAbs - 1
    """else:
      print("Holiday")
    """
    if (days > 0):
      dateBegin = dateBegin+datetime.timedelta(days=1)
    else:
      dateBegin = dateBegin-datetime.timedelta(days=1)
    dateDayOfTheYear = int(countDayOfTheYear(dateBegin))
  return dateBegin

def remWorkingDays(date, days, callendarNames):
  dateBegin = datetime.datetime.strptime(date,"%d-%m-%Y")
  dateDayOfTheYear = int(countDayOfTheYear(dateBegin))
  dateDayOfTheYearAfterDays = dateDayOfTheYear+days
  while (days > 0): 
    """print("("+str(days)+") "+str(dateBegin))"""
    if not(dateDayOfTheYear in joinCallendars(callendarNames, dateBegin.year, ["holidays"])):
      days = days - 1 
    """else:
      print("Holiday")
    """
    dateBegin = dateBegin-datetime.timedelta(days=1)
    dateDayOfTheYear = int(countDayOfTheYear(dateBegin))
  return dateBegin
  
"""
print(countDate("2021", 10))
print(countDayOfTheYear(datetime.datetime.strptime("30-10-2021","%d-%m-%Y")))
print(str(datetime.datetime.strptime("30-12-2021","%d-%m-%Y"))+"("+str(10)+")")
print(addWorkingDays("30-12-2021", 10, ["PL", "GS"]))
print(addWorkingDays("13-01-2022", -10, ["PL", "GS"]))
"""

def _find_next_id():
  return max(country["id"] for couontry in countries) + 1

"""curl -i http://127.0.0.1:5000/countDate -H "Content-Type: application/json" -X GET -v -d {days:10, date:30-12-2021, type:[PL,GS]} """
class CountDate(Resource):
  def get(self):
    days = request.json["days"]
    date = datetime.datetime.strptime(request.json["date"], "%d-%m-%Y")
    type = request.json["type"]
    return jsonify({'date':str(addWorkingDays(request.json["date"], days, type))})
  def put(self):
    days = request.json["days"]
    date = datetime.datetime.strptime(request.json["date"], "%d-%m-%Y")
    type = request.json["type"]
    return jsonify({'date':str(addWorkingDays(request.json["date"], days, type))})

"""curl -i 'http://127.0.0.1:5000/countDateGet?days=10&date=30-12-2021&type=PL&type=GS' """
class CountDateGet(Resource):
  def get(self):
    args = parser.parse_args()
    days = args["days"]
    date = args["date"]
    type = request.args.getlist("type")
    return jsonify({'date':str(addWorkingDays(date, days, type))})

api.add_resource(CountDate, '/countDate')
api.add_resource(CountDateGet, '/countDateGet')

if __name__ == '__main__':
  app.run(debug=True)
