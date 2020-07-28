import requests
import random
import time
import re

def get_links_from_html(html):
  css_link_re = re.compile('rel=\\"stylesheet\\" href=\\"(.*)\\"')
  js_re = re.compile('src=\\"(.*)\\"')
  return [re.findall(css_link_re, html)[0], re.findall(js_re, html)[0]]

def stress_test(URL, iters):
  start = time.perf_counter()
  url_queue = [URL for i in range(iters)]
  while(True):
    if len(url_queue) == 0:
      return time.perf_counter() - start
    else:
      url = random.choice(url_queue)
      if "css" in url or "js" in url:
        requests.get(url, verify=False)
      else:
        r = requests.get(url, verify=False)
        url_queue.extend([(URL + l) for l in get_links_from_html(r.text)])
      url_queue.remove(url)
    print(f"\r{len(url_queue)} Remaining in queue", end="")