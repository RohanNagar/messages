import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO

__author__ = "Raghav Sood"
__copyright__ = "Copyright 2014"
__credits__ = ["Raghav Sood"]
__license__ = "CC"
__version__ = "1.0"
__maintainer__ = "Raghav Sood"
__email__ = "raghavsood@appaholics.in"
__status__ = "Production"

if len(sys.argv) <= 1:
	print "Usage:\n 	python dumper.py [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
	print "Example conversation with Raghav Sood"
	print "	python dumper.py 1075686392 2000 0"
	sys.exit()

error_timeout = 30 # Change this to alter error timeout (seconds)
general_timeout = 7 # Change this to alter waiting time afetr every request (seconds)
messages = []
talk = sys.argv[1]
offset = int(sys.argv[3]) if len(sys.argv) >= 4 else int("0")
timestamp = int("0")
messages_data = "lolno"
end_mark = "\"payload\":{\"end_of_history\""
limit = int(sys.argv[2])
headers = {"origin": "https://www.facebook.com", 
"accept-encoding": "gzip,deflate", 
"accept-language": "en-US,en;q=0.8", 
"cookie": "datr=a9JFV0Rn4vKjLXV-0nY3AfkL; pl=n; lu=RAWIUyd4DsVN9gcaMOrId2BA; c_user=1399342159; xs=252%3AhbG69NXXhq3eRA%3A2%3A1466016537%3A16512; csm=2; s=Aa7Hxu8jtnnaKkAN.BXYbo1; sb=CqNhV11ZXAGauTp12_p6qJTt; p=-2; fr=0vYnIBsmW1NRk8H8E.AWW-75M4IrrNB_05ctxF6lrq2Uc.BXYaLp.bL.AAA.1.0.AWX8PqPn; act=1467050542773%2F1; presence=EDvF3EtimeF1467050594EuserFA21399342159A2EstateFDt2F_5b_5dElm2FnullEuct2F1467049921BEtrFA2loadA2EtwF3612772318EatF1467050585554EwmlFDfolderFA2inboxA2Ethread_5fidFA2user_3a609628589A2CG467050594573CEchFDp_5f1399342159F5CC; wd=882x805",
"pragma": "no-cache", 
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36", 
"content-type": "application/x-www-form-urlencoded", 
"accept": "*/*", 
"cache-control": "no-cache", 
"referer": "https://www.facebook.com/messages/zuck"}

base_directory = "Messages/"
directory = base_directory + str(talk) + "/"
pretty_directory = base_directory + str(talk) + "/Pretty/"

try:
	os.makedirs(directory)
except OSError:
	pass # already exists

try:
	os.makedirs(pretty_directory)
except OSError:
	pass # already exists

while end_mark not in messages_data:

	data_text = {"messages[user_ids][" + str(talk) + "][offset]": str(offset), 
	"messages[user_ids][" + str(talk) + "][limit]": str(limit), 
	"messages[user_ids][" + str(talk) + "][timestamp]": str(timestamp),
	"client": "web_messenger", 
	"__user": "1399342159", 
	"__a": "1", 
	"__dyn": "7AmajEzUGByFd112u6aOGeFxqeCwKyaF7By8VFLFwxBxCbzES2N6xybxu13wIwYxebkwy3eF8W49XDG4UiCxicxW6otz9UcXCxaFEW2PxOcxu5ocE88C9ADBy8K48hwCw", 
	"__req": "x", 
        "fb_dtsg": "AQEZoZsbSm7m:AQG_PSPcdHLd", 
	"ttstamp": "265816990111901159883109551095865817195808380991007276100", 
	"__rev": "2416037"}
	data = urllib.urlencode(data_text)
	url = "https://www.facebook.com/ajax/mercury/thread_info.php"
	
	print "Retrieving messages " + str(offset) + "-" + str(limit+offset) + " for conversation ID " + str(talk)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	compressed = StringIO.StringIO(response.read())
	decompressedFile = gzip.GzipFile(fileobj=compressed)
	
	
	outfile = open(directory + str(offset) + "-" + str(limit+offset) + ".json", 'w')
	messages_data = decompressedFile.read()
	messages_data = messages_data[9:]
	json_data = json.loads(messages_data)
	if json_data is not None and json_data['payload'] is not None:
		try:
			messages = messages + json_data['payload']['actions']
			timestamp = int(json_data['payload']['actions'][0]['timestamp']) - 1
		except KeyError:
			pass #no more messages
	else:
		print "Error in retrieval. Retrying after " + str(error_timeout) + "s"
		print "Data Dump:"
		print json_data
		time.sleep(error_timeout)
		continue
	outfile.write(messages_data)
	outfile.close()	
	command = "python -mjson.tool " + directory + str(offset) + "-" + str(limit+offset) + ".json > " + pretty_directory + str(offset) + "-" + str(limit+offset) + ".pretty.json"
	os.system(command)
	offset = offset + limit
	time.sleep(general_timeout) 

finalfile = open(directory + "complete.json", 'wb')
finalfile.write(json.dumps(messages))
finalfile.close()
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
os.system(command)
