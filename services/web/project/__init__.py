#!/usr/bin/env python3
from flask import Flask, render_template, request
from time import sleep
import requests

app = Flask(__name__, static_folder="assets")

site_title = "IP Address Lookup"


@app.route("/")
def home():
    page_body = ""

    detected_ip_address = get_users_ip_address()
    page_body += "<strong>Your Public IP Address</strong><BR>"
    page_body += process_ip_address(detected_ip_address)

    return display_homepage(detected_ip_address, page_body)


@app.route("/", methods=["POST"])
def home_post():
    page_body = ""

    sleep(0.25)

    submitted_ip_address = str(request.form["ip_address"])

    if submitted_ip_address == "":
        submitted_ip_address = get_users_ip_address()

    if submitted_ip_address == get_users_ip_address():
        page_body += "<strong>Your Public IP Address</strong><BR>"

    page_body += process_ip_address(submitted_ip_address)

    return display_homepage(submitted_ip_address, page_body)


def get_users_ip_address():
    return str(request.environ["REMOTE_ADDR"])


def process_ip_address(ip_address):
    page_body = ""

    try:
        api_url = "http://ip-api.com/line/" + ip_address
        result = requests.get(api_url).text
        result = result.replace("success\n", "")
        result = result.replace("\n", "<BR>")
        page_body += result

    except Exception:
        page_body += "Unable to lookup IP address, please try again."

    return page_body


def display_homepage(ip_address, page_body):
    return render_template(
        "home.html", site_title=site_title, ip_address=ip_address, page_body=page_body
    )


if __name__ == "__main__":
    app.run()
