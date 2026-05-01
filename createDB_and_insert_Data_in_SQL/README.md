# 🛒 Stores Sales Database


---



---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| SQL Server | Database engine |
| Python 3.x | Data generation |
| pyodbc | SQL Server connection |
| Faker | Realistic fake data |
| tqdm | Progress bars |
| python-dotenv | Secure config via `.env` |

---

## 📊 Database Scale

| Table | Rows |
|-------|------|
| Orders | ~1,000,000 |
| Order Items | ~2,200,000 |
| Customers | Tracked with behavior |
| Products | With category hierarchy |
| External Factors | Weather, holidays, etc. |

---

## 🚀 Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Store-Sales-Dataset-Analysis.git
cd Store-Sales-Dataset-Analysis
```

### 2. Create the database schema
Open SQL Server Management Studio (SSMS) and run:
```sql
database/create_retail_analytics_db.sql
```

### 3. Configure your environment
```bash
cp .env.example .env
```
Then edit `.env` with your SQL Server details:
```env
DB_SERVER=DESKTOP-XXXX\SQLEXPRESS
DB_NAME=Store_Sales_DataSetDB
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the data generator
```bash
python data-generator/generate_and_insert_data.py
```

---

## 🔒 Security Notes

- **Never commit your `.env` file** — it contains your database credentials
- `.env` is already listed in `.gitignore` for protection
- Use `.env.example` as a safe template to share with others

---

## 📝 Notes

- Uses **bulk insert** techniques for high-performance data loading
- Data is randomly generated using the **Faker** library for realism
- Progress tracked via **tqdm** progress bars during insertion
