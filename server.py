import uuid
from flask import Flask
from flask_cors import CORS
import game
from flask import request
from getNextPossibleResults import getNextPossibleResults
app = Flask(__name__)
CORS(app)

wordLength= 4
myGames = {}

@app.route("/createNewGame/<slots>/<letter_Count>")
def createNewGame(slots, letter_Count):
    id = str(uuid.uuid1())
    print('making new game : ' + id)
    myGames[id] = game.Game(int(slots), int(letter_Count))
    print(len(myGames) )
    return (id)

@app.route("/game/<id>/guess/<input_word>")
def guess(id, input_word):
    new_game = myGames[str(id)]
    print("id:"+id, "  Word:"+ input_word +
           "  secret: " +','.join(new_game.secret_word))
    new_game.current_guess = input_word
    new_game.guess_number+=1
    [blacks, whites] = new_game.getMarks(list(input_word.upper()) , new_game.secret_word)
    return (
        {
        "possibilities": getNextPossibleResults( [] , blacks , whites, [], input_word),
        "input_word": input_word,
        "secret_word": new_game.secret_word,
        "result": {"white" : whites, "black" : blacks},
        "game_id": id,
        "text" : (
        "<h1>Your result is: <div>BLACKS: " +str(blacks) +", WHITES: "+ str(whites) 
    +"</h1><ul><li>id:"+str(new_game.game_id)+"</li><li>secret_word:"+",".join(new_game.secret_word) +"</li></ul>")
    } )

@app.route('/scoreboard')
def scoreboard():
    return "<p>Scoreboard !</p>"
@app.route('/')
def hello_world():
    return "<p>Hello, World !</p>"
