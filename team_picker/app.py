from flask import Flask, request, jsonify, render_template_string, session
from pick_team import get_user_email_from_token, replace_user_password, get_password_reset_tokens, send_password_reset_email, put_password_reset_token_in_db, check_database_for_email, delete_user_account, add_new_user_to_db, check_if_email_is_valid, check_if_user_exists, check_if_username_is_valid, authenticate_user, check_if_password_is_valid, check_if_player_in_db, add_new_player_with_stats_to_db, get_user_uuid, get_player_pool_from_db, balance_teams
import random
import secrets
import hashlib
from datetime import datetime, timedelta
from website import NEW_HOME_HTML, PICK_TEAM_HTML, PICK_TEAM_HTML_LOGGED_IN, FORGOT_PASSWORD_HTML, RESET_PASSWORD_HTML


app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Required for sessions
# reset_token = secrets.token_hex(16)
# reset_token_expiry = datetime.now() + timedelta(hours=1)
# reset_token_hash = hashlib.sha256(reset_token.encode()).hexdigest()

@app.route('/')
def home():
    user = request.cookies.get('user', None)
    return render_template_string(NEW_HOME_HTML, user=user)

@app.route('/pick_team_logged_in')
def pick_team():
    user = request.cookies.get('user', None)
    if not user:
        return render_template_string(PICK_TEAM_HTML)
    return render_template_string(PICK_TEAM_HTML_LOGGED_IN, user=user)

@app.route('/pick_team_not_logged_in')
def pick_team_not_logged_in():
    return render_template_string(PICK_TEAM_HTML)

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email', '')
    username = data.get('username', '')
    password = data.get('password', '')
    
    email_check = check_if_email_is_valid(email)
    username_check = check_if_username_is_valid(username)
    password_check = check_if_password_is_valid(password)
    
    if email_check is not True:
        return jsonify({"error": email_check, "status": 400})
    if username_check is not True:
        return jsonify({"error": username_check, "status": 400})
    if password_check is not True:
        return jsonify({"error": password_check, "status": 400})
    
    if check_if_user_exists(email, username, database_name="testing") is True:
        add_new_user_to_db(username, email, password, database_name="testing")
        return jsonify({"message": "Account Created Successfully", "status": 201})
    else:
        return jsonify({"error": "User with this email or username already exists.", "status": 400})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    emailusername = data.get('emailusername', '')
    password = data.get('password', '')
    
    resp, uname = authenticate_user(emailusername, password, database_name="testing")
    if resp is True:
        response = jsonify({"message": "Login Successful", "status": 200})
        response.set_cookie("user", uname, max_age=60*60*24*7)  # 7 days
        return response
    else:
        return jsonify({"error": "Invalid email/username or password.", "status": 400})

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    response.set_cookie("user", "", expires=0)
    return response

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.get_json()
    player_name = data.get('name', '')
    wins = data.get('wins', 0)
    draws = data.get('draws', 0)
    losses = data.get('losses', 0)
    number_of_games = data.get('number_of_games', wins + draws + losses)
    
    created_by = request.cookies.get("user")
    if not created_by:
        return jsonify({"error": "Must be logged in to add players", "status": 401})
    
    user_uuid = get_user_uuid(created_by, database_name="testing")[0]
    player_check = check_if_player_in_db(player_name, database_name="testing")
    
    if player_check is True:
        add_new_player_with_stats_to_db(
            created_by=user_uuid, 
            player_name=player_name, 
            number_of_games=number_of_games, 
            wins=wins, 
            losses=losses,
            draws=draws, 
            database_name="testing"
        )
        return jsonify({"message": "Player created successfully", "status": 201})
    else:
        return jsonify({"error": player_check, "status": 400})

@app.route('/api/get_players', methods=['GET'])
def get_players():
    created_by = request.cookies.get("user")
    print("User UUID from cookie:", created_by)
    # if not created_by:
    #     return jsonify({"error": "Must be logged in to add players", "status": 401})
    
    user_uuid = get_user_uuid(created_by, database_name="testing")[0]
    # Mock data - replace with actual database query
    players = get_player_pool_from_db(number_of_players=10, user_id=user_uuid, database_name="testing")

    return jsonify({"players": players})

@app.route('/api/autoselect', methods=['POST'])
def autoselect():
    data = request.get_json()
    n = data.get('n', 10)
    created_by = request.cookies.get("user")
    # if not created_by:
    #     return jsonify({"error": "Must be logged in to add players", "status": 401})
    
    user_uuid = get_user_uuid(created_by, database_name="testing")[0]
    # Mock data - replace with actual database query
    players = get_player_pool_from_db(number_of_players=n, user_id=user_uuid, database_name="testing")
    print(players)
    # Mock implementation - replace with actual logic
    # This should fetch players and select them based on some algorithm
    chosen_players = random.sample(players, min(n, len(players)))
    
    # chosen = mock_players[:min(n, len(mock_players))]
    print(chosen_players)
    return jsonify({"chosen": chosen_players})

@app.route('/api/balanceteams', methods=['POST'])
def balance_the_teams():
    created_by = request.cookies.get("user")
    data = request.get_json()
    teamA = data.get('teamA', [])
    teamB = data.get('teamB', [])
    player_names = []
    if teamA + teamB == []:
        return jsonify({"error": "No players in teams to balance"}), 400
    else:
        for player in teamA + teamB:
            player_names.append(player['name'])
        print("Balancing teams:", player_names)
        teams = balance_teams(player_names, created_by)
    # Implement your balancing logic here
    # return jsonify({"message": "Teams balanced successfully"})
        return jsonify({"teamA": teams[0], "teamB": teams[1]})

@app.route('/delete_account', methods=['POST'])
def delete_account():
    created_by = request.cookies.get("user")
    if not created_by:
        return jsonify({"error": "Must be logged in to delete account", "status": 401})

    user_uuid = get_user_uuid(created_by, database_name="testing")[0]
    delete_user_account(user_uuid, database_name="testing")
    response = jsonify({"message": "Account deleted successfully"})
    response.set_cookie("user", "", expires=0)
    return response

@app.route('/forgot_password', methods=['GET'])
def forgot_password_page():
    """Display the forgot password page"""
    return render_template_string(FORGOT_PASSWORD_HTML)

@app.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    """Handle password reset request"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'error': 'Email is required', 'status': 400}), 400
    else:
        if check_database_for_email(email, database_name="testing"):
            token = secrets.token_urlsafe(32)
            put_password_reset_token_in_db(get_user_uuid(email=email, database_name="testing"), email, token, database_name="testing")
            reset_link = f"http://localhost:5000/reset_password?token={token}"
            print(f"Password reset link for {email}: {reset_link}")
            send_password_reset_email(email, reset_link)
        return jsonify({
        'message': 'If an account exists with this email, a password reset link has been sent.',
        'status': 200, 
    })
           # Check if user exists in your database
    # This is a placeholder - replace with your actual user lookup
    user = None  # Replace with: db.users.find_one({'email': email})

    
    # Generate reset token
    
    
    # Store token with expiry (1 hour)
    # reset_tokens[token] = {
    #     'email': email,
    #     'expires': datetime.now() + timedelta(hours=1)
    # }
    
    # In production, send email with reset link
    
    
    # For development, print to console

    # TODO: Send email with reset_link
    # send_email(email, "Password Reset", f"Click here to reset: {reset_link}")
    
    

@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password_page():
    """Display the reset password page"""
    token = request.args.get('token')
    print(f"Received token: {token}")
    # data = request.get_json()
    # email = data.get('email', '').strip().lower()
    valid_tokens = get_password_reset_tokens(database_name="testing")
    valid_tokens = [row[0] for row in valid_tokens]
    print(f"Valid tokens from DB: {valid_tokens}")
    if not token or token not in valid_tokens:
        return render_template_string("""
            <!doctype html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Invalid Token</title>
                <style>
                    body {
                        font-family: 'Segoe UI', sans-serif;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .card {
                        background: #fff;
                        padding: 40px;
                        border-radius: 16px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 400px;
                    }
                    h2 { color: #dc3545; }
                    button {
                        margin-top: 20px;
                        padding: 12px 24px;
                        border-radius: 8px;
                        border: none;
                        background: #667eea;
                        color: #fff;
                        cursor: pointer;
                        font-weight: 600;
                    }
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>❌ Invalid or Expired Token</h2>
                    <p>This password reset link is invalid or has expired.</p>
                    <button onclick="location.href='/'">Return Home</button>
                </div>
            </body>
            </html>
        """)

    print(f"Rendering reset password page for token: {token}")
    
    return render_template_string(RESET_PASSWORD_HTML, token=token)

@app.route('/submit_password_reset', methods=['POST'])
def submit_password_reset():
    """Handle password reset submission"""
    data = request.get_json()
    token = data.get('token')
    # token = request.args.get('token')
    print(f"Received token for password reset submission: {token}")
    email = get_user_email_from_token(token, database_name="testing")
    print(f"Email associated with token: {email}")
    new_password = data.get('password')
    password_is_valid = check_if_password_is_valid(new_password)
    if password_is_valid is True:
        confirm_password = data.get('confirm_password')
        if not confirm_password or confirm_password != new_password:
            return jsonify({'error': 'Passwords do not match', 'status': 400}), 400
        replace_user_password(email, confirm_password, database_name="testing")  
    else:
        return jsonify({'error': password_is_valid, 'status': 400}), 400
    
    
    print(f"Password reset successful for: {email}")
    
    return jsonify({
        'message': 'Password reset successful! You can now login with your new password.',
        'status': 200
    })

if __name__ == '__main__':
    app.run(debug=True)