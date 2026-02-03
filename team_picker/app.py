from flask import Flask, request, jsonify, render_template_string, session, make_response
from pick_team import DBUtils, BackEndUtils, Players
import random
import gunicorn
import secrets
import hashlib
from datetime import datetime, timedelta
from website import NEW_HOME_HTML, PICK_TEAM_HTML, PICK_TEAM_HTML_LOGGED_IN, FORGOT_PASSWORD_HTML, RESET_PASSWORD_HTML, INVALID_EXPIRED_RESET_TOKEN_HTML, INVALID_ACTIVATION_LINK_HTML, FAILED_ACCOUNT_ACTIVATION_HTML, ACCOUNT_ACTIVATED_HTML
import traceback


app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Required for sessions
# reset_token = secrets.token_hex(16)
# reset_token_expiry = datetime.now() + timedelta(hours=1)
# reset_token_hash = hashlib.sha256(reset_token.encode()).hexdigest()

@app.route('/')
def home():
    user = request.cookies.get('user', None)
    print("User from cookie:", user)
    print(type(user))
    response = make_response(render_template_string(NEW_HOME_HTML, user=user))
    user_email = DBUtils.get_user_email_from_username(user)
    if user is not None and user_email is not None:
        response.set_cookie('email', user_email, max_age=60*60*24*7)
    return response

@app.route('/pick_team_logged_in')
def pick_team():
    user = request.cookies.get('user', None)
    if user is None:
        return render_template_string(PICK_TEAM_HTML)
    return render_template_string(PICK_TEAM_HTML_LOGGED_IN, user=user)

@app.route('/pick_team_not_logged_in')
def pick_team_not_logged_in():
    return render_template_string(PICK_TEAM_HTML)

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    email_check = BackEndUtils.check_if_email_is_valid(email)
    username_check = BackEndUtils.check_if_username_is_valid(username)
    password_check = BackEndUtils.check_if_password_is_valid(password)

    if email_check is not True:
        return jsonify({"error": email_check, "status": 400})
    if username_check is not True:
        return jsonify({"error": username_check, "status": 400})
    if password_check is not True:
        return jsonify({"error": password_check, "status": 400})

    if DBUtils.check_if_user_exists(email, username) is True:
        try:
            # Generate activation token
            activation_token = secrets.token_urlsafe(32)
            
            # Store activation token in database
            # user_uuid = DBUtils.get_user_uuid(email=email, database_name="testing")
            DBUtils.put_activation_token_in_db(email, activation_token)

            # Send activation email
            activation_link = f"https://team-picker-e3k0.onrender.com/activate_account?token={activation_token}"
            BackEndUtils.send_activation_email(email, activation_link)

            # Add user to database with is_active=False
            DBUtils.add_new_user_to_db(username, email, password)

            return jsonify({
                "message": "Account created! Please check your email to activate your account.",
                "status": 201
            })
        except Exception as e:
            print(f"Error during account creation: {e}")
            return jsonify({"error": "An error occurred while creating the account.", "status": 500})
    else:
        return jsonify({"error": "User with this email or username already exists.", "status": 400})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    emailusername = data.get('emailusername', 'No email/username')
    password = data.get('password', 'No password')

    try:
        resp, uname = BackEndUtils.authenticate_user(emailusername, password)
        if resp is True:
            # Check if account is activated
            email = emailusername if '@' in emailusername else DBUtils.get_email_from_username(emailusername)
            print(f"Checking activation status for email: {email} and username: {uname}")
            if DBUtils.is_user_activated(email) == 0:
                return jsonify({
                    "error": "Please activate your account. Check your email for the activation link.",
                    "status": 403
                })
            response = jsonify({"message": "Login Successful", "status": 200})
            response.set_cookie("user", uname, max_age=60*60*24*7)  # 7 days
            return response
        else:
            return jsonify({"error": "Invalid email/username or password.", "status": 400})
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "An error occurred during login.", "status": 500})

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    response.set_cookie("user", "", expires=0)
    return response

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.get_json()
    user_email = request.cookies.get("email")
    player_name = data.get('name', '')
    wins = data.get('wins', 0)
    draws = data.get('draws', 0)
    losses = data.get('losses', 0)
    number_of_games = data.get('number_of_games', wins + draws + losses)
    
    # created_by = request.cookies.get("user")
    if not user_email:
        return jsonify({"error": "Must be logged in to add players", "status": 401})
    try:    
        # user_email = DBUtils.get_user_email(user_email, database_name="testing")[0]
        player_check = DBUtils.check_if_player_in_db(player_name)
        if player_check is True:
            DBUtils.add_new_player_with_stats_to_db(
                email=user_email,
                player_name=player_name, 
                number_of_games=number_of_games, 
                wins=wins, 
                losses=losses,
                draws=draws, 
            )
            return jsonify({"message": "Player created successfully", "status": 201})
        else:
            return jsonify({"error": player_check, "status": 400})
    except Exception as e:
        print(f"Error adding player: {e}")
        return jsonify({"error": "An error occurred while adding the player.", "status": 500})

@app.route('/get_players', methods=['GET'])
def get_players():
    user_email = request.cookies.get("email")
    print("User email from cookie:", user_email)
    # if not user_email:
    #     return jsonify({"error": "Must be logged in to add players", "status": 401})

    # user_uuid = DBUtils.get_user_uuid(user_email, database_name="testing")
    # Mock data - replace with actual database query
    try:
        players = DBUtils.get_player_pool_from_db(user_email)
    except Exception as e:
        print(f"Error getting players: {e}")
        return jsonify({"error": "An error occurred while retrieving players.", "status": 500})

    return jsonify({"players": players})

@app.route('/autoselect', methods=['POST'])
def autoselect():
    data = request.get_json()
    n = data.get('n', 10)
    created_by = request.cookies.get("email")
    # if not created_by:
    #     return jsonify({"error": "Must be logged in to add players", "status": 401})

    # user_uuid = DBUtils.get_user_uuid(created_by, database_name="testing")[0]
    # Mock data - replace with actual database query
    try:
        players = DBUtils.autoselect_players_from_db(email=created_by, number_of_players=n)
        print(players)
    except Exception as e:
        print(f"Error during player selection: {e}. Traceback: {traceback.format_exc()}, ErrorType: {type(e)}")
        return jsonify({"error": "An error occurred during player selection.", "status": 500})
    # Mock implementation - replace with actual logic
    # This should fetch players and select them based on some algorithm
    # chosen_players = random.sample(players, min(n, len(players)))
    
    # chosen = mock_players[:min(n, len(mock_players))]
    print(players)
    return jsonify({"chosen": players})

@app.route('/balanceteams', methods=['POST'])
def balance_the_teams():
    created_by = request.cookies.get("email")
    data = request.get_json()
    teamA = data.get('teamA', [])
    teamB = data.get('teamB', [])

    try:
        player_names = []
        if teamA + teamB == []:
            return jsonify({"error": "No players in teams to balance"}), 400
        else:
            for player in teamA + teamB:
                player_names.append(player['name'])
            print("Balancing teams:", player_names)
            teams = BackEndUtils.balance_teams(player_names, created_by)
        # Implement your balancing logic here
        # return jsonify({"message": "Teams balanced successfully"})
            return jsonify({"teamA": teams[0], "teamB": teams[1]})
    except Exception as e:
        print(f"Error balancing teams: {e} . Traceback: {traceback.format_exc()}, ErrorType: {type(e)}")
        return jsonify({"error": "An error occurred while balancing teams."}), 500

@app.route('/delete_account', methods=['POST'])
def delete_account():
    created_by = request.cookies.get("email")

    try:
        if not created_by:
            return jsonify({"error": "Must be logged in to delete account", "status": 401})

        DBUtils.delete_user_account(created_by)
        response = jsonify({"message": "Account deleted successfully"})
        response.set_cookie("email", "", expires=0)
        return response
    except Exception as e:
        print(f"Error deleting account: {e}")
        return jsonify({"error": "An error occurred while deleting the account.", "status": 500})

@app.route('/forgot_password', methods=['GET'])
def forgot_password_page():
    """Display the forgot password page"""
    return render_template_string(FORGOT_PASSWORD_HTML)

@app.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    """Handle password reset request"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    try:
        if not email:
            return jsonify({'error': 'Email is required', 'status': 400}), 400
        else:
            if DBUtils.check_database_for_email(email, database_name="testing"):
                token = secrets.token_urlsafe(32)
                DBUtils.put_password_reset_token_in_db(email, token)
                reset_link = f"https://team-picker-e3k0.onrender.com/reset_password?token={token}"
                print(f"Password reset link for {email}: {reset_link}")
                BackEndUtils.send_password_reset_email(email, reset_link)
            return jsonify({
            'message': 'If an account exists with this email, a password reset link has been sent.',
            'status': 200, 
        })
    except Exception as e:
        print(f"Error during password reset request: {e}")
        return jsonify({'error': 'An error occurred while processing the request.', 'status': 500}), 500
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
    try:
        valid_tokens = DBUtils.get_password_reset_tokens()
        print(f"Valid tokens from DB: {valid_tokens}")
        if not token or token not in valid_tokens:
            return render_template_string(INVALID_EXPIRED_RESET_TOKEN_HTML)

        print(f"Rendering reset password page for token: {token}")
        
        return render_template_string(RESET_PASSWORD_HTML, token=token)
    except Exception as e:
        print(f"Error during reset password page rendering: {e}")
        return jsonify({'error': 'An error occurred while processing the request.', 'status': 500}), 500

@app.route('/submit_password_reset', methods=['POST'])
def submit_password_reset():
    """Handle password reset submission"""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password').strip()
    # token = request.args.get('token')
    print(f"Received token for password reset submission: {token}")
    try:
        email = DBUtils.get_user_email_from_token(token)
        print(f"Email associated with token: {email}")
        password_is_valid = BackEndUtils.check_if_password_is_valid(new_password)
        if password_is_valid is True:
            confirm_password = data.get('confirm_password')
            if not confirm_password or confirm_password != new_password:
                return jsonify({'error': 'Passwords do not match', 'status': 400}), 400
            DBUtils.replace_user_password(email, confirm_password, database_name="testing")  
        else:
            return jsonify({'error': password_is_valid, 'status': 400}), 400
        
        print(f"Password reset successful for: {email}")
        
        return jsonify({
            'message': 'Password reset successful! You can now login with your new password.',
            'status': 200
        })
    except Exception as e:
        print(f"Error during password reset submission: {e}")
        return jsonify({'error': 'An error occurred while processing the request.', 'status': 500}), 500

# @app.route('/create_account', methods=['POST'])
# def create_account():
#     data = request.get_json()
#     email = data.get('email', '')
#     username = data.get('username', '')
#     password = data.get('password', '')
    
#     email_check = check_if_email_is_valid(email)
#     username_check = check_if_username_is_valid(username)
#     password_check = check_if_password_is_valid(password)
    
#     if email_check is not True:
#         return jsonify({"error": email_check, "status": 400})
#     if username_check is not True:
#         return jsonify({"error": username_check, "status": 400})
#     if password_check is not True:
#         return jsonify({"error": password_check, "status": 400})
    
#     if check_if_user_exists(email, username, database_name="testing") is True:
#         # Generate activation token
#         activation_token = secrets.token_urlsafe(32)
        
#         # Add user to database with is_active=False
#         add_new_user_to_db(username, email, password, database_name="testing", is_active=False)
        
#         # Store activation token in database
#         user_uuid = get_user_uuid(email=email, database_name="testing")
#         put_activation_token_in_db(user_uuid, email, activation_token, database_name="testing")
        
#         # Send activation email
#         activation_link = f"https://team-picker-e3k0.onrender.com/activate_account?token={activation_token}"
#         send_activation_email(email, activation_link)
        
#         return jsonify({
#             "message": "Account created! Please check your email to activate your account.",
#             "status": 201
#         })
#     else:
#         return jsonify({"error": "User with this email or username already exists.", "status": 400})


@app.route('/activate_account', methods=['GET'])
def activate_account():
    """Handle account activation via email link"""
    token = request.args.get('token')
    try:
        if not token:
            return render_template_string(INVALID_ACTIVATION_LINK_HTML)
        
        # Verify token and activate account
        email = DBUtils.get_user_email_from_activation_token(token)
        
        if not email:
            return render_template_string(FAILED_ACCOUNT_ACTIVATION_HTML)
        
        # Activate the user account
        DBUtils.activate_user_account(email)
        
        # Delete the used activation token
        DBUtils.delete_activation_token(token)

        return render_template_string(ACCOUNT_ACTIVATED_HTML)
    except Exception as e:
        print(f"Error during account activation: {e}. Traceback: {traceback.format_exc()}, ErrorType: {type(e)}")
        return jsonify({'error': 'An error occurred while processing the request.', 'status': 500}), 500


@app.route('/resend_activation', methods=['POST'])
def resend_activation():
    """Resend activation email if user didn't receive it"""
    data = request.get_json()
    email = data.get('email', '')
    
    try:
        if not email:
            return jsonify({'error': 'Email is required', 'status': 400}), 400
        
        # Check if user exists and is not already activated
        # if get_active_activation_tokens_for_email(email, database_name="testing") != [] and is_user_activated(email, database_name="testing") is False:
        #     return jsonify({
        #         'message': 'If an unactivated account exists with this email, an activation link has been sent.',
        #         'status': 200
        #     })
        
        # Check if account is already activated
        if DBUtils.is_user_activated(email, database_name="testing") == 1:
            return jsonify({
                'message': 'This account is already activated. Please log in.',
                'status': 200
            })
        
        # Generate new activation token
        activation_token = secrets.token_urlsafe(32)
        user_uuid = DBUtils.get_user_uuid(email=email, database_name="testing")
        
        # Delete old token and create new one
        DBUtils.delete_old_activation_tokens(email, database_name="testing")
        DBUtils.put_activation_token_in_db(user_uuid, email, activation_token, database_name="testing")

        # Send activation email
        activation_link = f"https://team-picker-e3k0.onrender.com/activate_account?token={activation_token}"
        BackEndUtils.send_activation_email(email, activation_link)

        return jsonify({
            'message': 'If an unactivated account exists with this email, an activation link has been sent.',
            'status': 200
        })
    except Exception as e:
        print(f"Error during resend activation: {e}")
        return jsonify({'error': 'An error occurred while processing the request.', 'status': 500}), 500

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    email = data.get('email', '')
    feedback_text = data.get('message', '')
    feedback_type = data.get('feedback_type', 'General')
    feedback_subject = data.get('subject', 'No Subject')

    try:
        # Here you would typically store the feedback in a database or send it via email
        print(f"Feedback received from {email}: {feedback_text}")
        DBUtils.store_user_feedback_in_db(email=email, feedback=feedback_text, feedback_type=feedback_type, feedback_subject=feedback_subject)
        BackEndUtils.send_feedback_email_notification(feedback_text, email, feedback_type, feedback_subject)

        return jsonify({"message": "Thank you for your feedback!", "status": 200})
    except Exception as e:
        print(f"Error during feedback submission: {e} Traceback: {traceback.format_exc()}, ErrorType: {type(e)}")
        return jsonify({"error": "An error occurred while submitting feedback.", "status": 500})

@app.route('/contact_us', methods=['POST'])
def contact_us():
    data = request.get_json()
    email = data.get('email', '')
    message = data.get('description', '')
    issue_type = data.get('issue_type', 'General Inquiry')
    issue_subject = data.get('subject', 'No Subject')
    issue_priority = data.get('priority', 'Normal')

    try:
        # Here you would typically store the message in a database or send it via email
        print(f"Contact message received from {email}: {message}")
        ticket_id = DBUtils.store_contact_us_message(email=email, message=message, issue_type=issue_type, issue_subject=issue_subject, issue_priority=issue_priority)
        BackEndUtils.send_contact_us_email_notification(message, email=email, ticket_id=ticket_id, issue_type=issue_type, subject=issue_subject, priority=issue_priority)
        BackEndUtils.send_contact_us_email_acknowledgement(message, email=email, issue_type=issue_type, subject=issue_subject, priority=issue_priority, ticket_id=ticket_id)
        return jsonify({"message": "Thank you for contacting us! We will get back to you shortly.", "status": 200, "ticket_id": ticket_id})
    except Exception as e:
        print(f"Error during contact us submission: {e} Traceback: {traceback.format_exc()}, ErrorType: {type(e)}")
        return jsonify({"error": "An error occurred while submitting your message.", "status": 500})

# Update the login route to check if account is activated
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     emailusername = data.get('emailusername', '')
#     password = data.get('password', '')
    
#     resp, uname = authenticate_user(emailusername, password, database_name="testing")
#     if resp is True:
#         # Check if account is activated
#         email = emailusername if '@' in emailusername else get_email_from_username(emailusername, database_name="testing")
#         if not is_user_activated(email, database_name="testing"):
#             return jsonify({
#                 "error": "Please activate your account. Check your email for the activation link.",
#                 "status": 403
#             })
        
#         response = jsonify({"message": "Login Successful", "status": 200})
#         response.set_cookie("user", uname, max_age=60*60*24*7)  # 7 days
#         return response
#     else:
#         return jsonify({"error": "Invalid email/username or password.", "status": 400})
    
if __name__ == '__main__':
    app.run(debug=True)