import csv
import os

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField

app = Flask(__name__, template_folder='template',static_folder='template/assets')
app.config['UPLOAD_FOLDER'] = 'static'
app.config['SECRET_KEY'] = 'supersecretkey'


class uploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload File')


@app.route('/', methods=['GET', "POST"])
@app.route('/pt', methods=['GET', "POST"])
def home():
    form = uploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        print(file.name)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                  app.config['UPLOAD_FOLDER'], secure_filename('c.csv')))  # Then save the file
        
        df = pd.read_csv(r'static/c.csv')
        day = pd.read_csv(r'day1.csv')
        df = np.array(df, dtype='S')
        df = np.char.lower(df)
        day = np.array(day, dtype='S')
        day = np.char.lower(day)
        z = np.setdiff1d(df, day)
        data = []
        for i in range(0, z.size):
            data.append(z[i].decode("utf-8"))
        initital = df.size
        final = z.size
        data.append(f'initial shortlis: {initital}')
        data.append(f'final shortlist: {final}')
        return render_template('pt.html',data =data)


    return render_template('upload.html', form=form)




app.run(host='0.0.0.0',port=8080)
