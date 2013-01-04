import unittest
from mock import Mock, patch, mock_open
from social_bar_model import SocialBarModel
import os
import json

class TestSocialBarModel(unittest.TestCase):
    def setUp(self):
        self.test_object = SocialBarModel()
        self.test_object.LOCAL_FACEBOOK_FILE = '/tmp/.fb_access_token'
        self.test_object.USER_IMAGES_LOCATION = '/tmp/'
        self.test_object.LOCAL_IMAGES_LOCATION = '/tmp/'
        self.test_object.LOCAL_SETTINGS_FILE = '/tmp/.social_bar_settings'
        with open(self.test_object.LOCAL_FACEBOOK_FILE, "w") as f:
            f.write('abc')
        with open(self.test_object.LOCAL_SETTINGS_FILE, "w") as fi:
            fi.write('TBD')
    
    def tearDown(self):
        os.system('rm -f /tmp/.fb_access_token')
        os.system('rm -f /tmp/.social_bar_settings')
    
    def test_get_stored_fb_access_token(self):
        os.path.exists = Mock(return_value=False)
        self.assertEqual(None, self.test_object.get_stored_fb_access_token())
        os.path.exists = Mock(return_value=True)
        self.assertEqual('abc', self.test_object.get_stored_fb_access_token())
    
    def test_save_fb_access_token(self):
        token = ''
        self.assertFalse(self.test_object.save_fb_access_token(token))
        token = 'def'
        self.assertTrue(self.test_object.save_fb_access_token(token))
        self.assertEqual(token, self.test_object.get_stored_fb_access_token())
    
    def test_store_settings(self):
        settings = 'blah'
        self.test_object._store_setting(settings)
        with open(self.test_object.LOCAL_SETTINGS_FILE, 'r') as f:
            stored = f.read()
        self.assertEqual(settings, json.loads(stored))
    
    def test_get_stored_picture_file_path(self):
        self.assertEqual(self.test_object.USER_IMAGES_LOCATION + 'avatar', self.test_object.get_stored_picture_file_path())
    
    def test_get_no_picture_file_path(self):
        self.assertEqual(self.test_object.LOCAL_IMAGES_LOCATION + 'no_image.jpg', self.test_object.get_no_picture_file_path())
    
    def test_get_logout_on_shutdown_active(self):
        settings = {'logout_on_shutdown':True}
        
        with open(self.test_object.LOCAL_SETTINGS_FILE, "w") as fi:
            fi.write(json.dumps(settings))
        
        self.assertTrue(self.test_object.get_logout_on_shutdown_active())
        
        with open(self.test_object.LOCAL_SETTINGS_FILE, "r") as f:
            saved = json.loads(f.read())
        
        self.assertEqual(saved, settings)
        
        settings = {'logout_on_shutdown':False}
        
        with open(self.test_object.LOCAL_SETTINGS_FILE, "w") as fi:
            fi.write(json.dumps(settings))
        
        self.assertFalse(self.test_object.get_logout_on_shutdown_active())
        
        with open(self.test_object.LOCAL_SETTINGS_FILE, "r") as f:
            saved = json.loads(f.read())
        
        self.assertEqual(saved, settings)
    
    def test_set_logout_on_shutdown_active(self):
        state = True
        self.test_object.set_logout_on_shutdown_active(state)
        with open(self.test_object.LOCAL_SETTINGS_FILE, "r") as f:
            saved = json.loads(f.read())
        self.assertEqual(state, saved.get('logout_on_shutdown', False))
    
    def test_logout(self):
        self.test_object.logout()
        self.assertFalse(os.path.isfile(self.test_object.LOCAL_FACEBOOK_FILE))
    