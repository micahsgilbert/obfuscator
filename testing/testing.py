from only_html_reqs import *
from full_site_reqs import *
from stress_test import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def average(l):
  return sum(l) / len(l)


OBFUSCATED_URL = "https://localhost:9000/2/"
CLEAN_URL = "http://localhost/2/"

print("         CLEAN          ")
print("------------------------")

clean_only_html = only_html_reqs(CLEAN_URL)
print("\rOnly HTML: ", average(clean_only_html))

clean_full_site = full_site_reqs(CLEAN_URL)
print("\rFull Site: ", average(clean_full_site))

clean_stress_time = stress_test(CLEAN_URL, 100)
print("\rStress Test: ", clean_stress_time)

print("")
print("          OBF           ")
print("------------------------")

obf_only_html = only_html_reqs(OBFUSCATED_URL)
print("\rOnly HTML: ", average(obf_only_html))

input("Clear session_mappings.json, then press enter")

obf_full_site = full_site_reqs(OBFUSCATED_URL)
print("\rFull Site: ", average(obf_full_site))

obf_stress_time = stress_test(OBFUSCATED_URL, 100)
print("\rStress Test: ", obf_stress_time)
