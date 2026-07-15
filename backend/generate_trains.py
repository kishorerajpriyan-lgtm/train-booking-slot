"""Generate ~200 realistic Indian trains with proper route_stations for any-pair searches.

Each train has a full ordered list of stations on its route, enabling search
for any origin-destination pair along that corridor.
"""
from datetime import time
from stations_data import STATION_BY_CODE, STATION_CODES

# ─── Route Definitions (station codes in order) ──────────────────────────────
# Each corridor is a list of station codes the train passes through.

ROUTES = {
    # Delhi ↔ Mumbai corridor
    "NDLS-BCT": ["NDLS", "MTJ", "AGC", "GWL", "JHS", "BPL", "ET", "KNW", "BSL", "MMR", "NK", "KYN", "BCT"],
    "BCT-NDLS": ["BCT", "KYN", "NK", "MMR", "BSL", "KNW", "ET", "BPL", "JHS", "GWL", "AGC", "MTJ", "NDLS"],

    # Delhi ↔ Howrah corridor
    "NDLS-HWH": ["NDLS", "CNB", "PRYJ", "MZP", "BBS", "HWH"],
    "HWH-NDLS": ["HWH", "BBS", "MZP", "PRYJ", "CNB", "NDLS"],

    # Delhi ↔ Chennai corridor
    "NDLS-MAS": ["NDLS", "AGC", "BPL", "NGP", "WL", "BZA", "OGL", "MAS"],
    "MAS-NDLS": ["MAS", "OGL", "BZA", "WL", "NGP", "BPL", "AGC", "NDLS"],

    # Delhi ↔ Bangalore corridor
    "NDLS-SBC": ["NDLS", "AGC", "BPL", "ET", "NGP", "SC", "GTL", "SBC"],
    "SBC-NDLS": ["SBC", "GTL", "SC", "NGP", "ET", "BPL", "AGC", "NDLS"],

    # Delhi ↔ Hyderabad
    "NDLS-HYB": ["NDLS", "AGC", "BPL", "NGP", "KZJ", "SC", "HYB"],
    "HYB-NDLS": ["HYB", "SC", "KZJ", "NGP", "BPL", "AGC", "NDLS"],

    # Mumbai ↔ Chennai
    "CSTM-MAS": ["CSTM", "KYN", "PUNE", "SUR", "GTL", "MAS"],
    "MAS-CSTM": ["MAS", "GTL", "SUR", "PUNE", "KYN", "CSTM"],

    # Mumbai ↔ Bangalore
    "CSTM-SBC": ["CSTM", "KYN", "PUNE", "SUR", "UBL", "DVG", "ASK", "SBC"],
    "SBC-CSTM": ["SBC", "ASK", "DVG", "UBL", "SUR", "PUNE", "KYN", "CSTM"],

    # Mumbai ↔ Howrah
    "CSTM-HWH": ["CSTM", "NK", "BSL", "NGP", "BSP", "JSG", "TATA", "HWH"],
    "HWH-CSTM": ["HWH", "TATA", "JSG", "BSP", "NGP", "BSL", "NK", "CSTM"],

    # Howrah ↔ Chennai
    "HWH-MAS": ["HWH", "BBS", "BAM", "VSKP", "BZA", "MAS"],
    "MAS-HWH": ["MAS", "BZA", "VSKP", "BAM", "BBS", "HWH"],

    # Howrah ↔ Bangalore
    "HWH-SBC": ["HWH", "BBS", "VSKP", "BZA", "GTL", "SBC"],
    "SBC-HWH": ["SBC", "GTL", "BZA", "VSKP", "BBS", "HWH"],

    # Delhi ↔ Ahmedabad
    "NDLS-ADI": ["NDLS", "GZB", "ALJN", "JP", "AII", "ADI"],
    "ADI-NDLS": ["ADI", "AII", "JP", "ALJN", "GZB", "NDLS"],

    # Mumbai ↔ Ahmedabad
    "BCT-ADI": ["BCT", "BVI", "VAPI", "ST", "BRC", "ADI"],
    "ADI-BCT": ["ADI", "BRC", "ST", "VAPI", "BVI", "BCT"],

    # Delhi ↔ Jammu
    "NDLS-JAT": ["NDLS", "UMB", "LDH", "JAT"],
    "JAT-NDLS": ["JAT", "LDH", "UMB", "NDLS"],

    # Delhi ↔ Amritsar
    "NDLS-ASR": ["NDLS", "UMB", "LDH", "ASR"],
    "ASR-NDLS": ["ASR", "LDH", "UMB", "NDLS"],

    # Delhi ↔ Patna
    "NDLS-PNBE": ["NDLS", "CNB", "PRYJ", "MZP", "MKA", "PNBE"],
    "PNBE-NDLS": ["PNBE", "MKA", "MZP", "PRYJ", "CNB", "NDLS"],

    # Delhi ↔ Lucknow
    "NDLS-LKO": ["NDLS", "GZB", "MB", "BE", "LKO"],
    "LKO-NDLS": ["LKO", "BE", "MB", "GZB", "NDLS"],

    # Delhi ↔ Jaipur
    "NDLS-JP": ["NDLS", "GZB", "ALJN", "JP"],
    "JP-NDLS": ["JP", "ALJN", "GZB", "NDLS"],

    # Chennai ↔ Bangalore
    "MAS-SBC": ["MAS", "KPD", "SBC"],
    "SBC-MAS": ["SBC", "KPD", "MAS"],

    # Bangalore ↔ Hyderabad
    "SBC-HYB": ["SBC", "GTL", "KCG", "HYB"],
    "HYB-SBC": ["HYB", "KCG", "GTL", "SBC"],

    # Mumbai ↔ Pune
    "CSTM-PUNE": ["CSTM", "KYN", "PNVL", "PUNE"],
    "PUNE-CSTM": ["PUNE", "PNVL", "KYN", "CSTM"],

    # Howrah ↔ Patna
    "HWH-PNBE": ["HWH", "BWN", "ASN", "DHN", "GAYA", "PNBE"],
    "PNBE-HWH": ["PNBE", "GAYA", "DHN", "ASN", "BWN", "HWH"],

    # Chennai ↔ Hyderabad
    "MAS-HYB": ["MAS", "OGL", "BZA", "WL", "KZJ", "SC", "HYB"],
    "HYB-MAS": ["HYB", "SC", "KZJ", "WL", "BZA", "OGL", "MAS"],

    # Delhi ↔ Bhopal (Shatabdi type)
    "NDLS-BPL": ["NDLS", "AGC", "GWL", "JHS", "BPL"],
    "BPL-NDLS": ["BPL", "JHS", "GWL", "AGC", "NDLS"],

    # Bangalore ↔ Mysore
    "SBC-MYS": ["SBC", "MYS"],
    "MYS-SBC": ["MYS", "SBC"],

    # Chennai ↔ Madurai
    "MAS-MDU": ["MAS", "TPJ", "MDU"],
    "MDU-MAS": ["MDU", "TPJ", "MAS"],

    # Delhi ↔ Guwahati
    "NDLS-GHY": ["NDLS", "MB", "LKO", "GKP", "KIR", "NJP", "GHY"],
    "GHY-NDLS": ["GHY", "NJP", "KIR", "GKP", "LKO", "MB", "NDLS"],

    # Delhi ↔ Dehradun
    "NDLS-DDN": ["NDLS", "GZB", "HW", "DDN"],
    "DDN-NDLS": ["DDN", "HW", "GZB", "NDLS"],

    # Delhi ↔ Chandigarh
    "NDLS-CDG": ["NDLS", "UMB", "CDG"],
    "CDG-NDLS": ["CDG", "UMB", "NDLS"],

    # Delhi ↔ Varanasi
    "NDLS-BSB": ["NDLS", "CNB", "PRYJ", "BSB"],
    "BSB-NDLS": ["BSB", "PRYJ", "CNB", "NDLS"],

    # Howrah ↔ Amritsar
    "HWH-ASR": ["HWH", "ASN", "DHN", "GAYA", "CNB", "DLI", "UMB", "ASR"],
    "ASR-HWH": ["ASR", "UMB", "DLI", "CNB", "GAYA", "DHN", "ASN", "HWH"],

    # Mumbai ↔ Delhi (via Bhopal)
    "CSTM-NDLS": ["CSTM", "KYN", "NK", "BSL", "ET", "BPL", "JHS", "AGC", "NDLS"],
    "NDLS-CSTM": ["NDLS", "AGC", "JHS", "BPL", "ET", "BSL", "NK", "KYN", "CSTM"],

    # Chennai ↔ Howrah
    "MAS-HWH": ["MAS", "OGL", "BZA", "VSKP", "BBS", "HWH"],
    "HWH-MAS": ["HWH", "BBS", "VSKP", "BZA", "OGL", "MAS"],

    # Mumbai ↔ Jaipur
    "BCT-JP": ["BCT", "ST", "BRC", "ADI", "AII", "JP"],
    "JP-BCT": ["JP", "AII", "ADI", "BRC", "ST", "BCT"],

    # Delhi ↔ Gwalior
    "NDLS-GWL": ["NDLS", "MTJ", "AGC", "GWL"],
    "GWL-NDLS": ["GWL", "AGC", "MTJ", "NDLS"],

    # Bangalore ↔ Hubli
    "SBC-UBL": ["SBC", "DVG", "UBL"],
    "UBL-SBC": ["UBL", "DVG", "SBC"],

    # Howrah ↔ Puri
    "HWH-PURI": ["HWH", "BBS", "KUR", "PURI"],
    "PURI-HWH": ["PURI", "KUR", "BBS", "HWH"],

    # Mumbai ↔ Goa
    "CSTM-MAO": ["CSTM", "PNVL", "ROHA", "MAO"],
    "MAO-CSTM": ["MAO", "ROHA", "PNVL", "CSTM"],

    # Chennai ↔ Trivandrum
    "MAS-TVC": ["MAS", "SA", "CBE", "ERS", "TVC"],
    "TVC-MAS": ["TVC", "ERS", "CBE", "SA", "MAS"],

    # Bangalore ↔ Chennai (via KPD)
    "SBC-MAS": ["SBC", "KPD", "MAS"],
    "MAS-SBC": ["MAS", "KPD", "SBC"],

    # Delhi ↔ Bikaner
    "NDLS-BKN": ["NDLS", "GZB", "JP", "AII", "BKN"],
    "BKN-NDLS": ["BKN", "AII", "JP", "GZB", "NDLS"],
}

# ─── Train Templates ─────────────────────────────────────────────────────────
# For each route, generate multiple trains with different types.
# train_type: (prefix_num, name_suffix, base_ac_fare_per_100km, base_sleeper_fare_per_100km)

TRAIN_TYPES = [
    # (number_prefix, type_name, ac_fare_mult, sleeper_fare_mult, duration_mult, speed_kmph)
    ("12", "Rajdhani Express", 1.4, 1.0, 0.85, 80),
    ("12", "Shatabdi Express", 1.3, 0.9, 0.8, 85),
    ("22", "Duronto Express", 1.2, 0.9, 0.85, 80),
    ("16", "Garib Rath", 0.8, 0.6, 0.9, 75),
    ("19", "Superfast Express", 1.0, 0.7, 0.95, 70),
    ("15", "Sampark Kranti", 1.0, 0.7, 0.95, 70),
    ("11", "Mail", 0.9, 0.6, 1.1, 60),
    ("13", "Express", 0.85, 0.55, 1.1, 60),
    ("18", "Intercity Express", 0.7, 0.5, 0.7, 75),
    ("14", "Jan Shatabdi", 0.8, 0.55, 0.8, 75),
]

DAYS_COMBOS = [
    "Mon,Tue,Wed,Thu,Fri,Sat,Sun",  # Daily
    "Mon,Wed,Fri",
    "Tue,Thu,Sat,Sun",
    "Mon,Tue,Wed,Thu,Fri",
    "Mon,Thu,Sat",
    "Tue,Fri,Sun",
    "Wed,Sat,Sun",
]

TRAIN_COUNTER = [0]


def estimate_distance(route: list[str]) -> int:
    """Estimate distance in km based on number of stations."""
    return max(100, len(route) * 120 + (len(route) % 5) * 50)


def make_trains():
    trains = []
    used_numbers = set()

    for route_key, route_stops in ROUTES.items():
        if len(route_stops) < 2:
            continue

        origin = route_stops[0]
        dest = route_stops[-1]
        distance = estimate_distance(route_stops)

        # Generate 1-3 trains per route depending on route importance
        num_trains = 3 if len(route_stops) >= 5 else 2 if len(route_stops) >= 3 else 1

        for i in range(min(num_trains, len(TRAIN_TYPES))):
            TRAIN_COUNTER[0] += 1
            prefix, type_name, ac_mult, sl_mult, dur_mult, speed = TRAIN_TYPES[i % len(TRAIN_TYPES)]
            seq = str(TRAIN_COUNTER[0]).zfill(3)
            train_num = prefix + seq

            if train_num in used_numbers:
                continue
            used_numbers.add(train_num)

            origin_name = STATION_BY_CODE.get(origin, {}).get("name", origin)
            dest_name = STATION_BY_CODE.get(dest, {}).get("name", dest)

            name = f"{origin_name} {dest_name} {type_name}"

            duration_h = max(3, int(distance / speed * dur_mult))
            duration_h = duration_h if duration_h > 0 else 3

            # Departure times: rotate through the day
            dep_hours = [6, 8, 14, 16, 19, 21, 23]
            dep_time = time(dep_hours[i % len(dep_hours)], (i * 15) % 60)
            arr_h = (dep_time.hour + duration_h) % 24
            arr_time = time(arr_h, dep_time.minute)

            days = DAYS_COMBOS[i % len(DAYS_COMBOS)]

            ac_fare = round(distance * 2.5 * ac_mult, 2)
            sleeper_fare = round(distance * 1.0 * sl_mult, 2)

            ac_seats = 30 + (TRAIN_COUNTER[0] % 5) * 5
            sleeper_seats = 60 + (TRAIN_COUNTER[0] % 8) * 8

            trains.append({
                "train_number": train_num,
                "train_name": name,
                "origin": origin,
                "destination": dest,
                "departure_time": dep_time,
                "arrival_time": arr_time,
                "duration_hours": duration_h,
                "running_days": days,
                "ac_seats": ac_seats,
                "sleeper_seats": sleeper_seats,
                "ac_fare": ac_fare,
                "sleeper_fare": sleeper_fare,
                "route_stations": route_stops,
            })

    return trains


if __name__ == "__main__":
    trains = make_trains()
    print(f"Generated {len(trains)} trains")
    for t in trains[:5]:
        print(f"  {t['train_number']} {t['train_name']}: {t['origin']} -> {t['destination']} "
              f"({len(t['route_stations'])} stops)")
