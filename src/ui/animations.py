import gtk
import gobject
import math
import time


class Animator(object):


    def __init__(self, tick_interval):
        self.animations = set()
        self.tick_interval = tick_interval
        gobject.timeout_add(self.tick_interval, self._on_tick)

    def set_animation(self, animation):
        self.animations.add(animation)

    def _on_tick(self):
        for animation in self.animations:
            try:
                animation._tick()
            except:
                pass
        return True


class Animation(object):


    def __init__(self, duration):
        """ duration is in ms """

        self.duration = duration
        self.start_ts = None
        self._is_running = False

    def run(self, reverse=False):
        self.reverse = reverse
        self.start_ts = None
        self._is_running = True

    def stop(self):
        self._is_running = False

    def is_running(self):
        return self._is_running


class LinearAnimationStep(object):


    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self._is_called = False

    def __call__(self):
        try:
            self.callback(*self.args, **self.kwargs)
            self._is_called = True
        except:
            pass

    def clear(self):
        self._is_called = False

    def is_called(self):
        return self._is_called


class LinearAnimation(Animation):


    def __init__(self, duration, steps):
        super(LinearAnimation, self).__init__(duration)
        self.step_time = duration / len(steps)
        self.steps = steps
        self.first_step = steps[0]
        self.last_step = steps[len(steps)-1]

    def run(self, reverse=False):
        self.clear_steps()
        super(LinearAnimation, self).run(reverse)

    def clear_steps(self):
        for step in self.steps:
            step.clear()

    def _calc_step_index(self):
        now_ts = time.time()
        if self.start_ts is None:
            self.start_ts = now_ts
            step_index = 0
        else:
            elapsed_time = now_ts - self.start_ts
            step_index = int(elapsed_time*1000 / self.step_time)
        first_index = 0
        last_index = len(self.steps)-1
        if self.reverse:
            step_index = last_index - step_index
            if step_index < 0:
                return None
        if step_index < len(self.steps):
            return step_index
        return None

    def _tick(self):
        if not self.is_running():
            return
        step_index = self._calc_step_index()
        if step_index is not None:
            step = self.steps[step_index]
            if not step.is_called():
                step()
        else:
            self.stop()

