from flask import Flask, render_template, request, jsonify
import json, os, time

app = Flask(__name__)

# ---------- DATA ----------
COLLEGE = [10.0100, 76.4527]   # [lat, lng]  SNGCE Kadayiruppu, Kolenchery (verified)

BUS_ROUTES = {
    "Bus-1":  {"name": "Elamkunnapuzha",     "start": [10.0900, 76.2160]},
    "Bus-2":  {"name": "North Paravur",       "start": [10.1410, 76.2080]},
    "Bus-3":  {"name": "Kothamangalam",       "start": [10.0630, 76.6280]},
    "Bus-4":  {"name": "Thalayolaparambu",    "start": [ 9.8000, 76.4420]},
    "Bus-5":  {"name": "Thodupuzha",          "start": [ 9.9000, 76.7150]},
    "Bus-6":  {"name": "Vaikom",              "start": [ 9.7480, 76.3960]},
    "Bus-7":  {"name": "Palluruthy",          "start": [ 9.9300, 76.2670]},
    "Bus-8":  {"name": "Chullickal",          "start": [ 9.9640, 76.2610]},
    "Bus-9":  {"name": "Angamaly",            "start": [10.1900, 76.3870]},
    "Bus-10": {"name": "Kothad",              "start": [10.0600, 76.3020]},
    "Bus-11": {"name": "Kaloor",              "start": [ 9.9980, 76.2910]},
}

# ---------- IN-MEMORY GPS STORE ----------
# { "Bus-1": {"lat": ..., "lng": ..., "ts": ...}, ... }
gps_store = {}

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html", buses=BUS_ROUTES)


# ── Driver page (open on driver's phone) ──────────────────────────────────────
@app.route("/driver")
def driver():
    return render_template("driver.html", buses=list(BUS_ROUTES.keys()))


# ── Driver posts GPS here every ~5 s ─────────────────────────────────────────
@app.route("/api/update", methods=["POST"])
def update_location():
    data = request.get_json()
    bus  = data.get("bus")
    lat  = data.get("lat")
    lng  = data.get("lng")

    if not bus or bus not in BUS_ROUTES or lat is None or lng is None:
        return jsonify({"error": "bad data"}), 400

    gps_store[bus] = {"lat": lat, "lng": lng, "ts": time.time()}
    return jsonify({"ok": True})


# ── Student map polls this ────────────────────────────────────────────────────
@app.route("/api/location/<bus>")
def get_location(bus):
    if bus not in BUS_ROUTES:
        return jsonify({"error": "unknown bus"}), 404

    entry = gps_store.get(bus)
    if not entry:
        # Fall back to static start position so map still loads
        start = BUS_ROUTES[bus]["start"]
        return jsonify({"lat": start[0], "lng": start[1],
                        "live": False, "ts": None})

    stale = (time.time() - entry["ts"]) > 30   # 30 s = stale
    return jsonify({
        "lat":  entry["lat"],
        "lng":  entry["lng"],
        "live": not stale,
        "ts":   entry["ts"]
    })


# ── Student tracking map ──────────────────────────────────────────────────────
@app.route("/map")
def map_view():
    bus = request.args.get("bus")
    if bus not in BUS_ROUTES:
        return "Invalid Bus", 400

    info = BUS_ROUTES[bus]
    return render_template("map.html",
                           bus=bus,
                           college=COLLEGE,
                           start=info["start"],
                           place=info["name"])


if __name__ == "__main__":
    # 0.0.0.0 so phones on the same Wi-Fi can reach it
    app.run(host="0.0.0.0", port=5000, debug=True)
