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

# [START gae_python38_render_template]
# [START gae_python3_render_template]
import datetime

from flask import Flask, render_template, request

app = Flask(__name__)
variable_dict = {}
log = ""
history = []

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/submit', methods=['POST'])
def submit_textarea():
    input_str = request.form["usercode"]
    operator(input_str)
    return render_template('index.html', this_history=history)

def operator(input_str):
    code_in_for_loop = ""
    target_iter = 1
    iter_value = -1
    global variable_dict
    for line in input_str.split('\n'):
        variable, init_value = findIntDefinition(line)
        loop_iter = findForLoop(line)
        loop_end = findForLoopEnd(line)
        plus = findPlusOperation(line)
        if (variable != ""):
            variable_dict[variable] = init_value
            reporter()
        elif (loop_iter > -1):
            iter_value = 0
            target_iter = loop_iter
        elif (loop_end > -1):
            for index in range(target_iter):
                operator(code_in_for_loop)
            code_in_for_loop = ""
            target_iter = 1
            iter_value = -1
        elif (iter_value > -1):
            code_in_for_loop += line + "\n"
        elif (plus != "" and plus in variable_dict):
            variable_dict[plus] = variable_dict[plus] + 1
            reporter()

def reporter():
    global log
    global history
    log = log + "===========================================\n"
    for variable in variable_dict:
        log = log + "[" + variable + "|" + str(variable_dict[variable]) + "]\n"
    log = log + "===========================================\n"
    history.append(variable_dict)

def findIntDefinition(input_str):
    p = re.compile(r'int \w+ = \d+;')
    m = p.match(input_str)
    if m == None:
        return "", -1
    p1 = re.compile(r'=')
    m1 = p1.search(input_str)
    equal_index = m1.start()
    p2 = re.compile(r';')
    m2 = p2.search(input_str)
    pointer2_index = m2.start()
    variable = input_str[4:equal_index-1]
    init_value = input_str[equal_index+2:pointer2_index]
    return variable, int(init_value)

def findForLoop(input_str):
    p = re.compile(r'for \(int \w+ = 0; \w+ < \d+; \w+\+\+\) \{')
    m = p.match(input_str)
    if m == None:
        return -1
    p1 = re.compile(r'<')
    m1 = p1.search(input_str)
    pointer1_index = m1.end()
    p2 = re.compile(r'; \w+\+\+\)')
    m2 = p2.search(input_str)
    pointer2_index = m2.start()
    iter_value = input_str[pointer1_index+1:pointer2_index]
    return int(iter_value)

def findForLoopEnd(input_str):
    p = re.compile(r'\}')
    m = p.match(input_str)
    if m == None:
        return -1
    return 1

def findPlusOperation(input_str):
    p = re.compile(r'\w+\+\+;')
    m = p.match(input_str)
    if m == None:
        return ""
    p1 = re.compile(r'\+\+')
    m1 = p1.search(input_str)
    plus_index = m1.start()
    variable = input_str[:plus_index]
    return variable

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_render_template]
# [END gae_python38_render_template]
