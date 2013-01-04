#!/usr/bin/env python
from social_bar_view import SocialBarView
from social_bar_presenter import SocialBarPresenter
from social_bar_model import SocialBarModel
from util.single_instance import DBusSingleAppInstance


if __name__ == "__main__":
    running = False
    try:
        running = DBusSingleAppInstance.is_running()
    except:
        pass
    if running:
        print "Social Bar already running!"
    else:
        presenter = SocialBarPresenter(SocialBarView(), SocialBarModel())
        presenter.get_view().set_presenter(presenter)
        presenter.get_view().main()

