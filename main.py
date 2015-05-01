#!/usr/bin/env python2
# $Id: main.py,v 1.1 2015/05/01 21:30:58 dhn Exp $
# -*- coding: utf-8 -*-

import sys
import soap
import utils
import getopt
import logging

__author__ = "Dennis 'dhn' Herrmann <dhn@4bit.ws>"
__version__ = "1.1-dev"
__copyright__ = "Copyright (c) 2015 Dennis 'dhn' Herrmann"
__license__ = "BSD"

savepoint = os.getenv("HOME") + "/ilias"
url = "http://www.ilias.fh-dortmund.de/ilias/webservice/" + \
        "soap/server.php?wsdl"


def getopts():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "fu:p:P:vh", ["fetch", "username=",
                                                 "password=", "proxy=",
                                                 "version", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    username = None
    password = None
    proxy = False
    proxy_url = None
    for opt, arg in opts:
        if opt in ("-f", "--fetch"):
            main(username, password, proxy, proxy_url)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-P", "--proxy"):
            proxy = True
            proxy_url = arg
        elif opt in ("-v", "--version"):
            version()
        elif opt in ("-h", "--help"):
            usage()
        else:
            assert False, "unhandled option"


def version():
    print("filias %s - %s" % (__version__, __copyright__))


def usage():
    print("usage: %s [options]" % __file__)
    print("   -f, --fetch           Fetch content from ILIAS Server.")
    print("   -u, --username=USER   Set ilias username to USER.")
    print("   -p, --password=PASS   Set ilias password to PASS.")
    print("   -P, --proxy [PROTOCOL://]HOST[:PORT] Use proxy on given port")
    print("   -h, --help            Show this help and exit.")
    print("   -v, --version         Show version info and exit.")


def main(username, password, proxy, proxy_url):
    if username and password:
        print("[*] Loggin into ILIAS...")
        session_id = soap.login(url, username, password)
        user_id = soap.getUserId(url, session_id)

        print("[*] Fetch all Course Information...")
        course = soap.getCourseIds(url, session_id, user_id)
        for ref_id in course:
            objects = soap.getCourseObjects(url, session_id, ref_id, user_id)
            utils.addMatchObjects(objects)
        
        print("[*] Create all Course name folders...")
        utils.createCourseNameFolder("./ilias")

        # utils.getAllFiles("./ilias", url, session_id)
        # soap.getExercise(url, session_id, ref_id, 1)
        # soap.getTreeChilds(url, session_id, ref_id, user_id)

        # Liefert die File: base64 encode!
        # content = soap.getFile(url, session_id, 388963, "1")
        # utils.writeFile("test.pdf", utils.base64decode(content))

        soap.logout(url, session_id)
    else:
        print("Please set username and password!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    else:
        getopts()
