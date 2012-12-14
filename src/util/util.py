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

CSS = '''@charset "utf-8";
/* CSS Document */

body {
background-image:url(bg.png) !important;
background-repeat:repeat;
}

.user img {
     -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    -moz-box-shadow: 1px 1px 6px 1px rgba(0, 0, 0, 0.3);
    -webkit-box-shadow: 1px 1px 6px 1px rgba(0, 0, 0, 0.3);
    box-shadow: 1px 1px 6px 1px rgba(0, 0, 0, 0.3);
    height: 32px;
  width: 32px;
}

.post-content {
    background: url("../images/divider.png") no-repeat #D5D5D5 !important;
    background-position: bottom !important;
    color: #000;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 12px;
    float:        left;
    padding:    10px;
    opacity:     0.85;
    -webkit-box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.45);
    -moz-box-shadow:    2px 2px 5px rgba(0, 0, 0, 0.45);
    box-shadow:         2px 2px 5px rgba(0, 0, 0, 0.45);
    border-radius:             5px;
    margin-bottom: 25px;
    -webkit-border-radius:     5px;
    -moz-border-radius:     5px;
    width: 250px !important;
}

.post-content span {
    color: #2e5790 !important;
    font-size: 13px;
    margin-bottom: 10px !important;
}

.post-content a {
  color: #2e5790;
    font-size: 11px;
    font-weight:bold;    
}

.imagecls img {
    border: solid 3px #fff;
    margin: 10px 0;
    max-width: 281px;    
}'''