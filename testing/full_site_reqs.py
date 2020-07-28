import requests
import time
import re

def get_links_from_html(html):
  css_link_re = re.compile('rel=\\"stylesheet\\" href=\\"(.*)\\"')
  js_re = re.compile('src=\\"(.*)\\"')
  return [re.findall(css_link_re, html)[0], re.findall(js_re, html)[0]]

def full_site_reqs(URL):
  times = []

  for i in range(50):
    start = time.perf_counter()
    r = requests.get(URL, verify=False)
    for link in get_links_from_html(r.text):
      requests.get(URL + link, verify=False)
    end = time.perf_counter() - start
    times.append(end)
    time.sleep(0.25)
    print(f"\rMade Request {i} of 50", end="")

  return times