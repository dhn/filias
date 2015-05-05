# $Id: utils.py,v 1.2 2015/05/05 07:21:54 dhn Exp $
# -*- coding: utf-8 -*-

import os
import sys
import sql
import soap
import base64
import xml.etree.ElementTree as ET


# Decode the base64 encoded files
def base64decode(content):
    return base64.b64decode(content)


# Write Content to File
def writeFile(filename, content):
    file_name = open(filename, "w")
    file_name.write(content)
    file_name.close()


# Set Proxy support
def setProxy(url, proxy, proxy_url):
    if proxy:
        connect = soap.init(url, proxy_url)
    else:
        connect = soap.init(url)

    return connect


# Create or Change Directory if folder is already exists
def create_dir(directory, changedir=False):
    if not os.path.exists(directory):
        os.makedirs(directory)

    if changedir:
        change_dir(directory)


# Change Directory
def change_dir(directory):
    if os.path.exists(directory):
        os.chdir(directory)


# Check if directory is empty
def isEmpty(directory):
    if os.listdir(directory):
        return True


# FIXME: Fix encoding
# The Content from ILIAS System (xml file)
# has to many unicode characters!
def fix_encoding():
    reload(sys)
    sys.setdefaultencoding('utf-8')


# Add and Match files/folders into SQL
def addMatchObjects(objects):
    fix_encoding()

    root = ET.fromstring(objects)
    for files in root:
        file_type = files.get('type')
        types = {"crs", "fold", "file"}

        # TODO: Add fileSize, fileExtension
        if file_type in types:
            title = files.find('Title').text
            last_update = files.find('LastUpdate').text
            obj_id = files.find('References').attrib['ref_id']

            # Set Course Parent Id to the obj_id
            if file_type in "crs":
                parent_id = obj_id
            else:
                parent_id = files.find('References').attrib['parent_id']

            file_size = ""

            if sql.create_db():
                sql.insert_into_db(title, obj_id, parent_id, last_update,
                                   file_size, file_type)


# Create CourseName folders
def createCourseNameFolder(savepoint):
    for crs_folder in sql.getCourseName():
        create_dir(savepoint + "/" + crs_folder[0])


# Get All Files
def getAllFiles(savepoint, url, session_id):
    for info in sql.getAllInformation():
        title = info[0]
        obj_id = info[1]
        parent_id = info[2]
        types = info[4]

        if types in "crs":
            print "%s" % title
        elif types in "fold":
            print "[%s]" % title
        elif types in "file":
            print "  %s" % title
