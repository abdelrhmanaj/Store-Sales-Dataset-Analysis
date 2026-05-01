"""
=============================================================
 Store_Sales_DataSetDB — Bulk Data Generator & Inserter
 Target: SQL Server via pyodbc
 Estimated row counts:
   CUSTOMER         200,000
   STORE              1,000
   PRODUCT              500
   PROMOTION            200
   ORDER          1,000,000
   ORDER_ITEM     2,200,000  (~2.2 items avg per order)
   PRICE_CHANGE      26,000  (~52 weeks x 500 products)
   EXTERNAL_FACTOR   52,000  (~52 weeks x 1,000 stores)
   SESSION          600,000  (~3 per customer)
   CAMPAIGN_TOUCH   800,000  (~4 per customer)
   SUPPORT_TICKET    40,000  (~1 per 5 customers)
=============================================================
 Requirements:
   pip install pyodbc faker tqdm

 Usage:
   1. Edit the CONNECTION_STRING below for your SQL Server
   2. Run:  python generate_and_insert_data.py
=============================================================
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import pyodbc
import random
import uuid
from datetime import date, datetime, timedelta
from faker import Faker
from tqdm import tqdm
import time

# ─── CONNECTION — edit this ───────────────────────────────────────────────────
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-72TNQAR;"          # e.g. localhost\\SQLEXPRESS or 192.168.1.10
    "DATABASE=Store_Sales_DataSetDB;"
    "Trusted_Connection=yes;"
         # your password
    # For Windows Authentication instead, replace UID/PWD with:
    # "Trusted_Connection=yes;"
)

BATCH_SIZE = 5_000          # rows per executemany call
SEED       = 42             # reproducible data

# ─── ROW COUNTS ──────────────────────────────────────────────────────────────
N_CUSTOMERS        = 200_000
N_STORES           = 1_000
N_PRODUCTS         = 500
N_PROMOTIONS       = 200
N_ORDERS           = 1_000_000
N_SESSIONS         = 600_000
N_CAMPAIGN_TOUCHES = 800_000
N_SUPPORT_TICKETS  = 40_000

random.seed(SEED)
fake = Faker("en_IN")       # Indian locale — matches the dataset
Faker.seed(SEED)

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def rand_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def rand_datetime(start: date, end: date) -> datetime:
    d = rand_date(start, end)
    return datetime(d.year, d.month, d.day,
                    random.randint(6, 23), random.randint(0, 59), random.randint(0, 59))

def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def bulk_insert(cursor, sql: str, rows: list, desc: str):
    total = len(rows)
    with tqdm(total=total, desc=desc, unit="rows", unit_scale=True) as bar:
        for batch in chunked(rows, BATCH_SIZE):
            cursor.executemany(sql, batch)
            cursor.connection.commit()
            bar.update(len(batch))

# ─── REFERENCE DATA (matches SKILL.md / CSV samples) ─────────────────────────

CATEGORIES = [
    ("CAT001","Beverages (Coffee/Malt)"),("CAT002","Dairy & Nutrition"),
    ("CAT003","Infant Nutrition"),       ("CAT004","Confectionery"),
    ("CAT005","Culinary (Soups/Seasonings)"),("CAT006","Breakfast Cereals"),
    ("CAT007","Petcare"),                ("CAT008","Bottled Water"),
    ("CAT009","Health Science & Nutrition Add-ons"),("CAT010","Others"),
]

CHANNELS = [
    ("CH001","Online"),("CH002","Mobile App"),
    ("CH003","Modern Trade"),("CH004","General Trade"),
]

MARKETING_CHANNELS = [
    ("MKT001","Email","Owned","Low"),("MKT002","SMS","Owned","Low"),
    ("MKT003","Push","Owned","Low"),("MKT004","WhatsApp","Owned","Low"),
    ("MKT005","Search Ads","Paid","High"),("MKT006","Social Ads","Paid","High"),
    ("MKT007","Display Ads","Paid","Medium"),("MKT008","Affiliate","Paid","Medium"),
    ("MKT009","Influencer","Paid","High"),("MKT010","Marketplace Banner","Paid","Medium"),
    ("MKT011","TV Campaign","Offline","Very High"),
    ("MKT012","In-Store Promotion","Offline","Medium"),
]

STORE_TYPES  = ["General Trade","Supermarket","Hypermarket","Modern Trade","Convenience"]
SEGMENTS     = ["Value","Mainstream","Premium"]
STATUSES     = ["active","active","active","churned"]           # 75% active
PAYMENT_TYPES= ["Credit Card","Debit Card","UPI","Cash on Delivery","Wallet"]
ISSUE_TYPES  = ["Delivery Delay","Wrong Item","Damaged Product","Payment Issue","Other"]
TICKET_STATUS= ["Resolved","Resolved","Open","Pending"]         # 50% resolved
DEVICES      = ["Mobile","Desktop","Tablet"]
REFERRERS    = ["Email","Direct","Affiliate","Search","Social","Push"]
BRANDS       = ["NESTLE","NESCAFE","MAGGI","KITKAT","MUNCH","MILKMAID","NESTEA"]
PROMO_TYPES  = ["PCT_OFF","BOGO","FIXED_OFF"]
CAMPAIGNS    = ["Health Bundle Offer","Weekend Deal","Subscribe & Save",
                "Festive Special","Loyalty Reward","New User Offer",
                "Flash Sale","Referral Bonus","Seasonal Deal"]
CHANNELS_MKT = ["Email","SMS","Push","WhatsApp"]

INDIAN_CITIES_STATES = [
    ("Mumbai","Maharashtra"),("Delhi","Delhi"),("Bengaluru","Karnataka"),
    ("Hyderabad","Telangana"),("Ahmedabad","Gujarat"),("Chennai","Tamil Nadu"),
    ("Kolkata","West Bengal"),("Pune","Maharashtra"),("Jaipur","Rajasthan"),
    ("Lucknow","Uttar Pradesh"),("Surat","Gujarat"),("Kanpur","Uttar Pradesh"),
    ("Nagpur","Maharashtra"),("Indore","Madhya Pradesh"),("Thane","Maharashtra"),
    ("Bhopal","Madhya Pradesh"),("Visakhapatnam","Andhra Pradesh"),
    ("Pimpri","Maharashtra"),("Patna","Bihar"),("Vadodara","Gujarat"),
    ("Ghaziabad","Uttar Pradesh"),("Ludhiana","Punjab"),("Agra","Uttar Pradesh"),
    ("Nashik","Maharashtra"),("Faridabad","Haryana"),("Meerut","Uttar Pradesh"),
    ("Rajkot","Gujarat"),("Varanasi","Uttar Pradesh"),("Srinagar","J&K"),
    ("Aurangabad","Maharashtra"),("Dhanbad","Jharkhand"),("Amritsar","Punjab"),
    ("Navi Mumbai","Maharashtra"),("Allahabad","Uttar Pradesh"),
    ("Ranchi","Jharkhand"),("Howrah","West Bengal"),("Coimbatore","Tamil Nadu"),
    ("Jabalpur","Madhya Pradesh"),("Gwalior","Madhya Pradesh"),
    ("Vijayawada","Andhra Pradesh"),("Jodhpur","Rajasthan"),("Madurai","Tamil Nadu"),
    ("Raipur","Chhattisgarh"),("Kota","Rajasthan"),("Chandigarh","Chandigarh"),
    ("Guwahati","Assam"),("Solapur","Maharashtra"),("Hubballi","Karnataka"),
    ("Mysuru","Karnataka"),("Tiruchirappalli","Tamil Nadu"),("Bareilly","Uttar Pradesh"),
    ("Moradabad","Uttar Pradesh"),("Gurgaon","Haryana"),("Aligarh","Uttar Pradesh"),
    ("Jalandhar","Punjab"),("Bhubaneswar","Odisha"),("Salem","Tamil Nadu"),
    ("Warangal","Telangana"),("Mira-Bhayandar","Maharashtra"),("Thiruvananthapuram","Kerala"),
    ("Bhiwandi","Maharashtra"),("Saharanpur","Uttar Pradesh"),("Gorakhpur","Uttar Pradesh"),
    ("Guntur","Andhra Pradesh"),("Amravati","Maharashtra"),("Bikaner","Rajasthan"),
    ("Noida","Uttar Pradesh"),("Jamshedpur","Jharkhand"),("Bhilai","Chhattisgarh"),
    ("Cuttack","Odisha"),("Firozabad","Uttar Pradesh"),("Kochi","Kerala"),
    ("Nellore","Andhra Pradesh"),("Bhavnagar","Gujarat"),("Dehradun","Uttarakhand"),
    ("Durgapur","West Bengal"),("Asansol","West Bengal"),("Rourkela","Odisha"),
    ("Nanded","Maharashtra"),("Kolhapur","Maharashtra"),("Ajmer","Rajasthan"),
    ("Gulbarga","Karnataka"),("Jamnagar","Gujarat"),("Ujjain","Madhya Pradesh"),
    ("Loni","Uttar Pradesh"),("Siliguri","West Bengal"),("Jhansi","Uttar Pradesh"),
    ("Ulhasnagar","Maharashtra"),("Jammu","J&K"),("Sangli","Maharashtra"),
    ("Mangaluru","Karnataka"),("Erode","Tamil Nadu"),("Belgaum","Karnataka"),
    ("Ambattur","Tamil Nadu"),("Tirunelveli","Tamil Nadu"),("Malegaon","Maharashtra"),
    ("Gaya","Bihar"),("Jalgaon","Maharashtra"),("Udaipur","Rajasthan"),
    ("Panipat","Haryana"),("Davanagere","Karnataka"),("Kozhikode","Kerala"),
]

SKU_SIZES    = ["Small","Regular","Large","Family"]
SKU_PACKS    = ["Single","Pack of 2","Pack of 4","Pack of 6","Pack of 12"]
SKU_VARIANTS = ["Classic","Vanilla","Chocolate","Pro","Lite","Gold","Original","Creamy"]

# ─── GENERATE IDs ─────────────────────────────────────────────────────────────

customer_ids  = [f"CUST{i:06d}" for i in range(1, N_CUSTOMERS + 1)]
store_ids     = [f"ST{i:04d}"   for i in range(1, N_STORES + 1)]
product_ids   = [f"PROD{i:05d}" for i in range(1, N_PRODUCTS + 1)]
promo_ids     = [f"PR{i:05d}"   for i in range(1, N_PROMOTIONS + 1)]
order_ids     = [f"ORD{i:08d}"  for i in range(1, N_ORDERS + 1)]
category_ids  = [c[0] for c in CATEGORIES]
channel_ids   = [c[0] for c in CHANNELS]

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("\n Connecting to SQL Server…")
    conn   = pyodbc.connect(CONNECTION_STRING, autocommit=False)
    cursor = conn.cursor()
    cursor.fast_executemany = True      # critical for speed with pyodbc
    print(" Connected.\n")

    start_all = time.time()

    # ── 1. CATEGORY ──────────────────────────────────────────────────────────
    print("► Inserting reference tables…")
    cursor.executemany(
        "INSERT INTO CATEGORY (category_id, category_name) VALUES (?,?)",
        CATEGORIES
    )
    conn.commit()

    # ── 2. CHANNEL ───────────────────────────────────────────────────────────
    cursor.executemany(
        "INSERT INTO CHANNEL (channel_id, channel_name) VALUES (?,?)",
        CHANNELS
    )
    conn.commit()

    # ── 3. MARKETING_CHANNEL ─────────────────────────────────────────────────
    cursor.executemany(
        "INSERT INTO MARKETING_CHANNEL (channel_id,channel_name,channel_type,cost_tier) VALUES (?,?,?,?)",
        MARKETING_CHANNELS
    )
    conn.commit()
    print("  ✓ CATEGORY, CHANNEL, MARKETING_CHANNEL done")

    # ── 4. STORE ─────────────────────────────────────────────────────────────
    store_rows = []
    for sid in store_ids:
        city, state = random.choice(INDIAN_CITIES_STATES)
        store_rows.append((sid, city, state, random.choice(STORE_TYPES)))
    bulk_insert(cursor,
        "INSERT INTO STORE (store_id,store_city,store_state,store_type) VALUES (?,?,?,?)",
        store_rows, "STORE")

    # ── 5. PROMOTION ─────────────────────────────────────────────────────────
    promo_rows = []
    base = date(2022, 1, 1)
    for pid in promo_ids:
        start = rand_date(base, date(2025, 6, 1))
        end   = start + timedelta(days=random.randint(7, 60))
        disc  = round(random.choice([5,10,15,20,25,30,50]), 2)
        promo_rows.append((pid, random.choice(PROMO_TYPES),
                           start.isoformat(), end.isoformat(), disc))
    bulk_insert(cursor,
        "INSERT INTO PROMOTION (promo_id,promo_type,start_date,end_date,discount_value) VALUES (?,?,?,?,?)",
        promo_rows, "PROMOTION")

    # ── 6. CUSTOMER ──────────────────────────────────────────────────────────
    customer_rows = []
    for cid in customer_ids:
        city, state = random.choice(INDIAN_CITIES_STATES)
        signup = rand_date(date(2020, 1, 1), date(2024, 12, 31))
        customer_rows.append((
            cid, signup.isoformat(), city, state,
            random.choice(SEGMENTS), random.choice(STATUSES)
        ))
    bulk_insert(cursor,
        "INSERT INTO CUSTOMER (customer_id,signup_date,city,state,segment,status) VALUES (?,?,?,?,?,?)",
        customer_rows, "CUSTOMER")

    # ── 7. PRODUCT ───────────────────────────────────────────────────────────
    product_rows = []
    for pid in product_ids:
        cat  = random.choice(category_ids)
        brand = random.choice(BRANDS)
        variant = random.choice(SKU_VARIANTS)
        size    = random.choice(SKU_SIZES)
        pack    = random.choice(SKU_PACKS)
        sku     = f"{brand} Beverages - {variant} ({size}, {pack})"
        product_rows.append((pid, cat, brand, sku))
    bulk_insert(cursor,
        "INSERT INTO PRODUCT (product_id,category_id,brand,sku_name) VALUES (?,?,?,?)",
        product_rows, "PRODUCT")

    # ── 8. ORDER ─────────────────────────────────────────────────────────────
    order_rows = []
    print("  Generating ORDER rows…")
    for oid in tqdm(order_ids, desc="ORDER", unit="rows", unit_scale=True):
        od   = rand_date(date(2022, 1, 1), date(2025, 12, 31))
        week = int(od.strftime("%W")) or 1
        order_rows.append((
            oid,
            random.choice(customer_ids),
            od.isoformat(),
            random.choice(store_ids),
            random.choice(channel_ids),
            random.choice(PAYMENT_TYPES),
            od.year, week
        ))

    bulk_insert(cursor,
        """INSERT INTO [ORDER]
           (order_id,customer_id,order_date,store_id,channel_id,payment_type,year,week)
           VALUES (?,?,?,?,?,?,?,?)""",
        order_rows, "ORDER (bulk)")

    # ── 9. ORDER_ITEM ────────────────────────────────────────────────────────
    # ~2.2 items per order on average  →  ~2.2M rows
    print("  Generating ORDER_ITEM rows…")
    oi_rows = []
    oi_idx  = 1
    promo_ids_with_none = promo_ids + [None] * (len(promo_ids) * 4)  # 20% chance promo

    for oid in tqdm(order_ids, desc="ORDER_ITEM gen", unit="orders", unit_scale=True):
        n_items = random.choices([1, 2, 3, 4, 5], weights=[30, 35, 20, 10, 5])[0]
        for _ in range(n_items):
            promo = random.choice(promo_ids_with_none)
            disc  = round(random.uniform(0, 20), 2) if promo else 0.0
            oi_rows.append((
                f"OI{oi_idx:010d}",
                oid,
                random.choice(product_ids),
                promo,
                random.randint(1, 6),
                disc
            ))
            oi_idx += 1

    bulk_insert(cursor,
        """INSERT INTO ORDER_ITEM
           (order_item_id,order_id,product_id,promo_id,quantity,item_discount)
           VALUES (?,?,?,?,?,?)""",
        oi_rows, "ORDER_ITEM")

    # ── 10. PRICE_CHANGE ─────────────────────────────────────────────────────
    print("  Generating PRICE_CHANGE rows…")
    pc_rows = []
    for pid in product_ids:
        base_price = round(random.uniform(50, 800), 2)
        for year in [2023, 2024, 2025]:
            # ~17 price changes per product per year on average
            changed_weeks = sorted(random.sample(range(1, 53), k=random.randint(8, 26)))
            price = base_price
            for wk in changed_weeks:
                price = round(price * random.uniform(0.97, 1.05), 2)
                pc_rows.append((pid, year, wk, price))

    bulk_insert(cursor,
        "INSERT INTO PRICE_CHANGE (product_id,year,week,unit_price) VALUES (?,?,?,?)",
        pc_rows, "PRICE_CHANGE")

    # ── 11. EXTERNAL_FACTOR ──────────────────────────────────────────────────
    print("  Generating EXTERNAL_FACTOR rows…")
    ef_rows  = []
    ef_idx   = 1
    ef_start = date(2022, 1, 3)   # first Monday of 2022
    for sid in tqdm(store_ids, desc="EXTERNAL_FACTOR", unit="stores"):
        for week_offset in range(0, 52 * 3):   # 3 years = ~156 weeks
            d    = ef_start + timedelta(weeks=week_offset)
            if d > date(2025, 12, 31):
                break
            year = d.year
            week = int(d.strftime("%W")) or 1
            ef_rows.append((
                f"F{ef_idx:010d}",
                sid,
                d.isoformat(),
                1 if random.random() < 0.06 else 0,      # 6% holiday
                round(random.uniform(10, 42), 2),         # temp_c
                round(random.uniform(0, 50), 2),          # rainfall_mm
                round(random.uniform(80, 120), 2),        # trend_index
                round(random.uniform(95, 115), 2),        # cpi_index
                year, week
            ))
            ef_idx += 1

    bulk_insert(cursor,
        """INSERT INTO EXTERNAL_FACTOR
           (factor_id,store_id,factor_date,is_holiday,temp_c,rainfall_mm,
            trend_index,cpi_index,year,week)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        ef_rows, "EXTERNAL_FACTOR")

    # ── 12. SESSION ──────────────────────────────────────────────────────────
    print("  Generating SESSION rows…")
    session_rows = []
    sampled_customers = random.choices(customer_ids, k=N_SESSIONS)
    for i, cid in enumerate(tqdm(sampled_customers, desc="SESSION", unit="rows", unit_scale=True)):
        sid = f"SE{i+1:010d}"
        session_rows.append((
            sid, cid,
            rand_datetime(date(2022, 1, 1), date(2025, 12, 31)).strftime("%Y-%m-%d %H:%M:%S"),
            random.randint(15, 1800),
            random.randint(1, 20),
            random.choice(DEVICES),
            random.choice(REFERRERS)
        ))

    bulk_insert(cursor,
        """INSERT INTO SESSION
           (session_id,customer_id,session_start,session_duration_sec,
            pages_viewed,device,referrer)
           VALUES (?,?,?,?,?,?,?)""",
        session_rows, "SESSION")

    # ── 13. CAMPAIGN_TOUCH ───────────────────────────────────────────────────
    print("  Generating CAMPAIGN_TOUCH rows…")
    ct_rows = []
    sampled_ct = random.choices(customer_ids, k=N_CAMPAIGN_TOUCHES)
    for i, cid in enumerate(tqdm(sampled_ct, desc="CAMPAIGN_TOUCH", unit="rows", unit_scale=True)):
        ct_rows.append((
            f"CT{i+1:010d}",
            cid,
            rand_date(date(2022, 1, 1), date(2025, 12, 31)).isoformat(),
            random.choice(CHANNELS_MKT),
            random.choice(CAMPAIGNS),
            random.choices([0, 1], weights=[75, 25])[0]   # 25% conversion
        ))

    bulk_insert(cursor,
        """INSERT INTO CAMPAIGN_TOUCH
           (touch_id,customer_id,touch_date,channel,campaign_name,outcome)
           VALUES (?,?,?,?,?,?)""",
        ct_rows, "CAMPAIGN_TOUCH")

    # ── 14. SUPPORT_TICKET ───────────────────────────────────────────────────
    print("  Generating SUPPORT_TICKET rows…")
    st_rows = []
    sampled_st = random.choices(customer_ids, k=N_SUPPORT_TICKETS)
    for i, cid in enumerate(tqdm(sampled_st, desc="SUPPORT_TICKET", unit="rows", unit_scale=True)):
        res_hr   = round(random.uniform(1, 120), 2)
        st_rows.append((
            f"T{i+1:08d}",
            cid,
            rand_date(date(2022, 1, 1), date(2025, 12, 31)).isoformat(),
            random.choice(ISSUE_TYPES),
            random.choice(TICKET_STATUS),
            res_hr,
            random.randint(1, 5),
            round(res_hr / 24, 2)
        ))

    bulk_insert(cursor,
        """INSERT INTO SUPPORT_TICKET
           (ticket_id,customer_id,created_date,issue_type,status,
            resolution_time_hr,csat_score,resolution_time_days)
           VALUES (?,?,?,?,?,?,?,?)""",
        st_rows, "SUPPORT_TICKET")

    # ── DONE ─────────────────────────────────────────────────────────────────
    elapsed = time.time() - start_all
    print(f"\n All tables inserted in {elapsed/60:.1f} minutes.")

    # Row count verification
    print("\n Row counts:")
    tables = [
        "CATEGORY","CHANNEL","MARKETING_CHANNEL","STORE","PROMOTION",
        "CUSTOMER","PRODUCT","[ORDER]","ORDER_ITEM","PRICE_CHANGE",
        "EXTERNAL_FACTOR","SESSION","CAMPAIGN_TOUCH","SUPPORT_TICKET"
    ]
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        n = cursor.fetchone()[0]
        print(f"  {t.replace('[','').replace(']',''):<22} {n:>12,}")

    cursor.close()
    conn.close()
    print("\n Done! Connection closed.")


if __name__ == "__main__":
    main()
