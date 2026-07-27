import threading
import time
import requests
import pandas as pd

URL = "http://127.0.0.1:8000/api/v1/screener"

results = []


def hit_api():

    start = time.perf_counter()

    try:

        response = requests.get(URL)

        elapsed = time.perf_counter() - start

        print("Status:", response.status_code)

        results.append({

            "status": response.status_code,

            "time": elapsed

        })

    except Exception as e:

        elapsed = time.perf_counter() - start

        print("ERROR:", e)

        results.append({

            "status": "FAILED",

            "time": elapsed

        })


threads = []

overall_start = time.perf_counter()

for _ in range(10):

    thread = threading.Thread(target=hit_api)

    thread.start()

    threads.append(thread)

for thread in threads:

    thread.join()

overall_end = time.perf_counter()


df = pd.DataFrame(results)

successful = (df["status"] == 200).sum()

failed = len(df) - successful

average = df["time"].mean()

minimum = df["time"].min()

maximum = df["time"].max()

total = overall_end - overall_start


print("=" * 50)

print("Requests :", len(df))

print("Successful :", successful)

print("Failed :", failed)

print("Average :", round(average,3))

print("Minimum :", round(minimum,3))

print("Maximum :", round(maximum,3))

print("Total :", round(total,3))

print("=" * 50)


df.to_csv(

    "reports/performance_results.csv",

    index=False

)