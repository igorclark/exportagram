import urllib2
import simplejson
import re
import mimetypes

from os.path import exists
from os import makedirs, sep
from sys import argv, exit

## construct url
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

while next_max_id:
	for i in data['data']:
		if i['caption']:
			caption = i['caption']['text']
		else:
			caption = ''

		location = dict()
		if i['location']:
			for el in ['latitude', 'longitude', 'name']:
				if i['location'].__contains__(el):
					location[el] = i['location'][el]
			
		p = {
			'id': i['id'],
			'caption': caption,
			'created_time': i['created_time'],
			'tags': i['tags'],
			'location': location,
			'images': [
				{'type': 'lo', 'url': i['images']['low_resolution']['url']},
				{'type': 'hi', 'url': i['images']['standard_resolution']['url']},
				{'type': 'th', 'url': i['images']['thumbnail']['url']}
			],
		}
		print "%s - %s" % (p['id'], p['caption'])
		img_dir = dl_dir + sep + p['id']
		if not exists(img_dir):
			makedirs(img_dir)

		json_file_path = img_dir + sep + p['id'] + '_json.txt'
		if not exists(json_file_path):
			with open(json_file_path, "w") as json_file:
				json_file.write(simplejson.dumps(p))

		for img in p['images']:
			img_file_path = img_dir + sep + p['id'] + '_' + img['type']
			match = re.compile(".*(?P<file_type>\.[a-z]+)$").match(img['url'])
			img_file_ext = None
			if match:
				img_file_ext = match.group('file_type')
				if exists(img_file_path + img_file_ext):
					continue

			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			response = opener.open(img['url'])

			if not img_file_ext:
				img_file_ext = mimetypes.guess_extension(response.info()['Content-Type'])
				if exists(img_file_path + img_file_ext):
					continue

			with open(img_file_path + img_file_ext, "wb") as img_file:
				img_file.write(response.read())


	new_url = url + "&max_id=" + next_max_id
	response = urllib2.urlopen(new_url)
	data = simplejson.loads(response.read())
	next_max_id = data['pagination']['next_max_id']

