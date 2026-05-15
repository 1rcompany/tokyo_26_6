from __future__ import annotations

from datetime import date, timedelta
from html import escape
from urllib.parse import quote_plus

import streamlit as st
import streamlit.components.v1 as components


TRANSPORT_OPTIONS = ["步行", "地鐵/JR", "巴士", "計程車", "租車", "新幹線", "飛機"]


DEFAULT_START_DATE = date(2026, 6, 13)
DEFAULT_END_DATE = date(2026, 6, 18)
DEFAULT_DAEGU_LAYOVER_TIME = "05:25 - 10:40（5 小時 15 分）"
DEFAULT_DAEGU_STARBUCKS = "Starbucks Daegu Jongro Gotaek（韓屋星巴克）"
DEFAULT_DAEGU_STARBUCKS_MAP = "https://www.google.com/maps/search/?api=1&query=Starbucks%20Daegu%20Jongro%20Gotaek"
DEFAULT_DAEGU_GUKBAP = "小頭火 豬肉湯飯"
DEFAULT_DAEGU_GUKBAP_MAP = "https://www.google.com/maps/search/?api=1&query=%E5%B0%8F%E9%A0%AD%E7%81%AB%20%E8%B1%AC%E8%82%89%E6%B9%AF%E9%A3%AF%20%E5%A4%A7%E9%82%B1"
DEFAULT_DAEGU_LAYOVER_NOTE = "星巴克 08:00 開門；若要出機場，09:00 左右開始回大邱機場。"


def trip_dates(start: date, end: date) -> list[date]:
    days = max((end - start).days + 1, 1)
    return [start + timedelta(days=i) for i in range(days)]


def default_area(day_index: int) -> str:
    return {
        1: "台北 / 大邱 / 東京",
        2: "東京商店街 / 河口湖",
        3: "河口湖 / 富士急樂園 / 御殿場 / 北池袋",
        4: "澀谷 / 原宿 / 新宿",
        5: "築地 / 銀座 / 淺草",
        6: "成田",
    }.get(day_index, "")


def default_morning(day_index: int) -> str:
    return {
        1: "02:00 從台北出發\n05:25 抵達大邱\n08:00 Starbucks Daegu Jongro Gotaek（韓屋星巴克）\n附近湯飯",
        2: "先搭高速巴士到東京\n到商店街逛街、吃東西",
        3: "一早看日出\n前往富士急樂園",
        4: "明治神宮 / 原宿 / 表參道",
        5: "築地場外市場 / 銀座",
        6: "前往成田機場，準備回程",
    }.get(day_index, "")


def default_lunch(day_index: int) -> str:
    return {
        1: "抵達東京後簡單午餐",
        2: "商店街附近",
        3: "富士急樂園內或附近快速吃",
        4: "澀谷 / 表參道附近",
        5: "築地 / 銀座附近",
        6: "機場內用餐或帶上飛機",
    }.get(day_index, "")


def default_afternoon(day_index: int) -> str:
    return {
        1: "10:40 從大邱出發\n12:45 抵達東京\n前往 9stay 威前放行李",
        2: "從東京前往河口湖\n入住 megu fuji 2021",
        3: "中午/下午前往御殿場 Outlet\n逛到越晚越好",
        4: "澀谷 Sky / 澀谷 Scramble / 逛街",
        5: "淺草寺 / 雷門 / 晴空塔周邊",
        6: "12:30 從成田機場起飛\n15:10 抵達台北",
    }.get(day_index, "")


def default_evening(day_index: int) -> str:
    return {
        1: "住宿附近晚餐，早點休息",
        2: "河口湖周邊晚餐，準備隔天早起看日出",
        3: "從御殿場搭高速巴士回東京，再前往北池袋 / 池袋 Bel Avenir",
        4: "新宿晚餐 / 歌舞伎町周邊散步",
        5: "上野 / 秋葉原 / 最後採買",
        6: "返台",
    }.get(day_index, "")


def default_notes(day_index: int) -> str:
    return {
        1: "大邱轉機時間：05:25 到 10:40，共 5 小時 15 分。若要出機場，09:00 左右建議開始回機場。",
        2: "先確認高速巴士班次與商店街停留時間，避免太晚到河口湖。",
        3: "日出、富士急、御殿場、回東京是很滿的一天，高速巴士末班車要先查好。",
        4: "澀谷 Sky 若要去，建議先填訂票連結與入場時間",
        5: "最後採買日，行李空間要預留",
        6: "國際線建議提早到機場",
    }.get(day_index, "")


def default_lodging(day_index: int) -> str:
    return {
        1: "9stay 威前",
        2: "megu fuji 2021",
        3: "池袋 Bel Avenir",
        4: "池袋 Bel Avenir",
        5: "池袋 Bel Avenir",
    }.get(day_index, "")


def default_transport(day_index: int) -> list[str]:
    if day_index in (1, 6):
        return ["飛機", "地鐵/JR"]
    return ["地鐵/JR"]


daegu_layover_time = DEFAULT_DAEGU_LAYOVER_TIME
daegu_starbucks = DEFAULT_DAEGU_STARBUCKS
daegu_starbucks_map = DEFAULT_DAEGU_STARBUCKS_MAP
daegu_gukbap = DEFAULT_DAEGU_GUKBAP
daegu_gukbap_map = DEFAULT_DAEGU_GUKBAP_MAP
daegu_layover_note = DEFAULT_DAEGU_LAYOVER_NOTE


def lodging_summary(lodging: dict) -> str:
    parts = [lodging["dates"], lodging["name"]]
    if lodging["nearest_station"]:
        parts.append(f"最近車站：{lodging['nearest_station']}")
    if lodging["map_link"]:
        parts.append(f"地圖：{lodging['map_link']}")
    return "｜".join(parts)


def map_embed_url(query: str) -> str:
    return f"https://www.google.com/maps?q={quote_plus(query)}&output=embed"


def map_search_url(query: str) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"


def html_lines(text: str) -> str:
    escaped = escape(text or "未填")
    return escaped.replace("\n", "<br>")


def build_printout(profile: dict, daily_plans: list[dict]) -> str:
    flights = profile["flights"]
    flight_rows = [
        ("去程 1", flights["outbound_leg_1"]),
        ("去程 2", flights["outbound_leg_2"]),
        ("回程", flights["return"]),
    ]
    flight_html = "".join(
        f"""
        <tr>
          <td>{escape(label)}</td>
          <td>{escape(flight["flight_number"] or "未填")}</td>
          <td>{escape(flight["departure_airport"])}<br>{escape(flight["departure_terminal"])}</td>
          <td>{escape(flight["arrival_airport"])}<br>{escape(flight["arrival_terminal"])}</td>
          <td>{escape(flight["departure_time"])}</td>
          <td>{escape(flight["arrival_time"])}</td>
        </tr>
        """
        for label, flight in flight_rows
    )
    lodging_html = "".join(
        f"""
        <section class="card">
          <h3>{escape(lodging["dates"])}｜{escape(lodging["name"])}</h3>
          <p><b>地址</b>：{html_lines(lodging["address"])}</p>
          <p><b>最近車站</b>：{escape(lodging["nearest_station"] or "未填")}</p>
          <p><b>入住/退房</b>：{escape(lodging["checkin"] or "未填")} / {escape(lodging["checkout"] or "未填")}</p>
        </section>
        """
        for lodging in profile["lodgings"]
    )
    days_html = "".join(
        f"""
        <section class="day">
          <h3>Day {plan["day"]}｜{escape(plan["date"])}｜{escape(plan["area"] or "未指定區域")}</h3>
          <div class="grid">
            <p><b>上午</b><br>{html_lines(plan["morning"])}</p>
            <p><b>午餐</b><br>{html_lines(plan["lunch"])}</p>
            <p><b>下午</b><br>{html_lines(plan["afternoon"])}</p>
            <p><b>晚上</b><br>{html_lines(plan["evening"])}</p>
          </div>
          <p><b>住宿</b>：{html_lines(plan["lodging"])}</p>
          <p><b>交通</b>：{escape(", ".join(plan["transport"]) if plan["transport"] else "未填")}</p>
          <p><b>提醒</b>：{html_lines(plan["notes"])}</p>
        </section>
        """
        for plan in daily_plans
    )
    layover = flights["daegu_layover"]
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <title>6/13~18 東京行</title>
  <style>
    @page {{ margin: 14mm; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", "Segoe UI", sans-serif; color: #1f2937; background: #f5f3ef; }}
    main {{ max-width: 980px; margin: 0 auto; background: #fff; padding: 28px; border-radius: 12px; }}
    h1 {{ margin: 0 0 6px; font-size: 30px; }}
    h2 {{ margin-top: 28px; padding-bottom: 8px; border-bottom: 2px solid #2f6f8f; }}
    h3 {{ margin: 0 0 10px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
    th, td {{ border: 1px solid #d7dde3; padding: 9px; text-align: left; vertical-align: top; }}
    th {{ background: #eef5f8; }}
    .card, .day {{ border: 1px solid #d7dde3; border-radius: 10px; padding: 14px; margin: 12px 0; background: #fbfcfd; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .meta {{ color: #5b6775; margin: 0 0 18px; }}
    .producer {{ font-weight: 700; color: #374151; margin: 0 0 18px; }}
    @media print {{ body {{ background: white; }} main {{ padding: 0; }} .day {{ break-inside: avoid; }} }}
  </style>
</head>
<body>
<main>
  <h1>6/13~18 東京行</h1>
  <p class="producer">Producer: Anson (An-Heng) Chen</p>
  <p class="meta">{escape(profile["start_date"])} - {escape(profile["end_date"])}</p>
  <h2>航班</h2>
  <table>
    <thead><tr><th>段落</th><th>航班</th><th>出發</th><th>抵達</th><th>出發時間</th><th>抵達時間</th></tr></thead>
    <tbody>{flight_html}</tbody>
  </table>
  <section class="card">
    <h3>大邱轉機</h3>
    <p><b>時間</b>：{escape(layover["time"])}</p>
    <p><b>星巴克</b>：{escape(layover["starbucks"])}</p>
    <p><b>湯飯</b>：{escape(layover["gukbap"])}</p>
    <p><b>備註</b>：{html_lines(layover["notes"])}</p>
  </section>
  <h2>住宿</h2>
  {lodging_html}
  <h2>每日行程</h2>
  {days_html}
</main>
</body>
</html>"""


st.set_page_config(
    page_title="東京行規劃",
    page_icon="🗾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      header[data-testid="stHeader"] {
        display: none;
      }
      div[data-testid="stDecoration"] {
        display: none;
      }
      .stApp {
        background:
          linear-gradient(180deg, rgba(20, 31, 45, 0.18), rgba(246, 248, 250, 0.90) 34%, rgba(246, 248, 250, 0.96)),
          url("https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=2200&q=85");
        background-size: cover;
        background-position: center 24%;
        background-attachment: fixed;
      }
      .main .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.5rem;
        max-width: 1180px;
      }
      [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(126, 92, 63, 0.16);
        border-radius: 8px;
        padding: 0.8rem 1rem;
      }
      [data-testid="stMetricValue"] { font-size: 1.35rem; }
      [data-testid="stTabs"] [role="tablist"] {
        gap: 0.25rem;
        border-bottom: 1px solid rgba(67, 83, 104, 0.18);
      }
      [data-testid="stTabs"] [role="tab"] {
        background: rgba(255, 255, 255, 0.58);
        border: 1px solid rgba(67, 83, 104, 0.12);
        border-bottom: 0;
        border-radius: 8px 8px 0 0;
        padding: 0.55rem 0.9rem;
      }
      [data-testid="stTabs"] [aria-selected="true"] {
        background: #ffffff;
        color: #8f4f32;
      }
      div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.72);
        border-radius: 8px;
      }
      label, .stMarkdown strong {
        color: #293241;
      }
      h1, h2, h3 {
        color: #25364a;
      }
      .trip-title {
        padding: 4.4rem 0 1rem 0;
        margin-bottom: 0.8rem;
      }
      .producer {
        color: rgba(31, 41, 55, 0.78);
        font-weight: 700;
        margin-top: -0.6rem;
        margin-bottom: 1rem;
      }
      .soft-note {
        color: rgba(49, 51, 63, 0.72);
        font-size: 0.96rem;
      }
      .day-card {
        border: 1px solid rgba(67, 83, 104, 0.14);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.86);
        box-shadow: 0 8px 22px rgba(72, 69, 64, 0.06);
      }
      .overview-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 0.7rem 0 1.1rem 0;
      }
      .overview-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(67, 83, 104, 0.14);
        border-radius: 8px;
        padding: 0.95rem;
        box-shadow: 0 10px 28px rgba(20, 31, 45, 0.08);
      }
      .overview-card h4 {
        margin: 0 0 0.45rem 0;
        color: #223047;
        font-size: 1rem;
      }
      .overview-card p {
        margin: 0.2rem 0;
        color: #344256;
        line-height: 1.45;
      }
      .timeline-card {
        background: rgba(255, 255, 255, 0.9);
        border-left: 5px solid #2f6f8f;
        border-radius: 8px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 10px 26px rgba(20, 31, 45, 0.08);
      }
      .timeline-card h4 {
        margin: 0 0 0.5rem 0;
        color: #1f3046;
      }
      .timeline-card .line {
        margin: 0.22rem 0;
        color: #334155;
      }
      .stTextInput input, .stTextArea textarea, .stMultiSelect [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-color: rgba(67, 83, 104, 0.16);
      }
      .stExpander {
        border-color: rgba(67, 83, 104, 0.14);
        background: rgba(255, 255, 255, 0.76);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="trip-title"><h1>6/13~18 東京行</h1></div>'
    '<div class="producer">Producer: Anson (An-Heng) Chen</div>',
    unsafe_allow_html=True,
)

profile_tab, wishlist_tab, itinerary_tab, map_tab, overview_tab = st.tabs(
    ["基本資料", "靈感菇", "每日行程", "Google Map", "總覽"]
)

with profile_tab:
    st.subheader("旅行基本資料")

    with st.expander("旅行日期", expanded=True):
        date_col1, date_col2, date_col3 = st.columns(3)
        with date_col1:
            start_date = st.date_input("出發日期", DEFAULT_START_DATE)
        with date_col2:
            end_date = st.date_input("回程日期", DEFAULT_END_DATE)

        if end_date < start_date:
            st.warning("回程日期早於出發日期，我先用出發當天當作最後一天。")
            end_date = start_date

        dates = trip_dates(start_date, end_date)
        trip_days = len(dates)
        with date_col3:
            st.metric("天數", f"{trip_days} 天")

with profile_tab:
    with st.expander("航班資訊", expanded=False):
        st.markdown("**航班摘要**")
        st.markdown(
            f"""
            <div class="overview-grid">
              <div class="overview-card"><h4>去程 1</h4><p>TW664<br>台北 02:00 → 大邱 05:25</p></div>
              <div class="overview-card"><h4>轉機</h4><p>大邱 5 小時 15 分<br>05:25 抵達 / 10:40 出發</p></div>
              <div class="overview-card"><h4>去程 2 / 回程</h4><p>TW251 大邱 10:40 → 成田 12:45<br>IT201 成田 12:30 → 台北 15:10</p></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st.expander("航班詳細資料", expanded=False):
        st.markdown("**去程第一段：台北 - 大邱**")
        leg1_col1, leg1_col2, leg1_col3 = st.columns(3)
        with leg1_col1:
            leg1_flight_number = st.text_input("航班號", "TW664", key="leg1_flight_number")
            leg1_departure_airport = st.text_input("出發機場", "台北", key="leg1_departure_airport")
            leg1_departure_terminal = st.text_input("出發航廈", "桃園 T1", key="leg1_departure_terminal")
        with leg1_col2:
            leg1_arrival_airport = st.text_input("抵達機場", "大邱", key="leg1_arrival_airport")
            leg1_arrival_terminal = st.text_input("抵達航廈", "大邱國際航廈", key="leg1_arrival_terminal")
            leg1_departure_time = st.text_input("出發時間", "2026 年 6 月 13 日 02:00", key="leg1_departure_time")
        with leg1_col3:
            leg1_arrival_time = st.text_input("抵達時間", "2026 年 6 月 13 日 05:25", key="leg1_arrival_time")
            leg1_notes = st.text_area("備註", key="leg1_notes", height=90)

        st.markdown("**去程第二段：大邱 - 東京**")
        leg2_col1, leg2_col2, leg2_col3 = st.columns(3)
        with leg2_col1:
            leg2_flight_number = st.text_input("航班號", "TW251", key="leg2_flight_number")
            leg2_departure_airport = st.text_input("出發機場", "大邱", key="leg2_departure_airport")
            leg2_departure_terminal = st.text_input("出發航廈", "大邱國際航廈", key="leg2_departure_terminal")
        with leg2_col2:
            leg2_arrival_airport = st.text_input("抵達機場", "東京成田", key="leg2_arrival_airport")
            leg2_arrival_terminal = st.text_input("抵達航廈", "成田 T2", key="leg2_arrival_terminal")
            leg2_departure_time = st.text_input("出發時間", "2026 年 6 月 13 日 10:40", key="leg2_departure_time")
        with leg2_col3:
            leg2_arrival_time = st.text_input("抵達時間", "2026 年 6 月 13 日 12:45", key="leg2_arrival_time")
            leg2_notes = st.text_area("備註", key="leg2_notes", height=90)

        st.markdown("**回程：東京 - 台北**")
        return_col1, return_col2, return_col3 = st.columns(3)
        with return_col1:
            return_flight_number = st.text_input("航班號", "IT201", key="return_flight_number")
            return_departure_airport = st.text_input("出發機場", "東京成田", key="return_departure_airport")
            return_departure_terminal = st.text_input("出發航廈", "成田 T2", key="return_departure_terminal")
        with return_col2:
            return_arrival_airport = st.text_input("抵達機場", "台北", key="return_arrival_airport")
            return_arrival_terminal = st.text_input("抵達航廈", "桃園 T1", key="return_arrival_terminal")
            return_departure_time = st.text_input("出發時間", "2026 年 6 月 18 日 12:30", key="return_departure_time")
        with return_col3:
            return_arrival_time = st.text_input("抵達時間", "2026 年 6 月 18 日 15:10", key="return_arrival_time")
            return_notes = st.text_area("備註", key="return_notes", height=90)

with profile_tab:
    st.subheader("住宿資訊")
    st.markdown(
        """
        <div class="overview-grid">
          <div class="overview-card"><h4>6/13</h4><p>9STAY 蔵前<br>蔵前 / 新御徒町</p></div>
          <div class="overview-card"><h4>6/14</h4><p>MEGU FUJI 2021<br>富士山站</p></div>
          <div class="overview-card"><h4>6/15 - 6/17</h4><p>池袋 Bel Avenir<br>北池袋</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("住宿詳細資料", expanded=False):
        st.markdown("**Day 1：9stay 威前**")
        stay1_col1, stay1_col2, stay1_col3 = st.columns(3)
        with stay1_col1:
            stay1_dates = st.text_input("住宿日期", "6/13 晚上", key="stay1_dates")
            stay1_name = st.text_input("住宿名稱", "9STAY 蔵前", key="stay1_name")
            stay1_booking_link = st.text_input("訂房連結", "https://www.klook.com/zh-TW/hotels/detail/1534072-9stay/", key="stay1_booking_link")
        with stay1_col2:
            stay1_map_link = st.text_input("地圖連結", "https://www.google.com/maps/search/?api=1&query=9STAY%20Kuramae%202-6-6%20Misuji%20Tokyo", key="stay1_map_link")
            stay1_address = st.text_area("地址", "東京都台東区三筋 2-6-6 / 2-6-6 Misuji, Taito-ku, Tokyo 111-0055", key="stay1_address", height=80)
            stay1_nearest_station = st.text_input("最近車站", "新御徒町站約400m、蔵前站（淺草線）", key="stay1_nearest_station")
        with stay1_col3:
            stay1_checkin = st.text_input("入住時間", "16:00 後", key="stay1_checkin")
            stay1_checkout = st.text_input("退房時間", "10:00 前", key="stay1_checkout")

        st.markdown("**Day 2：megu fuji 2021**")
        stay2_col1, stay2_col2, stay2_col3 = st.columns(3)
        with stay2_col1:
            stay2_dates = st.text_input("住宿日期", "6/14 晚上", key="stay2_dates")
            stay2_name = st.text_input("住宿名稱", "megu fuji 2021", key="stay2_name")
            stay2_booking_link = st.text_input("訂房連結", "https://megufuji.com/", key="stay2_booking_link")
        with stay2_col2:
            stay2_map_link = st.text_input("地圖連結", "https://www.google.com/maps/search/?api=1&query=Megu%20Fuji%202021%202-7-13%20Kamiyoshida%20Fujiyoshida", key="stay2_map_link")
            stay2_address = st.text_area("地址", "山梨県富士吉田市上吉田 2-7-13 / 2-7-13 Kamiyoshida, Fujiyoshida, Yamanashi 403-0005", key="stay2_address", height=80)
            stay2_nearest_station = st.text_input("最近車站", "富士山站，步行約1分鐘", key="stay2_nearest_station")
        with stay2_col3:
            stay2_checkin = st.text_input("入住時間", "15:00 - 20:00", key="stay2_checkin")
            stay2_checkout = st.text_input("退房時間", "10:00 前", key="stay2_checkout")

        st.markdown("**Day 3-5：池袋 Bel Avenir**")
        stay3_col1, stay3_col2, stay3_col3 = st.columns(3)
        with stay3_col1:
            stay3_dates = st.text_input("住宿日期", "6/15 - 6/17 晚上", key="stay3_dates")
            stay3_name = st.text_input("住宿名稱", "池袋 Bel Avenir", key="stay3_name")
            stay3_booking_link = st.text_input("訂房連結", "https://www.trip.com/hotels/tokyo-hotel-detail-127834273/bel-avenir/", key="stay3_booking_link")
        with stay3_col2:
            stay3_map_link = st.text_input("地圖連結", "https://www.google.com/maps/search/?api=1&query=Bel%20Avenir%203-46-12%20Kamiikebukuro%20Toshima%20Tokyo", key="stay3_map_link")
            stay3_address = st.text_area("地址", "東京都豊島区上池袋 3-46-12 / 3-46-12 Kamiikebukuro, Toshima-ku, Tokyo 170-0012", key="stay3_address", height=80)
            stay3_nearest_station = st.text_input("最近車站", "北池袋站步行約5分鐘、板橋站步行約11分鐘", key="stay3_nearest_station")
        with stay3_col3:
            stay3_checkin = st.text_input("入住時間", "16:00 - 22:00", key="stay3_checkin")
            stay3_checkout = st.text_input("退房時間", "10:00 前", key="stay3_checkout")

        st.subheader("地圖")
        map_targets = {
            "9STAY 蔵前": map_embed_url("9STAY Kuramae 2-6-6 Misuji Tokyo"),
            "MEGU FUJI 2021": map_embed_url("Megu Fuji 2021 2-7-13 Kamiyoshida Fujiyoshida"),
            "池袋 Bel Avenir": map_embed_url("Bel Avenir 3-46-12 Kamiikebukuro Toshima Tokyo"),
            "御殿場 Outlet": map_embed_url("Gotemba Premium Outlets"),
            "富士急樂園": map_embed_url("Fuji-Q Highland"),
        }
        selected_map = st.selectbox("地圖目標", list(map_targets.keys()))
        components.iframe(map_targets[selected_map], height=430)

with wishlist_tab:
    st.subheader("靈感菇")
    wishlist_text = st.text_area(
        "想放進旅程的景點、店家、購物點",
        height=260,
    )
    must_buy = st.text_input("必買/代購")

with itinerary_tab:
    st.subheader("每日行程")
    daily_plans: list[dict] = []

    for day_index, current_date in enumerate(dates, start=1):
        with st.expander(f"Day {day_index}｜{current_date.strftime('%Y-%m-%d')}", expanded=day_index <= 2):
            col1, col2, col3, col4 = st.columns([1.1, 1.1, 1, 1])
            with col1:
                area = st.text_input(
                    "今天主要區域",
                    key=f"area_{day_index}",
                    value=default_area(day_index),
                )
                morning = st.text_area("上午", key=f"morning_{day_index}", value=default_morning(day_index), height=90)
            with col2:
                lunch = st.text_input("午餐候選", key=f"lunch_{day_index}")
                afternoon = st.text_area("下午", key=f"afternoon_{day_index}", value=default_afternoon(day_index), height=90)
            with col3:
                transport = st.multiselect(
                    "主要交通",
                    TRANSPORT_OPTIONS,
                    default=default_transport(day_index),
                    key=f"transport_{day_index}",
                )
            with col4:
                lodging = st.text_area("居住資訊", key=f"lodging_{day_index}", value=default_lodging(day_index), height=90)

            if day_index == 1:
                st.markdown("**大邱轉機小行程**")
                layover_col1, layover_col2 = st.columns(2)
                with layover_col1:
                    daegu_layover_time = st.text_input(
                        "轉機時間",
                        DEFAULT_DAEGU_LAYOVER_TIME,
                        key="daegu_layover_time",
                    )
                    daegu_starbucks = st.text_input(
                        "星巴克",
                        DEFAULT_DAEGU_STARBUCKS,
                        key="daegu_starbucks",
                    )
                    daegu_starbucks_map = st.text_input(
                        "星巴克地圖連結",
                        DEFAULT_DAEGU_STARBUCKS_MAP,
                        key="daegu_starbucks_map",
                    )
                with layover_col2:
                    daegu_gukbap = st.text_input(
                        "湯飯",
                        DEFAULT_DAEGU_GUKBAP,
                        key="daegu_gukbap",
                    )
                    daegu_gukbap_map = st.text_input(
                        "湯飯地圖連結",
                        DEFAULT_DAEGU_GUKBAP_MAP,
                        key="daegu_gukbap_map",
                    )
                    daegu_layover_note = st.text_area(
                        "轉機備註",
                        DEFAULT_DAEGU_LAYOVER_NOTE,
                        key="daegu_layover_note",
                        height=80,
                    )

            evening = st.text_area("晚上", key=f"evening_{day_index}", value=default_evening(day_index), height=80)
            notes = st.text_area("提醒事項", key=f"notes_{day_index}", height=70)

            daily_plans.append(
                {
                    "day": day_index,
                    "date": current_date.isoformat(),
                    "area": area,
                    "morning": morning,
                    "lunch": lunch,
                    "afternoon": afternoon,
                    "evening": evening,
                    "lodging": lodging,
                    "transport": transport,
                    "notes": notes,
                }
            )

lodgings = [
    {
        "dates": stay1_dates,
        "name": stay1_name,
        "booking_link": stay1_booking_link,
        "map_link": stay1_map_link,
        "address": stay1_address,
        "nearest_station": stay1_nearest_station,
        "checkin": stay1_checkin,
        "checkout": stay1_checkout,
    },
    {
        "dates": stay2_dates,
        "name": stay2_name,
        "booking_link": stay2_booking_link,
        "map_link": stay2_map_link,
        "address": stay2_address,
        "nearest_station": stay2_nearest_station,
        "checkin": stay2_checkin,
        "checkout": stay2_checkout,
    },
    {
        "dates": stay3_dates,
        "name": stay3_name,
        "booking_link": stay3_booking_link,
        "map_link": stay3_map_link,
        "address": stay3_address,
        "nearest_station": stay3_nearest_station,
        "checkin": stay3_checkin,
        "checkout": stay3_checkout,
    },
]

map_places = {
    "住宿｜9STAY 蔵前": "9STAY Kuramae 2-6-6 Misuji Tokyo",
    "住宿｜MEGU FUJI 2021": "Megu Fuji 2021 2-7-13 Kamiyoshida Fujiyoshida",
    "住宿｜池袋 Bel Avenir": "Bel Avenir 3-46-12 Kamiikebukuro Toshima Tokyo",
    "機場｜桃園機場 T1": "Taiwan Taoyuan International Airport Terminal 1",
    "機場｜大邱國際機場": "Daegu International Airport",
    "機場｜成田機場 T2": "Narita International Airport Terminal 2",
    "大邱｜韓屋星巴克": "Starbucks Daegu Jongro Gotaek",
    "大邱｜小頭火 豬肉湯飯": "小頭火 豬肉湯飯 大邱",
    "東京｜築地場外市場": "Tsukiji Outer Market Tokyo",
    "東京｜銀座": "Ginza Tokyo",
    "東京｜淺草寺 / 雷門": "Sensoji Kaminarimon Tokyo",
    "東京｜晴空塔": "Tokyo Skytree",
    "東京｜澀谷 Sky": "Shibuya Sky Tokyo",
    "東京｜明治神宮": "Meiji Jingu Tokyo",
    "東京｜新宿": "Shinjuku Tokyo",
    "富士｜富士急樂園": "Fuji-Q Highland",
    "富士｜河口湖": "Lake Kawaguchiko",
    "購物｜御殿場 Outlet": "Gotemba Premium Outlets",
}

profile = {
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "lodgings": lodgings,
    "flights": {
        "outbound_leg_1": {
            "flight_number": leg1_flight_number,
            "departure_airport": leg1_departure_airport,
            "departure_terminal": leg1_departure_terminal,
            "arrival_airport": leg1_arrival_airport,
            "arrival_terminal": leg1_arrival_terminal,
            "departure_time": leg1_departure_time,
            "arrival_time": leg1_arrival_time,
            "notes": leg1_notes,
        },
        "outbound_leg_2": {
            "flight_number": leg2_flight_number,
            "departure_airport": leg2_departure_airport,
            "departure_terminal": leg2_departure_terminal,
            "arrival_airport": leg2_arrival_airport,
            "arrival_terminal": leg2_arrival_terminal,
            "departure_time": leg2_departure_time,
            "arrival_time": leg2_arrival_time,
            "notes": leg2_notes,
        },
        "return": {
            "flight_number": return_flight_number,
            "departure_airport": return_departure_airport,
            "departure_terminal": return_departure_terminal,
            "arrival_airport": return_arrival_airport,
            "arrival_terminal": return_arrival_terminal,
            "departure_time": return_departure_time,
            "arrival_time": return_arrival_time,
            "notes": return_notes,
        },
        "daegu_layover": {
            "time": daegu_layover_time,
            "starbucks": daegu_starbucks,
            "starbucks_map": daegu_starbucks_map,
            "gukbap": daegu_gukbap,
            "gukbap_map": daegu_gukbap_map,
            "notes": daegu_layover_note,
        },
    },
    "wishlist": wishlist_text,
    "must_buy": must_buy,
}

with map_tab:
    st.subheader("Google Map")
    st.markdown(
        """
        <div class="overview-grid">
          <div class="overview-card"><h4>住宿</h4><p>蔵前 / 富士山站 / 北池袋</p></div>
          <div class="overview-card"><h4>交通</h4><p>桃園 / 大邱 / 成田</p></div>
          <div class="overview-card"><h4>景點</h4><p>東京市區 / 河口湖 / 御殿場</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_place = st.selectbox("選擇地點", list(map_places.keys()))
    selected_query = map_places[selected_place]
    components.iframe(map_embed_url(selected_query), height=520)
    st.link_button("在 Google Maps 開啟", map_search_url(selected_query))

    st.markdown("**快速地點清單**")
    place_cols = st.columns(3)
    for index, (label, query) in enumerate(map_places.items()):
        with place_cols[index % 3]:
            st.markdown(f"[{label}]({map_search_url(query)})")

with overview_tab:
    st.subheader("行程總覽")
    st.markdown("**住宿**")
    for lodging in lodgings:
        st.write(lodging_summary(lodging))
    st.markdown("**航班**")
    st.write(
        f"{leg1_departure_airport} - {leg1_arrival_airport}｜"
        f"{leg1_departure_time} 出發｜{leg1_arrival_time} 抵達"
    )
    st.write(
        f"{leg2_departure_airport} - {leg2_arrival_airport}｜"
        f"{leg2_departure_time} 出發｜{leg2_arrival_time} 抵達"
    )
    st.write(
        f"{return_departure_airport} - {return_arrival_airport}｜"
        f"{return_departure_time} 出發｜{return_arrival_time} 抵達"
    )

    filled_days = [
        plan
        for plan in daily_plans
        if any(plan.get(k) for k in ("area", "morning", "lunch", "afternoon", "evening", "lodging", "notes"))
    ]
    if filled_days:
        for plan in filled_days:
            st.markdown(
                f"""
                <div class="day-card">
                  <strong>Day {plan["day"]}｜{plan["date"]}｜{plan["area"] or "未指定區域"}</strong><br>
                  上午：{plan["morning"] or "未填"}<br>
                  午餐：{plan["lunch"] or "未填"}<br>
                  下午：{plan["afternoon"] or "未填"}<br>
                  晚上：{plan["evening"] or "未填"}<br>
                  居住資訊：{plan["lodging"] or "未填"}<br>
                  交通：{", ".join(plan["transport"]) if plan["transport"] else "未填"}
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.download_button(
        "下載列印版 HTML",
        data=build_printout(profile, daily_plans),
        file_name="tokyo-trip-printout.html",
        mime="text/html",
    )
