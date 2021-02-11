#!python3
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


@app.route('/', methods=['GET', 'POST'])
def index():
    bmi = ''
    output=''
    if request.method == 'POST' and 'weight' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calc_bmi(weight, height)
        json = {'bmi': bmi, 'height': height, 'weight': weight}
        id = uuid.uuid1()
        users_bmi.document(str(id)).set(json)
        if (bmi <= 18.5): 
            output = "Under Weight"
        elif (bmi > 18.5 and bmi <= 24.9):
            output = "Normal Weight"
        elif (bmi > 24.9 and bmi <= 29.9):
            output = "Over Weight"
        elif (bmi > 30.0):
            output = "OBESE"
    return render_template("index.html",
                           bmi=bmi,output=output)


def calc_bmi(weight, height):
    return round((weight / ((height / 100) ** 2)), 2)


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run()
