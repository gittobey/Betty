import asyncio
import base64
import json
import time
import websockets
from datetime import datetime, timezone
import httpx
import re

# ====== CONFIGURATION ======
ID_ = "427003"
PID = "14001"
BET_STAKE = 50
BET_MATCH_INDEX = 1  # 1-based
REGSID = "2f0c243d-977a-47b5-aec6-841548f1eeca"
OTP = "2baae9f6-d40f-48b2-952a-67c7a03127e3"  # grab fresh from main site login

oddset_json = {
    "d6": {"mc": {"_default": {"o": "1.1", "r": 50000000, "s": 99999999.99}, "Win": {"o": "1.1"}, "Show": {"o": "1.1"}, "Place": {"o": "1.1"}, "Quinella": {"o": "1.15"}, "Exacta": {"o": "1.15"}, "Trifecta": {"o": "1.2"}, "OddEven": {"o": "1.06"}, "OverUnder": {"o": "1.06"}, "SumOfPlaces": {"o": "1.1"}}},
    "h6": {"mc": {"_default": {"o": "1.1", "r": 50000000, "s": 99999999.99}, "Win": {"o": "1.1"}, "Show": {"o": "1.1"}, "Place": {"o": "1.1"}, "Quinella": {"o": "1.15"}, "Exacta": {"o": "1.15"}, "Trifecta": {"o": "1.2"}, "OddEven": {"o": "1.06"}, "OverUnder": {"o": "1.06"}, "SumOfPlaces": {"o": "1.1"}}},
    "gl": {"mc": {"Match_Result": {"o": "1.05"}, "Double_Result": {"o": "1.05"}, "Double_Chance": {"o": "1.05"}, "Over_Under_1_5": {"o": "1.05"}, "Goal_NoGoal": {"o": "1.05"}, "Over_Under_2_5": {"o": "1.05"}, "GoalGoal_NoGoal": {"o": "1.05"}, "Over_Under_3_5": {"o": "1.05"}, "Over_Under_4_5": {"o": "1.05"}, "Over_Under_0_5": {"o": "1.05"}, "combi1": {"o": 1}, "combi2": {"o": 1}, "combi3": {"o": 1.05}, "combi4": {"o": 1.1}, "combi5": {"o": 1.15}, "combi6": {"o": 1.2}, "combi7": {"o": 1.25}, "combi8": {"o": 1.3}, "combi9": {"o": 1.35}, "combi10": {"o": 1.4}, "_default": {"o": 1.06, "r": 50000000, "s": 99999999.99}, "Correct_Score": {"o": 1.15}}},
    "d8": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "h8": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "kn": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "rl": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "pk": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "bj": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "gg": {"mi": 1.01, "ma": 500, "mc": {"_default": {"o": 1.2820512820513, "r": 50000000, "s": 99999999.99}}},
    "sp": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "lg": {"mc": {"_default": {"o": 1.2987012987013, "r": 50000000, "s": 99999999.99}}},
    "cg": {"mc": {"combi1": {"o": 1}, "combi2": {"o": 1}, "combi3": {"o": 1.05}, "combi4": {"o": 1.1}, "combi5": {"o": 1.15}, "combi6": {"o": 1.2}, "combi7": {"o": 1.25}, "combi8": {"o": 1.3}, "_default": {"o": 1.2820512820513, "r": 50000000, "s": 99999999.99}, "Correct_Score": {"o": 1.15}}},
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

leagueOddsLibraryById = {
    0: "Home", 1: "Away", 2: "Draw", 3: "HomeHome", 4: "HomeDraw",
    5: "HomeAway", 6: "DrawHome", 7: "DrawDraw", 8: "DrawAway",
    9: "AwayHome", 10: "AwayDraw", 11: "AwayAway", 12: "Draw_Away",
    13: "Home_Away", 14: "Home_Draw", 50: "under", 51: "over",
    72: "under2", 73: "over2", 74: "nog", 75: "gg",
    84: "under3", 85: "over3", 86: "under4", 87: "over4",
    88: "under0", 89: "over0",
}

# ====== AUTH ======
async def fetch_pin_hash(otp: str) -> str:
    params = "JnBpZD0xNDAwMSwxNDAwMywxNDAxMSwxNDAxMiwxNDAxNCwxNDAxNSwxNDAxNiwxNDAxNyZ2PTAmdGV4dD1QcmVtaWVy"
    url = (
        f"https://vsmobile.bet9ja.com/bet9ja-mobile/login/cmds/remoteLogin.php"
        f"?otp={otp}&game=league_premier&params={params}"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "Referer": "https://vsmobile.bet9ja.com/",
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        data = r.json()
        if data["result"] != "success":
            raise RuntimeError(f"remoteLogin failed: {data}")
        match = re.search(r"pinHash=([a-f0-9]{32})", data["targetURL"])
        if not match:
            raise RuntimeError("pinHash not found in targetURL")
        return match.group(1)

# ====== HELPERS ======
xs_counter = 1

def encode_payload(payload: str) -> str:
    return base64.b64encode(payload.encode()).decode()

def decode_payload(data) -> str:
    try:
        return base64.b64decode(data).decode()
    except Exception as e:
        return f"Error decoding: {e}"

def get_timestamp() -> str:
    return str(int(time.time() * 1000))

def get_xs() -> int:
    global xs_counter
    current = xs_counter
    xs_counter += 1
    return current

def get_minutes_since_midnight_utc() -> float:
    now = datetime.now(timezone.utc)
    return now.hour * 60 + now.minute + now.second / 60

def get_next_event_val(countdown: int, offset: int = 0) -> int:
    minutes_since_midnight = get_minutes_since_midnight_utc()
    e = int(minutes_since_midnight // countdown)
    val = e * countdown + offset
    while val <= minutes_since_midnight:
        val += countdown
    return int(val)

def extract_eid_and_start(payload: str) -> tuple:
    eid = None
    start = None
    for part in payload.split(";"):
        if part.startswith("eid="):
            eid = part.split("=")[1]
        elif part.startswith("start="):
            start = part.split("=")[1]
    return eid, start

def extract_onevda_data(raw_payload) -> dict:
    dpyld = base64.b64decode(raw_payload).decode()
    parts = dict(kv.split("=", 1) for kv in dpyld.split(";") if "=" in kv)
    base64_data = parts.get("data")
    decoded_str = base64.b64decode(base64_data).decode("utf-8")
    parsed = json.loads(decoded_str)
    for match in parsed.get("match", []):
        if match.get("stats") is None:
            match["stats"] = "None"
    return parsed

def parse_lsrr(raw_payload) -> list:
    decoded = base64.b64decode(raw_payload).decode()
    parts = dict(kv.split("=", 1) for kv in decoded.split(";") if "=" in kv)
    base64_data = parts.get("data")
    decoded_str = base64.b64decode(base64_data).decode("utf-8")
    return json.loads(decoded_str)

def parse_pl_response(r3: str) -> tuple:
    """Extract userid, balance, session_token from pl response."""
    userid = ""
    balance = 0.0
    session_token = ""
    for part in r3.split(";"):
        if part.startswith("userid="):
            userid = part.split("=")[1]
        elif part.startswith("cre="):
            try:
                balance = float(part.split("=")[1])
            except ValueError:
                pass
        elif part.startswith("token="):
            raw = part.split("=")[1]
            session_token = raw[:32]
    return userid, balance, session_token

def return_match_outcome(lsrr_pdata: list, market_index: int = 0) -> list:
    result = []
    for index, match in enumerate(lsrr_pdata):
        val = match["m_winningMarketIds"][market_index]
        label = leagueOddsLibraryById.get(val, f"Unknown({val})")
        result.append(f"Match_{index + 1}_{label}")
    return result

def get_match_result_market_id(parsed_lsrr: list, match_index_1based: int) -> int:
    match = parsed_lsrr[match_index_1based - 1]
    return match["m_winningMarketIds"][0]

def extract_bet_info(parsed_evda: dict, match_index_1based: int, market_id: int):
    match = parsed_evda["match"][match_index_1based - 1]
    home_abbr = match["players"][0]["teamName"]
    away_abbr = match["players"][1]["teamName"]
    for market_type, options in match["markets"].items():
        for option in options:
            try:
                m_id, odd = option.split("|")
                if int(m_id) == market_id:
                    return home_abbr, away_abbr, odd
            except ValueError:
                continue
    raise ValueError(
        f"Market ID {market_id} not found in match {match_index_1based} "
        f"({home_abbr} vs {away_abbr})"
    )

def build_bet_payload(eid, match_index, home_abbr, away_abbr,
                      market_id, odds, stake, clientid, session_token) -> str:
    d = f"gl|{eid}:{match_index}-{home_abbr}-{away_abbr}|{market_id}|{odds}|{stake};"
    return (
        f"cmd=sts8;st={ID_};oid=;eid={eid};pid={PID};i=unknown;"
        f"d={d};"
        f"clientid={clientid};domain=Comm.ts;s=NaN;"
        f"ts={get_timestamp()};xs={get_xs()}"
    )

def _parse_cr(tss_decoded: str) -> str:
    for part in tss_decoded.split(";"):
        if part.startswith("cr="):
            return part.split("=")[1]
    return "?"

# ====== BET ======
async def place_bet(websocket, eid, parsed_evda, parsed_lsrr, clientid, session_token):
    try:
        # Step 1: what did match 1 result in?
        market_id = get_match_result_market_id(parsed_lsrr, BET_MATCH_INDEX)
        outcome_name = leagueOddsLibraryById.get(market_id, f"Unknown({market_id})")
        print(f"[BET] Match {BET_MATCH_INDEX} result → {outcome_name} (market_id={market_id})")

        # Step 2: get team names + odds from evda for that outcome
        home_abbr, away_abbr, odds = extract_bet_info(
            parsed_evda, BET_MATCH_INDEX, market_id
        )
        print(f"[BET] {home_abbr} vs {away_abbr} | outcome={outcome_name} | odds={odds} | stake={BET_STAKE}")

        # Step 3: build and fire
        payload = build_bet_payload(
            eid=eid,
            match_index=BET_MATCH_INDEX,
            home_abbr=home_abbr,
            away_abbr=away_abbr,
            market_id=market_id,
            odds=odds,
            stake=BET_STAKE,
            clientid=clientid,
            session_token=session_token,
        )
        print(f"[BET] Sending: {payload}")
        await websocket.send(encode_payload(payload))

        # Step 4: read response
        raw_resp = await websocket.recv()
        resp = decode_payload(raw_resp)
        print(f"[BET] Response: {resp}")

        if "result=success" in resp:
            print("✅ BET PLACED SUCCESSFULLY")
        else:
            print("❌ BET FAILED")

    except Exception as e:
        print(f"[BET] Error: {e}")

# ====== MAIN ======
async def run():
    # Fetch fresh pinHash from remoteLogin
    print(f"[AUTH] Fetching fresh pinHash for OTP={OTP}...")
    pin_hash = await fetch_pin_hash(OTP)
    print(f"[AUTH] pinHash={pin_hash}")

    uri = "wss://vsmobile-proxy.bet9ja.com/goldenbox"
    async with websockets.connect(uri, open_timeout=30) as websocket:

        # S1: begin
        await websocket.send(encode_payload(
            f"cmd=begin;clientid=;domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        ))
        r1 = decode_payload(await websocket.recv())
        print(f"[S1] {r1}")
        clientid = ""
        for part in r1.split(";"):
            if part.startswith("clientid="):
                clientid = part.split("=")[1]
                break
        print(f"[INIT] clientid={clientid}")

        # S2: reg
        await websocket.send(encode_payload(
            f"cmd=reg;regsid={REGSID};tm=;v=w1.2_online;"
            f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        ))
        r2 = decode_payload(await websocket.recv())
        print(f"[S2] reg ok — {r2[:80]}...")

        # S3: pl (login with fresh pinHash)
        await websocket.send(encode_payload(
            f"cmd=pl;id={ID_};p={pin_hash};pid={PID};"
            f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        ))
        r3 = decode_payload(await websocket.recv())
        userid, balance, session_token = parse_pl_response(r3)
        print(f"[S3] pl ok — userid={userid} | balance=₦{balance:.2f} | token={session_token}")

        if not userid:
            print("❌ LOGIN FAILED — OTP may have expired, get a new one and retry")
            return
        if balance < BET_STAKE:
            print(f"❌ Insufficient balance ₦{balance:.2f} — need ₦{BET_STAKE}")
            return

        # S4: tss
        await websocket.send(encode_payload(
            f"cmd=tss;clientid={clientid};domain=Comm.ts;"
            f"s=NaN;ts={get_timestamp()};xs={get_xs()}"
        ))
        r4 = decode_payload(await websocket.recv())
        print(f"[S4] tss ok — cr={_parse_cr(r4)}")

        # S5: on_evda (before ot2 — confirmed from HAR)
        await websocket.send(encode_payload(
            f"cmd=on_evda;pid={PID};val={get_next_event_val(2, 0)};gid=gl;gevid=14;min=2;"
            f"oddset={json.dumps(oddset_json, separators=(',', ':'))};"
            f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        ))
        r5 = await websocket.recv()
        decoded5 = base64.b64decode(r5).decode()
        eid, start = extract_eid_and_start(decoded5)
        parsed_evda = extract_onevda_data(r5)
        print(f"[S5] on_evda ok — eid={eid} | start={start} | time_to_start={int(start) - time.time():.1f}s")

        # S6: ot2 (after on_evda — confirmed from HAR)
        await websocket.send(encode_payload(
            f"cmd=ot2;l=20;c=1;pid=14001,14003,14011,14012,14014,14015,14016,14017;"
            f"ft=0;ftt=0;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        ))
        await websocket.recv()
        print(f"[S6] ot2 ok")

        # ====== MAIN LOOP ======
        while True:

            # Keepalive: tss every 30s while more than 30s remain
            time2wait = int(start) - time.time() + 7
            print(f"[WAIT] {time2wait:.1f}s until lsrr window")

            while time2wait > 30:
                await websocket.send(encode_payload(
                    f"cmd=tss;clientid={clientid};domain=Comm.ts;"
                    f"s=NaN;ts={get_timestamp()};xs={get_xs()}"
                ))
                r_tss = decode_payload(await websocket.recv())
                print(f"[TSS] ping — {time2wait:.0f}s remaining | cr={_parse_cr(r_tss)}")
                await asyncio.sleep(30)
                time2wait = int(start) - time.time() + 7

            # Sleep until ~5s before lsrr window
            wait = int(start) - time.time() - 5
            if wait > 0:
                print(f"[WAIT] {wait:.1f}s until lsrr window...")
                await asyncio.sleep(wait)

            # S7: lsrr — fetch result
            print(f"[LSRR] Requesting at {time.strftime('%H:%M:%S')}")
            await websocket.send(encode_payload(
                f"cmd=lsrr;id={eid};e=1;pid={PID};"
                f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
            ))
            r_lsrr = await websocket.recv()
            print(f"[LSRR] Received at {time.strftime('%H:%M:%S')}")

            # Parse result
            parsed_lsrr = None
            try:
                parsed_lsrr = parse_lsrr(r_lsrr)
                outcomes = return_match_outcome(parsed_lsrr, 0)
                print(f"[RESULT] eid={eid} → {outcomes}")
            except Exception as e:
                print(f"[LSRR] Parse error: {e}")

            # Place bet immediately — passes session_token correctly
            if parsed_lsrr:
                await place_bet(
                    websocket, eid, parsed_evda,
                    parsed_lsrr, clientid, session_token
                )
            else:
                print("[BET] Skipped — lsrr parse failed")

            # Wait until start has passed, then fetch next game's evda
            gap = int(start) - time.time()
            if gap > 0:
                print(f"[WAIT] {gap:.1f}s before next on_evda...")
                await asyncio.sleep(gap)

            await websocket.send(encode_payload(
                f"cmd=on_evda;pid={PID};val={get_next_event_val(2, 0)};gid=gl;gevid=14;min=2;"
                f"oddset={json.dumps(oddset_json, separators=(',', ':'))};"
                f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
            ))
            r5 = await websocket.recv()
            decoded5 = base64.b64decode(r5).decode()
            eid, start = extract_eid_and_start(decoded5)
            parsed_evda = extract_onevda_data(r5)
            print(f"[EVDA] Next — eid={eid} | start={start} | time_to_start={int(start) - time.time():.1f}s")


asyncio.run(run())