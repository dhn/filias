#!/usr/bin/env python
# $Id: filias.py,v 1.1 2014/09/16 19:57:01 dhn Exp $
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 Dennis 'dhn' Herrmann
"""

import os
import sh
import re
import sys
import time
import getopt
import sqlite3
import requests
from threading import Thread
from bs4 import BeautifulSoup

username = ""
password = ""

savepoint = "/home/dhn/ilias"
proxy = False
proxy_url = ""

login_url = "https://www.ilias.fh-dortmund.de/ilias/login.php"
webdav_url = "http://ilias.fh-dortmund.de/ilias/webdav.php/ilias-fhdo/"
url = "http://www.ilias.fh-dortmund.de/ilias/ilias.php?baseClass=" + \
    "ilPersonalDesktopGUI&cmd=jumpToSelectedItems"

conn = sqlite3.connect(":memory:")


def getopts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f", ["fetch"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--fetch"):
            main()
        else:
            assert False, "unhandled option"


def usage():
    print("usage: %s [-f|--fetch]" % __file__)


def login(login_url, url, username, password, proxy=False, proxy_url=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {"username": username, "password": password}

    if proxy and proxy_url is not None:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
    else:
        proxies = {}

    session = requests.Session()
    html = session.post(login_url, headers=headers,
                        data=payload, proxies=proxies)
    return html.text


def login_webdav(login_url, username, password, proxy=False, proxy_url=None):
    headers = {"User-Agent": "Mozilla/5.0"}

    if proxy and proxy_url is not None:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
    else:
        proxies = {}

    html = requests.get(login_url, auth=(username, password),
                        headers=headers, proxies=proxies)
    return html.text


def load(url, crs_name):
    try:
        sh.wget("--reject", "html,htm", "--accept",
                "pdf,zip", "--no-parent", "-e", "robots=off",
                "--continue", "--no-host-directories", "--convert-links",
                "--cut-dirs=4", "--directory-prefix=" + crs_name, "--quiet",
                "--mirror", "--user-agent=\"\"", "--user=" + username,
                "--password=" + password, url)
    except sh.ErrorReturnCode_1:
        sys.exit(1)
    except sh.ErrorReturnCode_8:
        time.sleep(1)


def create_dir(directory, changedir=False):
    if not os.path.exists(directory):
        os.makedirs(directory)

    if changedir:
        change_dir(directory)


def change_dir(directory):
    if os.path.exists(directory):
        os.chdir(directory)


def set_course_info(html):
    regex = re.compile("crs_\d{1,8}")
    for crs in html("a", {"class": "il_ContainerItemTitle"}):
        match = re.search(regex, str(crs))
        if match:
            crs_id = match.group(0).replace("crs", "ref")
            crs_name = crs.string.replace(" ", "_").replace("/", "-")
            insert_sql_db(crs_name, crs_id)


def create_sql_db():
    state = False
    try:
        with conn:
            conn.execute(" \
                CREATE TABLE IF NOT EXISTS ilias ( \
                title TEXT NOT NULL, \
                crs_id INT, \
                UNIQUE (title, crs_id)) \
            ")
            state = True
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        conn.close()
    return state


def insert_sql_db(title, crs_id):
    try:
        with conn:
            conn.execute(" \
                INSERT INTO ilias (title, crs_id) \
                VALUES (?, ?)", (title, crs_id))
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        conn.close()


def show_sql_db():
    result = []
    try:
        with conn:
            result = conn.execute("SELECT * FROM ilias \
                                  ORDER BY title").fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        conn.close()
    return result


def main():
    if username and password:
        soup = BeautifulSoup(login(login_url, url, username,
                                   password, proxy, proxy_url))

        if create_sql_db():
            set_course_info(soup)
            create_dir(savepoint, True)
            for crs in show_sql_db():
                Thread(target=load, args=(webdav_url + crs[1], crs[0])).start()
    else:
        print("Please set username and password!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    else:
        getopts()
