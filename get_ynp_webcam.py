import logging
import urllib.request
import datetime
import os
import argparse

# set up parser and logging
parser = argparse.ArgumentParser(description='Scrape YNP webcam')
parser.add_argument('--cam', dest='camera', help='specify camera to scrape')
args = parser.parse_args()

logging.basicConfig(filename='ynp_webcam_scrape.log',\
	format='%(asctime)s - %(message)s',\
	datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('ynp_webcam')
logger.setLevel(logging.INFO)

if not args.camera:
	target = 'oldfaithful'
else:
	target = args.camera

#print(target)
if target not in ['oldfaithful', 'mtwashburn', 'electricpeak'] :
	logger.error('target not supported')
	exit(1)
	#raise ValueError

target_url_dict = { 'oldfaithful' : "https://www.nps.gov/webcams-yell/oldfaithvc.jpg", \
				'mtwashburn' : "https://www.nps.gov/webcams-yell/washburn2.jpg", \
				'electricpeak' : "https://www.nps.gov/webcams-yell/mammoth3.jpg"}

target_url = target_url_dict[target]

now = datetime.datetime.now()
now_str = now.strftime('%Y%m%d%H%M%S')

output_file_name = target + "_" + now_str + ".jpg"
fullfilename = os.path.join('/Users/dchoi/Dropbox/code/python/ynp_webcam/images',\
	output_file_name)

logger.info("Saving webcam image: " + target)
urllib.request.urlretrieve(target_url, fullfilename)