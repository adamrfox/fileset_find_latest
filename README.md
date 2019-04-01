Fileset Find Latest
<p>
A script to find the latest version of a file from a fileset on Rubrik.
<p>
The idea behind this script is to help automate file recovery on Rubrik outside of the WebUI.  Most of the time a file
request is for the latest version of a file.  The Rubrik UI has a Google-like serach that allows an authorized user to 
find it quickly, but some Rubrik customers will want to automate this outside of the Rubrik UI.  Fortunately, Rubrik CDM
is an API-first archetecture so it is possible to do this using the API.
<p>
Syntax:
<p>
The syntax is as follows:
<p>
fileset_find_latest.py [-hv] [-c creds] [-H host] cluster file
<p>
-h | --help: This is the help and displays the syntax<p>
-v | --versose: This adds the snapshotID to the output.  This is useful to automate the recovery<p>
-c | --creds=<user:password>: This allows the Rubrik user and password to be entered on the CLI rather than being
prompted.  This is here for the sake of convience and is, obviously, not secure.  Use at your discretion. <p>
-H | --host=<hostname>: By default the script will search all filesets for the file.  This flag allows the search to be 
narrowed down to a particular host.  This can steamline the output.<p>
cluster:  This is the name of the Rubrik cluster<p>
file:  This is the name of the file or directory.  This can be a full or partial name
<p>
Here are some examples:<p>
<pre>$ ./fileset_find_latest.py -v 172.21.10.81 new_file
User: admin
Password: 
Host: \\ntap94.rangers.lab\app_test
Fileset: smb_all
Path: \new_file
Backup date: 2019-03-29 10:53:34-07:00
Snapshot ID: 53250340-cbc8-4477-9f93-d96b1a952196
========================================
Host: fox-isln-test.rangers.lab:/ifs/small_test
Fileset: all
Path: /new_file_on_new_host.txt
Backup date: 2019-04-01 00:01:36-07:00
Snapshot ID: eae416be-5385-4a40-b575-01f69d541120
========================================`</pre>
Notice here that it found 2 instances of files that contain "new_file" so it showed both options, each with their
location, path and the date of the last time each was backed up (using the timezone of the cluster).  The SnapshotID is 
there bceause I specified the -v flag But let's assume 
you only wanted to search ntap94, you could do this:
<p>
</pre>$ ./fileset_find_latest.py -v -H ntap94.rangers.lab 172.21.10.81 new_file
User: admin
Password: 
Host: \\ntap94.rangers.lab\app_test
Fileset: smb_all
Path: \new_file
Backup date: 2019-03-29 10:53:34-07:00
Snapshot ID: 53250340-cbc8-4477-9f93-d96b1a952196
========================================</pre>
By specifying the host on the commande line with -H only the results from the ntap94 host are displayed.



