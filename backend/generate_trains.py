"""Generate ~196 trains with coaches and seats for compartment-based booking."""
from datetime import time
from stations_data import STATION_BY_CODE, STATION_CODES

ROUTES = {
    "NDLS-BCT": ["NDLS", "MTJ", "AGC", "GWL", "JHS", "BPL", "ET", "KNW", "BSL", "MMR", "NK", "KYN", "BCT"],
    "BCT-NDLS": ["BCT", "KYN", "NK", "MMR", "BSL", "KNW", "ET", "BPL", "JHS", "GWL", "AGC", "MTJ", "NDLS"],
    "NDLS-HWH": ["NDLS", "CNB", "PRYJ", "MZP", "BBS", "HWH"],
    "HWH-NDLS": ["HWH", "BBS", "MZP", "PRYJ", "CNB", "NDLS"],
    "NDLS-MAS": ["NDLS", "AGC", "BPL", "NGP", "WL", "BZA", "OGL", "MAS"],
    "MAS-NDLS": ["MAS", "OGL", "BZA", "WL", "NGP", "BPL", "AGC", "NDLS"],
    "NDLS-SBC": ["NDLS", "AGC", "BPL", "ET", "NGP", "SC", "GTL", "SBC"],
    "SBC-NDLS": ["SBC", "GTL", "SC", "NGP", "ET", "BPL", "AGC", "NDLS"],
    "NDLS-HYB": ["NDLS", "AGC", "BPL", "NGP", "KZJ", "SC", "HYB"],
    "HYB-NDLS": ["HYB", "SC", "KZJ", "NGP", "BPL", "AGC", "NDLS"],
    "CSTM-MAS": ["CSTM", "KYN", "PUNE", "SUR", "GTL", "MAS"],
    "MAS-CSTM": ["MAS", "GTL", "SUR", "PUNE", "KYN", "CSTM"],
    "CSTM-SBC": ["CSTM", "KYN", "PUNE", "SUR", "UBL", "DVG", "ASK", "SBC"],
    "SBC-CSTM": ["SBC", "ASK", "DVG", "UBL", "SUR", "PUNE", "KYN", "CSTM"],
    "CSTM-HWH": ["CSTM", "NK", "BSL", "NGP", "BSP", "JSG", "TATA", "HWH"],
    "HWH-CSTM": ["HWH", "TATA", "JSG", "BSP", "NGP", "BSL", "NK", "CSTM"],
    "HWH-MAS": ["HWH", "BBS", "BAM", "VSKP", "BZA", "MAS"],
    "MAS-HWH": ["MAS", "BZA", "VSKP", "BAM", "BBS", "HWH"],
    "HWH-SBC": ["HWH", "BBS", "VSKP", "BZA", "GTL", "SBC"],
    "SBC-HWH": ["SBC", "GTL", "BZA", "VSKP", "BBS", "HWH"],
    "NDLS-ADI": ["NDLS", "GZB", "ALJN", "JP", "AII", "ADI"],
    "ADI-NDLS": ["ADI", "AII", "JP", "ALJN", "GZB", "NDLS"],
    "BCT-ADI": ["BCT", "BVI", "VAPI", "ST", "BRC", "ADI"],
    "ADI-BCT": ["ADI", "BRC", "ST", "VAPI", "BVI", "BCT"],
    "NDLS-JAT": ["NDLS", "UMB", "LDH", "JAT"],
    "JAT-NDLS": ["JAT", "LDH", "UMB", "NDLS"],
    "NDLS-ASR": ["NDLS", "UMB", "LDH", "ASR"],
    "ASR-NDLS": ["ASR", "LDH", "UMB", "NDLS"],
    "NDLS-PNBE": ["NDLS", "CNB", "PRYJ", "MZP", "MKA", "PNBE"],
    "PNBE-NDLS": ["PNBE", "MKA", "MZP", "PRYJ", "CNB", "NDLS"],
    "NDLS-LKO": ["NDLS", "GZB", "MB", "BE", "LKO"],
    "LKO-NDLS": ["LKO", "BE", "MB", "GZB", "NDLS"],
    "NDLS-JP": ["NDLS", "GZB", "ALJN", "JP"],
    "JP-NDLS": ["JP", "ALJN", "GZB", "NDLS"],
    "MAS-SBC": ["MAS", "KPD", "SBC"],
    "SBC-MAS": ["SBC", "KPD", "MAS"],
    "SBC-HYB": ["SBC", "GTL", "KCG", "HYB"],
    "HYB-SBC": ["HYB", "KCG", "GTL", "SBC"],
    "CSTM-PUNE": ["CSTM", "KYN", "PNVL", "PUNE"],
    "PUNE-CSTM": ["PUNE", "PNVL", "KYN", "CSTM"],
    "HWH-PNBE": ["HWH", "BWN", "ASN", "DHN", "GAYA", "PNBE"],
    "PNBE-HWH": ["PNBE", "GAYA", "DHN", "ASN", "BWN", "HWH"],
    "MAS-HYB": ["MAS", "OGL", "BZA", "WL", "KZJ", "SC", "HYB"],
    "HYB-MAS": ["HYB", "SC", "KZJ", "WL", "BZA", "OGL", "MAS"],
    "NDLS-BPL": ["NDLS", "AGC", "GWL", "JHS", "BPL"],
    "BPL-NDLS": ["BPL", "JHS", "GWL", "AGC", "NDLS"],
    "SBC-MYS": ["SBC", "MYS"],
    "MYS-SBC": ["MYS", "SBC"],
    "MAS-MDU": ["MAS", "TPJ", "MDU"],
    "MDU-MAS": ["MDU", "TPJ", "MAS"],
    "NDLS-GHY": ["NDLS", "MB", "LKO", "GKP", "KIR", "NJP", "GHY"],
    "GHY-NDLS": ["GHY", "NJP", "KIR", "GKP", "LKO", "MB", "NDLS"],
    "NDLS-DDN": ["NDLS", "GZB", "HW", "DDN"],
    "DDN-NDLS": ["DDN", "HW", "GZB", "NDLS"],
    "NDLS-CDG": ["NDLS", "UMB", "CDG"],
    "CDG-NDLS": ["CDG", "UMB", "NDLS"],
    "NDLS-BSB": ["NDLS", "CNB", "PRYJ", "BSB"],
    "BSB-NDLS": ["BSB", "PRYJ", "CNB", "NDLS"],
    "HWH-ASR": ["HWH", "ASN", "DHN", "GAYA", "CNB", "DLI", "UMB", "ASR"],
    "ASR-HWH": ["ASR", "UMB", "DLI", "CNB", "GAYA", "DHN", "ASN", "HWH"],
    "CSTM-NDLS": ["CSTM", "KYN", "NK", "BSL", "ET", "BPL", "JHS", "AGC", "NDLS"],
    "NDLS-CSTM": ["NDLS", "AGC", "JHS", "BPL", "ET", "BSL", "NK", "KYN", "CSTM"],
    "MAS-HWH": ["MAS", "OGL", "BZA", "VSKP", "BBS", "HWH"],
    "HWH-MAS": ["HWH", "BBS", "VSKP", "BZA", "OGL", "MAS"],
    "BCT-JP": ["BCT", "ST", "BRC", "ADI", "AII", "JP"],
    "JP-BCT": ["JP", "AII", "ADI", "BRC", "ST", "BCT"],
    "NDLS-GWL": ["NDLS", "MTJ", "AGC", "GWL"],
    "GWL-NDLS": ["GWL", "AGC", "MTJ", "NDLS"],
    "SBC-UBL": ["SBC", "DVG", "UBL"],
    "UBL-SBC": ["UBL", "DVG", "SBC"],
    "HWH-PURI": ["HWH", "BBS", "KUR", "PURI"],
    "PURI-HWH": ["PURI", "KUR", "BBS", "HWH"],
    "CSTM-MAO": ["CSTM", "PNVL", "ROHA", "MAO"],
    "MAO-CSTM": ["MAO", "ROHA", "PNVL", "CSTM"],
    "MAS-TVC": ["MAS", "SA", "CBE", "ERS", "TVC"],
    "TVC-MAS": ["TVC", "ERS", "CBE", "SA", "MAS"],
    "NDLS-BKN": ["NDLS", "GZB", "JP", "AII", "BKN"],
    "BKN-NDLS": ["BKN", "AII", "JP", "GZB", "NDLS"],
}

TRAIN_TYPES = [
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
    "Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    "Mon,Wed,Fri", "Tue,Thu,Sat,Sun",
    "Mon,Tue,Wed,Thu,Fri", "Mon,Thu,Sat",
    "Tue,Fri,Sun", "Wed,Sat,Sun",
]

COUNTER = [0]


def estimate_distance(route):
    return max(100, len(route) * 120 + (len(route) % 5) * 50)


def generate_coaches(train_type_idx):
    """Generate coaches for a train based on its type."""
    # Rajdhani/Shatabdi: mostly AC, fewer sleeper
    # Express/Mail: more sleeper, fewer AC
    # Intercity: minimal

    if train_type_idx in (0, 1):  # Rajdhani/Shatabdi
        return [
            ("A1", "AC", 54), ("A2", "AC", 54), ("A3", "AC", 54),
            ("A4", "AC", 54), ("A5", "AC", 54), ("A6", "AC", 54),
            ("S1", "Sleeper", 72), ("S2", "Sleeper", 72),
        ]
    elif train_type_idx in (2, 3):  # Duronto/Garib Rath
        return [
            ("A1", "AC", 54), ("A2", "AC", 54), ("A3", "AC", 54),
            ("S1", "Sleeper", 72), ("S2", "Sleeper", 72),
            ("S3", "Sleeper", 72), ("S4", "Sleeper", 72),
        ]
    elif train_type_idx in (4, 5, 6, 7):  # Superfast/Sampark Kranti/Mail/Express
        return [
            ("A1", "AC", 54), ("A2", "AC", 54),
            ("S1", "Sleeper", 72), ("S2", "Sleeper", 72),
            ("S3", "Sleeper", 72), ("S4", "Sleeper", 72),
            ("S5", "Sleeper", 72), ("S6", "Sleeper", 72),
        ]
    else:  # Intercity/Jan Shatabdi
        return [
            ("A1", "AC", 54),
            ("S1", "Sleeper", 72), ("S2", "Sleeper", 72),
            ("S3", "Sleeper", 72), ("S4", "Sleeper", 72),
        ]


def generate_seats(coach_code, coach_type, total_seats):
    """Generate seat records for a coach."""
    seats = []
    if coach_type == "Sleeper":
        # 72 seats: 8 bays of 8 + 8 side berths
        for bay in range(9):
            base = bay * 8 + 1
            seats.append((f"{base}", "Lower", "Window"))
            seats.append((f"{base + 1}", "Middle", "Aisle"))
            seats.append((f"{base + 2}", "Upper", "Aisle"))
            seats.append((f"{base + 3}", "Lower", "Aisle"))
            seats.append((f"{base + 4}", "Middle", "Window"))
            seats.append((f"{base + 5}", "Upper", "Window"))
            seats.append((f"{base + 6}", "Side-Lower", "Side"))
            seats.append((f"{base + 7}", "Side-Upper", "Side"))
        seats = seats[:total_seats]
    else:  # AC
        for bay in range(9):
            base = bay * 6 + 1
            seats.append((f"{base}", "Lower", "Window"))
            seats.append((f"{base + 1}", "Upper", "Aisle"))
            seats.append((f"{base + 2}", "Lower", "Aisle"))
            seats.append((f"{base + 3}", "Upper", "Window"))
            seats.append((f"{base + 4}", "Side-Lower", "Side"))
            seats.append((f"{base + 5}", "Side-Upper", "Side"))
        seats = seats[:total_seats]
    return seats


def make_trains():
    trains = []
    used_numbers = set()

    for route_key, route_stops in ROUTES.items():
        if len(route_stops) < 2:
            continue

        origin = route_stops[0]
        dest = route_stops[-1]
        distance = estimate_distance(route_stops)
        num_trains = 3 if len(route_stops) >= 5 else 2 if len(route_stops) >= 3 else 1

        for i in range(min(num_trains, len(TRAIN_TYPES))):
            COUNTER[0] += 1
            prefix, type_name, ac_mult, sl_mult, dur_mult, speed = TRAIN_TYPES[i]
            seq = str(COUNTER[0]).zfill(3)
            train_num = prefix + seq
            if train_num in used_numbers:
                continue
            used_numbers.add(train_num)

            orig_name = STATION_BY_CODE.get(origin, {}).get("name", origin)
            dest_name = STATION_BY_CODE.get(dest, {}).get("name", dest)
            name = f"{orig_name} {dest_name} {type_name}"
            duration_h = max(3, int(distance / speed * dur_mult))
            dep_hours = [6, 8, 14, 16, 19, 21, 23]
            dep_time = time(dep_hours[i % len(dep_hours)], (i * 15) % 60)
            arr_h = (dep_time.hour + duration_h) % 24
            arr_time = time(arr_h, dep_time.minute)
            days = DAYS_COMBOS[i % len(DAYS_COMBOS)]
            ac_fare = round(distance * 2.5 * ac_mult, 2)
            sleeper_fare = round(distance * 1.0 * sl_mult, 2)

            coaches = generate_coaches(i % len(TRAIN_TYPES))

            trains.append({
                "train_number": train_num,
                "train_name": name,
                "origin": origin,
                "destination": dest,
                "departure_time": dep_time,
                "arrival_time": arr_time,
                "duration_hours": duration_h,
                "running_days": days,
                "ac_fare": ac_fare,
                "sleeper_fare": sleeper_fare,
                "route_stations": route_stops,
                "coaches": coaches,
            })

    return trains


if __name__ == "__main__":
    t = make_trains()
    print(f"Generated {len(t)} trains")
    for tr in t[:3]:
        print(f"  {tr['train_number']} {tr['train_name']}: {tr['origin']}->{tr['destination']} ({len(tr['coaches'])} coaches)")
