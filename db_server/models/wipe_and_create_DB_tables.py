import os

import UsersModel, db_server.models.ClubsModel as ClubsModel, db_server.models.ClubLeadersModels as ClubLeadersModels

print(os.getcwd())
yahtzee_db_name=f"{os.getcwd()}/yahtzeeDB.db"
print(yahtzee_db_name)
UsersModel.User(yahtzee_db_name).initialize_users_table()
ClubsModel.Game(yahtzee_db_name).initialize_games_table()
ClubLeadersModels.Scorecard(yahtzee_db_name).initialize_scorecards_table()