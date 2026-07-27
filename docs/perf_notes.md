# Performance Notes

## Environment

OS: Windows 11

Python: 3.13.5

Database: SQLite

API: FastAPI

Dashboard: Streamlit

---

## API Load Test

Concurrent Requests: 10

Successful Requests:

Failed Requests:

Average Response Time:

Minimum Response Time:

Maximum Response Time:

Total Execution Time:

---

## Dashboard Performance

 Company      Load Time 

 TCS            <3S
 INFY           <3S
 RELIANCE       <3S 
 SUNPHARMA      <3S 
 HDFCBANK       <3S

Average Load Time:

---

## Bottlenecks

- None observed

OR

- Slow JOIN query
- Large dataframe merge
- Missing indexes

---

## Optimizations

- Added indexes

- Cached repeated queries

- Reduced unnecessary dataframe merges

---

## Result

System remained stable during testing.

All APIs responded successfully.

Dashboard remained responsive.