import gtk
import math


class WindowAnimator(object):


    def __init__(self, window, start_alloc, end_alloc, callback, 
      animation_step, animation_time):
        self.window = window
        self.start_alloc = start_alloc
        self.end_alloc = end_alloc
        self.curr_alloc = gtk.gdk.Rectangle(start_alloc.x, start_alloc.y, 
          start_alloc.width, start_alloc.height)
        self.callback = callback
        self.animation_step = animation_step
        self.animation_time = animation_time

    def get_animation_time(self):
        return self.animation_time

    def _calc(self):
        delta_width = self.curr_alloc.width - self.end_alloc.width
        if math.fabs(delta_width) < self.animation_step:
            return True
        if delta_width < 0:
            self.curr_alloc.width += self.animation_step
            self.curr_alloc.x -= self.animation_step
        else:
            self.curr_alloc.width -= self.animation_step
            self.curr_alloc.x += self.animation_step
        return False

    def __call__(self):
        #print '__call__'
        if self._calc():
            print 'done'
            self.window.move(self.end_alloc.x, self.end_alloc.y)
            self.window.set_size_request(self.end_alloc.width, 
              self.end_alloc.height)
            if self.callback is not None:
                try:
                    self.callback()
                except:
                    pass
            return False
        else:
            self.window.move(self.curr_alloc.x, self.curr_alloc.y)
            self.window.set_size_request(self.curr_alloc.width, 
              self.curr_alloc.height)
            return True

