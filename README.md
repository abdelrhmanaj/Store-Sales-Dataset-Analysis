# Store Sales Dataset Analysis

---

## Project Idea
This project focuses on analyzing a store sales dataset to extract business insights, answer analytical and forecasting questions, and build a visualization dashboard to support decision-making.

The project includes data preprocessing, exploratory data analysis, forecasting using machine learning techniques, and building an interactive dashboard using Tableau.

---
## Team Name: Team 4
---

## Team Members
1. Abdelrhman Mohammed Mahmoud (Leader) 
2. Mahmoud Soudy Youssef
3. Abdelhalim Abdelmageed Shahat
4. Abdallah Amgad Hassan
5. Rana Mohamed Mostafa

---

## Data Cleaning Progress

### Datasets Overview
The project includes **13 datasets** across multiple CSV files covering various aspects of store sales operations:

| Dataset | Records | Key Fields | Status |
|---------|---------|-----------|--------|
| CAMPAIGN_TOUCH | Customer campaign interactions | touch_id, customer_id, campaign_name, outcome | ✅ Cleaned |
| CATEGORY | Product categories | category_id, category_name | ✅ Cleaned |
| CHANNEL | Sales channels | channel_id, channel_name | ✅ Cleaned |
| CUSTOMER | Customer information | customer_id, signup_date, city, state, segment, status | ✅ Cleaned |
| EXTERNAL_FACTOR | Weather & economic factors | factor_id, store_id, rainfall, temperature, CPI | ✅ Cleaned |
| MARKETING_CHANNEL | Marketing channels | channel_id, channel_name, channel_type, cost_tier | ✅ Cleaned |
| ORDER | Order transactions | order_id, customer_id, order_date, total_amount | ✅ Cleaned |
| ORDER_ITEM | Order line items | order_item_id, order_id, product_id, quantity, discount | ✅ Cleaned |
| PRICE_CHANGE | Product pricing history | product_id, year, week, unit_price | ✅ Cleaned |
| PRODUCT | Product information | product_id, product_name, category_id, price | ✅ Cleaned |
| PROMOTION | Promotional campaigns | promo_id, promo_type, start_date, discount_value | ✅ Cleaned |
| SESSION | Customer sessions | session_id, customer_id, session_date, items_viewed | ✅ Cleaned |
| STORE | Store information | store_id, store_city, store_state, store_type | ✅ Cleaned |
| SUPPORT_TICKET | Customer support tickets | ticket_id, customer_id, issue_type, status, resolution_time | ✅ Cleaned |

### Team Member Assignments
- **Rana Mohamed Mostafa** - PRICE_CHANGE, ORDER_ITEM
- **Mahmoud Soudy Youssef** - CAMPAIGN_TOUCH, CATEGORY, CHANNEL
- **Abdallah Amgad Hassan** - CUSTOMER, MARKETING_CHANNEL, EXTERNAL_FACTOR
- **Abdelrhman Mohammed Mahmoud** - ORDER, PRODUCT, SESSION
- **Abdelhalim Abdelmageed Shahat** - PROMOTION, STORE, SUPPORT_TICKET

### Data Cleaning Notebooks
All cleaning notebooks are located in `NoteBooks_For_Cleaning/`:
- `Rana.ipynb` - Data cleaning for PRICE_CHANGE and ORDER_ITEM
- `Soudy.ipynb` - Data cleaning for CAMPAIGN_TOUCH, CATEGORY, and CHANNEL
- `Abdallah.ipynb` - Data cleaning for CUSTOMER, MARKETING_CHANNEL, and EXTERNAL_FACTOR
- `Abdelrhmanaja.ipynb` - Data cleaning for ORDER, PRODUCT, and SESSION
- `Abdelhalim.ipynb` - Data cleaning for PROMOTION, STORE, and SUPPORT_TICKET

**Cleaned datasets are saved in:** `Cleaned_DataSet/` folder

---

## Project Plan

### 1. Research & Analysis
- Data preprocessing and cleaning  
- Build data model  
- Identify analysis questions  
- Target Audience: Business decision makers, sales managers  

### 2. Visual Identity
- Logo design for presentation and dashboard branding  

### 3. Main Designs
- Dashboard Design  
- Visualization Charts  
- Presentation Slides  

### 4. Complementary Products
- Data preprocessing notebook  
- Forecasting model notebook  

### 5. Review & Finalization
- Validate results  
- Optimize dashboard  
- Final documentation  

### 6. Final Presentation
- Present insights  
- Explain forecasting results  
- Demonstrate dashboard  

---

## Roles & Responsibilities
- Data Cleaning & Preprocessing — SQL, Python (Pandas)  
- Data Analysis & Visualization — Python (Matplotlib), Tableau  
- Forecasting Models — Python (Scikit-learn)  
- Dashboard Development — Tableau  
- Documentation & Presentation — Team Collaboration  

---

## KPIs (Key Performance Indicators)
- Data cleaning accuracy  
- Forecasting model accuracy  
- Dashboard usability  
- Query response time  
- Insight usefulness for decision making  

---

## Instructor
Mr .Abdelrahman Ashour

---

## Project Timeline (4 Weeks)

### Week 1 — Data Model & Preprocessing
**Tasks**
- Build data model  
- Clean and preprocess dataset  

**Tools**
- SQL  
- Python (Pandas, Matplotlib)  

**Deliverables**
- Cleaned dataset  
- Data preprocessing notebook  

---

### Week 2 — Analysis Questions Phase
**Tasks**
- Define business analysis questions  
- Analyze product categories and regions impact on sales  

**Tools**
- SQL  
- Python (Pandas, Matplotlib)  

**Deliverables**
- Set of analysis questions  
- Initial visualizations  

---

### Week 3 — Forecasting Phase
**Tasks**
- Define forecasting questions  
- Build forecasting models using trends  

**Tools**
- Python (Scikit-learn, Pandas, Matplotlib)  

**Deliverables**
- Forecasting visualizations  
- Model evaluation results  

---

### Week 4 — Dashboard & Final Presentation
**Tasks**
- Build Bower BI Dashboard  
- Prepare final report and presentation  

**Tools**
- SQL  
- Python  
- Power BI 

**Deliverables**
- Interactive dashboard  
- Final report  
- Final presentation  

---

## Tools & Technologies
- SQL  
- Python  
- Pandas
- Power BI  
---

## Expected Outcomes
- Clean and structured dataset  
- Business insights from sales data  
- Forecasting models for future sales trends  
- Interactive dashboard for decision makers  

---
