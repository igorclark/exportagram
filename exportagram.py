import urllib2
import simplejson
import re
import mimetypes
import datetime

from os.path import exists
from os import makedirs, sep
from sys import argv, exit

script, dl_dir, user_id, access_token = argv
url = "https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s&count=100" % (user_id, access_token)

if not exists(dl_dir):
	makedirs(dl_dir)

try:
	response = urllib2.urlopen(url)
except urllib2.HTTPError:
	print "HTTP error. Is the user_id and access_token correct?"
	exit(1)

data = simplejson.loads(response.read())
next_max_id = data['pagination']['next_max_id']

while True:
	for image in data['data']:
		if image['caption']:
			caption = image['caption']['text']
		else:
			caption = ''

		location = dict()
		if image['location']:
			for el in ['latitude', 'longitude', 'name']:
				if image['location'].__contains__(el):
					location[el] = image['location'][el]
			
		metadata = {
			'id': image['id'],
			'caption': caption,
			'created_time': image['created_time'],
			'tags': image['tags'],
			'location': location,
			'images': [
				{'type': 'lo', 'url': image['images']['low_resolution']['url']},
				{'type': 'hi', 'url': image['images']['standard_resolution']['url']},
				{'type': 'th', 'url': image['images']['thumbnail']['url']}
			],
		}
		ym = datetime.datetime.fromtimestamp(int(metadata['created_time'])).strftime('%Y' + sep + '%m' + sep + '%d')
		hms = datetime.datetime.fromtimestamp(int(metadata['created_time'])).strftime('%H-%M-%S')
		print "%s - %s" % (metadata['id'], metadata['caption'])
		img_dir = dl_dir + sep + ym + sep + hms + '_' + metadata['id']
		if not exists(img_dir):
			makedirs(img_dir)

		json_file_path = img_dir + sep + metadata['id'] + '_json.txt'
		if not exists(json_file_path):
			with open(json_file_path, "w") as json_file:
				json_file.write(simplejson.dumps(metadata))

		for imgdata in metadata['images']:
			img_file_path = img_dir + sep + metadata['id'] + '_' + imgdata['type']
			match = re.compile(".*(?P<file_type>\.[a-z]+)$").match(imgdata['url'])
			img_file_ext = None
			if match:
				img_file_ext = match.group('file_type')
				if exists(img_file_path + img_file_ext):
					continue

			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')] # just in case
			response = opener.open(imgdata['url'])

			if not img_file_ext:
				img_file_ext = mimetypes.guess_extension(response.info()['Content-Type'])
				if exists(img_file_path + img_file_ext):
					continue

			with open(img_file_path + img_file_ext, "wb") as img_file:
				img_file.write(response.read())

	if not next_max_id:
		break

	new_url = url + "&max_id=" + next_max_id
	response = urllib2.urlopen(new_url)
	data = simplejson.loads(response.read())
	if data['pagination'].__contains__('next_max_id'):
		next_max_id = data['pagination']['next_max_id']
	else:
		next_max_id = None

