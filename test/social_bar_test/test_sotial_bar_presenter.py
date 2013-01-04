import unittest
from mock import Mock
from social_bar_presenter import SocialBarPresenter
from facebook.facebook import GraphAPIError
from urllib2 import URLError
import subprocess
import webbrowser
import json
import simplejson

class TestSocialBarPresenter(unittest.TestCase):
    
    def setUp(self):
        self.model = Mock()
        self.view = Mock()
        self.dummy_fb_posts_result = [{'fql_result_set': [{'actor_id': 100000248582452L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 1579070479,
                                                                     'id': '100000248582452_532581543426794_99726789',
                                                                     'likes': 2,
                                                                     'post_fbid': 532636213421327L,
                                                                     'text': 'Pa i jesmo 8)',
                                                                     'text_tags': [],
                                                                     'time': 1356915462,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000248582452L,
                                                                     'id': '100000248582452_532581543426794_99726791',
                                                                     'likes': 1,
                                                                     'post_fbid': 532636300087985L,
                                                                     'text': 'Hahaha sa Bosnom se ne hvalim samo sa Republikom Srpskom, Srbijancu jedan :Ppp',
                                                                     'text_tags': [],
                                                                     'time': 1356915484,
                                                                     'user_likes': False},
                                                                    {'fromid': 100003530911621L,
                                                                     'id': '100000248582452_532581543426794_99726797',
                                                                     'likes': 1,
                                                                     'post_fbid': 532637696754512L,
                                                                     'text': 'Ne,ja sam iz Vojvodine,draga vaspitacice:-) Opasni ste,podrzavam takav stav!',
                                                                     'text_tags': [],
                                                                     'time': 1356915759,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000248582452L,
                                                                     'id': '100000248582452_532581543426794_99726824',
                                                                     'likes': 0,
                                                                     'post_fbid': 532642686754013L,
                                                                     'text': 'O izvinjavam se onda :DVojvodjaninu :PPP :DD',
                                                                     'text_tags': [],
                                                                     'time': 1356916742,
                                                                     'user_likes': False}],
                                                   'count': 9},
                                      'created_time': 1356908966,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 7,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532581543426794',
                                                'sample': [1075156666,
                                                           1584052844,
                                                           1731849671,
                                                           1187584108],
                                                'user_likes': True},
                                      'message': 'Kakva noc :))))',
                                      'permalink': 'http://www.facebook.com/jelena.baralic.7/posts/532581543426794',
                                      'post_id': '100000248582452_532581543426794',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356916742},
                                     {'actor_id': 1162122555,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356889835,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 3,
                                                'friends': [100000070471979L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=4568170439942',
                                                'sample': [1331425565],
                                                'user_likes': True},
                                      'message': '\'\'Muskarci kazu zenama da izgledaju bolje bez sminke, a onda flertuju s nekom nafrakanom kurvicom.Od toga zene stvarno posize."',
                                      'permalink': 'http://www.facebook.com/andjela.danas/posts/4568170439942',
                                      'post_id': '1162122555_4568170439942',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356889835},
                                     {'actor_id': 100000835512250L,
                                      'attachment': {'caption': '',
                                                     'description': '',
                                                     'fb_object_id': '100000835512250_1328563',
                                                     'fb_object_type': 'photo',
                                                     'icon': 'http://static.ak.fbcdn.net/rsrc.php/v2/yz/r/StEh3RhPvjk.gif',
                                                     'media': [{'alt': 'DEKIN UNUK MARKO!',
                                                                'href': 'http://www.facebook.com/photo.php?fbid=468568369847676&set=a.468568523180994.97114.100000835512250&type=1&relevant_count=1',
                                                                'photo': {'aid': '100000835512250_97114',
                                                                          'fbid': 468568369847676L,
                                                                          'height': 640,
                                                                          'images': [{'height': 640,
                                                                                      'src': 'http://sphotos-d.ak.fbcdn.net/hphotos-ak-ash4/s480x480/386730_468568369847676_678667523_n.jpg',
                                                                                      'width': 480}],
                                                                          'index': 1,
                                                                          'owner': 100000835512250L,
                                                                          'pid': '100000835512250_1328563',
                                                                          'width': 480},
                                                                'src': 'http://photos-d.ak.fbcdn.net/hphotos-ak-ash4/386730_468568369847676_678667523_s.jpg',
                                                                'type': 'photo'}],
                                                     'name': '',
                                                     'properties': []},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000835512250L,
                                                                     'id': '100000835512250_468568536514326_1205052',
                                                                     'likes': 3,
                                                                     'post_fbid': 468572096513970L,
                                                                     'text': u'Hvala Ljubo i Uro\u0161e fotografija je iz elitnog obdanista Primrose School of Midtown iz Atlante. Dekin veliki momak od 11 meseci.',
                                                                     'text_tags': [],
                                                                     'time': 1356632985,
                                                                     'user_likes': False},
                                                                    {'fromid': 1154645267,
                                                                     'id': '100000835512250_468568536514326_1206010',
                                                                     'likes': 0,
                                                                     'post_fbid': 468802523157594L,
                                                                     'text': 'Slobo on je isti ti.',
                                                                     'text_tags': [],
                                                                     'time': 1356685349,
                                                                     'user_likes': False},
                                                                    {'fromid': 1334716471,
                                                                     'id': '100000835512250_468568536514326_1206681',
                                                                     'likes': 0,
                                                                     'post_fbid': 468942066476973L,
                                                                     'text': 'Hahahaha,ajde kad ti kazes!!!',
                                                                     'text_tags': [],
                                                                     'time': 1356714829,
                                                                     'user_likes': False},
                                                                    {'fromid': 1334716471,
                                                                     'id': '100000835512250_468568536514326_1206711',
                                                                     'likes': 0,
                                                                     'post_fbid': 468949446476235L,
                                                                     'text': 'Nije ni bitno na koga lici bitno da je slatka bombona:-)',
                                                                     'text_tags': [],
                                                                     'time': 1356716361,
                                                                     'user_likes': False}],
                                                   'count': 4},
                                      'created_time': 1356632356,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 11,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=468568369847676',
                                                'sample': [1154645267,
                                                           100000294137413L,
                                                           1394576001,
                                                           100000682380114L],
                                                'user_likes': True},
                                      'message': 'DEKIN UNUK MARKO!',
                                      'permalink': 'http://www.facebook.com/photo.php?fbid=468568369847676&set=a.468568523180994.97114.100000835512250&type=1',
                                      'post_id': '100000835512250_468568536514326',
                                      'target_id': None,
                                      'type': 247,
                                      'updated_time': 1356716361},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 1758114957,
                                                                     'id': '100000278705228_532414723444480_90812071',
                                                                     'likes': 0,
                                                                     'post_fbid': 532429920109627L,
                                                                     'text': 'comment ',
                                                                     'text_tags': [],
                                                                     'time': 1356623845,
                                                                     'user_likes': False}],
                                                   'count': 1},
                                      'created_time': 1356621363,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532414723444480',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'status after changing profile',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/532414723444480',
                                      'post_id': '100000278705228_532414723444480',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356623845},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356619186,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 1,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532402510112368',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'test 3',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/532402510112368',
                                      'post_id': '100000278705228_532402510112368',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356619186},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000278705228L,
                                                                     'id': '100000278705228_532386923447260_90811766',
                                                                     'likes': 0,
                                                                     'post_fbid': 532388393447113L,
                                                                     'text': 'comment 1',
                                                                     'text_tags': [],
                                                                     'time': 1356616829,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000278705228L,
                                                                     'id': '100000278705228_532386923447260_90811767',
                                                                     'likes': 0,
                                                                     'post_fbid': 532388500113769L,
                                                                     'text': 'comment 2',
                                                                     'text_tags': [],
                                                                     'time': 1356616857,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000278705228L,
                                                                     'id': '100000278705228_532386923447260_90811769',
                                                                     'likes': 0,
                                                                     'post_fbid': 532388640113755L,
                                                                     'text': 'comment 3',
                                                                     'text_tags': [],
                                                                     'time': 1356616884,
                                                                     'user_likes': False},
                                                                    {'fromid': 100003810652435L,
                                                                     'id': '100000278705228_532386923447260_90811776',
                                                                     'likes': 0,
                                                                     'post_fbid': 532389170113702L,
                                                                     'text': 'comment 4',
                                                                     'text_tags': [],
                                                                     'time': 1356616979,
                                                                     'user_likes': False}],
                                                   'count': 4},
                                      'created_time': 1356616566,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 1,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532386923447260',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'test e2',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/532386923447260',
                                      'post_id': '100000278705228_532386923447260',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356616979},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356616509,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 1,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532386640113955',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'test e1',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/532386640113955',
                                      'post_id': '100000278705228_532386640113955',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356616509},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356615608,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532381973447755',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'test\n\nhttp://news.google.com/news/url?sa=t&ct2=us%2F0_6_g_1_0_t&gid=POP&bvm=section&usg=AFQjCNEUNyo3vzUMQB4RkuuQK9rAzjNuqQ&did=-7881807167661262117&cid=52778049356133&ei=sE3cUODBM4fh-Aalaw&rt=HOMEPAGE&vm=STANDARD&authuser=0&url=http%3A%2F%2Fwww.walesonline.co.uk%2Fnews%2Fuk-news%2F2012%2F12%2F27%2Fwinslet-marries-for-third-time-91466-32502955%2F',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/532381973447755',
                                      'post_id': '100000278705228_532381973447755',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356615608},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356615227,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=532378286781457',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': u'test\n\nAnyone who has seen \u201cOn the Waterfront\u201d knows East Coast longshoremen can be a tough bunch. Enlarge This Image. Librado Romero/The New York Times.\n\nhttp://www.youtube.com/watch?feature=player_embedded&v=lU_G7BF0xUg',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/532378286781457',
                                      'post_id': '100000278705228_532378286781457',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356615227},
                                     {'actor_id': 100000070471979L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000070471979L,
                                                                     'id': '100000070471979_536089769736701_6403801',
                                                                     'likes': 0,
                                                                     'post_fbid': 536105066401838L,
                                                                     'text': 'ajde caoooo',
                                                                     'text_tags': [],
                                                                     'time': 1356610897,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000168784972L,
                                                                     'id': '100000070471979_536089769736701_6403809',
                                                                     'likes': 1,
                                                                     'post_fbid': 536106436401701L,
                                                                     'text': 'Ahahaha. Cao. :P',
                                                                     'text_tags': [],
                                                                     'time': 1356611175,
                                                                     'user_likes': False},
                                                                    {'fromid': 1216637039,
                                                                     'id': '100000070471979_536089769736701_6404838',
                                                                     'likes': 1,
                                                                     'post_fbid': 536250296387315L,
                                                                     'text': 'Way to go babe!',
                                                                     'text_tags': [],
                                                                     'time': 1356630740,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000070471979L,
                                                                     'id': '100000070471979_536089769736701_6405256',
                                                                     'likes': 0,
                                                                     'post_fbid': 536295749716103L,
                                                                     'text': 'jeaa :D',
                                                                     'text_tags': [],
                                                                     'time': 1356638776,
                                                                     'user_likes': False}],
                                                   'count': 13},
                                      'created_time': 1356607273,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 26,
                                                'friends': [1579579346, 100002512076511L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=536089769736701',
                                                'sample': [100000181506612L,
                                                           100000111386462L],
                                                'user_likes': True},
                                      'message': 'ODLICAN (4.5) :D',
                                      'permalink': 'http://www.facebook.com/jovana.nedeljkovic.984/posts/536089769736701',
                                      'post_id': '100000070471979_536089769736701',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356638776},
                                     {'actor_id': 1244255466,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 1244255466,
                                                                     'id': '1244255466_10200193270054832_5890696',
                                                                     'likes': 1,
                                                                     'post_fbid': 10200193885870227L,
                                                                     'text': 'Znamo se. ;)',
                                                                     'text_tags': [],
                                                                     'time': 1356570276,
                                                                     'user_likes': False},
                                                                    {'fromid': 100001087246063L,
                                                                     'id': '1244255466_10200193270054832_5890698',
                                                                     'likes': 1,
                                                                     'post_fbid': 10200193887470267L,
                                                                     'text': 'A i njegov deo bas lici na mene :D',
                                                                     'text_tags': [],
                                                                     'time': 1356570297,
                                                                     'user_likes': False},
                                                                    {'fromid': 1244255466,
                                                                     'id': '1244255466_10200193270054832_5890703',
                                                                     'likes': 1,
                                                                     'post_fbid': 10200193889350314L,
                                                                     'text': u'Samo pre trojke, po\u0161to mi \u017ee\u0161\u0107e pada koncentracija. :D',
                                                                     'text_tags': [],
                                                                     'time': 1356570343,
                                                                     'user_likes': False},
                                                                    {'fromid': 1216637039,
                                                                     'id': '1244255466_10200193270054832_5910458',
                                                                     'likes': 1,
                                                                     'post_fbid': 10200220623778658L,
                                                                     'text': 'Veri najs',
                                                                     'text_tags': [],
                                                                     'time': 1356940364,
                                                                     'user_likes': False}],
                                                   'count': 10},
                                      'created_time': 1356560802,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 9,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=10200193270054832',
                                                'sample': [748072139,
                                                           1595440421,
                                                           100000554172694L,
                                                           1587145876],
                                                'user_likes': True},
                                      'message': u'- Koja re\u010d \u010dove\u010de, \u0161ta obja\u0161njava\u0161? Koja re\u010d jebote? Alo, koja re\u010d? Stani, alo, koja re\u010d?!\n- Pa "D" jebem te u usta bre!\n- \u0160ta "D" bre?!\n- Pa Pet Garet i Bili "D" Kid, \'s ti normalan bre?!\n- \'si ti normalan, pi\u010dka ti materina, jesmo rekli nema li\u010dnih imena?!',
                                      'permalink': 'http://www.facebook.com/kosta.beric/posts/10200193270054832',
                                      'post_id': '1244255466_10200193270054832',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356940364},
                                     {'actor_id': 100000070471979L,
                                      'attachment': {'caption': '',
                                                     'description': '',
                                                     'fb_object_id': '100000070471979_2190526',
                                                     'fb_object_type': 'photo',
                                                     'icon': 'http://static.ak.fbcdn.net/rsrc.php/v2/yz/r/StEh3RhPvjk.gif',
                                                     'media': [{'alt': 'I have a phone, nobody texts me, forever alone <3',
                                                                'href': 'http://www.facebook.com/photo.php?fbid=535223046490040&set=a.479852085360470.117951.100000070471979&type=1&relevant_count=1',
                                                                'photo': {'aid': '100000070471979_117951',
                                                                          'fbid': 535223046490040L,
                                                                          'height': 358,
                                                                          'images': [{'height': 96,
                                                                                      'src': 'http://photos-a.ak.fbcdn.net/hphotos-ak-ash3/533709_535223046490040_1019044536_s.jpg',
                                                                                      'width': 130},
                                                                                     {'height': 358,
                                                                                      'src': 'http://sphotos-a.ak.fbcdn.net/hphotos-ak-ash3/s480x480/533709_535223046490040_1019044536_n.jpg',
                                                                                      'width': 480}],
                                                                          'index': 1,
                                                                          'owner': 100000070471979L,
                                                                          'pid': '100000070471979_2190526',
                                                                          'width': 480},
                                                                'src': 'http://photos-a.ak.fbcdn.net/hphotos-ak-ash3/533709_535223046490040_1019044536_s.jpg',
                                                                'type': 'photo'}],
                                                     'name': '',
                                                     'properties': []},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100003405057307L,
                                                                     'id': '100000070471979_535844223094589_1776893',
                                                                     'likes': 2,
                                                                     'post_fbid': 535224129823265L,
                                                                     'text': u'ja znam da kuvam mnogo lepo majke mi,na\u0111ite mi nekog da se udajem :(',
                                                                     'text_tags': [],
                                                                     'time': 1356463528,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000070471979L,
                                                                     'id': '100000070471979_535844223094589_1776895',
                                                                     'likes': 1,
                                                                     'post_fbid': 535224269823251L,
                                                                     'text': 'hahah, ja bi tebe :D',
                                                                     'text_tags': [],
                                                                     'time': 1356463569,
                                                                     'user_likes': False},
                                                                    {'fromid': 100003405057307L,
                                                                     'id': '100000070471979_535844223094589_1776898',
                                                                     'likes': 0,
                                                                     'post_fbid': 535224486489896L,
                                                                     'text': u'sre\u0107o moja ute\u0161i me <3',
                                                                     'text_tags': [],
                                                                     'time': 1356463614,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000070471979L,
                                                                     'id': '100000070471979_535844223094589_1776902',
                                                                     'likes': 1,
                                                                     'post_fbid': 535224879823190L,
                                                                     'text': '<3',
                                                                     'text_tags': [],
                                                                     'time': 1356463679,
                                                                     'user_likes': False}],
                                                   'count': 4},
                                      'created_time': 1356560509,
                                      'description': u'Nedeljkovi\u0107 Jovana updated her cover photo.',
                                      'likes': {'can_like': True,
                                                'count': 15,
                                                'friends': [100000248582452L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=535223046490040',
                                                'sample': [1614502613,
                                                           100000181506612L,
                                                           100000757411429L],
                                                'user_likes': True},
                                      'message': '',
                                      'permalink': 'http://www.facebook.com/photo.php?fbid=535223046490040&set=a.479852085360470.117951.100000070471979&type=1&relevant_count=1',
                                      'post_id': '100000070471979_535844223094589',
                                      'target_id': None,
                                      'type': 373,
                                      'updated_time': 1356560509},
                                     {'actor_id': 100000070471979L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000070471979L,
                                                                     'id': '100000070471979_535745543104457_6401357',
                                                                     'likes': 0,
                                                                     'post_fbid': 535750796437265L,
                                                                     'text': u'ni Maja Simi\u0107 nece da spava, tako da NEMA NAMA SPAVANJA...ako ces ti da spavas to ne znaci da samo ja necu ;)',
                                                                     'text_tags': [{'id': 100000312288776L,
                                                                                    'length': 10,
                                                                                    'name': u'Maja Simi\u0107',
                                                                                    'offset': 3,
                                                                                    'type': 'user'}],
                                                                     'time': 1356545514,
                                                                     'user_likes': False},
                                                                    {'fromid': 100003026088050L,
                                                                     'id': '100000070471979_535745543104457_6401362',
                                                                     'likes': 1,
                                                                     'post_fbid': 535751979770480L,
                                                                     'text': 'a ok. . .',
                                                                     'text_tags': [],
                                                                     'time': 1356545664,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000312288776L,
                                                                     'id': '100000070471979_535745543104457_6401440',
                                                                     'likes': 1,
                                                                     'post_fbid': 535767083102303L,
                                                                     'text': 'Nema, nema. Ali nadoknadice se, i to DUPLO! :D',
                                                                     'text_tags': [],
                                                                     'time': 1356547910,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000070471979L,
                                                                     'id': '100000070471979_535745543104457_6401441',
                                                                     'likes': 1,
                                                                     'post_fbid': 535767353102276L,
                                                                     'text': 'tacno ;)',
                                                                     'text_tags': [],
                                                                     'time': 1356547941,
                                                                     'user_likes': False}],
                                                   'count': 7},
                                      'created_time': 1356544662,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 6,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=535745543104457',
                                                'sample': [100000181506612L,
                                                           1826480446,
                                                           100003697882056L,
                                                           100003962995236L],
                                                'user_likes': False},
                                      'message': 'NEMA NAMA SPAVANJAAAA...',
                                      'permalink': 'http://www.facebook.com/jovana.nedeljkovic.984/posts/535745543104457',
                                      'post_id': '100000070471979_535745543104457',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356547941},
                                     {'actor_id': 100000070471979L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356540797,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 7,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=535723126440032',
                                                'sample': [100000181506612L,
                                                           100003962995236L,
                                                           100001044896324L,
                                                           100003713998528L],
                                                'user_likes': False},
                                      'message': "I'm gonna find someone someday who might actually treat me well...",
                                      'permalink': 'http://www.facebook.com/jovana.nedeljkovic.984/posts/535723126440032',
                                      'post_id': '100000070471979_535723126440032',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356540797},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356535271,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531954820157137',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'logged in as  j.krsta@gmail.com',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531954820157137',
                                      'post_id': '100000278705228_531954820157137',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356535271},
                                     {'actor_id': 100000070471979L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100003713998528L,
                                                                     'id': '100000070471979_535672273111784_6400769',
                                                                     'likes': 1,
                                                                     'post_fbid': 535681706444174L,
                                                                     'text': u'idi u\u010di.ijoo',
                                                                     'text_tags': [],
                                                                     'time': 1356534473,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000070471979L,
                                                                     'id': '100000070471979_535672273111784_6400773',
                                                                     'likes': 0,
                                                                     'post_fbid': 535681836444161L,
                                                                     'text': 'ucim ja, ucim :P',
                                                                     'text_tags': [],
                                                                     'time': 1356534499,
                                                                     'user_likes': False},
                                                                    {'fromid': 100003713998528L,
                                                                     'id': '100000070471979_535672273111784_6400781',
                                                                     'likes': 1,
                                                                     'post_fbid': 535682239777454L,
                                                                     'text': 'vidim,vidim:p',
                                                                     'text_tags': [],
                                                                     'time': 1356534555,
                                                                     'user_likes': False}],
                                                   'count': 3},
                                      'created_time': 1356533172,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 13,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=535672273111784',
                                                'sample': [100000181506612L,
                                                           100003786505132L,
                                                           1241998226,
                                                           100003337832123L],
                                                'user_likes': True},
                                      'message': 'A mozda nas sudbina tek planira!',
                                      'permalink': 'http://www.facebook.com/jovana.nedeljkovic.984/posts/535672273111784',
                                      'post_id': '100000070471979_535672273111784',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356534555},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000278705228L,
                                                                     'id': '100000278705228_531910650161554_90808289',
                                                                     'likes': 0,
                                                                     'post_fbid': 531910856828200L,
                                                                     'text': 'good',
                                                                     'text_tags': [],
                                                                     'time': 1356529954,
                                                                     'user_likes': False}],
                                                   'count': 1},
                                      'created_time': 1356529911,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 1,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531910650161554',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': u'Chris Brown and Rihanna made sweet music yesterday in their own version of \u201cLove & Basketball.\u201d The on-again, off-again, on-again lovebirds were seated courtside at Staples Center in downtown Los Angeles for the Knicks-Lakers Christmas Day',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531910650161554',
                                      'post_id': '100000278705228_531910650161554',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356529954},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000278705228L,
                                                                     'id': '100000278705228_531892816830004_90808149',
                                                                     'likes': 1,
                                                                     'post_fbid': 531896730162946L,
                                                                     'text': 'video comment https://www.youtube.com/watch?feature=player_detailpage&v=vnvYymrCn4g',
                                                                     'text_tags': [],
                                                                     'time': 1356527733,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000278705228L,
                                                                     'id': '100000278705228_531892816830004_90808272',
                                                                     'likes': 0,
                                                                     'post_fbid': 531908940161725L,
                                                                     'text': 'http://www.youtube.com/watch?feature=player_detailpage&v=EFPosXIYGP0',
                                                                     'text_tags': [],
                                                                     'time': 1356529517,
                                                                     'user_likes': False}],
                                                   'count': 2},
                                      'created_time': 1356527103,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 2,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531892816830004',
                                                'sample': [],
                                                'user_likes': True},
                                      'message': 'video test\n\nhttps://www.youtube.com/watch?feature=player_detailpage&v=F9zT5VZKHI0',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531892816830004',
                                      'post_id': '100000278705228_531892816830004',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356529517},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [{'fromid': 100000278705228L,
                                                                     'id': '100000278705228_531892316830054_90808182',
                                                                     'likes': 1,
                                                                     'post_fbid': 531899673495985L,
                                                                     'text': 'image comment https://nt3.ggpht.com/news/tbn/px-YjDxVrrmt_M/11.jpg',
                                                                     'text_tags': [],
                                                                     'time': 1356528144,
                                                                     'user_likes': False},
                                                                    {'fromid': 100000278705228L,
                                                                     'id': '100000278705228_531892316830054_90808287',
                                                                     'likes': 0,
                                                                     'post_fbid': 531910320161587L,
                                                                     'text': 'http://www.benefitsofgreen-tea.com/images/benefits%20of%20green%20tea.jpg',
                                                                     'text_tags': [],
                                                                     'time': 1356529832,
                                                                     'user_likes': False}],
                                                   'count': 2},
                                      'created_time': 1356526998,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 1,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531892316830054',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'image test 2\n\nhttp://teacouncil.net/wp-content/uploads/2012/07/quantity-of-tea-Perfect-cup-of-tea.jpg',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531892316830054',
                                      'post_id': '100000278705228_531892316830054',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356529832},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356526831,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 2,
                                                'friends': [100000278705228L],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531891253496827',
                                                'sample': [],
                                                'user_likes': True},
                                      'message': 'endless image test\n\nhttp://a.abcnews.com/assets/images/v2/abcnews_logo_v2.png?v=1',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531891253496827',
                                      'post_id': '100000278705228_531891253496827',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356526831},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356526650,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531890160163603',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': "Survivors of a Christmas Day crash-landing of an airliner in Myanmar told terrifying tales of escape Wednesday as carrier Air Bagan said it had found the plane's black box and was investigating the accident that killed two people.\n\nhttp://a.abcnews.com//images/International/7c6a945af0e145aeb6a03ab906170fd7_mn.jpg",
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531890160163603',
                                      'post_id': '100000278705228_531890160163603',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356526650},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356526487,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531889223497030',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'http://news.cnet.com/8301-1023_3-57559921-93/amazon-the-five-biggest-stories-of-2012/',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531889223497030',
                                      'post_id': '100000278705228_531889223497030',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356526487},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356526411,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531888766830409',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': "MOBILE, Ala. - An enormous storm system that dumped snow and sleet on the nation's midsection and unleashed damaging tornadoes around the Deep South has begun punching its way toward the Northeast, slowing holiday travel.",
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531888766830409',
                                      'post_id': '100000278705228_531888766830409',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356526411},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356522820,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531871513498801',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'et 2',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531871513498801',
                                      'post_id': '100000278705228_531871513498801',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356522820},
                                     {'actor_id': 100000278705228L,
                                      'attachment': {'description': ''},
                                      'comments': {'can_post': True,
                                                   'can_remove': False,
                                                   'comment_list': [],
                                                   'count': 0},
                                      'created_time': 1356522791,
                                      'description': None,
                                      'likes': {'can_like': True,
                                                'count': 0,
                                                'friends': [],
                                                'href': 'http://www.facebook.com/browse/likes/?id=531871386832147',
                                                'sample': [],
                                                'user_likes': False},
                                      'message': 'et 1',
                                      'permalink': 'http://www.facebook.com/krsta.jovanovic.5/posts/531871386832147',
                                      'post_id': '100000278705228_531871386832147',
                                      'target_id': None,
                                      'type': 46,
                                      'updated_time': 1356522791}],
                  'name': 'posts'},
                 {'fql_result_set': [{'id': 100000248582452L,
                                      'name': 'Jelena Baralic',
                                      'pic': 'http://profile.ak.fbcdn.net/hprofile-ak-ash4/195265_100000248582452_1795006719_s.jpg',
                                      'pic_square': 'http://profile.ak.fbcdn.net/hprofile-ak-ash4/195265_100000248582452_1795006719_q.jpg'},
                                     {'id': 1162122555,
                                      'name': 'Andjela Danas',
                                      'pic': 'http://profile.ak.fbcdn.net/hprofile-ak-snc6/275602_1162122555_1128042646_s.jpg',
                                      'pic_square': 'http://profile.ak.fbcdn.net/hprofile-ak-snc6/275602_1162122555_1128042646_q.jpg'},
                                     {'id': 100000835512250L,
                                      'name': 'Aleksandar Mitic',
                                      'pic': 'http://profile.ak.fbcdn.net/hprofile-ak-prn1/23135_100000835512250_3916_s.jpg',
                                      'pic_square': 'http://profile.ak.fbcdn.net/hprofile-ak-prn1/23135_100000835512250_3916_q.jpg'},
                                     {'id': 100000278705228L,
                                      'name': 'Krsta Jovanovic',
                                      'pic': 'http://profile.ak.fbcdn.net/static-ak/rsrc.php/v1/yh/r/C5yt7Cqf3zU.jpg',
                                      'pic_square': 'http://profile.ak.fbcdn.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif'},
                                     {'id': 100000070471979L,
                                      'name': u'Nedeljkovi\u0107 Jovana',
                                      'pic': 'http://profile.ak.fbcdn.net/hprofile-ak-prn1/49865_100000070471979_461396874_s.jpg',
                                      'pic_square': 'http://profile.ak.fbcdn.net/hprofile-ak-prn1/49865_100000070471979_461396874_q.jpg'},
                                     {'id': 1244255466,
                                      'name': u'Kosta Beri\u0107',
                                      'pic': 'http://profile.ak.fbcdn.net/hprofile-ak-snc6/274196_1244255466_1945365338_s.jpg',
                                      'pic_square': 'http://profile.ak.fbcdn.net/hprofile-ak-snc6/274196_1244255466_1945365338_q.jpg'}],
                  'name': 'users'}]        
        
        self.test_object = SocialBarPresenter(model=self.model, view=self.view)
        self.mock_callback = Mock()
    
    def test_get_view(self):
        self.assertEqual(self.view, self.test_object.get_view())
    
    def test_get_model(self):
        self.assertEqual(self.model, self.test_object.get_model())
    
    def test_get_fb_news_feed(self):
        #success without callback
        self.test_object._graph_api.fql = Mock(return_value=self.dummy_fb_posts_result)
        self.test_object.parse_posts = Mock()
        self.test_object.render_posts_to_html = Mock()
        self.view.load_html = Mock()
        self.assertTrue(self.test_object.get_fb_news_feed())
        self.test_object.parse_posts.assert_called_once_with(self.dummy_fb_posts_result)
        self.test_object.render_posts_to_html.assert_called_once()
        self.test_object._view.load_html.assert_called_once()
        #success with callback
        self.assertEqual(None, self.test_object.get_fb_news_feed(self.mock_callback))
        self.mock_callback.assert_called_once()
        #GraphAPIError
        ex = GraphAPIError(Exception('Booom!'))
        ex.result = {}
        ex.result['error'] = {}
        ex.result['error']['code'] = 1
        self.test_object._graph_api.fql = Mock(side_effect=ex)
        self.test_object.oauth_exception_handler = Mock()
        self.assertEqual(None, self.test_object.get_fb_news_feed())
        self.test_object.oauth_exception_handler.assert_called_once_with(ex.result)
        #URLError
        self.test_object._graph_api.fql = Mock(side_effect=URLError(Exception('Booom!')))
        self.test_object.url_exception_handler = Mock()
        self.assertEqual(None, self.test_object.get_fb_news_feed())
        self.test_object.url_exception_handler.assert_called_once()
        #general Exception
        self.test_object._graph_api.fql = Mock(side_effect=Exception('Booom!'))
        self.assertEqual(None, self.test_object.get_fb_news_feed())

#        self.test_object._view.show_popup_notification = Mock()
#        self.test_object.fb_login = Mock()
#        self.assertEqual(None, self.test_object.get_fb_news_feed())
#        self.test_object.oauth_exception_handler.assert_called_once_with(ex.result)
    
    def test_fb_login(self):
        mp = Mock(subprocess.Popen)
        mp.stdout = ['FAILURE']
        self.assertEqual(None, self.test_object.fb_login())
        mp.stdout = ['ACCESS_TOKEN:abc']
        self.test_object.set_fb_access_token = Mock()
        self.test_object._fb_access_token = 'abc'
        self.assertNotEqual(None, self.test_object._graph_api)
        self.test_object.set_fb_access_token.assert_called_once()
        self.test_object.fb_login(self.mock_callback)
        self.mock_callback.assert_called_once()
    
    def test_post_to_fb(self):
        self.test_object.get_fb_news_feed = Mock()
        self.test_object._graph_api.put_wall_post = Mock()
        text = 'blah blah'
        result = self.test_object.post_to_fb(text)
        self.assertTrue(result)
        self.test_object._graph_api.put_wall_post.assert_called_once_with(text)
        self.test_object.get_fb_news_feed.assert_called_once()
        #GraphAPIError
        ex = GraphAPIError(Exception('Booom!'))
        ex.result = {}
        ex.result['error'] = {}
        ex.result['error']['code'] = 1
        self.test_object._graph_api.put_wall_post = Mock(side_effect=ex)
        self.test_object.oauth_exception_handler = Mock()
        self.assertFalse(self.test_object.post_to_fb(text))
        self.test_object.oauth_exception_handler.assert_called_once_with(ex.result)
        #URLError
        self.test_object._graph_api.put_wall_post = Mock(side_effect=URLError(Exception('Booom!')))
        self.test_object.url_exception_handler = Mock()
        self.assertFalse(self.test_object.post_to_fb(text))
        self.test_object.url_exception_handler.assert_called_once()
        #General Exception
        self.test_object._graph_api.put_wall_post = Mock(side_effect=Exception('Booom!'))
        self.assertFalse(self.test_object.post_to_fb(text))
    
    def test_post_fb_like(self):
        self.test_object._graph_api.put_like = Mock()
        pid = '123456'
        result = self.test_object.post_fb_like(pid)
        self.assertTrue(result)
        self.test_object._graph_api.put_like.assert_called_once_with(pid)
        #GraphAPIError
        ex = GraphAPIError(Exception('Booom!'))
        ex.result = {}
        ex.result['error'] = {}
        ex.result['error']['code'] = 1
        self.test_object._graph_api.put_like = Mock(side_effect=ex)
        self.test_object.oauth_exception_handler = Mock()
        self.assertFalse(self.test_object.post_fb_like(pid))
        self.test_object.oauth_exception_handler.assert_called_once_with(ex.result)
        #URLError
        self.test_object._graph_api.put_like = Mock(side_effect=URLError(Exception('Booom!')))
        self.test_object.url_exception_handler = Mock()
        self.assertFalse(self.test_object.post_fb_like(pid))
        self.test_object.url_exception_handler.assert_called_once()
        #General Exception
        self.test_object._graph_api.put_like = Mock(side_effect=Exception('Booom!'))
        self.assertFalse(self.test_object.post_fb_like(pid))
    
    def test_post_fb_comment(self):
        self.test_object._graph_api.put_comment = Mock()
        pid = '123456'
        text = 'blah blah'
        result = self.test_object.post_fb_comment(pid, text)
        self.assertTrue(result)
        self.test_object._graph_api.put_comment.assert_called_once_with(pid, text)
        #GraphAPIError
        ex = GraphAPIError(Exception('Booom!'))
        ex.result = {}
        ex.result['error'] = {}
        ex.result['error']['code'] = 1
        self.test_object._graph_api.put_comment = Mock(side_effect=ex)
        self.test_object.oauth_exception_handler = Mock()
        self.assertFalse(self.test_object.post_fb_comment(pid, text))
        self.test_object.oauth_exception_handler.assert_called_once_with(ex.result)
        #URLError
        self.test_object._graph_api.put_comment = Mock(side_effect=URLError(Exception('Booom!')))
        self.test_object.url_exception_handler = Mock()
        self.assertFalse(self.test_object.post_fb_comment(pid, text))
        self.test_object.url_exception_handler.assert_called_once()
        #General Exception
        self.test_object._graph_api.put_comment = Mock(side_effect=Exception('Booom!'))
        self.assertFalse(self.test_object.post_fb_comment(pid, text))
    
    def test_get_new_fb_posts(self):
        #success
        self.test_object._graph_api.fql = Mock(return_value=self.dummy_fb_posts_result)
        self.test_object.parse_posts = Mock()
        stamp = 123456
        self.assertNotEqual(None, self.test_object.get_new_fb_posts(callback=self.mock_callback, stamp=stamp))
        #GraphAPIError
        ex = GraphAPIError(Exception('Booom!'))
        ex.result = {}
        ex.result['error'] = {}
        ex.result['error']['code'] = 1
        self.test_object._graph_api.fql = Mock(side_effect=ex)
        self.test_object.oauth_exception_handler = Mock()
        self.assertEqual(None, self.test_object.get_new_fb_posts(callback=self.mock_callback, stamp=stamp))
        self.test_object.oauth_exception_handler.assert_called_once_with(ex.result)
        #URLError
        self.test_object._graph_api.fql = Mock(side_effect=URLError(Exception('Booom!')))
        self.test_object.url_exception_handler = Mock()
        self.assertEqual(None, self.test_object.get_new_fb_posts(callback=self.mock_callback, stamp=stamp))
        self.test_object.url_exception_handler.assert_called_once()
        #general Exception
        self.test_object._graph_api.fql = Mock(side_effect=Exception('Booom!'))
        self.assertEqual(None, self.test_object.get_new_fb_posts(callback=self.mock_callback, stamp=stamp))
        
    def test_set_fb_access_token(self):
        self.test_object._model.save_fb_access_token = Mock()
        token = 'abc'
        self.test_object.set_fb_access_token(token)
        self.assertEqual(token, self.test_object._fb_access_token)
        self.test_object._model.save_fb_access_token.assert_called_once_with(token)
    
    def test_oauth_exception_handler(self):
        result = {}
        result['error'] = {}
        result['error']['code'] = 1  #FB server error
        self.test_object._view.show_popup_notification = Mock()
        self.test_object.fb_login = Mock()
        self.test_object.oauth_exception_handler(result)
        self.test_object._view.show_popup_notification.assert_called_once()
        result['error']['code'] = 190  #Wrong token
        self.test_object.fb_login.assert_called_once()
    
    def test_url_exception_handler(self):
        self.test_object._view.show_popup_notification = Mock()
        self.test_object.url_exception_handler()
        self.test_object._view.show_popup_notification.assert_called_once()
    
    def test_navigator(self):
        like_uri = 'eossocialbar:LIKE?id=123456'
        comment_uri = 'eossocialbar:COMMENT?id=123456'
        view_post_uri = 'eossocialbar:VIEWPOST?url=http://www.facebook.com/123456'
        post_comment_uri = 'eossocialbar:POST_COMMENT?id=123456&comment_text=blah'
        view_poster_uri = 'eossocialbar:VIEW_POSTER?poster_id=123456'
        get_older_content_uri = 'eossocial:GET_OLDER_POSTS?url=123456'
        get_newer_content_uri = 'eossocial:GET_NEWER_POSTS:?url=123456'
        self.test_object.post_fb_like = Mock()
        self.test_object._view._browser.execute_script = Mock()
        webbrowser.open = Mock()
        self.test_object.display_comments = Mock()
        self.test_object.post_fb_comment = Mock()
        self.test_object.get_fb_news_feed = Mock()
        self.test_object.get_older_posts = Mock()
        
        result = self.test_object.navigator(like_uri)
        self.assertEqual(1, result)
        self.test_object.post_fb_like.assert_called_once_with('123456')
        self.test_object._view._browser.execute_script.assert_called_once()
        
        result = self.test_object.navigator(comment_uri)
        self.assertEqual(1, result)
        self.test_object.display_comments.assert_called_once_with({'id':['123456']})
        
        result = self.test_object.navigator(view_post_uri)
        self.assertEqual(1, result)
        webbrowser.open.assert_called_once_with('http://www.facebook.com/123456', new=1, autoraise=True)
        
        result = self.test_object.navigator(post_comment_uri)
        self.assertEqual(1, result)
        self.test_object.post_fb_comment.assert_called_once()
        self.test_object.get_fb_news_feed.assert_called_once()
        
        result = self.test_object.navigator(view_poster_uri)
        self.assertEqual(1, result)
        webbrowser.open.assert_called_with('http://www.facebook.com/123456', new=1, autoraise=True)
        
        result = self.test_object.navigator(get_older_content_uri)
        self.assertEqual(1, result)
        self.test_object.get_older_posts.assert_called_once()
        
        result = self.test_object.navigator(get_newer_content_uri)
        self.assertEqual(1, result)
        self.test_object.get_fb_news_feed.assert_called_once()
    
    def test_get_comments(self):
        pid = '123456'
        raw_comments = Mock()
        self.test_object._graph_api.request = Mock(return_value=raw_comments)
        self.assertEqual(raw_comments, self.test_object.get_commments(pid))
        self.test_object._graph_api.request.assert_called_once_with(pid+'/comments')
    
    def test_show_profile_page(self):
        profile = {'id':'123456'}
        webbrowser.open = Mock()
        self.test_object._graph_api.get_object = Mock(return_value=profile)
        self.test_object.show_profil_page()
        self.test_object._graph_api.get_object.assert_called_once()
        webbrowser.open.assert_called_once_with('http://www.facebook.com/123456')
    
    def test_get_profil_picture(self):
        profile = {'id':'123456'}
        self.test_object._graph_api.get_object = Mock(return_value=profile)
        self.test_object.get_image_dwn = Mock()
        self.test_object.get_profil_picture()
        self.test_object.get_image_dwn.assert_called_once_with('https://graph.facebook.com/123456/picture')
    
    def test_get_stored_picture_file_path(self):
        self.test_object._model.get_stored_picture_file_path = Mock()
        self.test_object.get_stored_picture_file_path()
        self.test_object._model.get_stored_picture_file_path.assert_called_once()
    
    def test_get_no_picture_file_path(self):
        self.test_object._model.get_no_picture_file_path = Mock()
        self.test_object.get_no_picture_file_path()
        self.test_object._model.get_no_picture_file_path.assert_called_once()
    
    def test_get_profile_display_name(self):
        profile = {'name':'John Doe'}
        self.test_object._graph_api.get_object = Mock(return_value=profile)
        self.assertEqual('John Doe', self.test_object.get_profil_display_name())
        self.test_object._graph_api.get_object.side_effect = Exception('Boom!')
        self.assertEqual('', self.test_object.get_profil_display_name())
    
    def test_get_logout_on_shutdown_active(self):
        self.test_object._model.get_logout_on_shutdown_active = Mock()
        self.test_object.get_logout_on_shutdown_active()
        self.test_object._model.get_logout_on_shutdown_active.assert_called_once()
    
    def test_set_logout_on_shutdown_active(self):
        state = True
        self.test_object._model.set_logout_on_shutdown_active = Mock()
        self.test_object.set_logout_on_shutdown_active(state)
        self.test_object._model.set_logout_on_shutdown_active.assert_called_once_with(state)
    
    def test_logout(self):
        self.test_object._model.logout = Mock()
        self.test_object.logout()
        self.assertEqual(None, self.test_object._fb_access_token)
        self.test_object._model.logout.assert_called_once()
    
    def test_parse_posts(self):
        result = self.test_object.parse_posts(self.dummy_fb_posts_result)
        self.assertEqual(len(self.dummy_fb_posts_result[0]['fql_result_set']), len(result.posts))
    
    def test_display_comments(self):
        q = {'id':['123456']}
        comments = {'data':['one', 'two', 'three', 'four', 'five']}
        self.test_object.get_commments = Mock(return_value=comments)
        self.test_object._view._browser.execute_script = Mock()
        script = 'show_comments(' + json.dumps(q['id'][0]) + ', ' + json.dumps(['two', 'three', 'four', 'five']) + ');'
        self.test_object.display_comments(q)
        self.test_object._view._browser.execute_script.assert_called_once_with(script)
    
    def test_get_older_posts(self):
        parsed = Mock()
        parsed.path = 'BLAH?url=123123'
        html = 'html'
        self.test_object.get_new_fb_posts = Mock(return_value=None)
        self.test_object.generate_posts_elements = Mock(return_value='html')
        self.assertEqual(None, self.test_object.get_older_posts(parsed))
        posts = Mock()
        posts.posts = ['one', 'two', 'three']
        posts.next_url = '123456'
        self.test_object.get_new_fb_posts = Mock(return_value=posts)
        self.test_object._view._browser.execute_script = Mock()
        script = 'show_older_posts(%s, %s);' % (simplejson.dumps(str(html)), simplejson.dumps(posts.next_url))
        self.test_object.get_older_posts(parsed)
        self.test_object._view._browser.execute_script.assert_called_once_with(script)
    
        
    