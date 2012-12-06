import datetime

class FacebookPost:
    def __init__(self, data):
        self.id = data['id']
        self.poster = data['from']['name']
        self.poster_image = 'http://www.facebook.com/' + data['from']['id'] + '/picture'
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
#    poster = 'ljuba'
#    avatar = 'http://facebook.com/ljuba.nedeljkovic.7/picture'
#    subject = 'Dummy subject'
#    text = 'Dummy text'
#    image = 'http://url.to.image.com/image.jpg'
#    date_created = '2012-12-9 11:25AM'
#    date_updated = '2012-12-9 11:25AM'