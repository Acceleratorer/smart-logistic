# -*- coding: utf-8 -*-
import os, re, time, uuid, inspect
import numpy as np
import pandas as pd
import folium
import requests
import gradio as gr

from gradio_iframe import iFrame  # stable iframe embedding [5](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html)[6](https://docs.pydantic.dev/latest/install/)
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from sklearn.metrics.pairwise import haversine_distances
from sklearn.neighbors import NearestNeighbors

EARTH_RADIUS_KM = 6371.0
OSRM_BASE = "https://router.project-osrm.org"  # OSRM route api [7](https://www.gradio.app/4.44.1/guides/sharing-your-app)[8](https://readmedium.com/ea19ba8b497a)

# ----------------------------
# CSS
# ----------------------------
APP_CSS = """
:root{
  --snart:#16a34a;
  --snart-dark:#064e3b;
  --bg:#f6fff9;
}
.gradio-container{background: var(--bg) !important;}
#snart_header{
  background: linear-gradient(90deg, var(--snart-dark), var(--snart));
  padding: 14px 16px; border-radius: 14px; color: white; font-weight: 800;
  box-shadow: 0 10px 25px rgba(0,0,0,.10);
}
#snart_sub{color:#dcfce7;font-weight:500;margin-top:4px}
.snart_card{
  border:1px solid rgba(22,163,74,.25);
  border-radius:14px; padding:12px 12px;
  background: rgba(220,252,231,.25);
}
.snart_badge{
  display:inline-block; padding:4px 10px; border-radius:999px;
  background: rgba(22,163,74,.15);
  border:1px solid rgba(22,163,74,.25);
  color:#065f46; font-weight:700; font-size:12px; margin-bottom:6px;
}
.small_note{color:#065f46;font-size:12px;opacity:.95}
"""

# ----------------------------
# Map file dir (served by /gradio_api/file=...) requires allow_list/allowed_paths [9](https://pypi.org/project/pydantic/)[10](https://www.kaggle.com/code/neha005/ml-model-with-gradio)
# ----------------------------
MAP_DIR = "snart_maps"
os.makedirs(MAP_DIR, exist_ok=True)

def cleanup_old_maps(max_files=50):
    files = [os.path.join(MAP_DIR, f) for f in os.listdir(MAP_DIR) if f.endswith(".html")]
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    for f in files[max_files:]:
        try: os.remove(f)
        except: pass

# ----------------------------
# Parse / geocode
# ----------------------------
LATLON_RE = re.compile(r"^\s*(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)\s*$")

def parse_latlon(text):
    m = LATLON_RE.match(text or "")
    if not m:
        return None
    lat = float(m.group(1)); lon = float(m.group(3))
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        return lat, lon
    return None

_geolocator = Nominatim(user_agent="snart_logistics_kaggle")
_geocode = RateLimiter(_geolocator.geocode, min_delay_seconds=1)

def geocode_address(addr_or_latlon: str):
    ll = parse_latlon(addr_or_latlon)
    if ll:
        return ll[0], ll[1], f"{ll[0]:.6f},{ll[1]:.6f}"
    loc = _geocode(addr_or_latlon)
    if loc is None:
        raise ValueError(f"Không tìm thấy địa chỉ: {addr_or_latlon}")
    return loc.latitude, loc.longitude, loc.address

# ----------------------------
# Route ordering (NN) + haversine fallback
# ----------------------------
def haversine_km(a_latlon, b_latlon):
    X = np.radians(np.array([a_latlon, b_latlon]))
    return float(haversine_distances(X[:1], X[1:]) * EARTH_RADIUS_KM)

def nearest_neighbor_route(coords, start=0, return_to_start=True):
    X = np.radians(np.array(coords))
    nn = NearestNeighbors(metric="haversine", algorithm="ball_tree")
    nn.fit(X)
    n = len(coords)
    visited = [False] * n
    route = [start]; visited[start] = True
    cur = start
    for _ in range(n - 1):
        _, idxs = nn.kneighbors([X[cur]], n_neighbors=n)
        for j in idxs[0]:
            j = int(j)
            if not visited[j]:
                route.append(j); visited[j] = True; cur = j
                break
    if return_to_start:
        route.append(start)
    return route

# ----------------------------
# OSRM road distance & geometry
# Endpoint: /route/v1/driving/{lon,lat;lon,lat...} [7](https://www.gradio.app/4.44.1/guides/sharing-your-app)[8](https://readmedium.com/ea19ba8b497a)
# ----------------------------
def osrm_leg_distance_km(a_latlon, b_latlon, timeout=20):
    (alat, alon), (blat, blon) = a_latlon, b_latlon
    url = f"{OSRM_BASE}/route/v1/driving/{alon},{alat};{blon},{blat}"
    params = {"overview": "false"}
    try:
        r = requests.get(url, params=params, timeout=timeout)
        if r.status_code != 200:
            return haversine_km(a_latlon, b_latlon)
        data = r.json()
        if data.get("code") != "Ok":
            return haversine_km(a_latlon, b_latlon)
        return float(data["routes"][0]["distance"]) / 1000.0
    except Exception:
        return haversine_km(a_latlon, b_latlon)

def osrm_route_geometry(coords_in_order, timeout=25):
    if len(coords_in_order) < 2:
        return None
    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords_in_order])
    url = f"{OSRM_BASE}/route/v1/driving/{coord_str}"
    params = {"overview": "full", "geometries": "geojson"}
    try:
        r = requests.get(url, params=params, timeout=timeout)
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("code") != "Ok":
            return None
        geom = data["routes"][0]["geometry"]["coordinates"]  # [lon,lat]
        return [(lat, lon) for lon, lat in geom]
    except Exception:
        return None

# ----------------------------
# Costing
# ----------------------------
CARGO_MULTIPLIER = {
    "Hàng thường": 1.0,
    "Dễ vỡ": 1.25,
    "Thực phẩm lạnh": 1.35,
    "Hàng cồng kềnh": 1.2,
    "Giá trị cao": 1.4
}

STOP_COLS = ["name", "address_or_latlon", "cargo_type", "weight_kg", "L_cm", "W_cm", "H_cm"]

def rule_cost(distance_km, weight, volume, cargo, base_fee, per_km, per_kg, per_m3):
    mult = CARGO_MULTIPLIER.get(cargo, 1.0)
    return (base_fee + distance_km * per_km + weight * per_kg + volume * per_m3) * mult

def normalize_stops(stops_like):
    if stops_like is None:
        return pd.DataFrame(columns=STOP_COLS)
    if isinstance(stops_like, pd.DataFrame):
        df = stops_like.copy()
    elif isinstance(stops_like, dict) and "data" in stops_like:
        df = pd.DataFrame(stops_like["data"], columns=STOP_COLS[:len(stops_like["data"][0])])
    else:
        df = pd.DataFrame(stops_like, columns=STOP_COLS[:len(stops_like[0])]) if len(stops_like) else pd.DataFrame(columns=STOP_COLS)
    for c in STOP_COLS:
        if c not in df.columns:
            df[c] = np.nan
    df["name"] = df["name"].astype(str)
    df["address_or_latlon"] = df["address_or_latlon"].astype(str)
    df["cargo_type"] = df["cargo_type"].astype(str)
    for c in ["weight_kg", "L_cm", "W_cm", "H_cm"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    return df[STOP_COLS]

# ----------------------------
# Map builder: save Folium HTML + inject click->postMessage
# Folium needs JS/CSS resources to render Leaflet [1](https://blog.afi.io/blog/osrm-route-api-free-directions-api-with-turn-by-turn-directions-and-polylines/)[2](https://stackoverflow.com/questions/79494994/installation-from-a-local-package-by-pip-is-not-possible-on-a-kaggle-notebook-in)
# ----------------------------
def build_map_file(coords, labels, route_idx=None, enable_pick=True, zoom=12):
    cleanup_old_maps()
    center = coords[0] if coords else (10.78, 106.67)
    m = folium.Map(location=center, zoom_start=zoom, tiles="OpenStreetMap")

    # markers
    for i, ((lat, lon), lab) in enumerate(zip(coords, labels)):
        folium.Marker(
            [lat, lon],
            tooltip=lab,
            icon=folium.Icon(
                color="green" if i == 0 else "blue",
                icon="home" if i == 0 else "truck",
                prefix="fa"
            )
        ).add_to(m)

    # route polyline (real road)
    if route_idx is not None and len(route_idx) >= 2:
        ordered = [coords[i] for i in route_idx]
        road = osrm_route_geometry(ordered)
        if road is not None:
            folium.PolyLine(road, color="#16a34a", weight=6, opacity=0.9).add_to(m)
        else:
            folium.PolyLine(ordered, color="red", weight=4, opacity=0.85).add_to(m)

    # ✅ enable picking: click on map -> postMessage to parent
    if enable_pick:
        map_var = m.get_name()
        pick_js = f"""
        <script>
        (function() {{
          var map = {map_var};
          if (!map) return;
          map.on('click', function(e) {{
            var msg = {{type:'snart_pick', lat: e.latlng.lat, lon: e.latlng.lng}};
            window.parent.postMessage(msg, '*');
          }});
        }})();
        </script>
        """
        m.get_root().html.add_child(folium.Element(pick_js))

    fpath = os.path.join(MAP_DIR, f"map_{uuid.uuid4().hex}.html")
    m.save(fpath)
    return fpath

def iframe_from_file(fpath, height=560):
    # served via /gradio_api/file=... needs allow_list/allowed_paths [9](https://pypi.org/project/pydantic/)[10](https://www.kaggle.com/code/neha005/ml-model-with-gradio)
    return f"""
    /gradio_api/file={fpath}
    </iframe>
    """

# ----------------------------
# CRUD + pick add
# ----------------------------
def add_stop(state_df, name, address_or_latlon, cargo_type, weight_kg, L_cm, W_cm, H_cm):
    df = normalize_stops(state_df)
    name = (name or "").strip() or f"Stop {len(df)+1}"
    address_or_latlon = (address_or_latlon or "").strip()
    if not address_or_latlon:
        raise gr.Error("Bạn chưa nhập địa chỉ hoặc lat,lon cho điểm giao.")
    new_row = {
        "name": name,
        "address_or_latlon": address_or_latlon,
        "cargo_type": cargo_type,
        "weight_kg": float(weight_kg or 0),
        "L_cm": float(L_cm or 0),
        "W_cm": float(W_cm or 0),
        "H_cm": float(H_cm or 0),
        "H_cm": float(H_cm or 0),
    }
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

def add_stop_from_picked(state_df, picked_latlon, default_name, cargo_type, weight_kg, L_cm, W_cm, H_cm):
    ll = parse_latlon(picked_latlon)
    if ll is None:
        raise gr.Error("Bạn chưa pick điểm trên map (hoặc tọa độ không hợp lệ).")
    lat, lon = ll
    addr = f"{lat:.6f},{lon:.6f}"
    return add_stop(state_df, default_name, addr, cargo_type, weight_kg, L_cm, W_cm, H_cm)

def delete_stop(state_df, row_index):
    df = normalize_stops(state_df)
    idx = int(row_index)
    if idx < 0 or idx >= len(df):
        raise gr.Error(f"Row index không hợp lệ. Hiện có {len(df)} dòng.")
    return df.drop(index=idx).reset_index(drop=True)

def clear_stops():
    return pd.DataFrame(columns=STOP_COLS)

# ----------------------------
# Optimize + Quote + leg table + map output
# ----------------------------
def optimize_and_quote(stops_like, depot_addr, depot_name, base_fee, per_km, per_kg, per_m3):
    df = normalize_stops(stops_like)
    if len(df) < 1:
        raise gr.Error("Cần ít nhất 1 điểm giao hàng.")

    depot_lat, depot_lon, _ = geocode_address(depot_addr)
    depot_latlon = (depot_lat, depot_lon)

    stops_latlon, stop_names, vols = [], [], []
    for _, r in df.iterrows():
        lat, lon, _ = geocode_address(r["address_or_latlon"])
        stops_latlon.append((lat, lon))
        stop_names.append(r["name"])
        vol = (r["L_cm"]/100.0) * (r["W_cm"]/100.0) * (r["H_cm"]/100.0)
        vols.append(float(vol))

    coords_all = [depot_latlon] + stops_latlon
    route_idx = nearest_neighbor_route(coords_all, start=0, return_to_start=True)

    def node_name(i):
        return f"Depot: {depot_name}" if i == 0 else f"Khách: {stop_names[i-1]}"

    stop_rows, leg_rows = [], []
    total_km, total_cost = 0.0, 0.0

    for step, (a, b) in enumerate(zip(route_idx[:-1], route_idx[1:]), start=1):
        km_leg = osrm_leg_distance_km(coords_all[a], coords_all[b])
        total_km += km_leg

        if b != 0:
            r = df.iloc[b-1]
            vol = vols[b-1]
            cost_leg = rule_cost(
                km_leg, float(r["weight_kg"]), float(vol), r["cargo_type"],
                float(base_fee), float(per_km), float(per_kg), float(per_m3)
            )
            total_cost += cost_leg
        else:
            cost_leg = 0.0

        leg_rows.append({
            "Chặng": step,
            "Từ": node_name(a),
            "Đến": node_name(b),
            "Km (đường thực tế)": round(km_leg, 2),
            "Chi phí chặng (VND)": int(round(cost_leg))
        })

        if b != 0:
            stop_rows.append({
                "Điểm giao": df.iloc[b-1]["name"],
                "Km chặng đến điểm": round(km_leg, 2),
                "Khối lượng (kg)": float(df.iloc[b-1]["weight_kg"]),
                "Thể tích (m³)": round(vols[b-1], 4),
                "Loại hàng": df.iloc[b-1]["cargo_type"],
                "Chi phí (VND)": int(round(cost_leg))
            })

        time.sleep(0.03)

    # map for both tabs
    labels = [f"🏠 {depot_name}"] + [f"📍 {n}" for n in stop_names]
    fpath = build_map_file(coords_all, labels, route_idx=route_idx, enable_pick=True, zoom=12)
    iframe_html = iframe_from_file(fpath, height=560)

    route_names = ["🏠 Depot" if i == 0 else stop_names[i-1] for i in route_idx]
    summary = (
        f"### ✅ Kết quả tối ưu\n"
        f"- **Tổng quãng đường (OSRM đường thực tế):** `{total_km:.2f} km`\n"
        f"- **Tổng chi phí (tính cho khách):** `{int(round(total_cost)):,} VND`\n\n"
        f"**Tuyến đi:** " + " → ".join(route_names)
    )

    return pd.DataFrame(stop_rows), pd.DataFrame(leg_rows), iframe_html, iframe_html, summary

# ----------------------------
# JS: capture postMessage from iframe and write into textbox
# Blocks(js=...) runs on load and can add event listeners [3](https://github.com/gradio-app/gradio/issues/2918)[4](https://colab.research.google.com/github/vanderbilt-data-science/ai-summer-gradio/blob/main/gradio-demo.ipynb)
# ----------------------------
JS_ON_LOAD = r"""
() => {
  window.addEventListener("message", (event) => {
    const d = event.data;
    if (!d || d.type !== "snart_pick") return;
    const val = `${Number(d.lat).toFixed(6)},${Number(d.lon).toFixed(6)}`;
    const box = document.querySelector("#picked_latlon textarea, #picked_latlon input");
    if (box) {
      box.value = val;
      box.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });
}
"""

# =========================
# UI
# =========================
with gr.Blocks(css=APP_CSS, js=JS_ON_LOAD, title="Snart Logistics 🐍") as demo:
    gr.HTML("""
    <div id="snart_header">
      🐍 <span style="font-size:20px;">Snart Logistics</span>
      <div id="snart_sub">Map hiển thị 2 tab + pick điểm trên map + OSRM đường thực tế</div>
    </div>
    """)

    with gr.Tabs():
        with gr.Tab("🧾 Nhập liệu"):
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["snart_card"]):
                        gr.HTML("<div class='snart_badge'>DEPOT</div>")
                        depot_name = gr.Textbox(label="Tên kho", value="Kho Snart")
                        depot_addr = gr.Textbox(label="Địa chỉ hoặc lat,lon", value="10.7769,106.7009")

                    with gr.Group(elem_classes=["snart_card"]):
                        gr.HTML("<div class='snart_badge'>PICK TRÊN MAP</div>")
                        picked_latlon = gr.Textbox(
                            label="Điểm vừa pick (auto-fill khi click map)",
                            value="",
                            elem_id="picked_latlon"
                        )
                        gr.Markdown("<div class='small_note'>Click lên map để pick. Sau đó bấm 'Thêm điểm từ map'.</div>")

                    with gr.Group(elem_classes=["snart_card"]):
                        gr.HTML("<div class='snart_badge'>THÊM ĐIỂM</div>")
                        stop_name = gr.Textbox(label="Tên điểm", placeholder="VD: Khách A")
                        stop_addr = gr.Textbox(label="Địa chỉ hoặc lat,lon", placeholder="VD: 10.8188,106.6518 hoặc 'Sân bay TSN'")
                        cargo_type = gr.Dropdown(choices=list(CARGO_MULTIPLIER.keys()), value="Hàng thường", label="Loại hàng")
                        with gr.Row():
                            weight_kg = gr.Number(label="Kg", value=5)
                            L_cm = gr.Number(label="D(cm)", value=30)
                            W_cm = gr.Number(label="R(cm)", value=20)
                            H_cm = gr.Number(label="C(cm)", value=15)
                        add_btn = gr.Button("➕ Thêm điểm (từ ô địa chỉ)", variant="primary")
                        add_pick_btn = gr.Button("📍 Thêm điểm từ map (picked)", variant="secondary")

                with gr.Column(scale=1.2):
                    with gr.Group(elem_classes=["snart_card"]):
                        gr.HTML("<div class='snart_badge'>DANH SÁCH</div>")
                        stops_table = gr.Dataframe(
                            headers=STOP_COLS,
                            value=pd.DataFrame([
                                ["Khách A", "10.8188,106.6518", "Dễ vỡ", 5, 30, 20, 15],
                                ["Khách B", "10.8142,106.7217", "Hàng thường", 8, 40, 30, 25],
                            ], columns=STOP_COLS),
                            interactive=True,
                            wrap=True
                        )
                        with gr.Row():
                            del_index = gr.Number(label="Xoá dòng (index)", value=0)
                            del_btn = gr.Button("🗑️ Xoá dòng")
                            clear_btn = gr.Button("🧹 Xoá tất cả")

                    with gr.Group(elem_classes=["snart_card"]):
                        gr.HTML("<div class='snart_badge'>MAP (NHẬP LIỆU)</div>")
                        # Map appears here too
                        map_input = iFrame(label="Map", value="")

                    with gr.Group(elem_classes=["snart_card"]):
                        gr.HTML("<div class='snart_badge'>GIÁ</div>")
                        base_fee = gr.Number(label="Phí mở đơn", value=15000)
                        per_km = gr.Number(label="VND / km", value=12000)
                        per_kg = gr.Number(label="VND / kg", value=800)
                        per_m3 = gr.Number(label="VND / m³", value=25000)
                        run_btn = gr.Button("🚚 Tối ưu & Báo giá", variant="primary")

        with gr.Tab("📍 Kết quả"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Bảng chi phí theo điểm giao")
                    out_table = gr.Dataframe(wrap=True)
                    gr.Markdown("### Bảng chặng A→B (km thực tế + chi phí)")
                    out_legs = gr.Dataframe(wrap=True)
                    out_summary = gr.Markdown()
                with gr.Column(scale=1.2):
                    gr.Markdown("### Map (Kết quả)")
                    map_result = iFrame(label="Map", value="")

    # events
    add_btn.click(add_stop,
                 inputs=[stops_table, stop_name, stop_addr, cargo_type, weight_kg, L_cm, W_cm, H_cm],
                 outputs=[stops_table])

    add_pick_btn.click(add_stop_from_picked,
                      inputs=[stops_table, picked_latlon, stop_name, cargo_type, weight_kg, L_cm, W_cm, H_cm],
                      outputs=[stops_table])

    del_btn.click(delete_stop, inputs=[stops_table, del_index], outputs=[stops_table])
    clear_btn.click(clear_stops, inputs=[], outputs=[stops_table])

    run_btn.click(optimize_and_quote,
                 inputs=[stops_table, depot_addr, depot_name, base_fee, per_km, per_kg, per_m3],
                 outputs=[out_table, out_legs, map_input, map_result, out_summary])

# allow-list map dir for /gradio_api/file=... [9](https://pypi.org/project/pydantic/)[10](https://www.kaggle.com/code/neha005/ml-model-with-gradio)
launch_kwargs = dict(share=True)
sig = inspect.signature(demo.launch)
if "allowed_paths" in sig.parameters:
    launch_kwargs["allowed_paths"] = [MAP_DIR]
elif "allow_list" in sig.parameters:
    launch_kwargs["allow_list"] = [MAP_DIR]

demo.launch(**launch_kwargs)