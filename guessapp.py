from flask import Flask, render_template, request, session, redirect, url_for



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management



@app.route('/')


def home():

    import random

    # Initialize the game if it hasn't been started or if the user is restarting
    if 'guess' not in session or 'attempts_left' not in session:
        session['guess'] = random.randint(1, 100)
        session['attempts_left'] = 10
        session['result'] = ""
        session['game_status'] = ""

    return render_template('app.html', result=session.get('result', "") , game_status=session.get('game_status', "")) 



@app.route('/guess', methods=['POST'])


def guess():
    pred = int(request.form['number'])
    guess = session.get('guess')
    attempts_left = session.get('attempts_left')
    result = ""
    game_status = ""


    if 1 <= pred <= 100:
        
        if pred == guess:
            
            result = "You have guessed the correct number :)"

            game_status = "Namba jeichitom Maaraa!!!!!"
            
            response = render_template('app.html', result=result, game_status=game_status)

            session.pop ('guess')  # Clear the guess for a new game
            
            session.pop('attempts_left')  # Clear attempts left

            return response
        
        else:
            
            attempts_left -= 1
            
            if attempts_left > 0:
                if pred > guess:
                    result = "Konjam kami ya guess panunga. Attempts left: {}".format(attempts_left)
                elif pred < guess:
                    result = "Konjam adhigam ah guess panunga. Attempts left: {}".format(attempts_left)
            else:
                result = "Sorry, all attempts are over! The number was {}.".format(guess)
                game_status = "*tha next time pathukalam....."

                res = render_template('app.html', result=result, game_status=game_status)
                
                session.pop('guess', None)  # Clear the guess for a new game
                
                session.pop('attempts_left', None)  # Clear attempts left

                return res
    else:
        result = "1-100 kula number guess panunga pa!!!"

    
    session['attempts_left'] = attempts_left
    
    session['result'] = result

    session['game_status'] = game_status

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,port=8000)
