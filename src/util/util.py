import urllib2
import json

def get_data(url):
    try:
        data = urllib2.urlopen(url).read()
        print 'DATA RETRIEVED:\n', data, '\n', '-'*80       
        return json.loads(data)
    except:
        return None