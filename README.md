## EXPORTAGRAM

#### WHAT IS THIS?

This is a dirty hack, by a total Python newbie. It exports all your Instagram images, with a bit of metadata for each one, into a directory you specify.

#### PREREQUISITES

- Working Python installation with pip

Getting Python set up can be arseache, and explaining it is beyond the scope of this README. Google "install pip python" if you want to have a go. Once you have, you can go ahead and install:

- Python library: simplejson
- Instagram Python client: https://github.com/Instagram/python-instagram

#### TO GET IT WORKING YOU NEED:

- Access token & User ID for Instagram API

#### IF YOU DON'T ALREADY HAVE THOSE, YOU NEED:

- Working credentials for a registered Instagram API OAuth Client.

- If you have one of those already set up, get the credentials from http://instagram.com/developer/clients/manage/
- If you don't have one set up, create a new one at http://instagram.com/developer/clients/register/ - put anything into "Application Name", "Description" and "Website URL", just to keep the form happy, and put "http://localhost/" (without the quotes) into "OAuth redirect_uri", and press "Register". The page that comes back should give you Client ID, Client Secret, and the Redirect URI you typed in.

Once this is set up, you need to run this script:

	https://github.com/Instagram/python-instagram/blob/master/get_access_token.py

- Type in the Client ID & Client Secret when prompted.
- When it asks about "requested scope", hit space.
- Copy the long URL it gives you, paste it into your browser's location bar and hit enter. It'll take you the Instagram site to get an access token to let your export script get access.
- Follow the steps and hit "Allow". It'll send you to a URL like this:

	http://localhost/?code=&lt;hex_code&gt;

- Copy the &lt;hex_code&gt; bit and paste it back in to the still-running get_access_token.py script. It'll output something like this:

```python
('&lt;your.access.token.string&gt;', {'username': 'igorclark', 'bio': 'twitter/@igorclark', 'website': 'http://www.igorclark.net', 'profile_picture': 'http://images.instagram.com/profiles/profile_166735_75sq_1345748031.jpg', 'full_name': u'Igor Clark \ue00e', 'id': '&lt;your_user_id&gt;'})
```

You now have your user ID and access_token.

#### YOU CAN NOW RUN exportagram.py IN YOUR TERMINALLIKE SO:

	$ python exportagram.py <directory_to_download_images_to> <your_user_id> <your.access.token.string>

It'll create &lt;directory_to_download_images_to&gt; if it doesn't exist, and will make one directory for each image, containing lo-res/standard-res/thumbnail versions of the image and a JSON metadata file. It doesn't bother with comments or anything that links to other user accounts; it does get caption, tags, date, location and the images themselves.

This obviously doesn't get your pictures onto any other services, but it means you have a backup of them all in the event your Instagram account is closed or deleted or the service goes down or, you know, anything like that.


