from flask import Flask, render_template, request, jsonify
import time, math

app = Flask(__name__)

COLLEGE = [10.0100, 76.4527]

def t(dep_h, dep_m, add_mins):
    total = dep_h * 60 + dep_m + add_mins
    return f"{total//60:02d}:{total%60:02d}"

# ── BUS ROUTES ────────────────────────────────────────────────────────────────
# Stops are just informational markers along the route.
# The route line is drawn by OSRM using only start → college (shortest path).
# Stop times are calculated from departure time.

BUS_ROUTES = {
    "Bus-1": {
        "name": "Elamkunnapuzha",
        "start": [10.0268, 76.2233],
        "depart": "07:35",
        "stops": [
            [10.0268, 76.2233, "Elamkunnapuzha",   t(7,35,0)],
            [10.0416, 76.2189, "Njarakkal",         t(7,35,8)],
            [10.0620, 76.2450, "Pallippuram",        t(7,35,16)],
            [10.0130, 76.2630, "Gosree Bridge",      t(7,35,26)],
            [ 9.9680, 76.2990, "Vyttila",            t(7,35,38)],
            [ 9.9750, 76.3500, "Tripunithura",       t(7,35,48)],
            [ 9.9880, 76.4100, "Irumpanam",          t(7,35,58)],
            [ 9.9950, 76.4400, "Kadayiruppu",        t(7,35,68)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-2": {
        "name": "North Paravur",
        "start": [10.1446, 76.2273],
        "depart": "07:45",
        "stops": [
            [10.1446, 76.2273, "North Paravur",      t(7,45,0)],
            [10.1492, 76.2350, "Chendamangalam",     t(7,45,7)],
            [10.1350, 76.2600, "Varapuzha",          t(7,45,14)],
            [10.1063, 76.3562, "Aluva",              t(7,45,24)],
            [10.0624, 76.3273, "Kalamassery",        t(7,45,35)],
            [ 9.9680, 76.2990, "Vyttila",            t(7,45,44)],
            [ 9.9750, 76.3500, "Tripunithura",       t(7,45,52)],
            [ 9.9880, 76.4100, "Irumpanam",          t(7,45,60)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-3": {
        "name": "Kothamangalam",
        "start": [10.0603, 76.6352],
        "depart": "07:45",
        "stops": [
            [10.0603, 76.6352, "Kothamangalam",      t(7,45,0)],
            [10.0400, 76.6100, "Keerampara",         t(7,45,8)],
            [ 9.9773, 76.5793, "Muvattupuzha",       t(7,45,22)],
            [ 9.9900, 76.5300, "Piravom",            t(7,45,32)],
            [ 9.9797, 76.4728, "Kolenchery Jn",      t(7,45,45)],
            [ 9.9950, 76.4400, "Kadayiruppu",        t(7,45,52)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-4": {
        "name": "Thalayolaparambu",
        "start": [9.7850, 76.4496],
        "depart": "07:25",
        "stops": [
            [ 9.7850, 76.4496, "Thalayolaparambu",   t(7,25,0)],
            [ 9.7216, 76.3927, "Vaikom",             t(7,25,18)],
            [ 9.7800, 76.4100, "Ettumanoor",         t(7,25,30)],
            [ 9.8600, 76.4000, "Kottayam",           t(7,25,46)],
            [ 9.9433, 76.3463, "Tripunithura",       t(7,25,65)],
            [ 9.9703, 76.4247, "Puthencruz",         t(7,25,76)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-5": {
        "name": "Thodupuzha",
        "start": [9.8959, 76.7184],
        "depart": "07:40",
        "stops": [
            [ 9.8959, 76.7184, "Thodupuzha",         t(7,40,0)],
            [ 9.9200, 76.6800, "Moolamattom",        t(7,40,9)],
            [ 9.9773, 76.5793, "Muvattupuzha",       t(7,40,25)],
            [ 9.9900, 76.5300, "Piravom",            t(7,40,35)],
            [ 9.9797, 76.4728, "Kolenchery Jn",      t(7,40,48)],
            [ 9.9950, 76.4400, "Kadayiruppu",        t(7,40,55)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-6": {
        "name": "Vaikom",
        "start": [9.7216, 76.3927],
        "depart": "07:35",
        "stops": [
            [ 9.7216, 76.3927, "Vaikom",             t(7,35,0)],
            [ 9.7500, 76.3900, "Kuruvilangad",       t(7,35,10)],
            [ 9.8600, 76.3700, "Erattupetta",        t(7,35,28)],
            [ 9.9433, 76.3463, "Tripunithura",       t(7,35,46)],
            [ 9.9703, 76.4247, "Puthencruz",         t(7,35,58)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-7": {
        "name": "Palluruthy",
        "start": [9.9216, 76.2736],
        "depart": "07:55",
        "stops": [
            [ 9.9216, 76.2736, "Palluruthy",         t(7,55,0)],
            [ 9.9300, 76.2850, "Thevara",            t(7,55,7)],
            [ 9.9680, 76.2990, "Vyttila",            t(7,55,14)],
            [ 9.9750, 76.3500, "Tripunithura",       t(7,55,22)],
            [ 9.9703, 76.4247, "Puthencruz",         t(7,55,36)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-8": {
        "name": "Chullickal",
        "start": [9.9477, 76.2566],
        "depart": "08:00",
        "stops": [
            [ 9.9477, 76.2566, "Chullickal",         t(8,0,0)],
            [ 9.9500, 76.2750, "Ernakulam South",    t(8,0,6)],
            [ 9.9680, 76.2990, "Vyttila",            t(8,0,14)],
            [ 9.9750, 76.3500, "Tripunithura",       t(8,0,22)],
            [ 9.9703, 76.4247, "Puthencruz",         t(8,0,36)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-9": {
        "name": "Angamaly",
        "start": [10.1926, 76.3869],
        "depart": "07:40",
        "stops": [
            [10.1926, 76.3869, "Angamaly",           t(7,40,0)],
            [10.1500, 76.3700, "Perumbavoor",        t(7,40,12)],
            [10.1063, 76.3562, "Aluva",              t(7,40,22)],
            [10.0624, 76.3273, "Kalamassery",        t(7,40,32)],
            [ 9.9680, 76.2990, "Vyttila",            t(7,40,42)],
            [ 9.9750, 76.3500, "Tripunithura",       t(7,40,50)],
            [ 9.9880, 76.4100, "Irumpanam",          t(7,40,58)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-10": {
        "name": "Kothad",
        "start": [10.0521, 76.2740],
        "depart": "07:55",
        "stops": [
            [10.0521, 76.2740, "Kothad",             t(7,55,0)],
            [10.0271, 76.3082, "Edapally Jn",        t(7,55,12)],
            [10.0200, 76.3400, "Palarivattom",       t(7,55,20)],
            [ 9.9680, 76.2990, "Vyttila",            t(7,55,28)],
            [ 9.9750, 76.3500, "Tripunithura",       t(7,55,36)],
            [ 9.9880, 76.4100, "Irumpanam",          t(7,55,44)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
    "Bus-11": {
        "name": "Kaloor",
        "start": [9.9921, 76.3019],
        "depart": "08:00",
        "stops": [
            [ 9.9921, 76.3019, "Kaloor",             t(8,0,0)],
            [ 9.9680, 76.2990, "Vyttila",            t(8,0,10)],
            [ 9.9750, 76.3500, "Tripunithura",       t(8,0,18)],
            [ 9.9703, 76.4247, "Puthencruz",         t(8,0,32)],
            [10.0100, 76.4527, "SNGCE College",      "09:00"],
        ]
    },
}

gps_store = {}

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlng = math.radians(lng2-lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def estimate_speed(bus_id):
    entry = gps_store.get(bus_id)
    if not entry or not entry.get("speed_history"):
        return 30
    history = entry["speed_history"][-5:]
    weights = list(range(1, len(history)+1))
    return max(5, min(60, sum(s*w for s,w in zip(history,weights))/sum(weights)))

def predict_stops(bus_id, bus_lat, bus_lng, is_live=False):
    route = BUS_ROUTES.get(bus_id)
    if not route:
        return []
    stops = route["stops"]
    speed = estimate_speed(bus_id) if is_live else 30
    dist_bus_college = haversine(bus_lat, bus_lng, COLLEGE[0], COLLEGE[1])
    now = time.localtime()
    now_mins = now.tm_hour * 60 + now.tm_min
    results = []
    for i, stop in enumerate(stops):
        slat, slng, sname, sched_time = stop
        dist_to_stop = haversine(bus_lat, bus_lng, slat, slng)
        dist_stop_college = haversine(slat, slng, COLLEGE[0], COLLEGE[1])
        passed = is_live and dist_bus_college < dist_stop_college and dist_to_stop > 0.3
        eta_mins = round((dist_to_stop/speed)*60) if not passed else None
        sh, sm2 = map(int, sched_time.split(":"))
        sched_mins_day = sh*60+sm2
        late, late_by = False, 0
        if not passed and eta_mins is not None:
            late_by = round((now_mins+eta_mins) - sched_mins_day)
            late = late_by > 5
        results.append({
            "name": sname, "lat": slat, "lng": slng,
            "dist_km": round(dist_to_stop, 2),
            "eta_mins": eta_mins, "passed": passed,
            "late": late, "late_by": late_by,
            "sched_time": sched_time,
            "is_college": i == len(stops)-1,
        })
    return results

@app.route("/")
def home():
    return render_template("index.html", buses=BUS_ROUTES)

@app.route("/driver")
def driver():
    return render_template("driver.html", buses=list(BUS_ROUTES.keys()))

@app.route("/map")
def map_view():
    bus = request.args.get("bus")
    if bus not in BUS_ROUTES:
        return "Invalid Bus", 400
    info = BUS_ROUTES[bus]
    return render_template("map.html", bus=bus, college=COLLEGE,
                           start=info["start"], place=info["name"],
                           depart=info["depart"], stops=info["stops"])

@app.route("/api/update", methods=["POST"])
def update_location():
    data = request.get_json()
    bus, lat, lng = data.get("bus"), data.get("lat"), data.get("lng")
    if not bus or bus not in BUS_ROUTES or lat is None or lng is None:
        return jsonify({"error":"bad data"}), 400
    now = time.time()
    prev = gps_store.get(bus)
    speed = 30
    if prev and prev.get("ts"):
        dt = now-prev["ts"]
        if dt > 1:
            speed = max(0, min(120, (haversine(prev["lat"],prev["lng"],lat,lng)/dt)*3600))
    history = (prev.get("speed_history",[]) if prev else [])+[speed]
    gps_store[bus] = {"lat":lat,"lng":lng,"ts":now,"speed_history":history[-20:],
                      "departure_ts":prev.get("departure_ts") if prev else now}
    return jsonify({"ok":True})

@app.route("/api/location/<bus>")
def get_location(bus):
    if bus not in BUS_ROUTES:
        return jsonify({"error":"unknown bus"}), 404
    start = BUS_ROUTES[bus]["start"]
    entry = gps_store.get(bus)
    if not entry:
        return jsonify({"lat":start[0],"lng":start[1],"live":False,"ts":None,
                        "stops":predict_stops(bus,start[0],start[1],False),"speed":0})
    age = time.time()-entry["ts"]
    if age > 120:
        return jsonify({"lat":start[0],"lng":start[1],"live":False,"ts":None,
                        "stops":predict_stops(bus,start[0],start[1],False),"speed":0})
    live = age <= 30
    return jsonify({"lat":entry["lat"],"lng":entry["lng"],"live":live,"ts":entry["ts"],
                    "stops":predict_stops(bus,entry["lat"],entry["lng"],live),
                    "speed":round(estimate_speed(bus),1)})

@app.route("/api/reset")
def reset_all():
    gps_store.clear()
    return jsonify({"ok":True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
