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
    if request.method == 'POST' and 'weight' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calc_bmi(weight, height)
        create(weight,height,bmi)
    return render_template("bmi_calc.html",
	                        bmi=bmi)
@app.route('/add', methods=['POST'])
def create(weight1,height1,bmi1):
    try:
        json={'bmi': bmi1, 'height': height1, 'weight':weight1}
        id = uuid.uuid1()
        users_bmi.document(str(id)).set(json)
        return json
    except Exception as e:
        return f"An Error Occurred: {e}"
def calc_bmi(weight, height):
    return round((weight / ((height / 100) ** 2)), 2)

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run()
