"""This also has an attempt to """


import asyncio
import base64
import json
import time
import websockets
from datetime import datetime, timezone

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

def encode_payload(payload: str) -> str:
    return base64.b64encode(payload.encode()).decode()

def decode_payload(payload: str) -> str:
    try:
        return base64.b64decode(payload).decode()
    except Exception as e:
        return f"Error decoding: {e}"

# Global counter for xs
xs_counter = 1

def get_xs() -> int:
    global xs_counter
    current = xs_counter
    xs_counter += 1
    return current

def get_minutes_since_midnight_utc() -> float:
    """Return minutes since midnight (UTC) as a float."""
    now = datetime.now(timezone.utc)
    return now.hour * 60 + now.minute + now.second / 60
def get_timestamp() -> str:
    return str(int(time.time() * 1000))
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

async def send_payloads():
    uri = "wss://vsmobile-proxy.bet9ja.com/goldenbox"

    async with websockets.connect(uri) as websocket:
        # === Send S1 ===
        s1_payload = f"cmd=begin;clientid=;domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        await websocket.send(encode_payload(s1_payload))
        print(f"Sent S1: ")

        r1 = await websocket.recv()
        r1_decoded = decode_payload(r1)
        print(f"Received R1: \n")

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
        print(f"Sent S2: ")

        r2 = await websocket.recv()
        print(f"Received R2: \n")

        # === Send S3 ===
        p = "2b4063bed18197c832c932681124894d" #changes with time,usually expires gotten from headers to vsmobile
        id_ = "427003"
        pid = "14001"
        s3_payload = (
            f"cmd=pl;id={id_};p={p};pid={pid};clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s3_payload))
        print(f"Sent S3: ")

        r3 = await websocket.recv()
        print(f"Received R3: \n")

        # === Send S4/tss ===
        s4_payload = (
            f"cmd=tss;clientid={clientid};domain=Comm.ts;"
            f"s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s4_payload))
        print(f"Sent S4: {time.strftime('%H:%M:%S')}")

        r4 = await websocket.recv()
        print(f"Received R4: {time.strftime('%H:%M:%S')}")


        #=== Send S5/on_evda ===

        s5_payload = (
            f"cmd=on_evda;pid=14001;val={get_next_event_val(2,0)};gid=gl;gevid=14;min=2;"
            f"oddset={json.dumps(oddset_json, separators=(',', ':'))};"
            f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s5_payload))
        print(f"Sent S5 (on_evda data) {time.strftime('%H:%M:%S')}")
        r5 = await websocket.recv()
        print(f"Received R5: \n")
        #payload = extract_onevda_data(r5) #extract live odds for the game eid
        decoded5 = base64.b64decode(r5).decode()
        eid, start = extract_eid_and_start(decoded5)
        # with open(f"evda{eid}.json", "w") as f:
        #     json.dump(extract_onevda_data(str(r5)), f, indent=4)
        # parsed_onevda_data = extract_onevda_data(str(r5))
        time2wait = int(start)-time.time()
        print(f"EID: {eid}, START: {start} time to wait: {time2wait}s \n")


        # === Send S6 ===
        s6_payload = (
            f"cmd=ot2;l=20;c=1;pid=14001,14003,14011,14012,14014,14015,14016,14017;ft=0;ftt=0;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
        )
        await websocket.send(encode_payload(s6_payload))
        print(f"Sent S6 (ot2): ")
        r6 = await websocket.recv()
        print(f"Received R6: \n")

        # Assume S6 has already been sent/received above

        # Calculate time2wait from R5 earlier
        time2wait = int(start) - time.time() +7
        print(f"Time to wait after S6: {time2wait:.2f}s \n")

        #Keep sending S4 if time2wait > 30s
        while time2wait > 30:
            s4_payload = (
                f"cmd=tss;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
            )
            await websocket.send(encode_payload(s4_payload))
            print(f"Sent S4/tss : ")
            r4 = await websocket.recv()
            print(f"Received R4: {time.strftime('%H:%M:%S')} \n")

            #Wait before next S4 to avoid spamming
            await asyncio.sleep(30)

            #Recalculate time2wait
            time2wait = int(start) - time.time() # or time2wait -30
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
        print(f"Sent S7: {time.strftime('%H:%M:%S')}")
        r7 = await websocket.recv()
        print(f"Received R7: at {time.strftime('%H:%M:%S')} \n")

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
        print(f"Result for {eid}: {outcome_list}")
        # with open(f"lssr_data{eid}.json", "w") as f:
        #     json.dump((parsed_lsrr_data), f, indent=4)




        while True:
            """loop to keep sending s5,s4 and s7 payloads"""
            #=== Send S5/on_evda ===
            if int(time.time()) < int(start):
                await asyncio.sleep(int(start)- int(time.time())) #wait for the time for the next on_evda to reach
                
            s5_payload = (
                f"cmd=on_evda;pid=14001;val={get_next_event_val(2,0)};gid=gl;gevid=14;min=2;"
                f"oddset={json.dumps(oddset_json, separators=(',', ':'))};"
                f"clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
            )
            await websocket.send(encode_payload(s5_payload))
            print(f"Sent S5 (on_evda data) {time.strftime('%H:%M:%S')}")
            r5 = await websocket.recv()
            print(f"Received R5: \n")
            #payload = extract_onevda_data(r5) #extract live odds for the game eid
            decoded5 = base64.b64decode(r5).decode()
            eid, start = extract_eid_and_start(decoded5)
            # with open(f"evda{eid}.json", "w") as f:
            #     json.dump(extract_onevda_data(str(r5)), f, indent=4)
            # parsed_onevda_data = extract_onevda_data(str(r5))
            time2wait = int(start)-time.time()
            print(f"EID: {eid}, START: {start} | time to wait: {time2wait}s")
            


            # Assume S6 has already been sent/received above

            # Calculate time2wait from R5 earlier
            time2wait = int(start) - time.time() +7
            print(f"Time to wait for next tss: {time2wait:.2f}s")

            #Keep sending S4 if time2wait > 30s
            while time2wait > 30:
                s4_payload = (
                    f"cmd=tss;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
                )
                await websocket.send(encode_payload(s4_payload))
                print(f"Sent S4/tss : ")
                r4 = await websocket.recv()
                print(f"Received R4: {time.strftime('%H:%M:%S')} \n")

                #Wait before next S4 to avoid spamming
                await asyncio.sleep(30)

                #Recalculate time2wait
                time2wait = int(start) - time.time() # or time2wait -30
                print(f"Updated time2wait: {time2wait:.2f}s")


            #When time2wait is <= 30, send S7
            await asyncio.sleep(time2wait-5) #lsrr is sent 113s after on_evda start
            #print(f"{start}\n {time.time()}")
            # while time.time() <= float(start)+3.0:
            #     print(float(start)-time.time() +3.0 )


            s7_payload = (
                f"cmd=lsrr;id={eid};e=1;pid=14001;clientid={clientid};domain=Comm.ts;s=NaN;ts={get_timestamp()};xs={get_xs()}"
            )
            await websocket.send(encode_payload(s7_payload))
            print(f"Sent S7: {time.strftime('%H:%M:%S')}")
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
            print(f"Result for {eid}: {outcome_list}")
            # with open(f"lssr_data{eid}.json", "w") as f:
            #     json.dump((parsed_lsrr_data), f, indent=4)



# === Run the main function ===
asyncio.run(send_payloads())
