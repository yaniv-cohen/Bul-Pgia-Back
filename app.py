import uuid
from flask import Flask
from flask_cors import CORS
import game
from getNextPossibleResults import getNextPossibleResults
app = Flask(__name__)
CORS(app)

wordLength= 4
myGames = {}
# fisrtGameId = "one"
# hi=game.Game(wordLength)
# myGames[hi.game_id] = hi
# base_game = myGames[hi.game_id]
# base_game.current_guess = ''
# print(myGames[hi.game_id].game_id)
# print("started game in server,  id: "+ base_game.game_id )

@app.route("/createNewGame/<slots>/<letter_Count>")
def createNewGame(slots, letter_Count):
    id = str(uuid.uuid1())
    print('making new game : ' + id)
    myGames[id] = game.Game(int(slots))
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
    return "<p>Invalid url</p>"

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)

# if app.config['LOG_WITH_GUNICORN']:
#     gunicorn_error_logger = logging.getLogger('gunicorn.error')
#     app.logger.handlers.extend(gunicorn_error_logger.handlers)
#     app.logger.setLevel(logging.DEBUG)