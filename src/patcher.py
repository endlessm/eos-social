import urllib2
# Find a JSON parser
try:
    import simplejson as json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import json
_parse_json = json.loads
from facebook.facebook import GraphAPIError


#def put_video(self, file, message=None):
#    print 'put_video', repr(file), repr(message)

def put_video(self, video, message=None, **kwargs):
    """Uploads an video using multipart/form-data.
    video=File like object for the video
    message=Caption for your video

    """
    object_id = "me"
    #it would have been nice to reuse self.request;
    #but multipart is messy in urllib
    post_args = {
        'access_token': self.access_token,
        'source': video,
        'description': message,
    }
    post_args.update(kwargs)
    content_type, body = self._encode_multipart_form(post_args)
    req = urllib2.Request(("https://graph.facebook.com/%s/videos" %
                           object_id),
                          data=body)
    req.add_header('Content-Type', content_type)
    try:
        data = urllib2.urlopen(req).read()
    #For Python 3 use this:
    #except urllib2.HTTPError as e:
    except urllib2.HTTPError, e:
        data = e.read() # Facebook sends OAuth errors as 400, and urllib2
                         # throws an exception, we want a GraphAPIError
    try:
        response = _parse_json(data)
        # Raise an error if we got one, but don't not if Facebook just
        # gave us a Bool value
        if (response and isinstance(response, dict) and
                response.get("error")):
            raise GraphAPIError(response)
    except ValueError:
        response = data

    return response


def patch_facebook_graph_api(graph_api):
    graph_api.put_video = put_video

