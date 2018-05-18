from nlpindo.worder import Worder

with open('example.peterpan.txt', 'r') as f:
    text = f.read()

worder = Worder()
print(worder.word_count(text))
print()
print(worder.tokenize('halo kawan saya ini itu'))
print()
print(worder.word_count('pakan di feedernya tersangkut karena kebasahan dan kehujanan dan keseleo'))
