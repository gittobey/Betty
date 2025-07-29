import asyncio
import websockets
import base64
import time
import json
from datetime import datetime, timezone
import urllib.parse

# ====helper keys=====
leagueOddsLibraryById = {
        0: "Home",
        1: "Away",
        2: "Draw",
        3: "HomeHome",
        4: "HomeDraw",
        5: "HomeAway",
        6: "DrawHome",
        7: "DrawDraw",
        8: "DrawAway",
        9: "AwayHome",
        10: "AwayDraw",
        11: "AwayAway",
        12: "Draw_Away",
        13: "Home_Away",
        14: "Home_Draw",
        15: "_0_0",
        16: "_1_0",
        17: "_2_0",
        18: "_3_0",
        19: "_4_0",
        20: "_5_0",
        21: "_6_0",
        22: "_0_1",
        23: "_1_1",
        24: "_2_1",
        25: "_3_1",
        26: "_4_1",
        27: "_5_1",
        28: "_0_2",
        29: "_1_2",
        30: "_2_2",
        31: "_3_2",
        32: "_4_2",
        33: "_0_3",
        34: "_1_3",
        35: "_2_3",
        36: "_3_3",
        37: "_0_4",
        38: "_1_4",
        39: "_2_4",
        40: "_0_5",
        41: "_1_5",
        42: "_0_6",
        43: "_0_Goals",
        44: "_1_Goals",
        45: "_2_Goals",
        46: "_3_Goals",
        47: "_4_Goals",
        48: "_5_Goals",
        49: "_6_Goals",
        50: "under",
        51: "over",
        72: "under2",
        73: "over2",
        74: "nog",
        75: "gg",
        84: "under3",
        85: "over3",
        86: "under4",
        87: "over4",
        88: "under0",
        89: "over0",
        90: "HomeScoresOver0",
        91: "AwayScoresOver0",
        92: "HomeScoresUnder0",
        93: "AwayScoresUnder0",
        94: "HomeScoresOver1",
        95: "AwayScoresOver1",
        96: "HomeScoresUnder1",
        97: "AwayScoresUnder1",
        98: "HomeScoresOver2",
        99: "AwayScoresOver2",
        100: "HomeScoresUnder2",
        101: "AwayScoresUnder2",
        102: "HomeScoresOver3",
        103: "AwayScoresOver3",
        104: "HomeScoresUnder3",
        105: "AwayScoresUnder3",
        106: "_1x2HomeScoresOver1",
        107: "_1x2DrawScoresOver1",
        108: "_1x2AwayScoresOver1",
        109: "_1x2HomeScoresUnder1",
        110: "_1x2DrawScoresUnder1",
        111: "_1x2AwayScoresUnder1",
        112: "_1x2HomeScoresOver2",
        113: "_1x2DrawScoresOver2",
        114: "_1x2AwayScoresOver2",
        115: "_1x2HomeScoresUnder2",
        116: "_1x2DrawScoresUnder2",
        117: "_1x2AwayScoresUnder2",
        118: "_1x2HomeScoresOver3",
        119: "_1x2DrawScoresOver3",
        120: "_1x2AwayScoresOver3",
        121: "_1x2HomeScoresUnder3",
        122: "_1x2DrawScoresUnder3",
        123: "_1x2AwayScoresUnder3",
        124: "_0-0_Goals",
        125: "_0-1_Goals",
        126: "_0-2_Goals",
        127: "_0-3_Goals",
        128: "_0-4_Goals",
        129: "_0-5_Goals",
        130: "_0-6_Goals",
        131: "_1-1_Goals",
        132: "_1-2_Goals",
        133: "_1-3_Goals",
        134: "_1-4_Goals",
        135: "_1-5_Goals",
        136: "_1-6_Goals",
        137: "_2-2_Goals",
        138: "_2-3_Goals",
        139: "_2-4_Goals",
        140: "_2-5_Goals",
        141: "_2-6_Goals",
        142: "_3-3_Goals",
        143: "_3-4_Goals",
        144: "_3-5_Goals",
        145: "_3-6_Goals",
        146: "_4-4_Goals",
        147: "_4-5_Goals",
        148: "_4-6_Goals",
        149: "_5-5_Goals",
        150: "_5-6_Goals",
        151: "_6-6_Goals",
        152: "1H_Home",
        153: "1H_Draw",
        154: "1H_Away"
}

teams = {
        "58": {
            "fifa": "WHU",
            "team": "west_ham"
        },
        "46": {
            "fifa": "MNC",
            "team": "manchester_city"
        },
        "60": {
            "fifa": "ASV",
            "team": "aston_villa"
        },
        "47": {
            "fifa": "CHE",
            "team": "chelsea"
        },
        "71": {
            "fifa": "BRI",
            "team": "brighton"
        },
        "49": {
            "fifa": "EVE",
            "team": "everton"
        },
        "55": {
            "fifa": "CRY",
            "team": "crystal_palace"
        },
        "972": {
            "fifa": "BRN",
            "team": "brentford"
        },
        "1053": {
            "fifa": "FOR",
            "team": "nottingham_forest"
        },
        "1161": {
            "fifa": "IPS",
            "team": "ipswich_town"
        },
        "63": {
            "fifa": "LEI",
            "team": "leicester_city"
        },
        "53": {
            "fifa": "NWC",
            "team": "newcastle"
        },
        "50": {
            "fifa": "MNU",
            "team": "manchester_united"
        },
        "525": {
            "fifa": "WOL",
            "team": "wolverhampton"
        },
        "512": {
            "fifa": "FUL",
            "team": "fulham"
        },
        "52": {
            "fifa": "SOU",
            "team": "southampton"
        },
        "45": {
            "fifa": "LIV",
            "team": "liverpool"
        },
        "67": {
            "fifa": "BOU",
            "team": "bournemouth"
        },
        "51": {
            "fifa": "TOT",
            "team": "tottenham"
        },
        "48": {
            "fifa": "ARS",
            "team": "arsenal"
        }
    }

oddset_json = {
    "d6": {
        "mc": {
            "_default": {"o": "1.1", "r": 50000000, "s": 99999999.99},
            "Win": {"o": "1.1"},
            "Show": {"o": "1.1"},
            "Place": {"o": "1.1"},
            "Quinella": {"o": "1.15"},
            "Exacta": {"o": "1.15"},
            "Trifecta": {"o": "1.2"},
            "OddEven": {"o": "1.06"},
            "OverUnder": {"o": "1.06"},
            "SumOfPlaces": {"o": "1.1"}
        }
    },
    "h6": {
        "mc": {
            "_default": {"o": "1.1", "r": 50000000, "s": 99999999.99},
            "Win": {"o": "1.1"},
            "Show": {"o": "1.1"},
            "Place": {"o": "1.1"},
            "Quinella": {"o": "1.15"},
            "Exacta": {"o": "1.15"},
            "Trifecta": {"o": "1.2"},
            "OddEven": {"o": "1.06"},
            "OverUnder": {"o": "1.06"},
            "SumOfPlaces": {"o": "1.1"}
        }
    },
    "gl": {
        "mc": {
            "Match_Result": {"o": "1.05"},
            "Double_Result": {"o": "1.05"},
            "Double_Chance": {"o": "1.05"},
            "Over_Under_1_5": {"o": "1.05"},
            "Goal_NoGoal": {"o": "1.05"},
            "Over_Under_2_5": {"o": "1.05"},
            "GoalGoal_NoGoal": {"o": "1.05"},
            "Over_Under_3_5": {"o": "1.05"},
            "Over_Under_4_5": {"o": "1.05"},
            "Over_Under_0_5": {"o": "1.05"},
            "combi1": {"o": 1},
            "combi2": {"o": 1},
            "combi3": {"o": 1.05},
            "combi4": {"o": 1.1},
            "combi5": {"o": 1.15},
            "combi6": {"o": 1.2},
            "combi7": {"o": 1.25},
            "combi8": {"o": 1.3},
            "combi9": {"o": 1.35},
            "combi10": {"o": 1.4},
            "_default": {"o": 1.06, "r": 50000000, "s": 99999999.99},
            "Correct_Score": {"o": 1.15}
        }
    },
    "d8": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "h8": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "kn": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "rl": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "pk": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "bj": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "gg": {
        "mi": 1.01,
        "ma": 500,
        "mc": {"_default": {"o": 1.2820512820513, "r": 50000000, "s": 99999999.99}}
    },
    "sp": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "lg": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "cg": {
        "mc": {
            "combi1": {"o": 1},
            "combi2": {"o": 1},
            "combi3": {"o": 1.05},
            "combi4": {"o": 1.1},
            "combi5": {"o": 1.15},
            "combi6": {"o": 1.2},
            "combi7": {"o": 1.25},
            "combi8": {"o": 1.3},
            "_default": {"o": 1.2820512820513, "r": 50000000, "s": 99999999.99},
            "Correct_Score": {"o": 1.15}
        }
    },
    "lk": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "ll": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "fg": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "mt": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "kt": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "ch": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "sn": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "me": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "sx": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "vw": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "rf": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "wc": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "l5": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}}
}

# === Helper functions ===
def encode_payload(payload: str) -> str:
    return base64.b64encode(payload.encode()).decode()

def decode_payload(payload: str) -> str:
    try:
        return base64.b64decode(payload).decode()
    except Exception as e:
        return f"Error decoding: {e}"

# Global counter for xs
xs_counter = 1

def get_timestamp() -> str:
    return str(int(time.time() * 1000))

def get_xs() -> int:
    global xs_counter
    current = xs_counter
    xs_counter += 1
    return current

def extract_eid_and_start(payload: str) -> tuple[str, str]:
    eid = None
    start = None
    for part in payload.split(";"):
        if part.startswith("eid="):
            eid = part.split("=")[1]
        elif part.startswith("start="):
            start = part.split("=")[1]
    return eid, start

def get_next_event_val(countdown: int, offset: int = 0) -> int:
    """
    Calculate the next valid 'val' parameter for Bet9ja WebSocket payload,
    using UTC time.
    """
    minutes_since_midnight = get_minutes_since_midnight_utc()
    e = int(minutes_since_midnight // countdown)
    val = e * countdown + offset

    while val <= minutes_since_midnight:
        val += countdown

    return int(val)

def get_minutes_since_midnight_utc() -> float:
    """Return minutes since midnight (UTC) as a float."""
    now = datetime.now(timezone.utc)
    return now.hour * 60 + now.minute + now.second / 60

def get_lsrr_result(teama, teamb, cscore):
    home_team = teams.get(str(teama), {}).get("team", f"team_{teama}")
    away_team = teams.get(str(teamb), {}).get("team", f"team_{teamb}")
    outcome = f"{leagueOddsLibraryById.get(cscore)[1]} - {leagueOddsLibraryById.get(cscore)[3]} "
    return home_team, away_team, outcome

def disp_match_outcome(home, away, outcome):
    print(f"{home} vs {away} => {outcome}")


def extract_onevda_data(payload):
    dpyld = str(base64.b64decode(payload))
    parts = dict(kv.split("=", 1) for kv in dpyld.split(";") if "=" in kv)
    base64_data = parts.get("data")

    decoded_bytes = base64.b64decode(base64_data)
    decoded_str = decoded_bytes.decode('utf-8')
    parsed_data = json.loads(decoded_str)
    for match in parsed_data.get("match", []):
        if match.get("stats") is None:
            match["stats"] = str("None")
    return parsed_data

def generate_match_odds(lsrr, evda):
    result = []

    # Create a mapping of team pairs to their market data for quick lookup
    evda_matches = {}
    for match in evda["match"]:
        team_a = match["players"][0]["teamId"]
        team_b = match["players"][1]["teamId"]
        key = f"{team_a}-{team_b}"
        evda_matches[key] = match["markets"]

    for idx, match in enumerate(lsrr):
        team_a = match["m_teamA"]
        team_b = match["m_teamB"]
        winning_market_ids = match["m_winningMarketIds"]

        # Skip if no valid winning market IDs
        if not winning_market_ids or all(mid == -1 for mid in winning_market_ids):
            continue

        # Try both possible team orderings
        key1 = f"{team_a}-{team_b}"
        key2 = f"{team_b}-{team_a}"

        markets = None
        if key1 in evda_matches:
            markets = evda_matches[key1]
        elif key2 in evda_matches:
            markets = evda_matches[key2]

        if not markets:
            continue

        # Get team names (use first ordering found)
        if key1 in evda_matches:
            team_a_name = next(m["players"][0]["teamName"] for m in evda["match"]
                               if m["players"][0]["teamId"] == team_a and m["players"][1]["teamId"] == team_b)
            team_b_name = next(m["players"][1]["teamName"] for m in evda["match"]
                               if m["players"][0]["teamId"] == team_a and m["players"][1]["teamId"] == team_b)
        else:
            team_a_name = next(m["players"][1]["teamName"] for m in evda["match"]
                               if m["players"][0]["teamId"] == team_b and m["players"][1]["teamId"] == team_a)
            team_b_name = next(m["players"][0]["teamName"] for m in evda["match"]
                               if m["players"][0]["teamId"] == team_b and m["players"][1]["teamId"] == team_a)

        # Find odds for each winning market ID
        for market_id in winning_market_ids:
            if market_id == -1:
                continue

            found = False
            for market_type, options in markets.items():
                for option in options:
                    try:
                        m_id, odd = option.split("|")
                        if int(m_id) == market_id:
                            result.append(f"{idx + 1}-{team_a_name}-{team_b_name}|{market_id}|{odd}")
                            found = True
                            break
                    except ValueError:
                        continue
                if found:
                    break

    return result

def return_match_outcome(lsrr_pdata,a):
    '''pass the json? formatted result and specify the marketis(a) e.g 4 is for correct score'''
    result = []
    if a == 0:
        for index, match in enumerate(lsrr_pdata):
            first_value = match["m_winningMarketIds"][a]
            if first_value == 0:
                result.append(f"Match_Result_{index}_Home")
            elif first_value == 1:
                result.append(f"Match_Result_{index}_Away")
            else:
                result.append(f"Match_Result_{index}_Draw")
        return result
    #other market extractors will come here


# === Main async function ===
async def send_payloads():
    uri = "wss://vsmobile-proxy.bet9ja.com/goldenbox"

    async with websockets.connect(uri) as websocket:
        # === Send S1 ===
        s1_payload = f"cmd=begin;clientid=;domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        await websocket.send(encode_payload(s1_payload))
        print(f"Sent S1: {s1_payload}")

        r1 = await websocket.recv()
        r1_decoded = decode_payload(r1)
        print(f"Received R1: {r1_decoded}")

        # === Extract clientid ===
        clientid = ""
        for part in r1_decoded.split(";"):
            if part.startswith("clientid="):
                clientid = part.split("=")[1]
                break



        # === Send S2 ===
        regsid =  "2f0c243d-977a-47b5-aec6-841548f1eeca"  #fixed doesnt change,combo of logincreds?
        s2_payload = (
            f"cmd=reg;regsid={regsid};tm=;v=w1.2_online;"
            f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s2_payload))
        print(f"Sent S2: {s2_payload}")

        r2 = await websocket.recv()
        print(f"Received R2: {decode_payload(r2)}")

        # === Send S3 ===
        p = "b03eb54de7ace161878c9da0edeb33f9" #changes with time,usually expires gotten from headers to vsmobile
        id_ = "427003"
        pid = "14001"
        s3_payload = (
            f"cmd=pl;id={id_};p={p};pid={pid};clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s3_payload))
        print(f"Sent S3: {s3_payload}")

        r3 = await websocket.recv()
        print(f"Received R3: {r3}")

        # === Send S4 ===
        s4_payload = (
            f"cmd=tss;clientid={clientid};domain=Comm.ts;"
            f"s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s4_payload))
        print(f"Sent S4: {time.strftime('%H:%M:%S')}")

        r4 = await websocket.recv()
        print(f"Received R4: {time.strftime('%H:%M:%S')}")

        #=== Send S5 ===


        s5_payload = (
            f"cmd=on_evda;pid=14001;val={get_next_event_val(2,0)};gid=gl;gevid=14;min=2;"
            f"oddset={json.dumps(oddset_json, separators=(',', ':'))};"
            f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s5_payload))
        print(f"Sent S5 (on_evda data) {time.strftime('%H:%M:%S')}")
        r5 = await websocket.recv()
        print(f"Received R5: ")
        #payload = extract_onevda_data(r5) #extract live odds for the game eid
        decoded5 = base64.b64decode(r5).decode()
        eid, start = extract_eid_and_start(decoded5)
        with open(f"evda{eid}.json", "w") as f:
            json.dump(extract_onevda_data(str(r5)), f, indent=4)
        parsed_onevda_data = extract_onevda_data(str(r5))
        time2wait = int(start)-time.time()
        print(f"EID: {eid}, START: {start}")
        print(f"time to wait: {time2wait}s")

        # === Send S6 ===
        s6_payload = (
            f"cmd=ot2;l=20;c=1;pid=14001,14003,14011,14012,14014,14015,14016,14017;ft=0;ftt=0;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s6_payload))
        print(f"Sent S6 (ot2): {s6_payload}")
        r6 = await websocket.recv()
        print(f"Received R6: {time.strftime('%H:%M:%S')}")

        # Assume S6 has already been sent/received above

        # Calculate time2wait from R5 earlier
        time2wait = int(start) - time.time() +7
        print(f"Time to wait after S6: {time2wait:.2f}s")

        #Keep sending S4 if time2wait > 30s
        while time2wait > 30:
            s4_payload = (
                f"cmd=tss;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
            )
            await websocket.send(encode_payload(s4_payload))
            print(f"Sent S4: {s4_payload}")
            r4 = await websocket.recv()
            print(f"Received R4: {time.strftime('%H:%M:%S')}")

            #Wait before next S4 to avoid spamming
            await asyncio.sleep(30)

            #Recalculate time2wait
            time2wait = int(start) - time.time()
            print(f"Updated time2wait: {time2wait:.2f}s")


        #When time2wait is <= 30, send S7
        await asyncio.sleep(time2wait-5) #lsrr is sent 113s after on_evda start
        #print(f"{start}\n {time.time()}")
        # while time.time() <= float(start)+3.0:
        #     print(float(start)-time.time() +3.0 )


        print(time.strftime("%H:%M:%S"))
        s7_payload = (
            f"cmd=lsrr;id={eid};e=1;pid=14001;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s7_payload))
        #print(f"Sent S7: {s7_payload}")
        r7 = await websocket.recv()
        print(f"Received R7: at {time.strftime('%H:%M:%S')} ")

        decoded_r7 = str(base64.b64decode(r7))
        parts = dict(kv.split("=", 1) for kv in decoded_r7.split(";") if "=" in kv)
        base64_data = parts.get("data")

        # Step 2: Base64 decode (handling URL-safe characters if present)
        decoded_bytes = base64.b64decode(base64_data)
        decoded_str = decoded_bytes.decode('utf-8')

        # Step 3: Attempt to load as JSON
        try:
            parsed_lsrr_data = json.loads(decoded_str)
            #print("Parsed JSON:", parsed_data)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            print("Decoded string:", decoded_str)

        outcome_list = return_match_outcome(parsed_lsrr_data, 0)
        print(outcome_list)
        # with open(f"lssr_data{eid}.json", "w") as f:
        #     json.dump((parsed_lsrr_data), f, indent=4)
        #Loop through the first 10 games



        #send bet payload after parsing data and generating payload
        #bet = generate_match_odds(parsed_lsrr_data, parsed_onevda_data)[0]
        # sts8_payload = (
        #     f"cmd=sts8;st=427003;oid=;eid={eid};pid=14001;i=unknown;d=gl|{eid}:5-MNU-LEI|51|1.21|100;;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        # )
        # print(f"sent sts8: {sts8_payload}")
        # #print(f"Sent sts8  {bet}: at {time.strftime('%H:%M:%S')} ")
        # await websocket.send(encode_payload(sts8_payload))
        # rsts8 = await websocket.recv()
        # print(f"Received rsts8: at {time.strftime('%H:%M:%S')} \n {rsts8} ")
        # print(base64.b64decode(rsts8).decode())


                # consequent payloads are in the sequence after s7
        #s5 -> s4 -> s4 -> s7


        # === Begin continuous receive loop ===
        while True:
            response = await websocket.recv()
            print(f"Raw Base64 Response: {response}")
            decoded = decode_payload(response)
            print(f"Decoded: {decoded}")

# === Run the main function ===
asyncio.run(send_payloads())

"""ftv=1; livlang=en; ak_bmsc=0F6957A41241A01C13C3AE5034EB24E5~000000000000000000000000000000~YAAQCwTGF7WZVsWWAQAAHbph8xsniJVlcyVGti9QrQ5E0xLJ2qrBr0LqFJNCzOU+XiPP5JQRFIB4KawTIH3Iadn+4oTcZ9/9K0QNF9q1G0nSJ6x5iewvW5fdAEQ2Acwof4eBrVoZQ7oR0M/oPM4KEF/ASlJqDgvEwaIUeyOM3baLl8eb+oPljSgKsSsBlUBxL9cdpQM+l+L6yBaAlukUQmBgf6Sij8r8iCpZwTwybLcMj816Y31BG92nrN+LRBBIXiCKqKin+pKBQoVmGpL3UUv13IwIvqCEthEKwGLduvB6eJlJxnbpha9t1g2xIwUDpN2awJM5JLBSnGytjzF3AuPl62CgqaEDtLZmp/yn0xh1+vvAutcmU0PPfBDPr+zxps03f9t6mCxD1z2w9CE40F8FcksZ0nkTghm2EjSww+XIcM/kcRIKjT95vzQ5fBklPgqrI0ypyLithTbG5JxGMIu3yIusp68UBcHgaA6AYnj/Da4VOMHqA5o8/7egyg==; bm_sv=84EE024038B8235BB3BF2C4692153140~YAAQCwTGF7eZVsWWAQAAjLph8xtHMvJNXxbSsIXnZXpn7+tkgAckoZp+wEKKlm2gLEGoTG+qCn+weLDms/6g2BQFo2d8kL+ukjSpQtXvNl9sU3fD24ETkE2uz4xqI80UywTeLb80A2b9l6pw0KfbhL7bpZ9nqnuTksTLAogndfZ9XzxcGMZDdtb48YaZVnSO/nAOmIrkjfP/IMyvKCb6o6xM9gb++dbphbF6h3XXlYO1wd8II92vHwdBYS2f885H~1; _gcl_au=1.1.312065277.1747839992; _ga=GA1.1.1589441803.1747839992; _fbp=fb.1.1747839992443.882832439282527437; _tgpc=104e32ab-a25e-5a28-ac59-730a78e3a2b5; _tglksd=eyJzIjoiODlmZTQzMjQtNzVkNS01MjAzLTgwMDAtOTBmMDk5ZmU5YmM4Iiwic3QiOjE3NDc4Mzk5OTI3MTgsInNvZCI6IihkaXJlY3QpIiwic29kdCI6MTc0NzgzOTk5MjcxOCwic29kcyI6Im8iLCJzb2RzdCI6MTc0NzgzOTk5MjcxOH0=; _sp_srt_id.55ca=a468fe2d-bcb6-43b6-bc69-568ae6273d77.1747839993.1.1747839993..17133314-9711-4e3f-87ca-36175360efc9....0; PHPSESSID=r6vlk6qrfqdncuv90ih93d5ns1; _ga_YYQNLHMCQS=GS2.1.s1747839992$o1$g0$t1747840000$j52$l0$h0$dJql16DPbhoQe8QguqpMxSQL0GO4ZuOZcHA"""