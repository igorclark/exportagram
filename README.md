This is a dirty hack by a total Python newbie to export all your Instagram images, with a bit of metadata for each one, into a directory you specify.

#### PREREQUISITES

- simplejson, urllib2
- Instagram Python client from https://github.com/Instagram/python-instagram

#### TO GET IT WORKING YOU NEED

- Access token & User ID for Instagram API
- Working credentials for a registered Instagram API OAuth Client.

- If you have one of those already set up, get the credentials from http://instagram.com/developer/clients/manage/
- If you don't have one set up, create a new one at http://instagram.com/developer/clients/register/ - put anything into "Application Name", "Description" and "Website URL", just to keep the form happy, and put "http://localhost/" (without the quotes) into "OAuth redirect_uri", and press "Register". The page that comes back should give you Client ID, Client Secret, and the Redirect URI you typed in.

Once this is set up, you need to run this script:

	https://github.com/Instagram/python-instagram/blob/master/get_access_token.py

- Type in the Client ID & Client Secret when prompted.
- When it asks about "requested scope", hit space.
- Copy the long URL it gives you, paste it into your browser's location bar and hit enter. It'll take you the Instagram site to get an access token to let your export script get access.
- Follow the steps and hit "Allow". It'll send you to a URL like this:

	http://localhost/?code=<hex_code>

- Copy the <hex_code> bit and paste it back in to the still-running get_access_token.py script. It'll output something like this:

('<your.access.token.string>', {'username': 'igorclark', 'bio': 'twitter/@igorclark', 'website': 'http://www.igorclark.net', 'profile_picture': 'http://images.instagram.com/profiles/profile_166735_75sq_1345748031.jpg',
 'full_name': u'Igor Clark \ue00e', 'id': '<your_user_id>'})

You now have your user ID and access_token. You can now run exportagram.py like so:

$ python exportagram.py <directory_to_download_images_to> <your_user_id> <your.access.token.string>

It'll create <directory_to_download_images_to> if it doesn't exist, and will make one directory for each image, containing lo-res/standard-res/thumbnail versions of the image and a JSON metadata file.
