# coding : -*- utf-8 -*-

import os
import shutil
import glob
import logging
import argparse
import datetime
import subprocess

# set up parser and logging
parser = argparse.ArgumentParser(description='YNP webcam post-processing')
parser.add_argument('--cam', dest='camera', help='specify camera to process')
parser.add_argument('--date', dest='date', help='specify date to process, YYYYMMDD')
args = parser.parse_args()

logging.basicConfig(filename='ynp_webcam_postproc.log',\
	format='%(asctime)s - %(message)s',\
	datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('ynp_webcam')
logger.setLevel(logging.INFO)

if not args.camera:
	target = 'oldfaithful'
else:
	target = args.camera

#yesterday = datetime.date.today() - datetime.timedelta(1)
#yesterday_str = yesterday.strftime('%Y%m%d')
today = datetime.date.today()
today_str = today.strftime('%Y%m%d')

if not args.date:
	target_date = today_str
else:
	target_date = args.date

#src_dir = '/Users/dchoi/Pictures/webcam/sandbox'
#stage_dir = '/Users/dchoi/Pictures/webcam/sandbox2'
#movie_dir = '/Users/dchoi/Pictures/webcam/sandbox2'
src_dir = '/home/dchoi/images'
stage_dir = '/home/dchoi/stage'
movie_dir = '/home/dchoi/movies'
gs_movie_path = 'gs://ynpwebcam/movies'
gs_image_path = 'gs://ynpwebcam/images'

#movie_dir = ''

logger.info('Creating time-lapse for ' + target + ' - ' + target_date)

logger.info('Clearing out stage directory')
#shutil.rmtree(stage_dir+'/*')
for file in os.listdir(stage_dir):
	file_path = os.path.join(stage_dir, file)
	try:
		if os.path.isfile(file_path):
			os.unlink(file_path)
	except Exception as e:
		print(e)

# copy files from pictures dir to staging dir
logger.info('Copying files to staging dir')
for file in glob.glob(src_dir+'/'+target+'_'+target_date+'*.jpg'):
	shutil.copy(file, stage_dir)

# run fdupes on stage dir
logger.info('de-duping files')
fdupes_cmd_list = ['fdupes', '-rdN', stage_dir]
fdupes_cmd = subprocess.call(fdupes_cmd_list)

if (fdupes_cmd != 0):
	logger.error('Error de-duping files')

# run ffmpeg
output_mpg_name = target + '_' + target_date + '.mp4'

logger.info('creating time-lapse')
ffmpeg_cmd_list = ['ffmpeg', '-pattern_type', 'glob', '-i', stage_dir+'/*.jpg', '-c:v',\
				   'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 
				   '-r', '18', movie_dir+'/'+output_mpg_name]
ffmpeg_cmd = subprocess.call(ffmpeg_cmd_list)

if (ffmpeg_cmd != 0):
	logger.error('Error creating movie')

logger.info('copying movie to gs bucket')
gsmovie_cmd_list = ['gsutil', 'cp', movie_dir+'/'+output_mpg_name, gs_movie_path+'/'+target]
gsmovie_cmd = subprocess.call(gsmovie_cmd_list)

if (gsmovie_cmd != 0):
	logger.error('Error copying to gs bucket')

logger.info('copying images to gs bucket')
gsimg_cmd_list = ['gsutil', '-m', 'mv', src_dir+'/'+target+'_'+target_date+'*.jpg', gs_image_path+'/'+target+'/'+target_date]
gsimg_cmd = subprocess.call(gsimg_cmd_list)

if (gsimg_cmd != 0):
	logger.error('Error moving images to gs bucket')

logger.info('post processing complete - ' + target + ' - ' + target_date)
