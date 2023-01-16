import json
import requests
from io import open
import pandas as pd
import csv
import os
import sys

#this function accepts a list of Sleeper Fantasy Football League IDs and outputs a "sleeper_data" folder with key API data for each league.
def sleeper_api_tapper(league_id=[]):
    
    #these empty lists will contain ids and information from sleeper APIs to use in certain URLs that require it.
    user_id = []
    draft_id = []
    nfl_week = []
    round = [*range(1,18)]

    #this function will create an empty "sleeper_data" folder where all final CSVs will be housed in.
    def create_folder(id):
        folder = f"sleeper_data_{str(id[-4:])}"
        path = os.getcwd()
        joined_path = os.path.join(path, folder)
        os.makedirs(joined_path, exist_ok=True)

    #this function will detect the OS type to correctly assign directory patterns.
    def directory_pattern():
        if sys.platform == "win32":
            return "\\"
        else:
            return "/"

    #this function receives the API URL reponse as a JSON file.
    def api_to_json(response=[]):
        for urls_keys in url_dict:
            print(url_dict[urls_keys])
            urls = url_dict[urls_keys]
            api_response = requests.request('GET', urls).text
            response.append(api_response)

    #this function converts the JSON file into a local CSV file inside the "sleeper_data" folder.
    def json_to_csv(id, response):
        for responses, urls_keys in zip(response, url_dict):
            data = json.loads(responses) 
            dataframe = pd.json_normalize(data)
            last_4_digits = str(id[-4:])   
            folder_path = str(os.getcwd())+str(directory_pattern())+f"sleeper_data_{league_ids[-4:]}"
            file_name = urls_keys + "_" + last_4_digits + ".csv"
            file_csv = dataframe.to_csv(os.path.join(folder_path, file_name))
            #these if statements will append the user_ids, draft_ids, and nfl_week to use in certain groups of links.
            if urls_keys == "users_in_a_league":
                user_id.extend(dataframe["user_id"])
            elif urls_keys == "drafts_for_a_league":
                draft_id.extend(dataframe["draft_id"])
            elif urls_keys == "nfl_state":
                nfl_week.extend(dataframe["week"])
            else:
               pass

    #this operation will provide the API links to pull from.
    if league_id:

        #league data for each league.
        for league_ids in league_id:
            create_folder(league_ids)
            url_dict = {
                "specific_league" : f"https://api.sleeper.app/v1/league/{league_ids}",
                "rosters_in_a_league" : f"https://api.sleeper.app/v1/league/{league_ids}/rosters",
                "users_in_a_league" : f"https://api.sleeper.app/v1/league/{league_ids}/users",
                "traded_picks" : f"https://api.sleeper.app/v1/league/{league_ids}/traded_picks",                
                "nfl_state" : f"https://api.sleeper.app/v1/state/nfl",                
                "drafts_for_a_league" : f"https://api.sleeper.app/v1/league/{league_ids}/drafts"
            }        
            league_api_response = []
            api_to_json(league_api_response)
            json_to_csv(league_ids, league_api_response)

        #matchup data for each league and each nfl week.
        for nfl_weeks in nfl_week:
            url_dict = {
                f"matchups_in_a_league_week{nfl_weeks}" : f"https://api.sleeper.app/v1/league/{league_ids}/matchups/{nfl_weeks}"
            }        
            matchups_api_response = []
            api_to_json(matchups_api_response)
            json_to_csv(league_ids, matchups_api_response)

        #transaction data for each league and each round.
        for rounds in round:
            url_dict = {
                f"transactions_round{rounds}" : f"https://api.sleeper.app/v1/league/{league_ids}/transactions/{rounds}"
            }      
            transactions_api_response = []
            api_to_json(transactions_api_response)
            json_to_csv(league_ids, transactions_api_response)
        
        #user data for each league.
        for user_ids in user_id:
            url_dict = {
                "users" : f"https://api.sleeper.app/v1/user/{user_ids}"
            }   
            user_api_response = []
            api_to_json(user_api_response)
            json_to_csv(user_ids, user_api_response)
        
        #draft data for each league.
        for draft_ids in draft_id:
            url_dict = {
                "picks_in_a_draft" : f"https://api.sleeper.app/v1/draft/{draft_ids}/picks"
            }   
            draft_api_response = []
            api_to_json(draft_api_response)
            json_to_csv(draft_ids, draft_api_response)          
 
    else:
        print('please provide league_id(s)')

#--------------------------------------#
#running the function with a league id
sleeper_api_tapper(
    league_id=[]
)