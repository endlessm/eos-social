import urllib
import urllib2
import json
import httplib

def get_data(url):
    try:
        data = urllib2.urlopen(url).read()
        print 'DATA RETRIEVED:\n', data, '\n', '-'*80       
        return json.loads(data)
    except:
        return None

def fb_auth_url(app_id, redirect_url, permissions=None):
    parameters = {'client_id':app_id, 'redirect_uri':redirect_url}
    if permissions:
        parameters['scope'] = ','.join(permissions)
    encoded_parameters = urllib.urlencode(parameters)
    auth_url = 'http://graph.facebook.com/oauth/authorize?'
    auth_url += encoded_parameters
    return auth_url

def delete_like(token, post_id):
    conn = httplib.HTTPSConnection('graph.facebook.com')
    conn.request('DELETE', '/' + post_id + '/likes?access_token=' + token, '') 
    resp = conn.getresponse()
    content = resp.read()
    print content