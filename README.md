# Financial Control – Football Project (Data Ingestion)

This repository is responsible for the financial data ingestion layer of the **Football Performance & Financial Control** project.

The application allows structured and standardized registration of financial transactions related to a recreational football group, such as monthly fees, expenses, and other revenues, eliminating manual spreadsheets and reducing data inconsistencies.

---

##  Project Objective

Provide a simple and reliable interface for registering financial transactions, ensuring data consistency and supporting financial analysis and dashboards.

This repository focuses **exclusively on financial data ingestion** and does not include analytical logic or visualizations.

---

##  Features

- Financial transaction registration (revenues and expenses)
- Transaction categorization by type and description
- Date and value validation
- Centralized and standardized data input via forms

---

##  Technologies Used

- Python  
- Streamlit  
- PostgreSQL  
- Supabase  
- SQL  

---

##  Repository Structure

financeiro_pelada/

├── app.py
├── requirements.txt
├── runtime.txt
└── README.md

---

##  Data Flow

1. Financial data is submitted through a Streamlit form  
2. Data is validated and processed using Python  
3. Records are stored in a PostgreSQL database hosted on Supabase  
4. Data is consumed by Power BI dashboards  

---

##  Related Project

This repository is part of an end-to-end data solution:

**Football Performance & Financial Control – End-to-End Data Project**  
👉 Main portfolio repository:  
https://github.com/GuilhermeBigaiski/Portfolio

---

##  Notes

This project was designed to allow non-technical users to register financial data without direct interaction with databases or spreadsheets.
