import logging
from collections import defaultdict
import requests
import json
import re
import csv
import time
import os
from datetime import datetime

# Constants
MAX_MATCHDAY = 38
WAIT_INTERVAL = 120  # seconds between retries

# Setup directories
os.makedirs('results', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_data():
    """Fetch JSON data from the API"""
    url = "https://vsmobile.bet9ja.com/shopadmin/standings_view/league_data.php?pid=14001"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://vsmobile.bet9ja.com/bet9ja-mobile/login/?game=league&OTP=1d5945b3-bab4-4e36-b40f-33c7eb02aa7b&mode=premier&lang=",
    }
    
    try:
        logger.info("Attempting to fetch data from API")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info("Data fetched successfully")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}", exc_info=True)
        return None
    except ValueError as e:
        logger.error(f"Error decoding JSON response: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Unexpected error in fetch_data: {e}", exc_info=True)
        return None

def extract_league_info(data):
    """Extract league_id and last matchday from the weeks data"""
    try:
        if not data:
            logger.warning("No data provided to extract_league_info")
            return None, None
            
        weeks = data.get("weeks", {})
        if not weeks:
            logger.warning("No weeks data found in JSON")
            return None, None
        
        # Get the last week entry
        last_week = list(weeks.values())[-1]
        league_id = last_week.get("league_id")
        last_matchday = last_week.get("matchday")
        
        try:
            return league_id, int(last_matchday)
        except (TypeError, ValueError) as e:
            logger.error(f"Error converting matchday to integer: {e}", exc_info=True)
            return league_id, None
    except Exception as e:
        logger.error(f"Unexpected error in extract_league_info: {e}", exc_info=True)
        return None, None

def extract_match_data(data):
    """Extract match data from JSON"""
    try:
        if not data:
            logger.warning("No data provided to extract_match_data")
            return [], []
            
        teams = data.get("teams", {})
        matches_by_week = data.get("matches", {})
        
        # Define all possible columns we want to extract
        # Define all possible columns we want to extract
        all_columns = [
            "id", "matchday", "HomeTeam", "HomeScore", "AwayScore", "AwayTeam",
            "Home", "Away", "Draw",
            "HomeHome", "HomeDraw", "HomeAway",
            "DrawHome", "DrawDraw", "DrawAway",
            "AwayHome", "AwayDraw", "AwayAway",
            "Draw_Away", "Home_Away", "Home_Draw",
            "_0_0", "_1_0", "_2_0", "_3_0", "_4_0", "_5_0", "_6_0",
            "_0_1", "_1_1", "_2_1", "_3_1", "_4_1", "_5_1",
            "_0_2", "_1_2", "_2_2", "_3_2", "_4_2",
            "_0_3", "_1_3", "_2_3", "_3_3",
            "_0_4", "_1_4", "_2_4",
            "_0_5", "_1_5",
            "_0_6",
            "_0_Goals", "_1_Goals", "_2_Goals", "_3_Goals", "_4_Goals", "_5_Goals", "_6_Goals",
            "under", "over", "under2", "over2", "nog", "gg",
            "under3", "over3", "under4", "over4", "under0", "over0",
            "HomeScoresOver0", "AwayScoresOver0", "HomeScoresUnder0", "AwayScoresUnder0",
            "HomeScoresOver1", "AwayScoresOver1", "HomeScoresUnder1", "AwayScoresUnder1",
            "HomeScoresOver2", "AwayScoresOver2", "HomeScoresUnder2", "AwayScoresUnder2",
            "HomeScoresOver3", "AwayScoresOver3", "HomeScoresUnder3", "AwayScoresUnder3",
            "_1x2HomeScoresOver1", "_1x2DrawScoresOver1", "_1x2AwayScoresOver1",
            "_1x2HomeScoresUnder1", "_1x2DrawScoresUnder1", "_1x2AwayScoresUnder1",
            "_1x2HomeScoresOver2", "_1x2DrawScoresOver2", "_1x2AwayScoresOver2",
            "_1x2HomeScoresUnder2", "_1x2DrawScoresUnder2", "_1x2AwayScoresUnder2",
            "_1x2HomeScoresOver3", "_1x2DrawScoresOver3", "_1x2AwayScoresOver3",
            "_1x2HomeScoresUnder3", "_1x2DrawScoresUnder3", "_1x2AwayScoresUnder3",
            "_0-0_Goals", "_0-1_Goals", "_0-2_Goals", "_0-3_Goals", "_0-4_Goals", "_0-5_Goals", "_0-6_Goals",
            "_1-1_Goals", "_1-2_Goals", "_1-3_Goals", "_1-4_Goals", "_1-5_Goals", "_1-6_Goals",
            "_2-2_Goals", "_2-3_Goals", "_2-4_Goals", "_2-5_Goals", "_2-6_Goals",
            "_3-3_Goals", "_3-4_Goals", "_3-5_Goals", "_3-6_Goals",
            "_4-4_Goals", "_4-5_Goals", "_4-6_Goals",
            "_5-5_Goals", "_5-6_Goals",
            "_6-6_Goals",
            "1H_Home", "1H_Draw", "1H_Away"
        ]
        
        match_data = []
        
        for week_num, week_matches in matches_by_week.items():
            for match_id, match in week_matches.items():
                # Initialize a dictionary with all columns set to 0
                row = defaultdict(int)
                
                # Add match ID and matchday
                row["id"] = match_id
                row["matchday"] = int(week_num)
                
                # Get team names and IDs
                teamA_id = match["teamA"]
                teamB_id = match["teamB"]
                teamA = teams.get(teamA_id, {}).get("team", f"team_{teamA_id}")
                teamB = teams.get(teamB_id, {}).get("team", f"team_{teamB_id}")
                
                # Set basic match info
                row["HomeTeam"] = teamA
                row["AwayTeam"] = teamB
                
                # Extract score from wonmarkets
                wonmarkets = match.get("wonmarkets", "").split(',')
                
                # Find the actual score (pattern like _1_0)
                for market in wonmarkets:
                    if market.startswith('_') and market.count('_') == 2:
                        parts = market.split('_')
                        if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
                            row["HomeScore"] = int(parts[1])
                            row["AwayScore"] = int(parts[2])
                            break
                
                # Set all won markets to 1
                for market in wonmarkets:
                    if market in all_columns:
                        row[market] = 1
                
                match_data.append(row)
        
        logger.info(f"Successfully extracted data for {len(match_data)} matches")
        return match_data, all_columns
    except Exception as e:
        logger.error(f"Unexpected error in extract_match_data: {e}", exc_info=True)
        return [], []

def save_to_csv(data, columns, league_id):
    """Save extracted data to CSV file"""
    try:
        if not league_id:
            raise ValueError("No league_id provided")
            
        filename = f"results/{league_id}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for row in data:
                complete_row = {col: row.get(col, 0) for col in columns}
                writer.writerow(complete_row)
        logger.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving to CSV: {e}", exc_info=True)
        raise

def process_data_with_retry():
    """Main processing function with retry logic"""
    try:
        logger.info("Starting data processing")
        while True:
            data = fetch_data()
            if not data:
                logger.warning(f"Failed to fetch data, retrying in {WAIT_INTERVAL} seconds...")
                time.sleep(WAIT_INTERVAL)
                continue
                
            league_id, last_matchday = extract_league_info(data)
            
            if not league_id or last_matchday is None:
                logger.warning("Could not determine league status, retrying...")
                time.sleep(WAIT_INTERVAL)
                continue
                
            logger.info(f"League {league_id}, current matchday: {last_matchday}")
            
            if last_matchday >= MAX_MATCHDAY:
                logger.info("All matchdays completed, processing data...")
                match_data, columns = extract_match_data(data)
                save_to_csv(match_data, columns, league_id)
                break
            else:
                remaining = MAX_MATCHDAY - last_matchday
                wait_time = remaining * WAIT_INTERVAL
                logger.info(f"Only {last_matchday} matchdays completed. Waiting for {remaining} matchdays ({wait_time} seconds)...")
                time.sleep(wait_time)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error in process_data_with_retry: {e}", exc_info=True)
    finally:
        logger.info("Data processing completed")

if __name__ == "__main__":
    try:
        process_data_with_retry()
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}", exc_info=True)