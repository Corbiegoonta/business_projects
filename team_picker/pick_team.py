# from send_whatsapp.src import sender
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import os
import random
import datetime
import sqlalchemy
import uuid
from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import update, select, join, Computed
from sqlalchemy.orm import Session
import copy
import uuid
from flask import Flask, request, jsonify, render_template_string
import bcrypt
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import resend
import traceback

# from models import User, Department  # Assuming the models above

app = Flask(__name__)

load_dotenv()
MY_EMAIL = os.getenv('RESEND_DOMAIN')
TEAM_PICKER_EMAIL = os.getenv('TEAM_PICKER_EMAIL')
MY_APP_PASSWORD = os.getenv('MY_APP_PASSWORD')
RESEND_API_KEY = os.getenv('RESEND_API_KEY')

resend.api_key = RESEND_API_KEY

# sqlalchemy_engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/testing')
sqlalchemy_engine = sqlalchemy.create_engine('postgresql://testing_70hf_user:RhDNPOBOz0Lo8UlSiRIIYFE7Dt6yfv1Z@dpg-d5rluacoud1c73eo14c0-a/testing_70hf')
connection = sqlalchemy_engine.connect()
session = Session(sqlalchemy_engine)
metadata = sqlalchemy.MetaData()
Base = declarative_base()

class PlayerLog(Base):
    __tablename__ = 'player_log'
    log_id = Column(sqlalchemy.UUID, primary_key=True) 
    match_id = Column(sqlalchemy.UUID, foreign_key=True)
    player_id = Column(sqlalchemy.UUID, foreign_key=True)
    player_team = Column(String)
    team_outcome = Column(String) 
    match_datetime = Column(DateTime)
    created_by = Column(String)
    updated_by = Column(String)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

class Players(Base):
    __tablename__ = 'players'
    player_id = Column(sqlalchemy.UUID, primary_key=True)
    player_name = Column(String)
    number_of_games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)
    points = Column(Integer)
    win_rate = Column(Float)
    points_win_rate = Column(Float)
    points_per_game = Column(Float)
    created_by = Column(String, foreign_key=True)
    updated_by = Column(String, foreign_key=True)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

class Users(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    email = Column(String)
    is_active = Column(Integer)
    password_hash = Column(String)  
    activated_datetime = Column(DateTime)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

class Matches(Base):
    __tablename__ = 'matches'
    match_id = Column(sqlalchemy.UUID, primary_key=True)
    team_1 = Column(String)
    team_2 = Column(String)
    team_1_rating = Column(Float)
    team_2_rating = Column(Float)
    team_1_score = Column(Integer)
    team_2_score = Column(Integer)
    location = Column(String)
    referee = Column(String)
    outcome = Column(String)
    match_date = Column(DateTime)
    match_result = Column(String)
    created_by = Column(String, foreign_key=True)
    updated_by = Column(String, foreign_key=True)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)


class PasswordResets(Base):
    __tablename__ = 'password_resets'
    reset_id = Column(sqlalchemy.UUID, primary_key=True)
    username = Column(String, foreign_key=True)
    email = Column(String)
    reset_token = Column(String)
    token_expiry = Column(DateTime)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

class ActivationTokens(Base):
    __tablename__ = 'activation_tokens'
    username = Column(String, foreign_key=True)
    email = Column(String)
    token = Column(String, primary_key=True)
    created_datetime = Column(DateTime)
    expires_datetime = Column(DateTime)

class Feedback(Base):
    __tablename__ = 'feedback'
    feedback_id = Column(sqlalchemy.UUID, primary_key=True)
    username = Column(String, foreign_key=True)
    email = Column(String)
    feedback_text = Column(String)
    text_length = Column(Integer)
    feedback_type = Column(String)
    feedback_subject = Column(String)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

class ContactUs(Base):
    __tablename__ = 'contact_us'
    contact_id = Column(sqlalchemy.UUID, primary_key=True)
    username = Column(String, foreign_key=True)
    email = Column(String)
    message = Column(String)
    issue_type = Column(String)
    issue_subject = Column(String)
    issue_priority = Column(String)
    text_length = Column(Integer)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

class Tables:
    """Class to create the necessary tables in a specified database if they do not exist."""
    def __init__(self):
        pass

    def create_matches_table():
        """Create the matches table in the specified database if it doesn't exist. The following columns are included:
        - match_id (UUID, primary key)
        - team_1 (String)
        - team_2 (String)
        - team_1_rating (Float)
        - team_2_rating (Float)
        - team_1_score (Integer)
        - team_2_score (Integer)
        - match_date (DateTime)
        - location (String)
        - referee (String)
        - outcome (String)
        - created_by (String, foreign key)
        - updated_by (String, foreign key)
        - created_datetime (DateTime, default current timestamp)
        - updated_datetime (DateTime, default current timestamp, on update current timestamp)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "matches"):
            sqlalchemy.Table("matches", metadata,
                sqlalchemy.Column('match_id', sqlalchemy.UUID, primary_key=True),
                sqlalchemy.Column('team_1', sqlalchemy.String),
                sqlalchemy.Column('team_2', sqlalchemy.String),
                sqlalchemy.Column('team_1_rating', sqlalchemy.Float),
                sqlalchemy.Column('team_2_rating', sqlalchemy.Float),
                sqlalchemy.Column('team_1_score', sqlalchemy.Integer),
                sqlalchemy.Column('team_2_score', sqlalchemy.Integer),
                sqlalchemy.Column('match_date', sqlalchemy.DateTime),
                sqlalchemy.Column('location', sqlalchemy.String),
                sqlalchemy.Column('referee', sqlalchemy.String),
                sqlalchemy.Column('outcome', sqlalchemy.String),
                sqlalchemy.Column('created_by', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('updated_by', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime, default=datetime.datetime.now()),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'matches' already exists.")

    def create_players_table():
        """Create the players table in the specified database if it doesn't exist. The following columns are included:
        - player_id (UUID, primary key)
        - player_name (String)
        - number_of_games (Integer)
        - wins (Integer)
        - losses (Integer)
        - draws (Integer)
        - points (Integer, computed as ROUND((wins * 3) + draws, 0))
        - win_rate (Float, computed as ROUND(CAST(wins AS NUMERIC) / NULLIF(number_of_games, 0), 3))
        - points_win_rate (Float, computed as ROUND(CAST(ROUND((wins * 3) + draws, 0) AS NUMERIC) / NULLIF(number_of_games * 3, 0), 3))
        - points_per_game (Float, computed as ROUND(CAST(ROUND((wins * 3) + draws, 0) AS NUMERIC) / NULLIF(number_of_games, 0), 3))
        - created_by (String, foreign key)
        - updated_by (String, foreign key)
        - created_datetime (DateTime, default current timestamp)
        - updated_datetime (DateTime, default current timestamp, on update current timestamp)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "players"):
            sqlalchemy.Table("players", metadata,
                sqlalchemy.Column('player_id', sqlalchemy.UUID, primary_key=True),
                sqlalchemy.Column('player_name', sqlalchemy.String),
                sqlalchemy.Column('number_of_games', sqlalchemy.Integer),
                sqlalchemy.Column('wins', sqlalchemy.Integer),
                sqlalchemy.Column('losses', sqlalchemy.Integer),
                sqlalchemy.Column('draws', sqlalchemy.Integer),
                sqlalchemy.Column('points', sqlalchemy.Integer, Computed("ROUND((wins * 3) + draws, 0)", persisted=True)),
                sqlalchemy.Column('win_rate', sqlalchemy.Float, Computed("COALESCE(ROUND(CAST(wins AS NUMERIC) / NULLIF(number_of_games, 0), 3), 0)", persisted=True)),
                sqlalchemy.Column('points_win_rate', sqlalchemy.Float, Computed("COALESCE(ROUND(CAST(ROUND((wins * 3) + draws, 0) AS NUMERIC) / NULLIF(number_of_games * 3, 0), 3), 0)", persisted=True)),
                sqlalchemy.Column('points_per_game', sqlalchemy.Float, Computed("COALESCE(ROUND(CAST(ROUND((wins * 3) + draws, 0) AS NUMERIC) / NULLIF(number_of_games, 0), 3), 0)", persisted=True)),
                sqlalchemy.Column('created_by', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('updated_by', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime, default=datetime.datetime.now()),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'players' already exists.")

    def create_users_table():
        """Create the users table in the specified database if it doesn't exist. The following columns are included:
        - username (String, primary key)
        - email (String)
        - password_hash (String)
        - is_active (Integer, default 0)
        - activated_at (DateTime)
        - created_by (String, foreign key)
        - updated_by (String, foreign key)
        - created_datetime (DateTime, default current timestamp)
        - updated_datetime (DateTime, default current timestamp, on update current timestamp)"""
        if not sqlalchemy_engine.dialect.has_table(connection, "users"):
            sqlalchemy.Table("users", metadata,
                sqlalchemy.Column('username', sqlalchemy.String, primary_key=True),
                sqlalchemy.Column('email', sqlalchemy.String),
                sqlalchemy.Column('password_hash', sqlalchemy.String),
                sqlalchemy.Column('is_active', sqlalchemy.Integer, default=0),
                sqlalchemy.Column('activated_at', sqlalchemy.DateTime),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime, default=datetime.datetime.now()),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'users' already exists.")

    def create_player_log_table():
        """Create the player_log table in the specified database if it doesn't exist. The following columns are included:
        - log_id (UUID, primary key)
        - match_id (UUID, foreign key)
        - player_id (UUID, foreign key)
        - team (String)
        - team_outcome (String)
        - match_datetime (DateTime, default current timestamp)
        - created_by (String, foreign key)
        - updated_by (String, foreign key)
        - created_datetime (DateTime, default current timestamp)
        - updated_datetime (DateTime, default current timestamp, on update current timestamp)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "player_log"):
            sqlalchemy.Table("player_log", metadata,
                sqlalchemy.Column('log_id', sqlalchemy.UUID, primary_key=True),
                sqlalchemy.Column('match_id', sqlalchemy.UUID, foreign_key=True),
                sqlalchemy.Column('player_id', sqlalchemy.UUID, foreign_key=True),
                sqlalchemy.Column('team', sqlalchemy.String),
                sqlalchemy.Column('team_outcome', sqlalchemy.String),
                sqlalchemy.Column('match_datetime', sqlalchemy.DateTime, default=datetime.datetime.now()),
                sqlalchemy.Column('created_by', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('updated_by', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime, default=datetime.datetime.now()),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'player_log' already exists.")

    def create_password_resets_table():
        """Create the password_resets table in the specified database if it doesn't exist. The following columns are included:
        - reset_id (UUID, primary key)
        - username (String, foreign key)
        - email (String)
        - reset_token (String)
        - token_expiry (DateTime)
        - created_datetime (DateTime, default current timestamp)
        - updated_datetime (DateTime, default current timestamp, on update current timestamp)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "password_resets"):
            sqlalchemy.Table("password_resets", metadata,
                sqlalchemy.Column('reset_id', sqlalchemy.UUID, primary_key=True),
                sqlalchemy.Column('username', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('email', sqlalchemy.String),
                sqlalchemy.Column('reset_token', sqlalchemy.String),
                sqlalchemy.Column('token_expiry', sqlalchemy.DateTime),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime, default=datetime.datetime.now()),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'password_resets' already exists.")

    def create_activation_tokens_table():
        """Create the activation_tokens table in the specified database if it doesn't exist. The following columns are included:
        - username (String, foreign key)
        - email (String)
        - token (String, primary key)
        - expires_at (DateTime)
        - created_at (DateTime, default current timestamp)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "activation_tokens"):
            sqlalchemy.Table("activation_tokens", metadata,
                sqlalchemy.Column('username', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('email', sqlalchemy.String),
                sqlalchemy.Column('token', sqlalchemy.String, primary_key=True),
                sqlalchemy.Column('expires_at', sqlalchemy.DateTime),
                sqlalchemy.Column('created_at', sqlalchemy.DateTime, default=datetime.datetime.now())
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'activation_tokens' already exists.")

    def create_feedback_table():
        """Create the feedback table in the specified database if it doesn't exist. The following columns are included:
        - feedback_id (Integer, primary key)
        - username (String, foreign key)
        - email (String)
        - feedback_text (String)
        - text_length (Integer, computed)
        - feedback_type (String)
        - feedback_subject (String)
        - created_datetime (DateTime)
        - updated_datetime (DateTime)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "feedback"):
            sqlalchemy.Table("feedback", metadata,
                sqlalchemy.Column('feedback_id', sqlalchemy.UUID, primary_key=True),
                sqlalchemy.Column('username', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('email', sqlalchemy.String),
                sqlalchemy.Column('feedback_text', sqlalchemy.String),
                sqlalchemy.Column('text_length', sqlalchemy.Integer, Computed("LENGTH(feedback_text)")),
                sqlalchemy.Column('feedback_type', sqlalchemy.String),
                sqlalchemy.Column('feedback_subject', sqlalchemy.String),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime)
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'feedback' already exists.")

    def create_contact_us_table():
        """Create the contact_us table in the specified database if it doesn't exist. The following columns are included:
        - contact_id (Integer, primary key)
        - username (String, foreign key)
        - email (String)
        - message (String)
        - text_length (Integer, computed)
        - issue_type (String)
        - issue_subject (String)
        - issue_priority (String)
        - created_datetime (DateTime)
        - updated_datetime (DateTime)
        """
        if not sqlalchemy_engine.dialect.has_table(connection, "contact_us"):
            sqlalchemy.Table("contact_us", metadata,
                sqlalchemy.Column('contact_id', sqlalchemy.UUID, primary_key=True),
                sqlalchemy.Column('email', sqlalchemy.String, foreign_key=True),
                sqlalchemy.Column('message', sqlalchemy.String),
                sqlalchemy.Column('text_length', sqlalchemy.Integer, Computed("LENGTH(message)")),
                sqlalchemy.Column('issue_type', sqlalchemy.String),
                sqlalchemy.Column('issue_subject', sqlalchemy.String),
                sqlalchemy.Column('issue_priority', sqlalchemy.String),
                sqlalchemy.Column('created_datetime', sqlalchemy.DateTime),
                sqlalchemy.Column('updated_datetime', sqlalchemy.DateTime)
            )
            metadata.create_all(sqlalchemy_engine)
        else:
            print("Error: Table 'contact_us' already exists.")

class Players:  
    def __init__(self):
        pass
    
    # def retrieve_all_player_data():
    #     """Retrieve all players from the players table in the database and return as a pandas DataFrame."""
    #     query = "SELECT * FROM players;"
    #     df = pd.read_sql_query(query, connection)
    #     connection.close()
    #     print(df)
        
    #     return df

    # # def retrieve_players(email: str=""):
    # #     """Retrieve all players from the players table in the database for a specific user and return as a list."""
    # #     df = Players.load_player_data(email=email)
    # #     players = df["player_name"].tolist()
    # #     print(players)

    # #     return players

    # def retrieve_win_rates(list_of_players: list):
    #     """Retrieve win rates for a list of players from the players table in the database and return as a list."""
    #     df = Players.load_player_data()
    #     win_rates = []
    #     for player in list_of_players:
    #         win_rates.append(df.loc[df['player_name'] == player, 'points_win_rate'].values[0]) 
    #     print(win_rates)

    #     return win_rates

    # def init_player_data():
    #     # df = load_player_data()
    #     df = dict()
    #     df["player_name"] = []
    #     df["wins"] = []
    #     df["losses"] = []
    #     df["draws"] = []
    #     df["win_rate"] = []
    #     df["number_of_games_played"] = []
    #     df = pd.DataFrame(df)
    #     df.to_csv('player_info.csv', index=False)

    # def init_team_data():
    #     df = pd.DataFrame(columns=["team_coloured", "team_white"])
    #     df.to_csv('team_info.csv', index=False)

    # def init_weekly_player_list():
    #     df = pd.DataFrame(columns=["player_name"])
    #     df.to_csv('list_of_players.csv', index=False)
    #     pass

    # def load_weekly_players():
    #     df = pd.read_csv('list_of_players.csv')
    #     weekly_players = df["player_name"].tolist()
    #     return weekly_players

    # def load_player_data(email: str=""):
    #     user_uuid = DBUtils.get_user_uuid(email=email)
    #     query = f"SELECT * FROM players WHERE created_by = {user_uuid};"
    #     df = pd.read_sql_query(query, connection)
    #     print(df)

    #     return df

    # def add_player(player_name: str):
    #     df = Players.load_player_data()
    #     print("add_player")
    #     print(df.loc[df.index.max()])
    #     df.loc[df.index.max()+1] = [player_name, 0, 0, 0, 0, 0, 0, 0]
    #     # print(df.loc[df.index.max()+1])
    #     # df.append({'player_name':player_name, 'wins':0, 'losses':0, 'draws':0, 'win_rate':0, 'number_of_games_played':0, 'points':0, 'points_win_rate':0}, ignore_index=True)
    #     print(df)
    #     df.to_csv('player_info.csv', index=False)
    #     # df["player_name"] = player_name
    #     pass

    # def remove_player(player_name: str):
    #     df = Players.load_player_data()
    #     df.loc[df['player_name'] == player_name] = None
    #     df.to_csv('player_info.csv', index=False)

    # def store_teams(team_1=[], team_2=[]):
    #     df = pd.DataFrame(columns=["team_1", "team_2"])
    #     df["team_1"] = team_1
    #     df["team_2"] = team_2
    #     df.to_csv('team_players.csv', index=False)
    #     pass

    # def get_player_stats(player_name: str):
    #     df = pd.read_csv('player_info.csv')
    #     player_stats = df.loc[df['player_name'] == player_name]
    #     print(f"Player Name: {player_name}\nWins: {player_stats['wins'].values[0]}\nLosses: {player_stats['losses'].values[0]}\nDraws: {player_stats['draws'].values[0]}\nWin Rate: {player_stats['win_rate'].values[0]*100}%\nPoints Win Rate: {player_stats['points_win_rate'].values[0]*100}%\nNumber of Games Played: {player_stats['number_of_games_played'].values[0]}")

    # def merge_player(player_names: list, true_name: str):
    #     df = Players.load_player_data()
    #     player_stats = df.loc[df['player_name'].isin(player_names)]
    #     wins = player_stats["wins"].sum()
    #     losses = player_stats["losses"].sum()
    #     draws = player_stats["draws"].sum()
    #     number_of_games_played = player_stats["number_of_games_played"].sum()
    #     win_rate = wins/number_of_games_played
    #     points = player_stats["points"].sum()
    #     points_win_rate = points/number_of_games_played * 3
    #     df.loc[df['player_name'] == true_name, 'wins'] = wins
    #     df.loc[df['player_name'] == true_name, 'losses'] = losses
    #     df.loc[df['player_name'] == true_name, 'draws'] = draws
    #     df.loc[df['player_name'] == true_name, 'win_rate'] = win_rate
    #     df.loc[df['player_name'] == true_name, 'number_of_games_played'] = number_of_games_played
    #     df.loc[df['player_name'] == true_name, 'points'] = points
    #     df.loc[df['player_name'] == true_name, 'points_win_rate'] = points_win_rate
    #     df.to_csv('player_info.csv', index=False)  

if sqlalchemy_engine.dialect.has_table(connection, "matches"):
    matches_table = sqlalchemy.Table('matches', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_matches_table(database_name="testing")
    matches_table = sqlalchemy.Table('matches', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "players"):
    players_table = sqlalchemy.Table('players', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_players_table()
    players_table = sqlalchemy.Table('players', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "users"):
    users_table = sqlalchemy.Table('users', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_users_table()
    users_table = sqlalchemy.Table('users', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "matches"):
    matches_table = sqlalchemy.Table('matches', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_matches_table()
    matches_table = sqlalchemy.Table('matches', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "player_log"):
    player_log_table = sqlalchemy.Table('player_log', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_player_log_table()
    player_log_table = sqlalchemy.Table('player_log', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "activation_tokens"):
    activation_tokens_table = sqlalchemy.Table('activation_tokens', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_activation_tokens_table()
    activation_tokens_table = sqlalchemy.Table('activation_tokens', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "password_resets"):
    password_resets_table = sqlalchemy.Table('password_resets', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_password_resets_table()
    password_resets_table = sqlalchemy.Table('password_resets', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "feedback"):
    feedback_table = sqlalchemy.Table('feedback', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_feedback_table()
    feedback_table = sqlalchemy.Table('feedback', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

if sqlalchemy_engine.dialect.has_table(connection, "contact_us"):
    contact_us_table = sqlalchemy.Table('contact_us', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
else:
    Tables.create_contact_us_table()
    contact_us_table = sqlalchemy.Table('contact_us', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)

# class Whatsapp:
#     def __init__(self):
#         pass

#     def connect_to_whatsapp(message_to_send: str, type_of_contact: str, contact: str):
#         load_dotenv()
#         hour_time = datetime.datetime.now().hour
#         minute_time = datetime.datetime.now().minute
#         send_message = sender.WhatsAppMessageSender(
#             mode='contact',
#             phone_number=os.getenv('MY_PHONE_NUMBER'),
#             message=message_to_send, 
#             time_hour=hour_time,
#             time_minute=minute_time+1
#             )
#         send_message.execute()
        # print(hour_time)
        # print(minute_time)

class DBUtils:
    def __init__(self):
        pass

    def query_db(query: str) -> pd.DataFrame:
        """Run a query on the specified database and return the results as a pandas DataFrame."""
        connection = sqlalchemy_engine.connect()
        with connection as conn:
            df = pd.read_sql_query(query, conn)

        return df

    # def run_query(query: str, database: str="postgres"):
    #     load_dotenv()
    #     sqlalchemy_engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{database}')
    #     connection = sqlalchemy_engine.connect()
    #     connection.execute(sqlalchemy.text(query))
    #     # with connection as conn, conn.begin():
    #     #     df = pd.read_sql_query(query, connection)
    #     # print(df)

    def add_new_match_to_db(username: str, team_1: str="Team_1", team_2: str="Team_2", team_1_rating: float=0.0, team_2_rating: float=0.0, team_1_players: list[uuid.UUID]=[], team_2_players: list[uuid.UUID]=[], team_1_score: int=0, team_2_score: int=0, location: str="Unknown", referee: str="Unknown", match_datetime: datetime.datetime = datetime.datetime.now(), outcome: str = "Unknown", created_datetime: datetime.datetime = datetime.datetime.now(), updated_datetime: datetime.datetime = datetime.datetime.now()):
        """Add a new match to the matches table in the specified database with the provided details."""
        match_uuid = uuid.uuid4()
        connection = sqlalchemy_engine.connect()
        matches_insert = sqlalchemy.insert(matches_table).values(
            match_id=match_uuid,
            team_1=team_1,
            team_2=team_2,
            team_1_rating=team_1_rating,
            team_2_rating=team_2_rating,
            team_1_score=team_1_score,
            team_2_score=team_2_score,
            match_datetime=match_datetime,
            location=location,
            referee=referee,
            outcome=outcome,
            created_by=username,
            updated_by=username,
            created_datetime=created_datetime,
            updated_datetime=updated_datetime
        )
        # player_log_insert = sqlalchemy.insert(player_log_table).values(
        #     log_id=uuid.uuid4(),
        #     match_id=match_uuid,
        #     user_id=user_id,
        #     player_id=uuid.uuid4(),
        #     date_created=datetime.datetime.now(),
        #     date_updated=datetime.datetime.now()
        # )
        for player1 in team_1_players:
            player_log_insert = sqlalchemy.insert(player_log_table).values(
                log_id=uuid.uuid4(),
                match_id=match_uuid,
                player_id=player1,
                team="Team 1",
                updated_by=username,
                date_created=datetime.datetime.now(),
                date_updated=datetime.datetime.now()
            )
        for player2 in team_2_players:
            player_log_insert = sqlalchemy.insert(player_log_table).values(
                log_id=uuid.uuid4(),
                match_id=match_uuid,
                player_id=player2,
                team="Team 2",
                updated_by=username,
                date_created=datetime.datetime.now(),
                date_updated=datetime.datetime.now()
            )
        with connection as conn:
            conn.execute(player_log_insert)
            conn.execute(matches_insert)
            conn.commit()

    def add_new_player_with_stats_to_db(username: str, player_name: str, number_of_games: int=0, wins: int=0, losses: int=0, draws: int=0, points: int=0, win_rate: float=0.0, points_win_rate: float=0.0, points_per_game: float=0.0, created_datetime=datetime.datetime.now(), updated_datetime=datetime.datetime.now()):
        """Add a new player to the players table in the specified database with the provided details."""
        new_uuid = uuid.uuid4()
        connection = sqlalchemy_engine.connect()
        insert = sqlalchemy.insert(players_table).values(
            player_id=new_uuid,
            player_name=player_name,
            number_of_games=number_of_games,
            wins=wins,
            losses=losses,
            draws=draws,
            created_by=username,
            updated_by=username,
            created_datetime=created_datetime,
            updated_datetime=updated_datetime
        )
        with connection as conn:
            conn.execute(insert)
            conn.commit()
        # query = f"INSERT INTO players (player_name, number_of_games, wins, losses, draws, points, win_rate, points_win_rate, points_per_game) VALUES ('{player_name}', {number_of_games}, {wins}, {losses}, {draws}, {points}, {win_rate}, {points_win_rate}, {points_per_game});"
        # connection.execute(sqlalchemy.text(query))

    def add_new_user_to_db(username: str, email: str, password_hash: str, is_active: int = 0, created_datetime=datetime.datetime.now(), updated_datetime=datetime.datetime.now()):
        """Add a new user to the users table in the specified database with the provided details."""
        table = sqlalchemy.Table('users', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
        # new_user_uuid = uuid.uuid4()
        connection = sqlalchemy_engine.connect()
        insert = sqlalchemy.insert(table).values(
            username=username,
            email=email,
            password_hash=BackEndUtils.create_password_hash(password_hash),
            is_active=is_active,
            created_datetime=created_datetime,
            updated_datetime=updated_datetime
        )
        with connection as conn:
            conn.execute(insert)
            conn.commit()

    def get_player_pool_from_db(username: str) -> list[dict]:
        """Retrieve a specified number of players from the players table in the database for a specific user and return as a list of dictionaries."""
        sel = sqlalchemy.select(players_table).where(players_table.c.created_by == username)
        connection = sqlalchemy_engine.connect()
        df = pd.read_sql_query(sel, connection)
        player_pool = []
        for row in range(len(df)):
            p = {}
            p["name"] = df.at[row, "player_name"]
            p["wins"] = int(df.at[row, "wins"])
            p["draws"] = int(df.at[row, "draws"])
            p["losses"] = int(df.at[row, "losses"])
            p["number_of_games"] = int(df.at[row, "number_of_games"])
            p["points_win_rate"] = float(df.at[row, "points_win_rate"])
            player_pool.append(p)

        return player_pool

    def update_player_in_db(original_name: str, new_name: str, wins: int | None, losses: int | None, draws: int | None):
        """Update a player's stats in the players table in the specified database."""
        connection = sqlalchemy_engine.connect()
        stmt = sqlalchemy.select(players_table).where(players_table.c.player_name == original_name)
        df = pd.read_sql_query(stmt, connection)
        initial_wins = int(df.at[0, "wins"])
        initial_losses = int(df.at[0, "losses"])
        initial_draws = int(df.at[0, "draws"])
        if wins is not None:
            if initial_wins != wins:
                initial_wins = wins
        if losses is not None:
            if initial_losses != losses:
                initial_losses = losses
        if draws is not None:
            if initial_draws != draws:
                initial_draws = draws
        new_number_of_games = wins + losses + draws
        stmt = players_table.update().where(players_table.c.player_name == original_name).values(
            player_name=new_name if new_name != "" else original_name,
            number_of_games=new_number_of_games,
            wins=initial_wins,
            losses=initial_losses,
            draws=initial_draws,
            updated_datetime=datetime.datetime.now()
        )
        with connection as conn:
            conn.execute(stmt)
            conn.commit()

    def autoselect_players_from_db(email: str, number_of_players: int) -> list[dict]:
        """Automatically select a specified number of players from the players table in the database for a specific user and return as a list of dictionaries."""
        sel = sqlalchemy.select(players_table).where(players_table.c.created_by == email)
        connection = sqlalchemy_engine.connect()
        df = pd.read_sql_query(sel, connection)
        # df = df.sample(n=number_of_players)
        player_pool = []
        for row in range(len(df)):
            p = {}
            p["name"] = df.at[row, "player_name"]
            p["wins"] = int(df.at[row, "wins"])
            p["draws"] = int(df.at[row, "draws"])
            p["losses"] = int(df.at[row, "losses"])
            p["number_of_games"] = int(df.at[row, "number_of_games"])
            p["points_win_rate"] = float(df.at[row, "points_win_rate"])
            player_pool.append(p)

        chosen_players = random.sample(player_pool, min(number_of_players, len(player_pool)))

        return chosen_players

    def update_match_outcome(match_id: uuid.UUID, outcome: str):
        """Update the outcome of a match in the matches table in the specified database."""
        connection = sqlalchemy_engine.connect()
        stmt = matches_table.update().where(matches_table.c.match_id == match_id).values(outcome=outcome)
        with connection as conn:
            conn.execute(stmt)
            conn.commit()

    def remove_player_from_db(player_id: uuid.UUID, player_name: str):
        """Remove a player from the players table in the specified database."""
        connection = sqlalchemy_engine.connect()
        stmt = players_table.delete().where(players_table.c.player_id == player_id and players_table.c.player_name == player_name)
        with connection as conn:
            conn.execute(stmt)
            conn.commit()

    def check_if_player_in_db(player_name: str) -> bool:
        """Check if a player with the given name exists in the players table in the specified database."""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT * FROM players WHERE player_name = '{player_name}';"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query))
            row = result.fetchone()
        if row:
            return "A player with this name already exists."
        return True

    def get_user_email_from_username(username: str) -> str | None:
        """Retrieve the user email for a given username or email from the users table in the specified database."""
        if username is None or username == "":
            return "Username cannot be empty."
        else:
            connection = sqlalchemy_engine.connect()
            query = f"SELECT email FROM users WHERE username = :username;"
            with connection as conn:
                result = conn.execute(sqlalchemy.text(query), {"username": username})
                return result.fetchone()[0]
            
    def retrieve_user_players(email: str) -> pd.DataFrame:
        """Retrieve all players from the players table in the database for a specific user and return as a pandas DataFrame."""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT * FROM players WHERE created_by = '{email}';"
        with connection as conn:
            df = pd.read_sql_query(query, conn)

        return df

    def delete_user_account(email: str):
        """Delete a user and all associated data from the database."""
        connection = sqlalchemy_engine.connect()
        stmtu = users_table.delete().where(users_table.c.email == email)
        stmtp = players_table.delete().where(players_table.c.created_by == email)
        stmtm = matches_table.delete().where(matches_table.c.created_by == email)
        stmtl = player_log_table.delete().where(player_log_table.c.created_by == email)
        stmta = activation_tokens_table.delete().where(activation_tokens_table.c.email == email)
        stmtpr = password_resets_table.delete().where(password_resets_table.c.email == email)
        with connection as conn:
            conn.execute(stmtu)
            conn.execute(stmtp)
            conn.execute(stmtm)
            conn.execute(stmtl)
            conn.execute(stmta)
            conn.execute(stmtpr)
            conn.commit()

    def check_database_for_email(email: str) -> bool:
        """Check if a user with the given email exists in the users table in the specified database."""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT * FROM users WHERE email = '{email}';"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query))
            row = result.fetchone()
        if row:
            return True
        return False

    def put_password_reset_token_in_db(email: str, token: str):
        """Store password reset token in database with expiry"""
        connection = sqlalchemy_engine.connect()
        new_uuid = uuid.uuid4()
        query = f"INSERT INTO password_resets (reset_id, email, reset_token, token_expiry, created_datetime, updated_datetime) VALUES ('{new_uuid}', '{email}', '{token}', NOW() + INTERVAL '1 hour', NOW(), NOW());"
        with connection as conn:
            conn.execute(sqlalchemy.text(query))
            conn.commit()

    def check_if_user_exists(email: str, username: str) -> bool:
        """Check if a user with the given email or username exists in the users table in the specified database."""
        connection = sqlalchemy_engine.connect()
        equery = f"SELECT * FROM users WHERE email = '{email}';"
        uquery = f"SELECT * FROM users WHERE username = '{username}';"
        with connection as conn:
            eresult = conn.execute(sqlalchemy.text(equery))
            uresult = conn.execute(sqlalchemy.text(uquery))
            erow = eresult.fetchone()
            urow = uresult.fetchone()
        if erow:
            return "Email already exists."
        if urow:
            return "Username already exists."
        return True

    def get_password_reset_tokens() -> list[str]:
        """Retrieve all active password reset tokens from the database"""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT reset_token FROM password_resets WHERE token_expiry > NOW() AND token_expiry < NOW() + INTERVAL '1 hour';"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query))
            rows = result.fetchall()

        return [row[0] for row in rows]

    def replace_user_password(email: str, new_password: str):
        """Update the user's password in the users table in the specified database."""
        connection = sqlalchemy_engine.connect()
        query = "UPDATE users SET password_hash = :password_hash, updated_datetime = NOW() WHERE email = :email;"
        with connection as conn:
            conn.execute(sqlalchemy.text(query), {"password_hash": BackEndUtils.create_password_hash(new_password), "email": email})
            conn.commit()

    def get_user_email_from_token(token: str) -> str | None:
        """Get user email from password reset token if valid"""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT email FROM password_resets WHERE reset_token = :reset_token AND token_expiry > NOW();"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query), {"reset_token": token})
            row = result.fetchone()
        if row:
            return row[0]
        return None

    def get_active_activation_tokens_for_email(email: str):
        """Retrieve all active activation tokens for a specific email from the database"""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT token FROM activation_tokens WHERE expires_at > NOW() and email = :email"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query), {"email": email})
            tokens = [row[0] for row in result.fetchall()]

        return tokens

    def put_activation_token_in_db(email: str, token: str):
        """Store activation token in database with expiry"""
        connection = sqlalchemy_engine.connect()
        new_uuid = uuid.uuid4()
        tokens_insert = sqlalchemy.insert(activation_tokens_table).values(
            activation_id=new_uuid,
            email=email,
            token=token,
            expires_at=datetime.datetime.now() + datetime.timedelta(hours=24),  # Token valid for 24 hours
            created_at=datetime.datetime.now()
        )
        with connection as conn:
            conn.execute(tokens_insert)
            conn.commit()

    # def get_user_email_from_activation_token(token: str):
    #     """Get user email from activation token if valid"""
    #     connection = sqlalchemy_engine.connect()
    #     query = f"SELECT email FROM activation_tokens WHERE token = {token} AND expires_at > NOW()"
    #     with connection as conn:
    #         result = conn.execute(sqlalchemy.text(query))
    #         row = result.fetchone()

    #     return row[0] if row else None

    def activate_user_account(email: str):
        """Set user account as active"""
        connection = sqlalchemy_engine.connect()
        query = "UPDATE users SET is_active = 1, activated_at = :datetime WHERE email = :email;"
        with connection as conn:
            conn.execute(sqlalchemy.text(query), {"datetime": datetime.datetime.now(), "email": email})
            conn.commit()

    def delete_activation_token(token: str):
        """Remove activation token after use"""
        connection = sqlalchemy_engine.connect()
        query = f"DELETE FROM activation_tokens WHERE token = :token;"
        with connection as conn:
            conn.execute(sqlalchemy.text(query), {"token": token})
            conn.commit()

    def get_user_email_from_activation_token(token: str, database_name: str = "postgres") -> str | None:
        """Get user email from activation token if valid"""
        connection = sqlalchemy_engine.connect()
        query = "SELECT email FROM activation_tokens WHERE token = :token AND expires_at > NOW();"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query), {"token": token})
            row = result.fetchone()
        
        return row[0] if row else None

    # def activate_user_account(email: str):
    #     """Set user account as active"""
    #     connection = sqlalchemy_engine.connect()
    #     query = f"UPDATE users SET is_active = 1, activated_at = %s WHERE email = %s"
    #     with connection as conn:
    #         conn.execute(sqlalchemy.text(query), (datetime.datetime.now(), email))
    #         conn.commit()

    def delete_activation_token(token: str):
        """Remove activation token after use"""
        connection = sqlalchemy_engine.connect()
        query = "DELETE FROM activation_tokens WHERE token = :token;"
        with connection as conn:
            conn.execute(sqlalchemy.text(query), {"token": token})
            conn.commit()

    def delete_old_activation_tokens(email: str):
        """Remove old activation tokens for a user"""
        connection = sqlalchemy_engine.connect()
        query = "DELETE FROM activation_tokens WHERE email = :email AND expires_at < :expires_at;"
        with connection as conn:
            conn.execute(sqlalchemy.text(query), {"email": email, "expires_at": datetime.datetime.now()})
            conn.commit()

    def is_user_activated(email: str) -> int:
        """Check if user account is activated"""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT is_active FROM users WHERE email = :email"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query), {"email": email})
            row = result.fetchone()
        
        return row[0]

    def get_email_from_username(username: str) -> str | None:
        """Get email address from username"""
        connection = sqlalchemy_engine.connect()
        query = f"SELECT email FROM users WHERE username = :username"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query), {"username": username})
            row = result.fetchone()
        
        return row[0] if row else None


    def get_activation_tokens():
        """Get all valid activation tokens (for verification purposes)"""
        connection = sqlalchemy_engine.connect()
        query = "SELECT token FROM activation_tokens WHERE expires_at > NOW()"
        with connection as conn:
            result = conn.execute(sqlalchemy.text(query))
            tokens = result.fetchall()
        
        return [row[0] for row in tokens]

    def store_user_feedback_in_db(email: str, feedback: str, feedback_type: str="General", feedback_subject: str="User Feedback"):
        """Store user feedback in the database"""
        connection = sqlalchemy_engine.connect()
        # user_id = DBUtils.get_user_uuid(email=email)
        feedback_insert = sqlalchemy.insert(feedback_table).values(
            feedback_id=uuid.uuid4(),
            email=email,
            # user_iduser_id,
            feedback_text=feedback,
            feedback_type=feedback_type,
            feedback_subject=feedback_subject,
            # text_length=len(feedback),
            created_datetime=datetime.datetime.now(),
            updated_datetime=datetime.datetime.now()
        )
        with connection as conn:
            conn.execute(feedback_insert)
            conn.commit()

    def store_contact_us_message(email: str, message: str, issue_type: str="General Inquiry", issue_subject: str="Contact Us Message", issue_priority: str="Normal") -> str:
        """Store contact us message in the database"""
        connection = sqlalchemy_engine.connect()
        ticket_id = uuid.uuid4()
        contact_us_insert = sqlalchemy.insert(contact_us_table).values(
            contact_id=ticket_id,
            email=email,
            message=message,
            issue_type=issue_type,
            issue_subject=issue_subject,
            issue_priority=issue_priority,
            # text_length=len(message),
            created_datetime=datetime.datetime.now(),
            updated_datetime=datetime.datetime.now()
        )
        with connection as conn:
            conn.execute(contact_us_insert)
            conn.commit()
        return str(ticket_id)

class BackEndUtils:
    def __init__(self):
        pass

    def check_if_email_is_valid(email: str) -> bool:
        """Check if the provided email is valid."""
        email = email.strip()
        if email == "":
            return ("Email cannot be empty.")
        if ("@" not in email or "." not in email) or len([i for i in email if i == "@"]) > 1:
            return ("This email is invalid.")
        atindex = email.index("@")
        for i in range(1, len(email)):
            if email[-i] == ".":
                dotindex = email.index(email[-i])
        dotindicies = [i for i in range(len(email)) if email[i] == "."]
        if (atindex == 0) or (dotindex <= atindex + 1):
            return ("This email is invalid.")
        if " " in email:
            return ("Spaces are not allowed in email.")
        return True

    def check_if_username_is_valid(username: str) -> bool:
        """Check if the provided username is valid."""
        if username == "":
            return ("Username cannot be empty.")
        elif not username.isalnum():
            return ("Special characters are not allowed in username.")
        elif " " in username:
            return ("Spaces are not allowed in username.")
        return True

    def check_if_password_is_valid(password: str) -> bool:
        """Check if the provided password is valid."""
        if password == "":
            return ("Password cannot be empty.")
        if len(password) < 8:
            return ("Password must be at least 8 characters long.")
        return True

    def create_password_hash(password: str) -> str:
        """Create a hashed password using bcrypt."""
        # Generate a salt
        salt = bcrypt.gensalt(rounds=15)
        bytes_password = password.encode('utf-8')
        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(bytes_password, salt)
        return hashed_password.decode('utf-8')

    def authenticate_user(username_email: str, password: str) -> list[bool, str | None]:
        """Authenticate a user by checking the provided username/email and password against the database."""
        connection = sqlalchemy_engine.connect()
        uquery = f"SELECT username FROM users WHERE email = '{username_email}' OR username = '{username_email}'"
        pquery = f"SELECT password_hash FROM users WHERE email = '{username_email}' OR username = '{username_email}';"
        
        with connection as conn:
            presult = conn.execute(sqlalchemy.text(pquery))
            uresult = conn.execute(sqlalchemy.text(uquery))
            prow = presult.fetchone()
            urow = uresult.fetchone()
        if prow is None:
            return [False, None]
        stored_hash = prow[0]
        bytes_password = password.encode('utf-8')
        bytes_stored_hash = stored_hash.encode('utf-8')
        return bcrypt.checkpw(bytes_password, bytes_stored_hash), urow[0]

    def send_password_reset_email(email: str, password_reset_link: str):
        """Send password reset email to user"""
        try:
            resend.Emails.send({'from': MY_EMAIL, 
                                'to': email, 
                                'subject': "Password Reset Request - Team Picker", 
                                'html': f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f9f9f9;
                    }}
                    .content {{
                        background-color: white;
                        padding: 30px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .button {{
                        display: inline-block;
                        padding: 12px 30px;
                        margin: 20px 0;
                        background-color: #667eea;
                        color: #ffffff !important;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                    }}
                    .footer {{
                        margin-top: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="content">
                        <h2>Reset Your Password</h2>
                        <p>Hello,</p>
                        <p>We received a request to reset the password for your account. Click the button below to choose a new one:</p>
                        <a href="{password_reset_link}" class="button">Reset Password</a>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #667eea;">{password_reset_link}</p>
                        <p><strong>Note:</strong> This link will expire in {1} hour. </p>
                        <p>If you didn't request a password reset, you can safely ignore this email. Your password will not change until you access the link above and create a new one.</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                        <p>&copy; {datetime.datetime.now().year} Team Picker</p>
                    </div>
                </div>
            </body>
            </html>
            """})
        except Exception as e:
            print(f"Failed to send password reset email: {str(e)}")

    def send_activation_email(email: str, activation_link: str):
        """Send activation email to user"""
        try:
            resend.Emails.send({'from': MY_EMAIL, 
                                'to': email, 
                                'subject': "Account Activation - Team Picker", 
                                'html': f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f9f9f9;
                    }}
                    .content {{
                        background-color: white;
                        padding: 30px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .button {{
                        display: inline-block;
                        padding: 12px 30px;
                        margin: 20px 0;
                        background-color: #667eea;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                    }}
                    .footer {{
                        margin-top: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="content">
                        <h2>Welcome to Team Picker! Please Activate Your Account</h2>
                        <p>Thank you for creating an account. To get started, please activate your account by clicking the button below:</p>
                        <a href="{activation_link}" class="button">Activate Account</a>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #667eea;">{activation_link}</p>
                        <p>This link will expire in 24 hours.</p>
                        <p>If you didn't create this account, please ignore this email.</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated email. Please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """})
            print(f"Activation email sent successfully to {email}")
        except Exception as e:
            print(f"Failed to send activation email: {str(e)}")
    
        # # Configure your SMTP settings
        # SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP server
        # SMTP_PORT = 587
        # SMTP_USERNAME = MY_EMAIL
        # SMTP_PASSWORD = MY_APP_PASSWORD

        # subject = "Activate Your Account"
        
        # html_body = f"""
        # <!DOCTYPE html>
        # <html>
        # <head>
        #     <style>
        #         body {{
        #             font-family: Arial, sans-serif;
        #             line-height: 1.6;
        #             color: #333;
        #         }}
        #         .container {{
        #             max-width: 600px;
        #             margin: 0 auto;
        #             padding: 20px;
        #             background-color: #f9f9f9;
        #         }}
        #         .content {{
        #             background-color: white;
        #             padding: 30px;
        #             border-radius: 8px;
        #             box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        #         }}
        #         .button {{
        #             display: inline-block;
        #             padding: 12px 30px;
        #             margin: 20px 0;
        #             background-color: #667eea;
        #             color: white;
        #             text-decoration: none;
        #             border-radius: 8px;
        #             font-weight: bold;
        #         }}
        #         .footer {{
        #             margin-top: 20px;
        #             text-align: center;
        #             color: #666;
        #             font-size: 12px;
        #         }}
        #     </style>
        # </head>
        # <body>
        #     <div class="container">
        #         <div class="content">
        #             <h2>Welcome! Please Activate Your Account</h2>
        #             <p>Thank you for creating an account. To get started, please activate your account by clicking the button below:</p>
        #             <a href="{activation_link}" class="button">Activate Account</a>
        #             <p>Or copy and paste this link into your browser:</p>
        #             <p style="word-break: break-all; color: #667eea;">{activation_link}</p>
        #             <p>This link will expire in 24 hours.</p>
        #             <p>If you didn't create this account, please ignore this email.</p>
        #         </div>
        #         <div class="footer">
        #             <p>This is an automated email. Please do not reply.</p>
        #         </div>
        #     </div>
        # </body>
        # </html>
        # """
        
        # For development, just print to console
        # print(f"\n{'='*60}")
        # print(f"ACTIVATION EMAIL for {email}")
        # print(f"{'='*60}")
        # print(f"Link: {activation_link}")
        # print(f"{'='*60}\n")
        # print(f"EMAIL USERNAME: {SMTP_USERNAME}")
        # print(f"EMAIL PASSWORD: {SMTP_PASSWORD}")
        # print(f"{'='*60}\n")
        
        # Uncomment below to actually send emails in production

            # msg = MIMEMultipart('alternative')
            # msg['Subject'] = subject
            # msg['From'] = SMTP_USERNAME
            # msg['To'] = email
            
            # html_part = MIMEText(html_body, 'html')
            # msg.attach(html_part)
            
            # server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            # server.starttls()
            # server.login(SMTP_USERNAME, SMTP_PASSWORD)
            # server.send_message(msg)
            # server.quit()
           
    def send_feedback_email_notification(feedback: str, email: str, feedback_type: str, feedback_subject: str):
        """Send feedback email notification to admin"""
        resend.Emails.send({'from': MY_EMAIL, 
                                            'to': TEAM_PICKER_EMAIL, 
                                            'subject': f"Feedback - {feedback_subject} - {feedback_type} - {email}",
                                            'html': f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f4f7f6;
        }}
        .content {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            border-top: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .field-label {{
            font-weight: bold;
            color: #667eea;
            text-transform: uppercase;
            font-size: 12px;
            margin-bottom: 4px;
        }}
        .field-value {{
            margin-bottom: 20px;
            background: #fdfdfd;
            padding: 10px;
            border-radius: 4px;
            border: 1px solid #f0f0f0;
        }}
        .feedback-text {{
            white-space: pre-wrap;
            font-style: italic;
            color: #444;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #888;
            font-size: 12px;
        }}
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            background: #667eea;
            color: white;
            border-radius: 4px;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="header">
                <h2 style="margin-top: 0;">New Feedback Received</h2>
                <p>A user has submitted feedback via the automated system.</p>
            </div>

            <div class="field-label">Subject</div>
            <div class="field-value"><strong>{feedback_subject}</strong></div>

            <div class="field-label">Type</div>
            <div class="field-value"><span class="badge">{feedback_type}</span></div>

            <div class="field-label">From</div>
            <div class="field-value">{email}</div>

            <div class="field-label">Message</div>
            <div class="field-value feedback-text">"{feedback}"</div>

        </div>
        <div class="footer">
            <p>System Notification | Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>This is an automated email. Please do not reply directly to this notification.</p>
        </div>
    </div>
</body>
</html>"""})
 
        # msg = EmailMessage()
        # msg.set_content(f"New user feedback received from {user_uuid}:\n\n{feedback}")
        # msg['Subject'] = f'New User Feedback - {user_uuid}'
        # msg['From'] = MY_EMAIL
        # msg['To'] = MY_EMAIL
        # print("Connecting to SMTP server for feedback notification...")
        # with smtplib.SMTP('smtp.gmail.com', port=587) as s:
        #     s.starttls()
        #     s.login(MY_EMAIL, MY_APP_PASSWORD)
        #     print("Sending feedback notification email...")
        #     s.send_message(msg)
        #     print("Feedback notification email sent.")

    def send_contact_us_email_notification(message: str, email: str, issue_type: str, priority, subject: str, ticket_id: str):
        """Send contact us email notification to admin"""
        resend.Emails.send({'from': MY_EMAIL, 
                                            'to': TEAM_PICKER_EMAIL, 
                                            'subject': f"Issue {priority} - {subject} - {issue_type} - {email}",
                                            'html': f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f0f2f5;
        }}
        .content {{
            background-color: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }}
        .header {{
            border-bottom: 2px solid #eee;
            margin-bottom: 25px;
            padding-bottom: 15px;
        }}
        .header h2 {{
            color: #1a1a1a;
            margin: 0;
            font-size: 22px;
        }}
        .meta-table {{
            width: 100%;
            margin-bottom: 25px;
            border-collapse: collapse;
        }}
        .meta-table td {{
            padding: 8px 0;
            vertical-align: top;
        }}
        .label {{
            font-weight: bold;
            color: #777;
            width: 120px;
            font-size: 13px;
            text-transform: uppercase;
        }}
        .value {{
            color: #333;
            font-size: 15px;
        }}
        .priority-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            background-color: #e2e8f0;
        }}
        /* Optional: You can handle dynamic priority colors in your backend logic */
        .message-box {{
            background-color: #f8fafc;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 4px;
            margin-top: 10px;
        }}
        .footer {{
            margin-top: 25px;
            text-align: center;
            color: #94a3b8;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="header">
                <h2>📩 New Contact Inquiry</h2>
            </div>

            <table class="meta-table">
                <tr>
                    <td class="label">Subject:</td>
                    <td class="value"><strong>{subject}</strong></td>
                </tr>
                <tr>
                    <td class="label">Priority:</td>
                    <td class="value">
                        <span class="priority-tag">{priority}</span>
                    </td>
                </tr>
                <tr>
                    <td class="label">Issue Type:</td>
                    <td class="value">{issue_type}</td>
                </tr>
                <tr>
                    <td class="label">From:</td>
                    <td class="value"><a href="mailto:{email}" style="color: #667eea; text-decoration: none;">{email}</a></td>
                </tr>
            </table>

            <div class="label" style="margin-bottom: 10px;">Message Contents:</div>
            <div class="message-box">
                <p style="margin: 0; white-space: pre-wrap;">{message}</p>
            </div>

            <div style="margin-top: 30px; text-align: center;">
                <a href="mailto:{email}?subject=Re: {subject}" 
                   style="background-color: #667eea; color: white; padding: 12px 25px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
                   Reply to User
                </a>
            </div>
        </div>
        
        <div class="footer">
            <p>Sent via Website Contact Form</p>
            <p>Internal Tracking ID: {ticket_id}</p>
            <p>This is an automated email. Please do not reply</p>
        </div>
    </div>
</body>
</html>"""})

    #     msg = EmailMessage()
    #     msg.set_content(f"New contact us message received from {user_uuid} ({email}):\n\n{message}")
    #     msg['Subject'] = f'New Contact Us Message - {user_uuid}'
    #     msg['From'] = MY_EMAIL
    #     msg['To'] = MY_EMAIL
    #     print("Connecting to SMTP server for contact us notification...")
    #     with smtplib.SMTP('smtp.gmail.com', port=587) as s:
    #         s.starttls()
    #         s.login(MY_EMAIL, MY_APP_PASSWORD)
    #         print("Sending contact us notification email...")
    #         s.send_message(msg)
    #         print("Contact us notification email sent.")
    
    def send_contact_us_email_acknowledgement(message: str, email: str, issue_type: str, subject: str, priority: str, ticket_id: str):
        """Send contact us email acknowledgement to user"""
        resend.Emails.send({'from': MY_EMAIL, 
                                            'to': email, 
                                            'subject': "We Received Your Message - Team Picker",
                                            'html': f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f4f7f6;
        }}
        .content {{
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            text-align: center;
        }}
        .icon {{
            font-size: 48px;
            margin-bottom: 20px;
        }}
        .header h2 {{
            color: #2d3748;
            margin-bottom: 10px;
        }}
        .details-box {{
            text-align: left;
            background-color: #f8fafc;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
            border: 1px solid #e2e8f0;
        }}
        .details-title {{
            font-weight: bold;
            font-size: 14px;
            color: #667eea;
            text-transform: uppercase;
            margin-bottom: 10px;
            display: block;
        }}
        .footer {{
            margin-top: 25px;
            text-align: center;
            color: #94a3b8;
            font-size: 12px;
        }}
        .divider {{
            height: 1px;
            background-color: #e2e8f0;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="icon">📨</div>
            <div class="header">
                <h2>We've Received Your Message</h2>
                <p>Hi there! Thanks for reaching out. This is a quick note to let you know that your message has landed safely in our inbox.</p>
            </div>

            <div class="details-box">
                <span class="details-title">Submission Summary</span>
                <p style="margin: 5px 0;"><strong>Subject:</strong> {subject}</p>
                <p style="margin: 5px 0;"><strong>Issue Type:</strong> {issue_type}</p>
                <p style="margin: 5px 0;"><strong>Priority:</strong> {priority}</p>
                <div class="divider"></div>
                <p style="margin: 0; font-style: italic; color: #4a5568;">"{message}"</p>
            </div>

            <p>Our team is currently reviewing your inquiry. You can generally expect a response within **24-48 business hours**.</p>
            
            <p style="font-size: 14px; color: #718096;">Your Reference ID: <strong>#{ticket_id}</strong></p>
        </div>
        
        <div class="footer">
            <p>&copy; 2026 Your Company Name. All rights reserved.</p>
            <p>If you didn't send a message to us, please disregard this email.</p>
        </div>
    </div>
</body>
</html>"""})
        # msg = EmailMessage()
        # msg.set_content(f"Thank you for contacting us. We have received your message:\n\n{message}\n\nWe will get back to you shortly.")
        # msg['Subject'] = 'Contact Us Acknowledgement'
        # msg['From'] = MY_EMAIL
        # msg['To'] = email
        # print("Connecting to SMTP server for contact us acknowledgement...")
        # with smtplib.SMTP('smtp.gmail.com', port=587) as s:
        #     s.starttls()
        #     s.login(MY_EMAIL, MY_APP_PASSWORD)
        #     print("Sending contact us acknowledgement email...")
        #     s.send_message(msg)
        #     print("Contact us acknowledgement email sent.")

    def balance_teams(list_of_player_names: list, email: str):
        all_players = DBUtils.retrieve_user_players(email)
        print(all_players[all_players["points_win_rate"].isna()])
        all_players.fillna(0, inplace=True)
        print(all_players[all_players["points_win_rate"].isna()]["points_win_rate"])
        match_players = all_players[all_players['player_name'].isin(list_of_player_names)]
        print(match_players)
        players_ids = match_players["player_name"].tolist()
        player_points_win_rates = match_players["points_win_rate"].tolist()
        if len(match_players) % 2 != 0:
            print("Warning: Odd number of players selected. The selection may be unbalanced.")
        for player_id, points_win_rate in zip(players_ids, player_points_win_rates):
            print(f"{match_players['player_name'].loc[match_players['player_name'] == player_id].values[0]} has a points win rate of {points_win_rate}.")

        team_1 = []
        team_1_rating = []
        team_2 = []
        team_2_rating = []

        total_average_win_rate = np.mean(player_points_win_rates)
        print("Total average win rate:", total_average_win_rate)

        if np.mean(player_points_win_rates) == 0:
            print("All players have a win rate of 0. Teams will be selected randomly.")
            if len(match_players) % 2 != 0:
                team_1 = random.sample(players_ids, len(players_ids)//2 + 1)
                team_2 = [player for player in players_ids if player not in team_1]
            else:
                team_1 = random.sample(players_ids, len(players_ids)/2)
                team_2 = [player for player in players_ids if player not in team_1]

            DBUtils.add_new_match_to_db(
                email=email,
                team_1_players=team_1,
                team_2_players=team_2
            )
            # return team_1, team_2, 0, 0
        else:
            first_team = random.choice([team_1, team_2])
            if first_team == team_1:
                team = team_1
                opp = team_2
                player_ratings = team_1_rating
                opp_player_ratings = team_2_rating
            else:
                team = team_2
                opp = team_1
                player_ratings = team_2_rating
                opp_player_ratings = team_1_rating

            while players_ids != []:
                if team == [] and opp == []:
                    player = random.choice(players_ids)
                    rating_index = players_ids.index(player)
                    rating = player_points_win_rates[rating_index] 
                    print(match_players['player_name'].loc[match_players['player_name'] == player].values[0])
                    # print(match_players)
                    print(player_points_win_rates)
                    team.append(player)
                    player_ratings.append(rating)
                    players_ids.remove(player)
                    del player_points_win_rates[rating_index] 
                elif len(team) < len(opp):
                    gaps = []
                    for player, rating in zip(players_ids, player_points_win_rates):
                        g = copy.deepcopy(player_ratings)
                        g.append(rating)
                        gn = np.mean(g)
                        gaps.append(abs(gn - np.mean(opp_player_ratings)))
                    min_gap_index = gaps.index(min(gaps))
                    team.append(players_ids[min_gap_index])
                    player_ratings.append(player_points_win_rates[min_gap_index])
                    print(match_players['player_name'].loc[match_players['player_name'] == players_ids[min_gap_index]].values[0])
                    print("Team:")
                    # print(match_players)
                    print(player_points_win_rates)
                    players_ids.remove(players_ids[min_gap_index])
                    del player_points_win_rates[min_gap_index]
                elif len(team) > len(opp):
                    gaps = []
                    for player, rating in zip(players_ids, player_points_win_rates):
                        g = copy.deepcopy(opp_player_ratings)
                        g.append(rating)
                        gn = np.mean(g)
                        gaps.append(abs(gn - np.mean(player_ratings)))
                    min_gap_index = gaps.index(min(gaps))
                    opp.append(players_ids[min_gap_index])
                    opp_player_ratings.append(player_points_win_rates[min_gap_index])
                    print(match_players['player_name'].loc[match_players['player_name'] == players_ids[min_gap_index]].values[0])
                    print("Opponent Team:")
                    # print(match_players)
                    print(player_points_win_rates)
                    players_ids.remove(players_ids[min_gap_index])
                    del player_points_win_rates[min_gap_index]
                elif len(team) == len(opp):
                    if np.mean(player_ratings) <= np.mean(opp_player_ratings):
                        gaps = []
                        for player, rating in zip(players_ids, player_points_win_rates):
                            g = copy.deepcopy(player_ratings)
                            g.append(rating)
                            gn = np.mean(g)
                            gaps.append(abs(gn - np.mean(opp_player_ratings)))
                        min_gap_index = gaps.index(min(gaps))
                        team.append(players_ids[min_gap_index])
                        player_ratings.append(player_points_win_rates[min_gap_index])
                        print(match_players['player_name'].loc[match_players['player_name'] == players_ids[min_gap_index]].values[0])
                        print("Team:")
                        # print(match_players)
                        print(player_points_win_rates)
                        players_ids.remove(players_ids[min_gap_index])
                        del player_points_win_rates[min_gap_index]
                    else:
                        gaps = []
                        for player, rating in zip(players_ids, player_points_win_rates):
                            g = copy.deepcopy(opp_player_ratings)
                            g.append(rating)
                            gn = np.mean(g)
                            gaps.append(abs(gn - np.mean(player_ratings)))
                        min_gap_index = gaps.index(min(gaps))
                        opp.append(players_ids[min_gap_index])
                        opp_player_ratings.append(player_points_win_rates[min_gap_index])
                        print(match_players['player_name'].loc[match_players['player_name'] == players_ids[min_gap_index]].values[0])
                        print("Opponent Team:")
                        # print(match_players)
                        print(player_points_win_rates)
                        players_ids.remove(players_ids[min_gap_index])
                        del player_points_win_rates[min_gap_index]

                
                print(f"Team 1: {team} has an average win rate of {np.mean(player_ratings)}")
                print(f"Team 2: {opp} has an average win rate of {np.mean(opp_player_ratings)}")
        teama = []
        teamb = []
        for name in team:
            row = all_players[all_players['player_name'] == name]
            print(row)
            p = {}
            # print(type(df["player_name"].iloc[row]))
            p["name"] = name
            p["wins"] = int(row["wins"].values[0])
            p["draws"] = int(row["draws"].values[0])
            p["losses"] = int(row["losses"].values[0])
            p["number_of_games"] = int(row["number_of_games"].values[0])
            p["points_win_rate"] = float(row["points_win_rate"].values[0])
            teama.append(p)
        for name in opp:
            row = all_players[all_players['player_name'] == name]
            print(row)
            p = {}
            # print(type(df["player_name"].iloc[row]))
            p["name"] = name
            p["wins"] = int(row["wins"].values[0])
            p["draws"] = int(row["draws"].values[0])
            p["losses"] = int(row["losses"].values[0])
            p["number_of_games"] = int(row["number_of_games"].values[0])
            p["points_win_rate"] = float(row["points_win_rate"].values[0])
            teamb.append(p)
        print("Final Teams:")
        print(teama)
        print(teamb)
        return teama, teamb, np.mean(team_1_rating), np.mean(team_2_rating), total_average_win_rate

    def process_match_day():

        result = None
        # user_id = int(get_data_from_postgres("SELECT * FROM users LIMIT 1;")["user_id"].values[0])
        user_id = 1
        tab = sqlalchemy.Table('matches', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
        stmt = matches_table.update().where(tab.c.user_id == user_id).values(outcome="Unknown")
        connection.execute(stmt)
        connection.commit()
        DBUtils.get_data_from_postgres(f"SELECT * FROM matches WHERE user_id = {user_id}")
        result_confirmed = True
        while result_confirmed is True:
            init = DBUtils.get_data_from_postgres(f"SELECT * FROM matches WHERE user_id = {user_id} ORDER BY match_date DESC LIMIT 1;")
            init_result = init["outcome"].values[0]
            init_match_id = init["match_id"].values[0]
            # init_datetime = get_data_from_postgres(f"SELECT * FROM matches WHERE user_id = {user_id} ORDER BY match_date DESC LIMIT 1;")["match_date"].values[0]
            if init_result == "Unknown":
                update_result = input("Would you like to update the result of the last match? Yes or No?\n").lower()
                rc = True
                while rc is True:
                    if update_result == "no":
                        break
                    elif update_result == "yes":
                        result = input("Which team won the last match? Team 1, Team 2 or Draw?\n").lower().capitalize()
                        if result == "Team 1" or result == "Team 2" or result == "Draw":
                            DBUtils.update_match_outcome(match_id=init_match_id, outcome=result)
                            result_confirmed = False
                            rc = False
                        else:
                            print("Invalid input. Please input Team 1, Team 2 or Draw.")
                    else:
                        print("Invalid input. Please input Yes or No.")
            else:
                break
        

        if result is not None:
            if result == "Draw":
                pl_draw_update = player_log_table.update().where(player_log_table.c.match_id == init_match_id).values(team_outcome="Draw")
                p_draws_update = update(players_table).where(PlayerLog.match_id == init_match_id).values(draws=(players_table.c.draws+1))
                p_points_update = update(players_table).where(PlayerLog.match_id == init_match_id).values(points=(players_table.c.points+1))
                connection.execute(pl_draw_update)
                connection.execute(p_draws_update)
                connection.execute(p_points_update)
            else:
                pl_win_update = player_log_table.update().where(player_log_table.c.match_id == init_match_id and player_log_table.c.team == result).values(team_outcome="Win")
                pl_lose_update = player_log_table.update().where(player_log_table.c.match_id == init_match_id and player_log_table.c.team != result).values(team_outcome="Lose")
                p_wins_update = update(players_table).where(PlayerLog.team == result and PlayerLog.match_id == init_match_id).values(wins=(players_table.c.wins+1))
                p_losses_update = update(players_table).where(PlayerLog.team != result and PlayerLog.match_id == init_match_id).values(losses=(players_table.c.losses+1))
                p_points_update = update(players_table).where(PlayerLog.team == result and PlayerLog.match_id == init_match_id).values(points=(players_table.c.points+3))
                connection.execute(pl_win_update)
                connection.execute(pl_lose_update)
                connection.execute(p_wins_update)
                connection.execute(p_losses_update)
                connection.execute(p_points_update)
            p_nog_update = update(players_table).where(players_table.c.player_id == PlayerLog.player_id).values(number_of_games=(players_table.c.number_of_games+1))
            connection.execute(p_nog_update)
            connection.commit()
        else:
            print("No result to process.")

        match_players = DBUtils.get_player_pool_from_db(number_of_players=10, user_id=user_id)
        players_ids = match_players["player_id"].tolist()
        player_points_win_rates = match_players["points_win_rate"].tolist()
        # print(type(player_points_win_rates[0]))
        if len(match_players) % 2 != 0:
            print("Warning: Odd number of players selected. The selection may be unbalanced.")
        for player_id, points_win_rate in zip(players_ids, player_points_win_rates):
            print(f"{match_players['player_name'].loc[match_players['player_id'] == player_id].values[0]} has a win rate of {points_win_rate}.")

        # player_ids_backup = copy.deepcopy(players_ids)

        team_1 = []
        team_1_rating = []
        team_2 = []
        team_2_rating = []

        if np.mean(player_points_win_rates) == 0:
            print("All players have a win rate of 0. Teams will be selected randomly.")
            if len(match_players) % 2 != 0:
                team_1 = random.sample(players_ids, len(players_ids)//2 + 1)
                team_2 = [player for player in players_ids if player not in team_1]
            else:
                team_1 = random.sample(players_ids, len(players_ids)/2)
                team_2 = [player for player in players_ids if player not in team_1]

            DBUtils.add_new_match_to_db(
                user_id=user_id,
                team_1_players=team_1,
                team_2_players=team_2
            )
            # return team_1, team_2, 0, 0
        else:
            first_team = random.choice([team_1, team_2])
            if first_team == team_1:
                team = team_1
                opp = team_2
                player_ratings = team_1_rating
                opp_player_ratings = team_2_rating
            else:
                team = team_2
                opp = team_1
                player_ratings = team_2_rating
                opp_player_ratings = team_1_rating

            while players_ids != []:
                if team == [] and opp == []:
                    player = random.choice(players_ids)
                    rating_index = players_ids.index(player)
                    rating = player_points_win_rates[rating_index] 
                    print(match_players['player_name'].loc[match_players['player_id'] == player].values[0])
                    # print(match_players)
                    print(player_points_win_rates)
                    team.append(player)
                    player_ratings.append(rating)
                    players_ids.remove(player)
                    del player_points_win_rates[rating_index] 
                elif len(team) < len(opp):
                    gaps = []
                    for player, rating in zip(players_ids, player_points_win_rates):
                        g = copy.deepcopy(player_ratings)
                        g.append(rating)
                        gn = np.mean(g)
                        gaps.append(abs(gn - np.mean(opp_player_ratings)))
                    min_gap_index = gaps.index(min(gaps))
                    team.append(players_ids[min_gap_index])
                    player_ratings.append(player_points_win_rates[min_gap_index])
                    print(match_players['player_name'].loc[match_players['player_id'] == players_ids[min_gap_index]].values[0])
                    print("Team:")
                    # print(match_players)
                    print(player_points_win_rates)
                    players_ids.remove(players_ids[min_gap_index])
                    del player_points_win_rates[min_gap_index]
                elif len(team) > len(opp):
                    gaps = []
                    for player, rating in zip(players_ids, player_points_win_rates):
                        g = copy.deepcopy(opp_player_ratings)
                        g.append(rating)
                        gn = np.mean(g)
                        gaps.append(abs(gn - np.mean(player_ratings)))
                    min_gap_index = gaps.index(min(gaps))
                    opp.append(players_ids[min_gap_index])
                    opp_player_ratings.append(player_points_win_rates[min_gap_index])
                    print(match_players['player_name'].loc[match_players['player_id'] == players_ids[min_gap_index]].values[0])
                    print("Opponent Team:")
                    # print(match_players)
                    print(player_points_win_rates)
                    players_ids.remove(players_ids[min_gap_index])
                    del player_points_win_rates[min_gap_index]
                elif len(team) == len(opp):
                    if np.mean(player_ratings) <= np.mean(opp_player_ratings):
                        gaps = []
                        for player, rating in zip(players_ids, player_points_win_rates):
                            g = copy.deepcopy(player_ratings)
                            g.append(rating)
                            gn = np.mean(g)
                            gaps.append(abs(gn - np.mean(opp_player_ratings)))
                        min_gap_index = gaps.index(min(gaps))
                        team.append(players_ids[min_gap_index])
                        player_ratings.append(player_points_win_rates[min_gap_index])
                        print(match_players['player_name'].loc[match_players['player_id'] == players_ids[min_gap_index]].values[0])
                        print("Team:")
                        # print(match_players)
                        print(player_points_win_rates)
                        players_ids.remove(players_ids[min_gap_index])
                        del player_points_win_rates[min_gap_index]
                    else:
                        gaps = []
                        for player, rating in zip(players_ids, player_points_win_rates):
                            g = copy.deepcopy(opp_player_ratings)
                            g.append(rating)
                            gn = np.mean(g)
                            gaps.append(abs(gn - np.mean(player_ratings)))
                        min_gap_index = gaps.index(min(gaps))
                        opp.append(players_ids[min_gap_index])
                        opp_player_ratings.append(player_points_win_rates[min_gap_index])
                        print(match_players['player_name'].loc[match_players['player_id'] == players_ids[min_gap_index]].values[0])
                        print("Opponent Team:")
                        # print(match_players)
                        print(player_points_win_rates)
                        players_ids.remove(players_ids[min_gap_index])
                        del player_points_win_rates[min_gap_index]

                
                print(f"Team 1: {team} has an average win rate of {np.mean(player_ratings)}")
                print(f"Team 2: {opp} has an average win rate of {np.mean(opp_player_ratings)}")

            DBUtils.add_new_match_to_db(
                user_id=user_id,
                team_1_rating=np.mean(player_ratings),
                team_2_rating=np.mean(opp_player_ratings)
            )

        # return team, opp, np.mean(player_ratings), np.mean(opp_player_ratings)
    
    


        # player = random.choice(players_ids)
        # rating_index = players_ids.index(player)
        # rating = player_points_win_rates[rating_index] 
        # if team == []:
        #     team.append(player)
        #     print(match_players['player_name'].loc[match_players['player_id'] == player].values[0])
        #     print(match_players)
        #     print(player_points_win_rates)
        #     player_ratings.append(float(rating))
        #     players_ids.remove(player)
        #     del player_points_win_rates[rating_index]       
        # else:
            


        #     if np.mean(player_ratings) <= np.mean(opp_player_ratings):
        # team.append(player)
        # print(match_players['player_name'].loc[match_players['player_id'] == player].values[0])
        # print(match_players)
        # print(player_points_win_rates)
        # rating_index = players_ids.index(player)
        # rating = player_points_win_rates[rating_index]
        # player_ratings.append(float(rating))
        # players_ids.remove(player)
        # del player_points_win_rates[rating_index]


#     counter = 0
#     for number in range(len(match_players)):
#         if counter % 2 == 0:
#             team = team_1
#             player_ratings = team_1_rating
#             team_rating = np.mean(team_1_rating)
#             opp_team_rating = np.mean(team_2_rating)
#         else:
#             team = team_2
#             player_ratings = team_2_rating
#             team_rating = np.mean(team_2_rating)
#             opp_team_rating = np.mean(team_1_rating)
#         switch = True
#         if team_rating > opp_team_rating:
#             temp_players = []
#             while switch is True:
#                 player = random.choice(players_ids)
#                 player_name = match_players["player_name"].loc[match_players['player_id'] == player].values[0]
#                 rating_index = players_ids.index(player)
#                 rating = player_points_win_rates[rating_index]
#                 temp_players.append(player)
#                 print(player_name)
#                 print(f"Rating: {rating}")
#                 print(f"Opponent Rating: {opp_team_rating}")
#                 print(f"Min Win Rate: {min(player_points_win_rates)}")
#                 print(players_ids)
#                 print(player_points_win_rates)
#                 if (opp_team_rating < min(player_points_win_rates)) or (opp_team_rating == min(player_points_win_rates)):
#                     switch = False
#                 elif rating < opp_team_rating:
#                     switch = False
#                 elif len(set(temp_players)) == len(match_players):
#                     switch = False
#                 # elif len(players_ids) == 0:
#                 #     switch = False
#         elif team_rating < opp_team_rating:
#             temp_players = []
#             while switch is True:
#                 player = random.choice(players_ids)
#                 rating_index = players_ids.index(player)
#                 rating = player_points_win_rates[rating_index]
#                 temp_players.append(player)
#                 print(2)
#                 print(player)
#                 print(f"Rating: {rating}")
#                 print(f"Opponent Rating: {opp_team_rating}")
#                 print(f"Min Win Rate: {min(player_points_win_rates)}")
#                 print(players_ids)
#                 print(player_points_win_rates)
#                 if (opp_team_rating < max(player_points_win_rates)) or (opp_team_rating == max(player_points_win_rates)):
#                     switch = False
#                 elif rating > opp_team_rating:
#                     switch = False
#                 elif len(set(temp_players)) == len(match_players):
#                     switch = False
#         else:
#             player = random.choice(players_ids)
#         team.append(player)
#         print(match_players['player_name'].loc[match_players['player_id'] == player_id].values[0])
#         print(match_players)
#         print(player_points_win_rates)
#         rating_index = players_ids.index(player)
#         rating = player_points_win_rates[rating_index]
#         player_ratings.append(float(rating))
#         players_ids.remove(player)
#         del player_points_win_rates[rating_index]
#         counter += 1
    
#     store_teams(team_1, team_2)

#     print(f"Team 1: {team_1} has an average win rate of {np.mean(team_1_rating)}")
#     print(f"Team 2: {team_2} has an average win rate of {np.mean(team_2_rating)}")
# operation = False

        # get_data_from_postgres(f"SELECT * FROM player_log WHERE match_id = {init_match_id};")
    # last_result = pd.read_csv('team_players.csv')
    # player_record = pd.read_csv('player_info.csv')
    # if conf_check is True:
    #     while conf_check is True:
    #         update_result = input("Would you like to update the result of the last match? Yes or No?\n").lower()
    #         if update_result == "no":
    #             check = input("Are you sure you don't want to update the result of the last match? If it is not updated, the player list will be overwritten.\n").lower()
    #             if check == "yes":
    #                 break
    #             elif check == "no":
    #                 continue
    #             else:
    #                 print("Invalid input. Please input Yes or No.")
    #         elif update_result == "yes":
    #             last_match_result = input("Which team won the last match? Team 1, Team 2 or Draw?\n").lower()
    #             team_1 = last_result["team_1"].tolist()
    #             team_2 = last_result["team_2"].tolist()
    #             if last_match_result == "team 1":
    #                 for player in team_1:
    #                     player_record.loc[player_record['player_name'] == player, 'wins'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'points'] += 3
    #                     player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
    #                     player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
    #                 for player in team_2:
    #                     player_record.loc[player_record['player_name'] == player, 'losses'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'points'] += 0
    #                     player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
    #                     player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
    #             elif last_match_result == "team 2":
    #                 for player in team_2:
    #                     player_record.loc[player_record['player_name'] == player, 'wins'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'points'] += 3
    #                     player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
    #                     player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
    #                 for player in team_1:
    #                     player_record.loc[player_record['player_name'] == player, 'losses'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'points'] += 0
    #                     player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
    #                     player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
    #             elif last_match_result == "draw":
    #                 for player in (team_1 + team_2):
    #                     player_record.loc[player_record['player_name'] == player, 'draws'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
    #                     player_record.loc[player_record['player_name'] == player, 'points'] += 3
    #                     player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
    #                     player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
    #             else:
    #                 print("Invalid input. Please input Team 1, Team 2 or Draw.")
    #             player_record.to_csv('player_info.csv', index=False)     
    #             store_teams()
    #         else:
    #             print("Invalid input. Please input Yes or No.")
    #         conf_check = False
    # store_teams()
    # operation = True
    # while operation is True:
    #     option = int(input("Would you like to do today? Please choose a number.\n1. Add a player\n2. Remove a player\n3. Merge players\n4. Pick a team\n5. Exit"))
    #     if type(option) == int and option in [1, 2, 3, 4]:
    #         if option == 1:
    #             player_name = input("Please enter the name of the player you would like to add.\n")
    #             add_player(player_name)
    #             operation = False
    #         elif option == 2:
    #             player_name = input("Please enter the name of the player you would like to remove.\n")
    #             remove_player(player_name)
    #             operation = False
    #         elif option == 3:
    #             player_names = input("Please enter the names of the players you would like to merge. Please separate them with a comma.\n").split(",")
    #             true_name = input("Please enter the name of the player you would like to merge them into.\n")
    #             merge_player(player_names, true_name)
    #             operation = False
    #         elif option == 5:
    #             break
    #         elif option == 4:
    #             players_this_week = load_weekly_players()
    #             players_on_record = retrieve_players()

    #             for player in players_this_week:
    #                 if player not in players_on_record:
    #                     add_player(player)

    #             win_rates = retrieve_win_rates(players_this_week)
    #             print(win_rates)
            
    #             for player, win_rate in zip(players_this_week, win_rates):
    #                 print(f"{player} has a win rate of {win_rate}.")

    #             team_1 = []
    #             team_1_rating = []
    #             team_2 = []
    #             team_2_rating = []

    #             counter = 0
    #             for number in range(len(players_this_week)):
    #                 if counter % 2 == 0:
    #                     team = team_1
    #                     player_ratings = team_1_rating
    #                     team_rating = np.mean(team_1_rating)
    #                     opp_team_rating = np.mean(team_2_rating)
    #                 else:
    #                     team = team_2
    #                     player_ratings = team_2_rating
    #                     team_rating = np.mean(team_2_rating)
    #                     opp_team_rating = np.mean(team_1_rating)
    #                 switch = True
    #                 if team_rating > opp_team_rating:
    #                     temp_players = []
    #                     while switch is True:
    #                         player = random.choice(players_this_week)
    #                         rating_index = players_this_week.index(player)
    #                         rating = win_rates[rating_index]
    #                         temp_players.append(player)
    #                         print(player)
    #                         print(f"Rating: {rating}")
    #                         print(f"Opponent Rating: {opp_team_rating}")
    #                         print(f"Min Win Rate: {min(win_rates)}")
    #                         if (opp_team_rating < min(win_rates)) or (opp_team_rating == min(win_rates)):
    #                             switch = False
    #                         elif rating < opp_team_rating:
    #                             switch = False
    #                         elif len(set(temp_players)) == len(players_this_week):
    #                             switch = False
    #                 elif team_rating < opp_team_rating:
    #                     temp_players = []
    #                     while switch is True:
    #                         player = random.choice(players_this_week)
    #                         rating_index = players_this_week.index(player)
    #                         rating = win_rates[rating_index]
    #                         temp_players.append(player)
    #                         print(2)
    #                         print(player)
    #                         print(f"Rating: {rating}")
    #                         print(f"Opponent Rating: {opp_team_rating}")
    #                         print(f"Min Win Rate: {min(win_rates)}")
    #                         if (opp_team_rating < max(win_rates)) or (opp_team_rating == max(win_rates)):
    #                             switch = False
    #                         elif rating > opp_team_rating:
    #                             switch = False
    #                         elif len(set(temp_players)) == len(players_this_week):
    #                             switch = False
    #                 else:
    #                     player = random.choice(players_this_week)
    #                 team.append(player)
    #                 print(player)
    #                 print(players_this_week)
    #                 print(win_rates)
    #                 rating_index = players_this_week.index(player)
    #                 rating = win_rates[rating_index]
    #                 player_ratings.append(float(rating))
    #                 players_this_week.remove(player)
    #                 del win_rates[rating_index]
    #                 counter += 1
                
    #             store_teams(team_1, team_2)

    #             print(f"Team 1: {team_1} has an average win rate of {np.mean(team_1_rating)}")
    #             print(f"Team 2: {team_2} has an average win rate of {np.mean(team_2_rating)}")
    #         operation = False
    #     else:
    #         print("This is an invalid input. Please input an integer between 1 and 4.")

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print("Code started at: " + str(start_time))

    # place code here
    # store_teams()
    # get_data_from_postgres()
    # run_query("CREATE TABLE games (game_id SERIAL PRIMARY KEY, user_id uuid, game_date TIMESTAMP NOT NULL, team_coloured VARCHAR(100)[], team_white VARCHAR(100)[], team_coloured_score INT NOT NULL, team_white_score INT NOT NULL);")
    # process_match_day()
    # add_new_player_with_stats_to_db("Test Player")
    # create_matches_table("matches")
    # print(get_data_from_postgres("SELECT * FROM matches ORDER BY match_date DESC LIMIT 1;")["outcome"].values[0])
    # add_new_match_to_db(team_1="Team A", team_2="Team B", team_1_score=5, team_2_score=3, location="Local Park", referee="Referee Name", match_date=datetime.datetime.now(), outcome="Team A")
    # add_new_table_to_db("players_test")
    # create_user_table("users")
    # print(get_data_from_postgres(f"SELECT * FROM matches WHERE user_id = {get_data_from_postgres('SELECT * FROM users LIMIT 1;')['user_id'].values[0]};"))
    # process_match_day()
    # create_matches_table("testing")
    # create_player_log_table("testing")
    # create_password_reset_table("testing")
    # create_users_table("testing")
    # check_if_user_exists("nicholaicorbie@yahoo.com", database_name="testing")
    # print(authenticate_user("nicholaicorbie@yahoo.com", "1234", database_name="testing"))
    # get_data_from_postgres(f"SELECT * FROM player_log WHERE match_id = {1};")
    # user_id = int(get_data_from_postgres("SELECT * FROM users LIMIT 1;")["user_id"].values[0])
    # result = "Draw"
    # init = get_data_from_postgres(f"SELECT * FROM matches WHERE user_id = {user_id} ORDER BY match_date DESC LIMIT 1;")
    # # init_result = init["outcome"].values[0]
    # init_match_id = int(init["match_id"].values[0])
    # print(init_match_id)
    # print(type(init_match_id))
    # Tables.create_feedback_table("testing")
    # Tables.create_contact_us_table("testing")
    # DBUtils.query_db("SELECT * FROM users;")
    # if result:
    #     player_log_table = sqlalchemy.Table('player_log', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
    #     players_table = sqlalchemy.Table('players', sqlalchemy.MetaData(), autoload_with=sqlalchemy_engine)
    #     stmt1 = None
    #     if result == "Draw":
    #         stmt = player_log_table.update().where(player_log_table.c.match_id == init_match_id).values(team_outcome="Draw")
    #     else:
    #         stmt = player_log_table.update().where(player_log_table.c.match_id == init_match_id and player_log_table.c.team == result).values(team_outcome="Win")
    #         stmt1 = player_log_table.update().where(player_log_table.c.match_id == init_match_id and player_log_table.c.team != result).values(team_outcome="Lose")
    #     stmt2 = players_table.update().where(players_table.c.player_id==sqlalchemy.select(player_log_table.c.player_id).where(player_log_table.c.match_id == init_match_id).as_scalar()).values(number_of_games=players_table.c.number_of_games+1)
    #     # stmt2 = players_table.update().values(number_of_games=players_table.c.number_of_games)
    #     # with sqlalchemy_engine.connect() as connection:
    #     connection.execute(stmt)
    #     if stmt1 is not None:
    #         connection.execute(stmt1)
    #     connection.execute(stmt2)
    #     connection.commit()
    # else:
    #     print("No result to process.")

    end_time = datetime.datetime.now()
    print("Code ended at: " + str(end_time))
    runtime = end_time - start_time
    print(f"Code ran in {runtime/60} minutes and {runtime} seconds.")

# enforce equal length constraint
# true team balance