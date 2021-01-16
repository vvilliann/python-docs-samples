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
import random

from flask import Flask, render_template, request

app = Flask(__name__)

# Username -> nickname dictionary
usertable = {
    "defaultusername": "defaultname"
}

words = [
    ["小米", "大米"],
    ["任天堂Switch", "索尼PS5"],
    ["沙尘暴", "雾霾"],
    ["亚利桑那", "路易斯安那"],
    ["波多黎各", "关岛"],
    ["法拉第", "特斯拉"],
    ["伏特加", "朗姆酒"],
    ["微软", "亚马逊"],
    ["海参", "海星"],
    ["引力波", "黑洞"],
    ["宠物小精灵", "皮卡丘"],
    ["多山", "地震"],
    ["跨性别者", "双性恋"],
    ["列宁", "恩格斯"],
    ["刘邦", "陈胜"],
    ["金瓶梅", "西厢记"],
    ["白鹭", "天鹅"],
    ["Napa", "Mission Peak"],
    ["无人机", "大疆"],
    ["小白", "Jefferey Zhao"],
    ["王维", "李白"],
    ["腰果", "香蕉"],
    ["绿宝石", "翡翠"],
    ["南北朝", "五代十国"],
    ["商朝", "周朝"],
    ["自由女神", "圣女贞德"],
    ["趾甲", "指甲"],
    ["石膏", "大理石"],
    ["维纳斯", "雅典娜"],
    ["吸血鬼", "蚊子"],
    ["诸葛亮", "孙权"],
    ["《What does the fox say》", "《江南》"],
    ["一夜狼人", "剧本杀"],
    ["罗密欧", "高帅富"],
    ["马卡龙", "提拉米苏"],
    ["肠粉", "煲仔饭"],
    ["澳门", "大西洋城"],
    ["古驰Gucci", "香奈儿Channel"],
    ["蚕蛾", "蚕茧"],
    ["指挥棒", "长笛"],
    ["杨玉环", "王昭君"],
    ["纽约时报", "卫报"],
    ["华陈鹤立", "司马相如"],
    ["人妖", "太监"],
    ["Python", "Javascript"],
    ["猎豹", "鬣狗"],
    ["非洲", "埃及"],
    ["复活节", "愚人节"],
    ["美人鱼", "半人马"],
    ["天皇", "沙皇"]
]

identity = [0, 1] # 1 is spy, 0 is normal, 2 is idiot
identity_table = {
    "dummy_name" : 0,
    "dummy_spy" : 1,
}

peoplenum = 7
spynum = 2
seed = 0

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
          if not (usertable[user] == password):
              return render_template('index.html', word="", randomseed=seed, user="Login fail!", password="Password wrong!", peoplenum=peoplenum, spynum=spynum)
      else:
          usertable[user] = password
      return render_template('index.html', word="", randomseed=seed, user=user, password=password, peoplenum=peoplenum, spynum=spynum)
   else:
      user = request.args['name']
      password = request.args['password']
      if (user in usertable):
          if not (usertable[user] == password):
              return render_template('index.html', word="", randomseed=seed, user="Login fail!", password="Password wrong!", peoplenum=peoplenum, spynum=spynum)
      else:
          usertable[user] = password
      return render_template('index.html', word="", randomseed=seed, user=user, password=password, peoplenum=peoplenum, spynum=spynum)

@app.route('/setupgame/<user>/<password>', methods=['POST'])
def setupgame(user, password):
    if (user in usertable):
          if not (usertable[user] == password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!", peoplenum=peoplenum, spynum=spynum)
    else:
        return render_template('index.html', word="", randomseed=0, user="Login fail!", password="User not exist!", peoplenum=peoplenum, spynum=spynum)
    
    peoplenum = int(request.form['peoplenum'])
    spynum = int(request.form['spynum'])
    currsize = len(words)
    seed = random.randint(0, currsize - 1)
    
    # Set up identity
    identity = [0] * (peoplenum + 10)
    identity_table = {}
    for iter in range(spynum):
        humanseed = random.randint(0, peoplenum - 1)
        while not (identity[humanseed] == 0):
            humanseed = random.randint(0, peoplenum - 1)
        identity[humanseed] = 1
    
    # [END submitted]
    # [START render_template]
    return render_template('index.html', word="", randomseed=seed, user=user, password=password, peoplenum=peoplenum, spynum=spynum)
    # [END render_template]

@app.route('/receiveword/<user>/<password>/<randomseed>', methods=['POST'])
def receiveword(user, password, randomseed):
    if (user in usertable):
          if not (usertable[user] == password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!", peoplenum=peoplenum, spynum=spynum)
    else:
        return render_template('index.html', word="", randomseed=0, user="Login fail!", password="User not exist!", peoplenum=peoplenum, spynum=spynum)
    
    if not (user in identity_table):
        identity_table[user] = identity[len(identity_table) - 1]
    
    your_identity = identity_table[user]
    word = words[randomseed][your_identity]
    
    # [END submitted]
    # [START render_template]
    return render_template('index.html', word=word, randomseed=randomseed, user=user, password=password, peoplenum=peoplenum, spynum=spynum)
    # [END render_template]

@app.route('/changeword/<user>/<password>', methods=['POST'])
def changeword(user, password):
    if (user in usertable):
          if not (usertable[user] == password):
              return render_template('index.html', word="", randomseed=0, user="Login fail!", password="Password wrong!", peoplenum=peoplenum, spynum=spynum)
    else:
        return render_template('index.html', word="", randomseed=0, user="Login fail!", password="User not exist!", peoplenum=peoplenum, spynum=spynum)
    
    currsize = len(words)
    seed = random.randint(0, currsize - 1)
    
    # Set up identity
    identity = [0] * (peoplenum + 10)
    identity_table = {}
    for iter in range(spynum):
        humanseed = random.randint(0, peoplenum - 1)
        while not (identity[humanseed] == 0):
            humanseed = random.randint(0, peoplenum - 1)
        identity[humanseed] = 1
    if not (user in identity_table):
        identity_table[user] = identity[len(identity_table) - 1]
    
    your_identity = identity_table[user]
    word = words[seed][your_identity]
    
    # [END submitted]
    # [START render_template]
    return render_template('index.html', word=word, randomseed=seed, user=user, password=password, peoplenum=peoplenum, spynum=spynum)
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
