import httplib, urllib, logging, re, sys
import json
import argparse
import time
import socket
import pprint
from subprocess import check_output


def check_traffic():
    """
    query cl-netstat in json format and parse output to print interface output to DATABASE
    """

    header = 'traffic,host=leaf01'
    body = ''

    try:

        out = check_output("sudo cl-netstat -j", shell=True).strip()
        if out != '':
            json_out = json.loads(out)

            for key in json_out:
                line = ''
                line += ',interface=%s ' % str(key)
                # print key
                # print json_out[key]
                for value in json_out[key]:
                    #print value
                    if value == 'TX_OK':
                        #print json_out[key][value]
                        line += 'TX_OK=%s' % json_out[key]['TX_OK']
                    if value == 'RX_OK':
                        #print json_out[key][value]
                        line += ',RX_OK=%s\n' % json_out[key]['RX_OK']
                body += header + line

        else:
            print "Empty output: sudo cl-netstat -j"

    except:
        print "Broken command: sudo cl-netstat -j"

    return body

influx_server = "192.168.207.254"
influx_port = 8086

conn = httplib.HTTPConnection(influx_server, influx_port)
#params = urllib.urlencode({'db': 'mydb', 'u': 'root', 'p': 'cn321'})
params = urllib.urlencode({'db': 'mydb'})
headers = {
        'Content-Type': 'application/octet-stream',
        'User-Agent': 'cl-influxpush',
}
#body = 'temperature,host=switchA external=10,internal=5,outside=7,inside="TEST"'
#body = 'traffic,host=leaf01 interface=swp32,TX_OK=13991,RX_OK=3400'

while True:
    try:
        body = check_traffic()
        print body


        conn.request("POST", "/write?%s" % params, body, headers)
        resp = conn.getresponse()
        info ="%s, %s" % (resp.status, resp.reason)
        print info
    except:
        print "ERROR: Quitting application"

    time.sleep(5)


