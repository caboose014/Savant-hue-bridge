#!/usr/bin/python
#     
#     'PhilipsHue'
#     Copyright (C) '2017'  Emersive Technologies Ltd
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse
import json
import urllib2
from time import sleep

parser = argparse.ArgumentParser(description='Savant - Hue Bridge')
parser.add_argument('-u', '--url',
                    help="URL for the API call",
                    type=str,
                    required=True)
parser.add_argument('-b', '--body',
                    help="Body for the request (i.e. JSON data) - Only required for control",
                    type=str,
                    required=False)
parser.add_argument('-s', '--scenes',
                    help="Return a list of scenes from the poll command",
                    action='store_true',
                    required=False)
args = parser.parse_args()
full_url = "http://%s" % args.url

if args.body:
    if "devicetype" in json.loads(args.body):
        result = json.loads(urllib2.urlopen(urllib2.Request(full_url, json.dumps(args.body))))[0]
        if result["error"]:
            print json.dumps({"error": {"description": result["error"]["description"]}})
        elif result["success"]["username"]:
            print json.dumps({"success": {"username": result["success"]["username"]}})
        else:
            print json.dumps(result)
        sleep(1)
    else:
        body = json.loads(args.body)
        if "bri" in body:
            if body['bri'] < 1:
                body['on'] = False
                body.pop('bri', None)
        request = urllib2.Request(full_url, json.dumps(body))
        request.get_method = lambda: 'PUT'
        print urllib2.urlopen(request).read()
else:
    returndata = json.loads(urllib2.urlopen(full_url).read())
    if args.url.endswith('lights'):
        for load in returndata:
            try:
                if not returndata[load]['state']['on']:
                    returndata[load]['state']['bri'] = 0
                    returndata[load]['state']['hue'] = 0
                    returndata[load]['state']['sat'] = 0
                print json.dumps({"light": {"num": load, "info": returndata[load]}})
                sleep(0.01)
            except KeyError:
                pass
    elif args.url.endswith('groups'):
        for load in returndata:
            try:
                if returndata[load]["type"] == "Room":
                    if not returndata[load]['action']['on']:
                        returndata[load]['action']['bri'] = 0
                        returndata[load]['action']['hue'] = 0
                        returndata[load]['action']['sat'] = 0
                    print json.dumps({"group": {"num": load, "info": returndata[load]}})
                    sleep(0.01)
            except KeyError:
                pass
    elif args.url.endswith('scenes'):
        for load in returndata:
            try:
                if len(returndata[load]["appdata"]) > 0:
                    print json.dumps({"scene": {"code": load, "info": {"name": returndata[load]["name"], "lights": ', '.join(returndata[load]["lights"])}}})
                    sleep(0.01)
            except KeyError:
                pass
    elif args.url.endswith('sensors'):
        for load in returndata:
            try:
                if returndata[load]["modelid"] == "SML001":
                    print json.dumps({"sensor": {"num": load, "info": {"name": returndata[load]["name"], "state": returndata[load]["state"]}}})
                    sleep(0.01)
            except KeyError:
                pass
    else:
        try:
            for load in returndata["lights"]:
                if not returndata["lights"][load]['state']['on']:
                    returndata["lights"][load]['state']['bri'] = 0
                    returndata["lights"][load]['state']['hue'] = 0
                    returndata["lights"][load]['state']['sat'] = 0
                print json.dumps({"light": {"num": load, "info": returndata["lights"][load]}})
                sleep(0.01)
        except KeyError:
            pass
        try:
            for load in returndata["groups"]:
                if returndata["groups"][load]["type"] == "Room":
                    if not returndata["groups"][load]['action']['on']:
                        returndata["groups"][load]['action']['bri'] = 0
                        returndata["groups"][load]['action']['hue'] = 0
                        returndata["groups"][load]['action']['sat'] = 0
                    print json.dumps({"group": {"num": load, "info": returndata["groups"][load]}})
                    sleep(0.01)
        except KeyError:
            pass
        if args.scenes:
            try:
                for load in returndata["scenes"]:
                    if len(returndata["scenes"][load]["appdata"]) > 0:
                        print json.dumps({"scene": {"code": load, "info": {"name": returndata["scenes"][load]["name"], "lights": ', '.join(returndata["scenes"][load]["lights"])}}})
                        sleep(0.01)
            except KeyError:
                pass
        try:
            for load in returndata["sensors"]:
                if returndata["sensors"][load]["modelid"] == "SML001":
                    print json.dumps({"sensor": {"num": load, "info": {"name": returndata["sensors"][load]["name"], "state": returndata["sensors"][load]["state"]}}})
                    sleep(0.01)
        except KeyError:
            pass

