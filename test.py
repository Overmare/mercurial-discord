import hooks
from mercurial import util

class Ctx:
    def branch(self):
        return b"default"

    def description(self):
        return ("Did a thing\nMercurial version is " + util.version().decode("utf-8")).encode("utf-8")

    def files(self):
        return [b"code.cpp"]

    def hex(self):
        return b"1234567890abcdef1234567890abcdef12345678"

    def user(self):
        return b"Anonymous"

class UI:
    def write(self, msg):
        print(msg.decode("utf-8"))

hooks.incoming(UI(), [Ctx()], 0)
print("Done")