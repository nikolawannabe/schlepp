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

class SavedSession:
    key = ""
    secret = ""
    token = ""
    token_secret = ""
    def __init__(self, key, secret, token, token_secret):
        self.key = key
        self.secret = secret
        self.token = token
        self.token_secret = token_secret

def getPickledAccessToken():
    f = open(".schlepp.key")
    mySessionInfo = pickle.load(f)
    print "Successfully found your key."
    return mySessionInfo

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
    storedSession = SavedSession(dropbox_key, dropbox_secret, access_token.key, access_token.secret)
    pickle.dump(storedSession, f)
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
    SessionInfo = {}
    if (not(os.path.exists(".schlepp.key"))):
        print "Didn't find an access token.  Getting one for you."
        getFirstAccessToken()
    SessionInfo = getPickledAccessToken()
    print "Schlepping."
    sess = session.DropboxSession(SessionInfo.key, SessionInfo.secret,dropbox_access_type)
    sess.set_token(SessionInfo.token,SessionInfo.token_secret)
    client = client.DropboxClient(sess)
    f = open(uploadFile)
    response = client.put_file(uploadFile, f)
    print "Successfully uploaded.  Sharing."
    shareresponse = client.share(response['path'])
    print "Shared: ", shareresponse['url']


