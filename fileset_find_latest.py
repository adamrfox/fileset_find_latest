#!/usr/bin/python

import rubrik_cdm
import sys
import getopt
import getpass
import urllib3
import datetime
import pytz
urllib3.disable_warnings()

def usage():
    sys.stderr.write("Usage: fileset_find_latest.py [-hv] [-c creds] [-H host] cluster file\n")
    sys.stderr.write("-v | --verbose: Verbose output.  Includes the SnapshotID (for API)\n")
    sys.stderr.write("-c <creds> | --creds=<creds>: Specify cluster credentials. This is not secure\n")
    sys.stderr.write("\t\tcreds are in the form of user:password\n")
    sys.stderr.write("-H <host> | --host=<host>: Specify a host for the search\n")
    sys.stderr.write("-h | --help: Prints this message\n")
    sys.stderr.write("cluster: Name or IP of the cluster\n")
    sys.stderr.write("file: Filename (full or partial) to find\n")
    exit(0)

if __name__ == "__main__":
    filesets = []
    snapshots = []
    file = ""
    user = ""
    password = ""
    latest_time = {}
    latest_snap = {}
    latest_ts = {}
    host = {}
    fs_template = {}
    template = {}
    file_path = {}
    verbose = False
    server_host = ""


    optlist, args = getopt.getopt (sys.argv[1:], 'hc:vH:', ['help','creds=', 'verbose', 'host='])
    for opt, a in optlist:
        if opt in ('-h', "--help"):
            usage()
        if opt in ('-c', "--creds"):
            creds = a.split(':')
            (user, password) = creds
        if opt in ('-v', "--verbose"):
            verbose = True
        if opt in ('-H', "--host"):
            server_host = a
    rubrik_cluster = args[0]
    file = args[1]
    if user == "":
        user = raw_input("User: ")
    if password == "":
        password = getpass.getpass("Password: ")
    rubrik = rubrik_cdm.Connect(rubrik_cluster, user, password)
    cluster_info = rubrik.get('v1', '/cluster/me')
    cluster_tz = cluster_info['timezone']['timezone']
    fs_data = rubrik.get('v1', '/fileset')
    for x in fs_data['data']:
        if server_host == "" or server_host == x['hostName']:
            filesets.append(x['id'])
    for fs in filesets:
        endpoint = "/fileset/" + fs + "/search?path=" + file
        fs_search = rubrik.get('v1',str(endpoint))
        if fs_search['total'] > 0:
            del snapshots[:]
            for f in fs_search['data']:
                for v in f['fileVersions']:
                    snapshots.append(v['snapshotId'])
            latest_ts[fs] = 0
            for snap in snapshots:
                endpoint = "/fileset/snapshot/" + snap + "?verbose=false"
                snap_data = rubrik.get('v1', str(endpoint))
                snap_time = datetime.datetime.strptime(snap_data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                snap_time_utc = pytz.utc.localize(snap_time)
                snap_ts = int((snap_time - datetime.datetime(1970,1,1)).total_seconds())
                if snap_ts > latest_ts[fs]:
                    latest_snap[fs] = snap
                    file_path[fs] = f['path']
                    latest_time[fs] = snap_time_utc
                    latest_ts[fs] = snap_ts

    for x in latest_snap.keys():
        endpoint = "/fileset/" + x
        fs_info = rubrik.get('v1', str(endpoint))
        host[x] = fs_info['hostName']
        fs_template[x] = fs_info['templateId']
        endpoint = "/fileset_template/" + fs_template[x]
        fs_templateInfo = rubrik.get('v1',str(endpoint))
        template[x] = fs_templateInfo['name']
        latest_time_st = latest_time[x].astimezone(pytz.timezone(cluster_tz))
        print "Host: " + host[x]
        print "Fileset: " + template[x]
        print "Path: " + file_path[x]
        print "Backup date: " + str(latest_time_st)
        if verbose:
            print "Snapshot ID: " + latest_snap[x]
        print "========================================"

