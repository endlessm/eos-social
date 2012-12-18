import datetime
from math import floor

class FacebookPost:
    def __init__(self, data):
        self.id = data['id']
        self.poster = data['from']['name']
        self.poster_id = data['from']['id']
        self.poster_image = 'https://graph.facebook.com/' + data['from']['id'] + '/picture'
        self.image = ''
        self.subject = ''
        self.actions = {}
        self.likes = {}
        self.comments = {}
        
        if data.has_key('message'):
            text = data['message']
        elif data.has_key('story'):
            text = data['story']
        else:
            text = 'No text.'     # Can this happen? If so, internationalize or set to empty string!
        
        self.text = text
        
        if data.has_key('name'):
            self.subject = data['name']
        
        if data.has_key('picture'):
            self.image = data['picture']
        
        self.date_created = str(datetime.datetime.strptime(data['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))
        self.date_updated = str(datetime.datetime.strptime(data['updated_time'],'%Y-%m-%dT%H:%M:%S+0000'))
        self.time_elapsed = datetime.datetime.utcnow() - datetime.datetime.strptime(data['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
        self.time_elapsed_string = self.get_elapsed_string(self.time_elapsed)
        
        if data.has_key('actions'):
            self.actions = data['actions']
        
        if data.has_key('likes'):
            self.likes = data['likes']
        
        if data.has_key('comments'):
            self.comments = data['comments']
    
    def __str__(self):
        rv =  'id      : ' + self.id + '\n'
        rv += 'from    : ' + self.poster + '\n'
        rv += 'avatar  : ' + self.poster_image + '\n'
        rv += 'subject : ' + self.subject + '\n'
        rv += 'text    : ' + self.text + '\n'
        rv += 'image   : ' + self.image + '\n'
        rv += 'created : ' + self.date_created + '\n'
        rv += 'updated : ' + self.date_updated + '\n'
        rv += 'likes   : ' + unicode(self.likes) + '\n'
        rv += 'comments: ' + unicode(self.comments) + '\n'
        rv += 'actions : ' + unicode(self.actions) + '\n'
        rv += '-'*80
        return rv
    
    def get_elapsed_string(self, delta):
        if delta.days:
            return self.pluralize(delta.days, 'DAY')
        if int(floor(delta.seconds/3600)):
            return self.pluralize(int(floor(delta.seconds/3600)), 'HOUR')
        if int(floor(delta.seconds/60)):
            return self.pluralize(int(floor(delta.seconds/60)), 'MINUTE')
        return self.pluralize(delta.seconds, 'SECOND')
    
    def pluralize(self, num, period_name):
        if num == 1:
            return self.singular(num, period_name)
        else:
            return self.plural(num, period_name)
    
    def singular(self, num, period_name):
        if period_name == 'DAY':
            return str(num) + ' ' + 'day ago'
        if period_name == 'HOUR':
            return str(num) + ' ' + 'hour ago'
        if period_name == 'MINUTE':
            return str(num) + ' ' + 'minute ago'
        if period_name == 'SECOND':
            return str(num) + ' ' + 'second ago'
    
    def plural(self, num, period_name):
        if period_name == 'DAY':
            return str(num) + ' ' + 'days ago'
        if period_name == 'HOUR':
            return str(num) + ' ' + 'hours ago'
        if period_name == 'MINUTE':
            return str(num) + ' ' + 'minutes ago'
        if period_name == 'SECOND':
            return str(num) + ' ' + 'seconds ago'    
#    poster = 'ljuba'
#    avatar = 'http://facebook.com/ljuba.nedeljkovic.7/picture'
#    subject = 'Dummy subject'
#    text = 'Dummy text'
#    image = 'http://url.to.image.com/image.jpg'
#    date_created = '2012-12-9 11:25AM'
#    date_updated = '2012-12-9 11:25AM'