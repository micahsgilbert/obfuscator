import requests
import time

def only_html_reqs(URL):
  times = []

  for i in range(50):
    start = time.perf_counter()
    r = requests.get(URL, verify=False)
    end = time.perf_counter() - start
    times.append(end)
    print(f"\rMade Request {i} of 50", end="")
    time.sleep(0.25)

  return times