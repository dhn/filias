#!/usr/bin/env python2
# $Id: main.py,v 1.0 2015/04/29 20:53:18 dhn Exp $
# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Dennis 'dhn' Herrmann
"""

import sys
import soap
import utils
import getopt
import logging

username = "deher003"
password = "1dHOHZCc"

url = "http://www.ilias.fh-dortmund.de/ilias/webservice/" + \
        "soap/server.php?wsdl"

def getopts():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f", ["fetch"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--fetch"):
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
            assert False, "unhandled option"


def usage():
    print("usage: %s [-f|--fetch]" % __file__)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    else:
        getopts()
