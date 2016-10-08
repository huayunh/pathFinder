import pathFinder
# developed and test on python 2.7.9
# @author Huayun Huang

# 0 = safe
# anything else = not accessible
# the map is not necessarily a square
# but do not use space in the middle. Use 1 instead.
environment = ( # this is a 20*20 matrix
"""
00110000100000000000
00100111001000000000
00101000001000000000
00100000001000100000
00000000011001000000
00000000000100100000
00010000001001000000
00010000001001000000
00000010000001011110
00000100000001000000
00000100000000100000
00000100011110001000
00010000111000000000
00010001111111101111
00000011111101100000
00010000000010000000
00010000100000011000
00010000100011011000
00001000100011010000
00001000100011001111
"""
)

# coordinate on where they start
start, end = (19, 0), (0, 19)

# the smaller, the faster to find the path, and longer the path is.
# the bigger, the slower to find the path, and shorter the path is.
# This is just a general rule. But if you dare to put 60 here it is 
# just going to run forever.
# must be a positive integer. 
# suggested value: between 4 and 7. 
interval = 7

# find the path. Store the path into a list as tuples.
path = pathFinder.find(environment, start, end, interval)
print "final path"
# print the final map into the console
pathFinder.printMap(path, environment)
print path