#!/bin/bash

# simple script to get the old faithful webcam picture via curl

OUTPUT_DIR=/Users/dchoi/Pictures/webcam

#TARGET_URL='https://www.nps.gov/webcams-yell/oldfaithvc.jpg'
TARGET_URL='https://www.nps.gov/webcams-yell/washburn2.jpg'
BATCHDATE=`date +%Y%m%d%H%M%S`

# Timestamp function used for logging
function TIMESTAMP() {
	echo `date '+%F %T'`
}

status=$(curl -s -o /dev/null -w "%{http_code}\n" ${TARGET_URL})

if [ "${status}" -ne 200 ];
then
	echo "`TIMESTAMP` - Unsuccessful; check URL";
else 
	# use curl to get picture
	curl ${TARGET_URL} > ${OUTPUT_DIR}/mt_washburn_${BATCHDATE}.jpg
	echo "`TIMESTAMP` - Picture downloaded"
fi


#curl https://www.nps.gov/webcams-yell/oldfaithvc.jpg > ${OUTPUT_DIR}/old_faithful_${BATCHDATE}.jpg

