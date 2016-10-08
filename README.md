# pathFinder
Given a map, a starting point and a finishing point, how to find the shortest path? 
Note: the map is not a graph. It is simply a matrix of string.

You can try the thing out either with pathFinder.py, or pathFinderMain.py. The first
one contains all the algorithms, with the main functions at the bottom. The second 
one is a wrapper. 

The thing generally works pretty well with a relatively open map. However if your 
map contains several rooms, the runtime is going to be longer. For example, if you
have a map like this: (1 = inaccessible, 0 = accessible)

00000000100000
00010000000000
00000000000000
11111110111111
00000010100000
00000000100000
00000110000000

Then it is going to take you longer to find a path than this:

00000000101110
00010110000000
00000000011000
11001110100011
00000010100000
00110000100110
00000110000000

Even if the second one has more 1's than the first one.
enjoy!

Huayun Huang 

