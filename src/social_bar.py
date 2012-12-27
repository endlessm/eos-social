#!/usr/bin/env python
from social_bar_view import SocialBarView
from social_bar_presenter import SocialBarPresenter
from social_bar_model import SocialBarModel


if __name__ == "__main__":
    presenter = SocialBarPresenter(SocialBarView(), SocialBarModel())
    presenter.get_view().set_presenter(presenter)
    presenter.get_view().main()

