from collections import defaultdict

from imxInsights.exceptions import ImxException, exception_handler


class BuildExceptions:
    def __init__(self):
        self.exceptions: defaultdict[str, list[ImxException]] = defaultdict()

    def add(self, exception: ImxException, puic):
        if puic in self.exceptions:
            if exception.msg not in [msg.msg for msg in self.exceptions[puic]]:
                self.exceptions[puic].append(exception)
        else:
            self.exceptions[puic] = [exception]

    def handle_all(self):
        for exceptions in self.exceptions.values():
            for exception in exceptions:
                exception_handler.handle_exception(exception)
