from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import create_tables, register_user, login_user, add_review, get_reviews_by_movie

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

gamesDict = {
    "Apex Legends" : {
        "link" : "ApexLegends",
        "description" : "Apex Legends, released on February 4, 2019, garnered immense popularity, reaching 25 million players within its first week and an impressive 50 million players within the initial month. Subsequently, its player base has continued to grow, making it one of the widely played battle royale games. For the latest and most accurate information, it is advisable to check the official Apex Legends website or reliable gaming industry sources, as specific statistics about the current player base may not be publicly disclosed by the developers."
    },
    "Call of Duty Warzone" : {
        "link" : "CallofDutyWarzone2",
        "description" : "As of my last knowledge update in January 2022, there hasn't been an official announcement or release of Warzone 2. Plans for sequels and new versions of popular games can be dynamic and subject to change. For the latest and most accurate information, I recommend checking the official channels of the game developers, such as Infinity Ward or Activision, and reputable gaming news sources for any recent updates or announcements regarding a potential Warzone 2."
    },
    "Counter Strike GO" : {
        "link" : "CounterStrikeGO",
        "description" : "Counter-Strike: Global Offensive (CS:GO) is a popular multiplayer first-person shooter developed by Valve and Hidden Path Entertainment. Released in 2012, it is the fourth game in the Counter-Strike series. CS:GO features classic team-based gameplay, iconic maps, and a competitive scene. It has remained a prominent title in the esports community, attracting millions of players worldwide."
    },
    "Fortnite" : {
        "link" : "Fortnite",
        "description" : "Fortnite, developed by Epic Games, is a widely popular battle royale game that took the gaming world by storm upon its release in 2017. Known for its vibrant graphics, unique building mechanics, and frequent updates, Fortnite has amassed a massive player base. The game's cross-platform availability and regular events contribute to its cultural impact and sustained popularity in the gaming community."
    },
    "Genshin Impact" : {
        "link" : "GenshinImpact",
        "description" : "Genshin Impact, an action role-playing game by miHoYo, has gained immense popularity since its release in 2020. Set in the fantasy world of Teyvat, players explore diverse landscapes, solve puzzles, and engage in real-time combat. Notable for its stunning anime-inspired visuals, extensive character roster, and a free-to-play model, Genshin Impact has become a global sensation, appealing to both fans of single-player and multiplayer experiences."
    },
    "League of Legends" : {
        "link" : "LeagueofLegends",
        "description" : "League of Legends (LoL), developed by Riot Games, is a highly popular multiplayer online battle arena (MOBA) game. Launched in 2009, it has become a global esports phenomenon. Players, known as summoners, choose unique champions and engage in strategic team-based battles. Regular updates, a competitive scene, and a massive player community contribute to its enduring success."
    },
    "Minecraft" : {
        "link" : "Minecraft",
        "description" : "Minecraft, created by Mojang Studios, is a sandbox game that allows players to explore a blocky, procedurally generated world with infinite terrain. It has various gameplay modes, including survival mode where players gather resources and maintain health, and creative mode where unlimited resources and flight are available. Minecraft's open-ended nature and extensive modding community contribute to its enduring popularity since its initial release in 2011."
    },
    "PUBG Battleground" : {
        "link" : "PUBGBattleground",
        "description" : "PlayerUnknown's Battlegrounds (PUBG) is a battle royale game developed and published by PUBG Corporation. Released in 2017, PUBG gained immense popularity for its intense multiplayer gameplay. In the game, 100 players parachute onto an island, scavenge for weapons, and strive to be the last person or team standing as the play area shrinks. PUBG significantly influenced the battle royale genre and remains a widely played and enjoyed game globally."
    },
    "Valorant" : {
        "link" : "Valorant",
        "description" : "Valorant is a tactical first-person shooter (FPS) game developed and published by Riot Games. Launched in 2020, Valorant combines precise gunplay with unique agent abilities, introducing a strategic layer to traditional FPS gameplay. The game features a variety of agents, each with distinct abilities, adding depth to team-based engagements. Valorant has gained a large player base and is known for its competitive scene and regular updates, keeping the gameplay experience fresh and engaging."
    }
}


# Form functions
def validate_registration_form(username, email, password, confirm_password):
    if not username or not email or not password or not confirm_password:
        flash('All fields are required.', 'danger')
        return False

    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return False
    # Add more validation as needed
    return True


def validate_login_form(username, password):
    if not username or not password:
        flash('All fields are required.', 'danger')
        return False
    # Add more validation as needed
    return True


def validate_review_form(movie_title, review_text):
    if not movie_title or not review_text:
        flash('All fields are required.', 'danger')
        return False
    # Add more validation as needed
    return True


# Routes for user authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in request.cookies:
        return redirect(url_for('index'))

    if request.method == 'POST':
        form = (
            request.form['username'],
            request.form['email'],
            request.form['password'],
            request.form['confirm_password']  # Include the confirm_password field
        )

        if validate_registration_form(*form):
            # Update the function call to pass all four parameters
            result = register_user(form[0], form[1], form[2], form[3])

            if result:
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Username or email already exists.', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in request.cookies:
        return redirect(url_for('index'))

    if request.method == 'POST':
        form = (
            request.form['username'],
            request.form['password']
        )

        if validate_login_form(*form):
            user = login_user(*form)

            if user:
                flash('Login successful!', 'success')
                response = redirect(url_for('index'))
                response.set_cookie('user_id', str(user[0]))
                return response
            else:
                flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


# Route for adding reviews
@app.route('/add_review/<movie_title>', methods=['GET', 'POST'])
def add_review_route(movie_title):
    if 'user_id' not in request.cookies:
        flash('You need to log in to add a review.', 'danger')
        return redirect(url_for('login'))

    user_id = int(request.cookies.get('user_id'))

    if request.method == 'POST':
        form = (
            movie_title,  # Pass the movie_title from the URL
            request.form['review_text']
        )

        if validate_review_form(*form):
            add_review(user_id, *form)
            flash('Review added successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('add_review.html', movie_title=movie_title)


@app.route('/logout')
def logout():
    # Clear the user_id cookie to log the user out
    response = redirect(url_for('index'))
    response.delete_cookie('user_id')
    flash('Logout successful!', 'success')
    return response


@app.route('/')
def index():
    return render_template('index.html')  # Adjust the template name as needed

# ... (your other code)


@app.route('/games')
def games():
    return render_template('games.html')


# Route for displaying reviews for a specific movie
@app.route('/game/<movie_title>')
def movie_reviews(movie_title):
    print(movie_title)
    # Fetch reviews for the specified movie from the database
    reviews = get_reviews_by_movie(movie_title)
    reviews = [review[0] for review in reviews]
    print("name")
    print(movie_title)
    info = gamesDict[movie_title]
    image_link = info["link"]
    print(image_link)
    movie_description = info["description"]
    arr = [movie_title, image_link, movie_description, reviews]
    return render_template('movie_reviews.html', arr=arr)



if __name__ == '__main__':
    create_tables()  # Ensure that the database tables are created before running the app
    app.run(debug=True)