from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
import json
import random

app = Flask(__name__)
app.secret_key = 'Alexis est un Dieu sur Terre'  
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

words = []
with open("wordle_game/liste_5.txt", 'r') as nf:
    data = nf.read()
    words = data.split("\n")


def get_word(words=words):
    return random.choice(words)


# Function to read the JSON file
def read_users():
    with open('users.json', 'r') as file:
        return json.load(file)

# Function to write to the JSON file
def write_users(data):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)


def read_scores():
    with open('scores.json', 'r') as file:
        return json.load(file)
    
def write_scores(data):
    with open('scores.json', 'w') as file:
        json.dump(data, file, indent=4)

def init_game():
    session['attempts'] = []


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return render_template('login.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = read_users()
        # Vérification des identifiants
        if username in users['users'] and users['users'][username]['password'] == password:
            print("User found")
            session['username'] = username
            session['equipe'] = users['users'][username]['equipe']
            return render_template('index.html')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('equipe', None)
    return render_template('login.html')

@app.route('/get_score', methods=['GET'])
def get_score():
    if 'username' not in session:
        return jsonify(success=False, message="Non connecté")
    users_scores = read_scores()
    score = {team: users_scores[team]['score'] for team in users_scores if team != 'admin' and team != 'test'}
    return jsonify(success=True, score=score)

@app.route('/view_results')
def view_results():
    if 'username' not in session:
        return render_template('login.html')
    
    if request.method == 'GET':
        users_scores = read_scores()
        score = {}
        for team in users_scores:
            score[team] = users_scores[team]['score']
    
        return render_template('view_results.html', scores=score)
    return jsonify(success=False)

@app.route('/admin_results')
def admin_results():
    if 'username' not in session:
        return render_template('login.html')
    elif session.get('equipe') != 'admin':
        return render_template('index.html')
    elif request.method == 'GET':
        users_scores = read_scores()
        score = {team: users_scores[team]['score'] for team in users_scores}
        return render_template('admin_results.html', scores=score)

@app.route('/update_points', methods=['POST'])
def update_points():
    data = request.json
    team = data['team']
    delta = data['delta']

    users_scores = read_scores()
    if team in users_scores:
        users_scores[team]['score'] += delta
        write_scores(users_scores)
        return jsonify(success=True, new_score=users_scores[team]['score'])
    return jsonify(success=False)

@app.route('/gestion_users', methods=['GET', 'POST'])
def gestion_user():
    if 'username' not in session:
        return render_template('login.html')
    elif session.get('equipe') != 'admin':
        return render_template('index.html')
    elif request.method == 'GET':
        users = read_users()
        return render_template('gestion_users.html', users=users['users'])
    elif request.method == 'POST':
        data = request.json
        users = read_users()
        if data['action'] == 'add':
            users['users'][data['username']] = {'password': data['password'], 'equipe': data['equipe'], 'word': get_word(), 'attempt': [], 'score': 0}
            write_users(users)
            scores = read_scores()
            scores[data['equipe']] = {'score': 0}
            write_scores(scores)
            return jsonify(success=True)
        elif data['action'] == 'delete':
            del users['users'][data['username']]
            write_users(users)
            return jsonify(success=True)
        elif data['action'] == 'update_word':
            if data['username'] in users['users']:
                users['users'][data['username']]['word'] = get_word()
                users['users'][data['username']]['attempt'] = []
                write_users(users)
                return jsonify(success=True)
        elif data['action'] == 'update_password':
            if data['username'] in users['users']:
                users['users'][data['username']]['password'] = data['new_password']
                write_users(users)
                return jsonify(success=True)
        return jsonify(success=False)
    
@app.route('/play_wordle', methods=['GET', 'POST'])
def play_wordle():
    if 'username' not in session:
        return render_template('login.html')

    if request.method == 'POST':
        data = request.json
        users = read_users()
        username = session['username']

        if username in users['users']:
            word = users['users'][username]['word']
            wordtry = data['word']
            wordtry = wordtry.lower()
            if wordtry not in words or len(word) != len(wordtry):
                return jsonify(success=False, message="Le mot n'est pas dans la liste ou la longueur est incorrecte")

            attempts = users['users'][username]['attempt']

            if wordtry in attempts:
                return jsonify(success=False, message="Le mot a déjà été proposé")

            if len(attempts) >= 5:
                return jsonify(success=False, message="Nombre maximum de tentatives atteint")

            users['users'][username]['attempt'].append(wordtry)
            write_users(users)

            well_placed = {}
            in_word = {}
            out = []
            alphabet = {chr(i): 'grey' for i in range(97, 123)}

            for i in range(len(word)):
                if wordtry[i] == word[i]:
                    well_placed[i] = wordtry[i]
                    alphabet[wordtry[i]] = 'green'
                elif wordtry[i] in word:
                    if wordtry[i] in in_word:
                        in_word[wordtry[i]].append(i)
                    else:
                        in_word[wordtry[i]] = [i]
                    if alphabet[wordtry[i]] != 'green':
                        alphabet[wordtry[i]] = 'orange'
                else:
                    out.append(wordtry[i])
                    alphabet[wordtry[i]] = 'red'

            for attempt in attempts:
                for i in range(len(word)):
                    if attempt[i] == word[i]:
                        alphabet[attempt[i]] = 'green'
                    elif attempt[i] in word:
                        if alphabet[attempt[i]] != 'green':
                            alphabet[attempt[i]] = 'orange'
                    else:
                        alphabet[attempt[i]] = 'red'
            if wordtry == word or len(attempts) >= 5:
                scores = read_scores()
                scores[session['equipe']]['score'] += 6 - len(attempts)
                write_scores(scores)

            game_won = wordtry == word
            game_over = game_won or len(attempts) >= 5

            return jsonify(success=True, well_placed=well_placed, in_word=in_word, out=out, alphabet=alphabet, attempts=attempts, game_won=game_won, game_over=game_over)

        return jsonify(success=False, message="L'utilisateur n'existe pas")

    users = read_users()
    attempts = users['users'][session['username']]['attempt']
    return render_template('play_wordle.html', attempts=attempts)


@app.route('/get_attempts_colors', methods=['POST'])
def get_attempts_colors():
    if 'username' not in session:
        return jsonify(success=False, message="Non connecté")

    username = session['username']
    users = read_users()

    if username in users['users']:
        word = users['users'][username]['word']
        attempts = users['users'][username]['attempt']

        response = []
        game_won = False
        for attempt in attempts:
            well_placed = []
            in_word = []
            out = []
            temp = []
            temp_attempt = []
            for i in range(len(word)):
                if attempt[i] == word[i]:
                    well_placed.append(i)
                elif attempt[i] not in word:
                    out.append(attempt[i])
                    temp.append(word[i])
                else:
                    temp.append(word[i])
                    temp_attempt.append(attempt[i])
            print(temp, temp_attempt)
            for i in range(len(temp)):
                for j in range(len(temp_attempt)):
                    if temp[i] == temp_attempt[j]:
                        in_word.append(temp[i])
                        del temp_attempt[j]
                        break


            if attempt == word:
                game_won = True

            response.append({
                'attempt': attempt,
                'well_placed': well_placed,
                'in_word': in_word,
                'out': out
            })

        game_over = game_won or len(attempts) >= 5
        print(response)
        return jsonify(success=True, attempts=response, game_won=game_won, game_over=game_over)

    return jsonify(success=False, message="L'utilisateur n'existe pas")



if __name__ == '__main__':
    app.run(debug=False, port=5005)
