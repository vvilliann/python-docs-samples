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

# [START gae_python37_app]
from flask import Flask
import random

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

roommembertable = {
    "reserved": {}
}

roomidentitytable = {
    "reserved": []
}

roomuserlisttable = {
    "reserved": []
}

currturn = {
    "reserved": "0-0"
}

currlady = {
    "reserved": "someuser"
}

usertable = {
    "defaultusername": "defaultname"
}

# Game config explanation:
# O: Oberon; M: Merlin; P: Percival; X: Mordrad; L: Lancelot-Good; l: Lancelot-Bad;
# A: Assassin; Y: Loyalty; N: Minion; G: Morgana;
# p: Bad Percival - cannot see other bad people, can see merlin and morgana
# H: Liu De Hua - he is a bad people, can only vote success. Merlin or other bad people cannot see him. He knows Mordrad and Mordrad knows him.
# W: Liang Chao Wei - he is a good people, can only vote fail. He knows Merlin and Merlin knows him.
# K: last bit, if K means we have lake lady, if it is k it means we don't have lake lady.

configtable = {
    "reserved": "OMPAYYG"
}

# status code: available/ready(to join)/in game/finished
roomstatus = {
    "reserved": "available"
}

@app.route('/yin')
def hellomaster():
    """Return a friendly HTTP greeting."""
    return "Hello Master!"

@app.route('/other')
def helloguys():
    """Return a friendly HTTP greeting."""
    return "Hello Guys!"

@app.route('/registeruser/<username>/<nickname>/<room>')
def registeruser(username, nickname, room):
    """Return an existing room information."""
    usertable[username] = nickname
    if (roommembertable.contains_key(room)):
        if (len(roommembertable[room]) == len(configtable[room]) - 1):
            return "room full!"
        roommembertable[room].add(username)
        outputstr = ""
        for user in roommembertable[room]:
            outputstr = outputstr + user + "|"
        return outputstr + "|" + configtable[room]
    return "room not available!"

@app.route('/registerroom/<username>/<nickname>/<room>/<config>')
def registerroom(username, nickname, room, config):
    """Returns whether room is available."""
    usertable[username] = nickname
    if (roommembertable.contains_key(room) && roomstatus[room] == "in game"):
        return "room " + room + " is not available!"
    roommembertable[room] = {}
    roommembertable[room].add(username)
    roomstatus[room] = "available"
    
@app.route('/startgame/<username>/<room>')
def startgame(username, room):
    """Starts a game. Enters into game page."""
    if (roomstatus[room] != "in game")
        roomstatus[room] = "in game"
        # Initialize the game setup
        # Initialize the seats
        userlist = list(roommembertable[room])
        currsize = len(userlist)
        roomuserlisttable[room] = []
        while (currsize > 0):
            randindex = random.randint(0, currsize - 1)
            roomuserlisttable[room].append(userlist[randindex])
            userlist.remove(userlist[randindex])
            currsize--
        # Initialize the identity
        currsize = len(configtable[room]) - 1
        configstr = configtable[room]
        roomidentitytable[room] = ""
        while (currsize > 0):
            randindex = random.randint(0, currsize - 1)
            roomidentitytable[room] = roomuserlisttable[room] + configstr[randindex]
            configstr.replace(configstr[randindex], '')
            currsize--
        # Initialize the turn counter
        currturn[room] = "1-1"
        # Initialize the lake lady
        if (configstr[0] == 'K'):
            currlady[room] = roomuserlisttable[room][len(roomuserlisttable[room]) - 1]
        else:
            currlady[room] = "nobody"
    return generatecurrentinfo(room)

def printnamelist(namelist):
    """Given a list of name, return a single string with | as spliter."""
    outputstr = ""
    for name in namelist:
        outputstr = outputstr + name + "|"
    return outputstr

def generatecurrentinfo(room):
    outputstr = printnamelist(roomuserlisttable[room]) + "||"
    outputstr = outputstr + roomidentitytable[room] + "||"
    outputstr = outputstr + currturn[room] + "||"
    outputstr = outputstr + currlady[room] + "||"    
    
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
