# node-obfuscation

A proxy to automatically obfuscate the DOM elements and structure to guard against automated attacks and web scraping. Created as my 2020 summer internship project with UNO and Dr. Rui Zhao.

## Setup

Just clone and run `npm install`. The python modules required are in `requirements.txt`.

## Usage Requirements

This proxy uses HTTPS and as such requires an SSL certificate. The certificate should be stored in `cert/cert.pem` and the private key in `cert/privkey.pem`.
There should be two environment variables set. The first is `TARGET`, which refers to the target of the reverse proxy. If you are running the proxy on the same machine that the webserver is on, `http://localhost` should work. The second is `PORT`, which is where the obfuscated site will be served. If it is not set, it defaults to 9000.

## What exactly it does

- Replaces all `id`s and `class`es with randomly generated strings in the HTML, CSS, and JS.
- Changes input `name`s in forms, and inserts JS to change the names back when the form is submitted
- Adds random amounts of `divs` to the beginning and end of elements in order to prevent structure-based scraping.

## Future ideas

- More comprehensive obfuscation of the structure of the DOM
- JS obfuscation
- Make into a framework to allow for easier expansion and customization

## A note

**This project is only a proof of concept.** It is far from optimized in many regards. The database module, `tinydb` is far from production ready. It literally just stores everything in a JSON file. That means that query times eventually begin to suffer. There are also issues where 2 instances of the script try to access the db file at the same time. In relation to that, the fact that a new instance of the obfuscation script must be run on every new request means that in high-demand situations, memory usage may become an issue.
