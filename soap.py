# $Id: soap.py,v 1.0 2015/04/29 20:45:33 dhn Exp $
# -*- coding: utf-8 -*-

import utils, re, sys
import xml.etree.ElementTree as ET
from suds.client import Client

# Initial
def init(url):
    client = Client(url)
    client.options.location = url[0:len(url)-5]
    return client


# Login
def login(url, user, passwd):
    return init(url).service.loginLDAP(client="ilias-fhdo",
        username=user, password=passwd)


# Logout
def logout(url, sid):
    if not init(url).service.logout(sid=sid):
        print("Failed: Logout failed")
        

# Get User Id
def getUserId(url, sid):
    return init(url).service.getUserIdBySid(sid=sid)


# Get all Course Id's
def getCourseIds(url, sid, uid):
    course = []
    utils.fix_encoding()
    regex = re.compile('il_crs_member_\d{1,8}')
    xml = init(url).service.getUserRoles(sid=sid, user_id=uid)

    for crs in ET.fromstring(xml):
        match = re.search(regex, str(crs[0].text))
        if match:
            course.append(match.group(0)[14:])

    return course


# Get all XML Objects: File, Size, Last Change etc.
def getCourseObjects(url, sid, ref_id, uid):
    return init(url).service.getXMLTree(sid=sid, ref_id=ref_id,
            types="", user_id=uid)


# Get Ref Id by obj_id: return values -> array
def getRefIdByObjId(url, sid, obj_id):
    object_id = str(init(url).service.getRefIdsByObjId(sid, obj_id))
    return object_id.replace("[", "").replace("]", "")
    # return init(url).service.getRefIdsByObjId(sid, obj_id)


# Get Object Id by ref_id: return values -> array
def getObjIdsByRefIds(url, sid, ref_id):
    return init(url).service.getObjIdsByRefIds(sid=sid, ref_id=ref_id)


# Get Exercise
def getExercise(url, sid, ref_id, mode):
    return init(url).service.getExerciseXML(sid=sid, ref_id=ref_id,
            attachment_mode=mode)


# Get Tree Childs
def getTreeChilds(url, sid, ref_id, uid):
    return init(url).service.getTreeChilds(sid=sid, ref_id=ref_id,
            types="", user_id=uid)


# Get the File
# attachment_mode:
# 0 - no file contents
# 1 - plain content (base64encoded)
# 2 - zlib + base64
# 3 - gzip + base64)
def getFile(url, sid, ref_id, mode):
    xml = init(url).service.getFileXML(sid=sid, ref_id=ref_id,
            attachment_mode=mode)

    root = ET.fromstring(xml)
    return root.find('Content').text
