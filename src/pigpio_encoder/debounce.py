from machine import Timer


def debounce(wait):
    """Postpone a functions execution until after some time has elapsed

    :type wait: int
    :param wait: The amount of Seconds to wait before the next call can execute.
    """

    def decorator(fun):
        class Debounced():
            tid = 10

            def __init__(self):
                self.run = True
                self.tid = Debounced.tid
                Debounced.tid += 1

            def __call__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

                if self.run:
                    self.call_it()

                self.run = False
                self.t = Timer(5)
                self.t.init(mode=Timer.ONE_SHOT, period=wait, callback=self.clear_run)

            def call_it(self):
                fun(*self.args, **self.kwargs)

            def clear_run(self, dummy):
                self.run = True

        return Debounced()

    return decorator
