#!/usr/bin/python
from dropbox import client, session
import pickle
import sys,os

dropbox_key = ""
dropbox_secret = ""
dropbox_token = ""
dropbox_token_secret = ""

dropbox_access_type = 'app_folder'
accessToken = {}

def getPickledAccessToken():
    f = open(".schlepp.key")
    accessToken = pickle.load(f)
    dropbox_token = accessToken.key
    dropbox_token_secret = accessToken.secret
    print "Successfully found your key."

def getFirstAccessToken():
    print "Enter your Dropbox Key: "
    dropbox_key = raw_input()
    print "Enter your Dropbox Secret: "
    dropbox_secret = raw_input()
    sess = session.DropboxSession(dropbox_key, dropbox_secret, dropbox_access_type)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    print "url:" + url
    print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
    raw_input()
    access_token = sess.obtain_access_token(request_token)
    #print "Where would you like to store your access token? [~/.schlepp]: "
    #filelocation = raw_input()
    filelocation = ""
    if (filelocation == ""):
        filelocation = ".schlepp.key"
    f = open(filelocation, 'w')
    pickle.dump(access_token, f)
    print "All done getting access token."

if __name__ == "__main__":
    uploadFile = ""
    if len(sys.argv) > 1:
        upLoadFile = sys.argv[1]
        print "I see you'd like to schlepp", uploadFile
    else:
        print "What file to schlepp?: ",
        uploadFile = raw_input()
    if (os.path.exists(uploadFile)):
        print "Good, I found your file."
    else:
        print "Looks like I can't find that file."
        sys.exit(1)
    try:
        getPickledAccessToken()
    except IOError:
        print "Didn't find an access token.  Getting one for you."
        getFirstAccessToken()
        getPickledAccessToken()
    print "Schlepping."
    sess = session.DropboxSession(dropbox_key, dropbox_secret,dropbox_access_type)
    sess.set_token(dropbox_token,dropbox_token_secret) 
    sess.set_token("blah","blaaaah") 
    f = open(uploadFile)
    response = client.put_file(uploadFile, f)
    print "uploaded: ", response
    shareresponse = client.share(response['path'])
    print "Shared: ", shareresponse.url


