import hooks

class Ctx:
    def branch(self):
        return "default"

    def description(self):
        return "Did a thing\nhala hala hala burr durr twang"

    def files(self):
        return ["code.cpp"]

    def hex(self):
        return "1234567890abcdef1234567890abcdef12345678"

    def user(self):
        return "Anonymous"

class UI:
    def write(self, msg):
        print(msg)

hooks.incoming(UI(), [Ctx()], 0)
print("Done")