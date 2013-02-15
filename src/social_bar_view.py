import gtk
import gobject
from facebook.fb_auth_view import FBAuthView
from ui import MainWindow
from ui import SimplePopUp
import webkit
from ui import PostMessage
from ui import PostMessageSendArea
import os
from ui import UserAvatar
from ui import WelcomePanel
from ui import MultiPanel
from ui import UserProfileMenu
from ui import LogoutLabel
from ui import UserNameLabel
import gettext
import time
from settings import Settings
from ui import SelectDialog
import os
from ui import ErrorDialog
import json

gettext.install('eos-social', '/usr/share/locale', unicode=True, names=['ngettext'])

ALT = '<Alt>'

class SocialBarView(MainWindow):
    

    def __init__(self):
        super(SocialBarView, self).__init__()
        self.connect('destroy', self._destroy)
        self._presenter = None
        self.set_title(Settings.MAIN_WINDOW_TITLE)
        super(SocialBarView, self).set_ignore_win_names(Settings.IGNORE_WIN_NAMES)

    def create_shortcuts(self, accelgroup=gtk.AccelGroup()):
        for hotkey, modifier, callback in self._shortcuts:
            key, modifier = gtk.accelerator_parse(modifier + hotkey)
            accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, callback)
        self.add_accel_group(accelgroup)

    def set_presenter(self, presenter):
        super(SocialBarView, self).set_background_image('/usr/share/eos-social/images/bg-right.png')
        self._presenter = presenter
        self._create()

    def _create(self):
        self._browser = webkit.WebView()
        self._browser.connect("navigation-requested", self._navigation_handler)
        self._shortcuts = [('Left', ALT, lambda a, widget, c, m: self._browser.go_back()),
                           ('Right', ALT, lambda a, widget, c, m: self._browser.go_forward())]
        self.create_shortcuts()
        self.post_message_area = PostMessageSendArea()
        self.user_avatar_menu = UserProfileMenu(self._presenter)
        self.user_avatar_menu.connect('user-profile-action', self._on_action)
        self.user_name = UserNameLabel(self._presenter.get_profil_display_name())
        self.user_name.connect('user-name-action', self._on_action)
        self.user_name.connect("size-allocate", self._user_name_size_request)
        self.logout = LogoutLabel('x Logout')
        self.logout.connect('logout-label-action', self._on_action)
        self.user_avatar = UserAvatar(self.user_avatar_menu)
        self.user_avatar.set_presenter(self._presenter)
        self.post_message_area.connect('post-panel-action', self._on_action)
        self.post_message = PostMessage(self.post_message_area, self.user_avatar, self.user_name, self.logout)
        self.post_message.connect('post-panel-action', self._on_action)
        self._browser.connect('button_press_event', lambda w, e: self.post_message._on_click(self, e))

        self.main_container = gtk.ScrolledWindow()
        #self.main_container.pack_start(self.post_message, expand=False, fill=False, padding=0)
        self.main_container.add(self._browser)

        self.welcome_panel = WelcomePanel()
        self.welcome_panel.connect('welcome-panel-action', self._on_action)
        self.wraper_main = MultiPanel()
        self.wraper_main.add_panel(self.main_container, 'main_container')
        #self.wraper_main.add_panel(self.welcome_panel, 'welcome_panel')
        self.add(self.wraper_main)
        self.show_all()
        
        self._browser.load_uri('http://m.facebook.com')

        if self._presenter.is_user_loged_in():
            self.wraper_main.show_panel('main_container')
            self._perform_login()
        else:
            self.wraper_main.show_panel('welcome_panel')
            #self.show_delayed()
        self.logout.hide()
        self.user_name.hide()

    def _user_name_size_request(self, widget, allocation):
        x = self.user_avatar.allocation.x - self.user_name.allocation.width - 8
        y = self.user_name.allocation.y
        self.post_message.toolbar.move(self.user_name, x, y)

    def expand_text_field(self):
        vadjust = self.post_message_area.text_area.get_vadjustment()
        offset = int(vadjust.get_value())
        h = self.post_message_area.allocation.height
        new_h = h + offset
        if new_h < 100:
            new_h = 100
        main_h = self.post_message.allocation.height + offset
        if main_h < self.post_message.COLLAPSED_HEIGHT:
            main_h = self.post_message.COLLAPSED_HEIGHT
        self.post_message.set_size_request(400, main_h)
        self.post_message_area.set_size_request(400, new_h)
        self.post_message_area.text_area.set_size_request(400, new_h)

    def show_error_dlg(self):
        self.freeze()
        err_dlg = ErrorDialog()
        err_dlg.set_title(Settings.ERROR_DIALOG_TITLE)
        state = self.get_current_state()
        if state is not None:
            err_dlg.run(state.x, state.y, state.width, Settings.ERROR_DIALOG_HEIGHT)
            err_dlg.destroy()
        self.unfreeze()

    def _on_avatar_action(self):
        if self.user_avatar.get_is_expanded():
            self._presenter.show_profil_page()
            self.user_avatar.set_is_expanded(False)
            self.logout.hide()
            self.user_name.hide()
        else:
            self.user_avatar.set_is_expanded(True)
            x = self.user_avatar.allocation.x - self.user_name.allocation.width - 8
            y = self.user_name.allocation.y
            self.post_message.toolbar.move(self.user_name, x, y)
            x = self.user_avatar.allocation.x - self.logout.allocation.width - 8
            y = self.logout.allocation.y
            self.post_message.toolbar.move(self.logout, x, y)
            self.logout.show()
            self.user_name.show()

    def _on_post_action(self):
        self.post_message.toggle_text_field()
        self.post_message_area.set_default_text()
        self.post_message_area.set_selected_file_path(None)

    def _on_cancel_action(self):
        self.post_message.collapse_text_field()
        self.post_message_area.set_default_text()
        self.post_message_area.set_selected_file_path(None)

    def _on_close_action(self):
        self.hide()

    def _is_success(self, ret):
        try:
            status = json.loads(ret)
            code = status.get('code', 1)
            if code == 0:
                return True
        except:
            from traceback import format_exc
            print format_exc()
        return False

    def _on_send_action(self):
        text = self.post_message_area.get_post_message()
        selected_file = self.post_message_area.get_selected_file_path()
        selected_file_type = self.post_message_area.get_selected_file_type()
        if selected_file_type == 'image':
            ret = self._presenter.upload_image(selected_file, text)
            if not self._is_success(ret):
                self.show_error_dlg()
        elif selected_file_type == 'video':
            ret = self._presenter.upload_video(selected_file, text)
            if not self._is_success(ret):
                self.show_error_dlg()
        else:
            if text is not None:
                self._presenter.post_to_fb(text)
        self.post_message_area.clear_text(True)
        self.post_message_area.set_selected_file_path(None)
        self.post_message.collapse_text_field()

    def _on_user_name_action(self):
        self._presenter.show_profil_page()
        self.user_avatar.set_is_expanded(False)
        self.logout.hide()
        self.user_name.hide()

    def _on_user_profile_action(self):
        self._presenter.show_profil_page()

    def _on_login_action(self):
        self._perform_login()

    def _on_logout_on_shutdown_active_action(self):
        self._presenter.set_logout_on_shutdown_active(True)

    def _on_logout_on_shutdown_inactive_active(self):
        self._presenter.set_logout_on_shutdown_active(False)

    def _on_logout_action(self):
        self.user_avatar.set_is_expanded(False)
        self.logout.hide()
        self.user_name.hide()
        self.wraper_main.show_panel('welcome_panel')
        self._presenter.logout()

    def _on_post_msg_changed(self):
        self.expand_text_field()
        text = self.post_message_area.get_post_message()
        selected_file = self.post_message_area.get_selected_file_path()
        if (text is not None) or (selected_file is not None):
            self.post_message_area.enable_posting()
        else:
            self.post_message_area.disable_posting()

    def _on_image_upload(self):
        def _callback(file_path):
            text = self.post_message_area.get_post_message()
            self.post_message_area.set_selected_file_path(file_path, type='image')
            self._on_post_msg_changed()
        select_dialog = SelectDialog(success_callback=_callback)
        select_dialog.set_title(Settings.SELECT_DIALOG_TITLE)
        select_dialog.filter(
          Settings.SELECT_IMAGE_DIALOG_FILTER_NAME, 
          Settings.SELECT_IMAGE_DIALOG_FILTER
          )
        select_dialog.run()
        select_dialog.destroy()

    def _on_video_upload(self):
        def _callback(file_path):
            text = self.post_message_area.get_post_message()
            self.post_message_area.set_selected_file_path(file_path, type='video')
            self._on_post_msg_changed()
        select_dialog = SelectDialog(success_callback=_callback)
        select_dialog.set_title(Settings.SELECT_DIALOG_TITLE)
        select_dialog.filter(
          Settings.SELECT_VIDEO_DIALOG_FILTER_NAME,
          Settings.SELECT_VIDEO_DIALOG_FILTER
          )
        select_dialog.run()
        select_dialog.destroy()

    def _on_action(self, widget, action):
        if action == 'post':
            self._on_post_action()
        elif action == 'cancel':
            self._on_cancel_action()
        elif action == 'close':
            self._on_close_action()
        elif action == 'send':
            self._on_send_action()
        elif action == 'avatar':
            self._on_avatar_action()
        elif action == 'user-name':
            self._on_user_name_action()
        elif action == 'user_profile':
            self._on_user_profile_action()
        elif action == 'login':
            self._on_login_action()
        elif action == 'logout_on_shutdown_active':
            self._on_logout_on_shutdown_active_action()
        elif action == 'logout_on_shutdown_inactive':
            self._on_logout_on_shutdown_inactive_active()
        elif action == 'logout':
            self._on_logout_action()
        elif action == 'post_msg_changed':
            self._on_post_msg_changed()
        elif action == 'image_upload':
            self._on_image_upload()
        elif action == 'video_upload':
            self._on_video_upload()
        else:
            print 'no action ->', action

    def _perform_login(self):

        def _callback():
            self._presenter.get_fb_news_feed()
            self._presenter.get_profil_picture()
            file_path = self._presenter.get_stored_picture_file_path()
            self.user_avatar.set_avatar(file_path)
            self.user_name.set_text(self._presenter.get_profil_display_name())
            self.wraper_main.show_panel('main_container')

        if self._presenter.is_user_loged_in():
            _callback()
        else:
            self._presenter.fb_login(callback=_callback)
        #self.show_delayed()

    def show_popup_notification(self, notification_text):
        SimplePopUp(notification_text).show()
    
    def show_browser(self):
        self._browser.show()
    
    def load_html(self, html):
        self._browser.load_uri('http://m.facebook.com')
        #result = self._browser.load_string(html, 'text/html', 'utf-8', '')
        self.show_browser()
    
    def _navigation_handler(self, view, frame, request, data=None):
        #return self._presenter.navigator(request.get_uri())
        return False
    
    def _destroy(self, *args):
        gtk.main_quit()

    def main(self):
        gobject.threads_init()
        gtk.threads_init()
        gtk.main()

