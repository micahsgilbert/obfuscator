import sys
import base64
import json
import random
import os
import binascii
import AdvancedHTMLParser
import time
import re
from tinydb import TinyDB, Query
from tinydb.operations import decrement

#todo
# name replacement
# js replacement - search and replace

BASE_URL = "https://intern.micahsgilbert.dev:9000"

def get_random():
  return ('a','b','c','d','e','f')[random.randint(0,5)] + binascii.b2a_hex(os.urandom(8)).decode("utf-8")

encoded_body = sys.argv[1]
content_type = sys.argv[2]
session_id = sys.argv[3]
body = base64.b64decode(encoded_body).decode("utf-8")

db = TinyDB("/home/mgilbert/node-obfuscation/obfuscation/session_mappings.json")

if ("html" in content_type):
  random_session_id = get_random()

  parser = AdvancedHTMLParser.AdvancedHTMLParser()
  parser.parseStr(body)

  css_remaining = 0
  scripts_remaining = 0

  for link in parser.getElementsByTagName("link"):
    if link.rel == "stylesheet" and (link.href.startswith(BASE_URL) or not link.href.startswith("http")):
      link.href = link.href + "?sess=" + random_session_id
      css_remaining += 1

  for script in parser.getElementsByTagName("script"):
    if script.src.startswith(BASE_URL) or not script.src.startswith("http"):
      script.src = script.src + "?sess=" + random_session_id
      scripts_remaining += 1

  db.insert({'_id': random_session_id, "_creation_time": round(time.time()), "_css_remaining": css_remaining, '_js_remaining': scripts_remaining})

  ids = set()
  classes = set()

  id_pattern = re.compile('id="(.*?)"')
  class_pattern = re.compile('class="(.*?)"')

  ids = list(set(re.findall(id_pattern, body))) 
  classes_not_split = list(set(re.findall(class_pattern, body))) # elems with 2 classes exist as 1 entry w/ space
  classes = []

  for c in classes_not_split:
    classes.extend(c.split(" "))
  
  classes = list(set(classes))

  for i in ids:
    new_id = get_random()

    q = Query()
    db.update({"#" + i: "#" + new_id}, q._id == random_session_id)

    parser.getElementById(i).id = new_id

  for c in classes:
    new_class = get_random()

    q = Query()
    db.update({"." + c: "." + new_class}, q._id == random_session_id)

    for tag in parser.getElementsByClassName(c):
      tag.addClass(new_class)
      tag.removeClass(c)

  for d in [*parser.getElementsByTagName("div"), *parser.getElementsByTagName("form")]:
    children = d.getChildren()
    for i in range(random.randint(1,4)):
      randomDiv = "<div id=\"" + get_random() + "\"></div>"
      d.insertBefore(parser.createElementFromHTML(randomDiv), d.firstElementChild)

    for i in range(random.randint(1,4)):
      randomDiv = "<div id=\"" + get_random() + "\"></div>"
      d.appendChild(parser.createElementFromHTML(randomDiv))

  #todo - create duplicate forms that have display:none, as well as randomized classes

  formReplacements = []

  for form in parser.getElementsByTagName("form"):
    fData = {}
    i = get_random()
    form.id = i
    fData["_id"] = i
    for i in form.getChildren().getElementsByTagName("input"):
      if (i.name):
        r = get_random()
        fData[i.name] = r
        i.name = r
    formReplacements.append(fData)

  q = Query()
  db.update({"_formData": formReplacements}, q._id == random_session_id)

  print(base64.b64encode(parser.getHTML().encode("utf-8")).decode("utf-8"))


elif ("css" in content_type and session_id != "null"):
  q = Query()
  sess = db.get(q._id == session_id)

  if (sess):

    q = Query()
    db.update(decrement("_css_remaining"), q._id == session_id)

    for mapping in sess.keys():

      if not mapping.startswith("_"):

      # actual css replacement happens here
        body = body.replace(mapping + " ", sess[mapping] + " ")
        body = body.replace(mapping + "{", sess[mapping] + "{")


    print(base64.b64encode(body.encode("utf-8")).decode("utf-8"))
  else:
    print(encoded_body)
  
elif ("javascript" in content_type and session_id != "null"):
  time.sleep(0.1)
  q = Query()
  sess = db.get(q._id == session_id)

  if (sess):

    q = Query()
    db.update(decrement("_js_remaining"), q._id == session_id)

    for mapping in sess.keys():
      if not mapping.startswith("_"):
        m1 = mapping
        m2 = sess[mapping]
        if (mapping.startswith("#") or mapping.startswith(".")):
          m1 = mapping[1:]
          m2 = sess[mapping][1:]

        body = body.replace("\"" + m1 + "\"" , "\"" + m2 + "\"")

    for form in sess["_formData"]:
      body += ";window.addEventListener('load', () => {document.getElementById('" + form["_id"] + "').addEventListener('submit', e => {"
      #body += "e.preventDefault();\n"
      for i in form.keys():
        if (not i.startswith("_")):
          body += "Array.prototype.slice.call(document.getElementById('" + form["_id"] + "').getElementsByTagName('input')).forEach(i => {if (i.name === '" + form[i] + "') {i.name = '" + i + "'}});"
      body += "})});"
      
        

    print(base64.b64encode(body.encode("utf-8")).decode("utf-8"))

  else:
    print(encoded_body)

else:
  print(encoded_body)

# remove expired session ids after 30 seconds or when all reqs have been made
q = Query()
db.remove((q._css_remaining == 0 and q._js_remaining == 0) or time.time() - q._creation_time > 30)