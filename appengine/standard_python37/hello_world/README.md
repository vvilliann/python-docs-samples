How should the APIs being called:

1, Client call to get all available rooms:
/getallavailablerooms
Y is available to host, R is available to join, N is not available to host or join.

2, Client choose a room, select his nickname, and send request to host:
/registerroom/<username>/<nickname>/<room>/<config>
Note: 
  1) The username is a kind of UUID which never repeats or editable by user
  2) The nickname is defined by user, they could change or not
  3) The room is of course the room number
  4) The config is the game setup

At the same time, host also register user's name
/registeruser/<username>/<nickname>/<room>
Note:
  Most of the definition of inputs/outputs are the same with above.
  Users may use this method to override his nickname.

3, Non-host client choose a room, and send request to join:
(Only for room that is hosted, which made the host "Ready")
/registeruser/<username>/<nickname>/<room>
which is same as above

4, Client query current status of the game:
/getgameinfo/<username>/<room>
The game can do a query every second

5, Start game
/startgame/<username>/<room>
The game will start, only host can start the game
This will return the game info in such format:
    username1^nickname1||username2^nickname2||OMPAYYG||currturn||currlady[room]||otherinfo     

6, Each user get the identity information from:
/getgameinfo/<username>/<room>

7, Client start to give a proposal (only those in their turn):
/propose/<username>/<room>/<index1>/<index2>/<index3>/<index4>/<index5>/<index6>/<index7>
All the clients in game load proposal result every second using:
/loadproposal/<username>/<room>
with output of indexes of selected players

8, Users start to vote for the proposal:
/voteproposal/<username>/<room>/<vote>
All the clients in game load vote result every second using:
/loadvotes/<username>/<room>

9, Do the task:
/act/<username>/<room>/<action>
  
10, Load the act result:
/loadacts/<username>/<room>
  
11, Next turn:
/nextturn/<username>/<room>/<turn>
Automatically called after all the votes completed

12, Kill Merlin:
/killmerlin/<username>/<room>/<merlin>

