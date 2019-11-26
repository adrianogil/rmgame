import txtgamelib

from txtgamelib import when, say

@when('test')
def test():
    # Method is handled before. So that line is not executed
    say("Test commands works!")

say('Testing say')

txtgamelib.start()

