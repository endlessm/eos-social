#!/usr/bin/env python
import urllib
import os
from social_bar_view import SocialBarView
from social_bar_presenter import SocialBarPresenter
from social_bar_model import SocialBarModel


class Global(object):
    quit = False
    @classmethod
    def set_quit(cls, *args, **kwargs):
        cls.quit = True


if __name__ == "__main__":
    SocialBarView.start_gtk_thread()

    uri = 'file://' + urllib.pathname2url(os.path.abspath('demo.xhtml'))
    view = SocialBarView.synchronous_gtk_message(SocialBarView)(
        uri, 
        quit_function=Global.set_quit
        )

    presenter = SocialBarPresenter(view, SocialBarModel())
    presenter.get_view().set_presenter(presenter)
    #presenter.get_view().main()
    presenter_main = SocialBarView.main_wraper(presenter.main, quit_obj=Global)
    presenter_main(quit_obj=Global)
    


