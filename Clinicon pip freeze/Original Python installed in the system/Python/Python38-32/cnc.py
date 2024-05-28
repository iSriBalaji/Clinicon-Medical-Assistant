#!/usr/bin/python3
class JustCounter:
 __secretCount = 0
 def count(self):
  self.__secretCount += 1
  print(self.__secretCount)
counter = JustCounter()
counter.count()
counter.count()
print(_JustCounter.__secretCount)
