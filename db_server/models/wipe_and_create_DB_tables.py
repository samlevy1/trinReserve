import os

import UsersModel, ClubsModel, RoomsModel, ClubLeadersModel
# , db_server.models.ClubsModel as ClubsModel, db_server.models.ClubLeadersModels as ClubLeadersModels

print(os.getcwd())
trinReserve_db_name=f"{os.getcwd()}/trinReserveDB.db"
print(trinReserve_db_name)
UsersModel.User(trinReserve_db_name).initialize_users_table()
ClubsModel.Club(trinReserve_db_name).initialize_clubs_table()
RoomsModel.Room(trinReserve_db_name).initialize_rooms_table()
ClubLeadersModel.Leader(trinReserve_db_name).initialize_leaders_table()
# ClubLeadersModels.Scorecard(yahtzee_db_name).initialize_scorecards_table()