#!python3
import json
import os
import uuid
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, render_template, request

app = Flask(__name__)

cred = credentials.Certificate('serviceAccountKey.json')
default_app = initialize_app(cred)
db = firestore.client()
users_bmi = db.collection('usersbmi')

app.config['DEBUG'] = True
@app.route('/')
def home_page():
    """The home page."""
    return render_template('index.html')

@app.route('/bmi', methods=['GET', 'POST'])
def index():
    bmi = ''
    output = ''
    if request.method == 'POST' and 'weight' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        username = request.form.get('smname')
        bmi = calc_bmi(weight, height)
        if (bmi <= 18.5):
            output = "Under Weight"
        elif (bmi > 18.5 and bmi <= 24.9):
            output = "Normal Weight"
        elif (bmi > 24.9 and bmi <= 29.9):
            output = "Over Weight"
        elif (bmi > 30.0):
            output = "OBESE"
        json = {'bmi': bmi, 'height': height, 'weight': weight, 'output': output, 'user':username}
        id = uuid.uuid1()
        users_bmi.document(str(id)).set(json)
    return render_template("bmi_calc.html",
                           bmi=bmi,output=output)


def calc_bmi(weight, height):
    return round((weight / ((height / 100) ** 2)), 2)

@app.route('/forgetpassword.html')
def password():

    """forgotpassword page"""

    return render_template('forgetpassword.html')


@app.route('/history', methods=['GET', 'POST'])
def getdata():
  try:
      username = request.form.get('smname')
      all_users = [doc.to_dict() for doc in users_bmi.where(u'user', u'==', 'abithavalli.offl@gmail.com').stream()]
      forallusers = json.dumps(all_users)
      cnt= len(all_users)
      return render_template("retrieve.html",jres=all_users,count=cnt)

  except Exception as e:
    return "Error: {e}"
  return render_template("retrieve.html")

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run()


