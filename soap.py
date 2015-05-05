# $Id: soap.py,v 1.0 2015/04/29 20:45:33 dhn Exp $
# -*- coding: utf-8 -*-

import re
import utils
import xml.etree.ElementTree as ET
from suds.client import Client


# Initial
def init(url, proxy=None):
    if proxy is not None:
        proxy_settings = dict(http=proxy, https=proxy)
        client = Client(url, proxy=proxy_settings)
    else:
        client = Client(url)

    client.options.location = url[0:len(url)-5]
    return client


# Login
def login(url, user, passwd, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)

    return connect.service.loginLDAP(client="ilias-fhdo",
                                     username=user, password=passwd)


# Logout
def logout(url, sid, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)

    if not connect.service.logout(sid=sid):
        print("Failed: Logout failed")


# Get User Id
def getUserId(url, sid, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)

    return connect.service.getUserIdBySid(sid=sid)


# Get all Course Id's
def getCourseIds(url, sid, uid, proxy, proxy_url):
    course = []
    regex = re.compile('il_crs_member_\d{1,8}')
    connect = utils.setProxy(url, proxy, proxy_url)
    xml = connect.service.getUserRoles(sid=sid, user_id=uid)

    for crs in ET.fromstring(xml):
        match = re.search(regex, str(crs[0].text))
        if match:
            course.append(match.group(0)[14:])

    return course


# Get all XML Objects: File, Size, Last Change etc.
def getCourseObjects(url, sid, ref_id, uid, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)

    return connect.service.getXMLTree(sid=sid, ref_id=ref_id,
                                      types="", user_id=uid)


# Get Ref Id by obj_id: return values -> array
def getRefIdByObjId(url, sid, obj_id, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)
    object_id = str(connect.service.getRefIdsByObjId(sid, obj_id))

    return object_id.replace("[", "").replace("]", "")
    # return init(url).service.getRefIdsByObjId(sid, obj_id)


# Get Object Id by ref_id: return values -> array
def getObjIdsByRefIds(url, sid, ref_id, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)

    return connect.service.getObjIdsByRefIds(sid=sid, ref_id=ref_id)


# Get Exercise
def getExercise(url, sid, ref_id, mode, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)

    return connect.service.getExerciseXML(sid=sid, ref_id=ref_id,
                                          attachment_mode=mode)


# Get Tree Childs
def getTreeChilds(url, sid, ref_id, uid, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)
    return connect.service.getTreeChilds(sid=sid, ref_id=ref_id,
                                         types="", user_id=uid)


# Get the File
# attachment_mode:
# 0 - no file contents
# 1 - plain content (base64encoded)
# 2 - zlib + base64
# 3 - gzip + base64)
def getFile(url, sid, ref_id, mode, proxy, proxy_url):
    connect = utils.setProxy(url, proxy, proxy_url)
    xml = connect.service.getFileXML(sid=sid, ref_id=ref_id,
                                     attachment_mode=mode)

    root = ET.fromstring(xml)
    return root.find('Content').text
