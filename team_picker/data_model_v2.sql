CREATE TABLE "matches" (
  "match_id" uuid PRIMARY KEY,
  "team_1" text,
  "team_2" text,
  "team_1_rating" double,
  "team_2_rating" double,
  "team_1_score" int,
  "team_2_score" int,
  "match_datetime" timestamp,
  "location" text,
  "referee" text,
  "outcome" text,
  "created_by" uuid,
  "updated_by" uuid,
  "created_datetime" timestamp,
  "updated_datetime" timestamp
);

CREATE TABLE "players" (
  "player_id" uuid PRIMARY KEY,
  "player_name" text,
  "number_of_games" int,
  "wins" int,
  "draws" int,
  "losses" int,
  "points" int,
  "win_rate" float,
  "points_win_rate" float,
  "points_per_game" float,
  "created_by" uuid,
  "updated_by" uuid,
  "created_datetime" timestamp,
  "updated_datetime" timestamp
);

CREATE TABLE "users" (
  "user_id" uuid PRIMARY KEY,
  "user_name" text,
  "email" text,
  "password" text,
  "created_by" uuid,
  "updated_by" uuid,
  "created_datetime" timestamp,
  "updated_datetime" timestamp
);

CREATE TABLE "player_log" (
  "log_id" uuid PRIMARY KEY,
  "match_id" uuid,
  "player_id" uuid,
  "player_team" text,
  "team_outcome" text,
  "match_datetime" timestamp,
  "created_by" uuid,
  "updated_by" uuid,
  "created_datetime" timestamp,
  "updated_datetime" timestamp
);

ALTER TABLE "matches" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("user_id");

ALTER TABLE "player_log" ADD FOREIGN KEY ("match_id") REFERENCES "matches" ("match_id");

ALTER TABLE "player_log" ADD FOREIGN KEY ("player_id") REFERENCES "players" ("player_id");

ALTER TABLE "player_log" ADD FOREIGN KEY ("match_datetime") REFERENCES "matches" ("match_datetime");

ALTER TABLE "matches" ADD FOREIGN KEY ("team_1") REFERENCES "player_log" ("player_team");

ALTER TABLE "matches" ADD FOREIGN KEY ("team_2") REFERENCES "player_log" ("player_team");

ALTER TABLE "matches" ADD FOREIGN KEY ("updated_by") REFERENCES "users" ("user_id");

ALTER TABLE "player_log" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("user_id");

ALTER TABLE "player_log" ADD FOREIGN KEY ("updated_by") REFERENCES "users" ("user_id");

ALTER TABLE "players" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("user_id");

ALTER TABLE "players" ADD FOREIGN KEY ("updated_by") REFERENCES "users" ("user_id");
