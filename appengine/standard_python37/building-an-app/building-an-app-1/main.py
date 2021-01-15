# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import datetime

from flask import Flask, render_template

app = Flask(__name__)

# Username -> nickname dictionary
usertable = {
    "defaultusername": "defaultname"
}

words = [
    "小米"
]

peoplenum = 7

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/form')
def form():
    return render_template('index.html')
# [END form]

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      password = request.form['password']
      if (user in usertable):
          if (usertable[user] != password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!")
      else:
          usertable[user] = password
      return render_template('index.html', word="", randomseed=0, user=user, password=password)
   else:
      user = request.args['name']
      password = request.args['password']
      if (user in usertable):
          if (usertable[user] != password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!")
      else:
          usertable[user] = password
      return render_template('index.html', word="", randomseed=0, user=user, password=password)

@app.route('/setupgame', methods=['POST'])
def receiveword():
    peoplenum = request.form['peoplenum']
    # [END submitted]
    # [START render_template]
    return render_template('index.html', word="", randomseed=0, user=user, password=password)
    # [END render_template]

@app.route('/receiveword', methods=['POST'])
def receiveword():
    user = request.form['name']
    password = request.form['password']
    if (user in usertable):
          if (usertable[user] != password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!")
    else:
        return render_template('index.html', word="", randomseed=0, user="Login fail!", password="User not exist!")
    word = "小米"
    randomseed = 100
    
    # [END submitted]
    # [START render_template]
    return render_template('index.html', word=word, randomseed=randomseed, user=user, password=password)
    # [END render_template]

@app.route('/changeword', methods=['POST'])
def changeword():
    user = request.form['name']
    password = request.form['password']
    if (user in usertable):
          if (usertable[user] != password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!")
    else:
        return render_template('index.html', word="", randomseed=0, user="Login fail!", password="User not exist!")
    word = "大米"
    randomseed = 200
    
    # [END submitted]
    # [START render_template]
    return render_template('index.html', word=word, randomseed=randomseed, user=user, password=password)
    # [END render_template]

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
