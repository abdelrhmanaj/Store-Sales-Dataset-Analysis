Project: Store Sales Data Cleaning
Engineer: Abdelhalim Abdelmageed
Date: April 16, 2026

Scope:
Cleaned and pre-processed 6 core datasets: PROMOTION, STORE, SUPPORT_TICKET, CUSTOMER, MARKETING_CHANNEL, and EXTERNAL_FACTOR.

Key Transformations Applied:
1. Data Type Standardization:
   - Converted all date columns to datetime64 format for accurate time-series analysis.
   - Ensured numerical fields (e.g., discount_value, resolution_time_hr) are float64.

2. Missing Value Imputation:
   - Categorical nulls were filled with "Unknown".
   - Numerical nulls in External Factors (Temp, Rainfall, CPI) were filled using the Median to avoid outliers.

3. Text Normalization:
   - Applied Title Case formatting to City and State names for consistency.

4. Feature Engineering:
   - Created 'resolution_time_days' from 'resolution_time_hr' to provide better insights into support efficiency.

Status: All datasets are validated and exported to CSV format in the 'Cleaned_DataSet' folder.