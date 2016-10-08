import string
# developed and test on python 2.7.9
# @author Huayun Huang

def printMap(path,theMap):
    """
    @ Parameter:
        path  [(int,int)]
            the path to draw on the map
        theMap [str] or str
            the parsed/unparsed map representing the environment
    @ Usage:
        for the debugging of this program. To output into the console.
    """
    if path == []:
        print theMap
        print 
        return
    if type(theMap) == str:
        newMap = parseMapString(theMap)
    else:
        newMap = theMap + []
    if path == None:
        print None
        return

    for (r,c) in path:
        newStr = list(newMap[r])
        newStr[c] = "-"
        newMap[r] = "".join(newStr)

    (r,c) = path[0]
    newStr = list(newMap[r])
    newStr[c] = "+"
    newMap[r] = "".join(newStr)

    (r,c) = path[-1]
    newStr = list(newMap[r])
    newStr[c] = "+"
    newMap[r] = "".join(newStr)

    print "\n".join(newMap)
    print 


def parseMapString(mapString):
    """
    @ Parameter: 
        mapString str
            a string that represent the map.
    @ Return:
        A string list that split the mapString by its rows.
    @ Usage: 
        Whenever we want to turn a map string into a string list.
    """
    mapString = mapString.splitlines()
    accMap = []
    for i in xrange(len(mapString)):
        currLine = mapString[i].strip()
        if currLine:
            accMap += [currLine]
    return accMap

def getNeighbors(mapList, r, c, direction = [0,1,2,3]):
    # return a list of tuples represent the accessible neighbors
    if r >= len(mapList):
        raise Exception("given coordinate on row is out of bound")
    elif c >= len(mapList[r]):
        raise Exception("given coordinate on col is out of bound")

    nList =[]

    for it in direction:
        if it == 0: 
            # left
            if c != 0 and mapList[r][c-1] == '0': 
                nList += [(r, c-1)]
        elif it == 1:
            # right
            if c != len(mapList[r]) - 1 and mapList[r][c+1] == '0':
                nList += [(r, c+1)]
        elif it == 2:
            # down
            if r < len(mapList) - 1 and c < len(mapList[r+1]) and mapList[r+1][c] =='0':
                nList += [(r+1, c)]
        elif it == 3:
            # up
            if r != 0 and c < len(mapList[r-1]) and mapList[r-1][c] == '0':
                nList += [(r-1, c)]

    return nList

def getDirection(startPoint, endPoint):
    """
    @ Parameter:
        startPoint (int, int) 
            the coordinate of starting point
        endPoint   (int, int) 
            the coordinate of ending point
    @ Return:
         a list of integer indicating the best direction to do the
         recursive search based on the starting point and the ending
         point of the search.
    @ Usage:
        Generally should be called inside find_recursion.
    """

    # 0 = L
    # 1 = R
    # 2 = D
    # 3 = U
    (x1,y1) = startPoint
    (x2,y2) = endPoint
    lr = y2 - y1
    ud = x2 - x1
    if lr > 0: # at right
        if ud > 0: # at down
            if lr > ud: # right more
                return [1,2,3,0]
            else: # down more
                return [2,1,0,3]
        else: # at up
            if lr > (-ud): # right more
                return [1,3,2,0]
            else: # up more
                return [3,1,0,2]
    else: # at left
        if ud > 0: # at down
            if (-lr) > ud: # left more
                return [0,2,3,1]
            else: # down more
                return [2,0,1,3]
        else: # at up
            if (-lr) > (-ud): # left more
                return [0,3,2,1]
            else: # up more
                return [3,0,1,2]

def findOnePath(startPoint, endPoint, accessMap):
    """
    @ Parameter:
        startPoint (int, int) 
            the coordinate of starting point
        endPoint   (int, int) 
            the coordinate of ending point
        accessMap  [str]
            the string list map that indicates whether a place is 
            accessible or not
    @ Return:
        A list of int tuple, representing the fastest path from 
        startPoint to the endPoint. If there does not exist such a 
        path, return None instead.
        *** Only find one path for the purpose of planning ***
    @ Usage:
        Generally should be called by the wrapper function find() 
    """

    # get ready for the recursion.
    if startPoint == endPoint:
        return []
    (r,c) = endPoint
    if accessMap[r][c] != "0":
        return None
    currPath = None

    su = 0
    for r in accessMap:
        su += len(r)

    # similar to flood fill.
    # currPath guaranteed to include starting point
    def find_recursion(currPath_r):
        i,j ,= currPath_r[-1]
        if (i,j) == endPoint:
            # reach the ending point!
            return currPath_r
        elif len(currPath_r) > (su / 2):
            return -1
        else:
            neighbors = getNeighbors(accessMap, i, j, 
                getDirection(currPath_r[-1], endPoint))
            if len(neighbors) == 0:
                return -1
            for nextStep in neighbors:
                if nextStep in currPath_r:
                    continue
                else:
                    thePath = find_recursion(currPath_r + [nextStep])
                    if thePath != -1:
                        return thePath
            return -1

    currPath = find_recursion([startPoint])
    if currPath == -1:
        return None
    else:
        return currPath

def findPath(startPoint, endPoint, accessMap, maxL):
    """
    @ Parameter:
        startPoint (int, int) 
            the coordinate of starting point
        endPoint   (int, int) 
            the coordinate of ending point
        accessMap  [str]
            the string list map that indicates whether a place is 
            accessible or not
        maxL       int
            a thershold. When a recursion path has a length more than
            maxL, we consider the path doesn't exist.
    @ Return:
        A list of int tuple, representing the shortest path from 
        startPoint to the endPoint. If there does not exist such a 
        path, return None instead.
    @ Usage:
        Generally should be called by the wrapper function find() 
    """

    # get ready for the recursion.
    if startPoint == endPoint:
        return []
    currPath = None

    # similar to flood fill.
    # currPath guaranteed to include starting point
    def find_recursion(currPath_r, currL):
        i,j = currPath_r[-1]
        if (i,j) == endPoint:
            # reach the ending point!
            if len(currPath_r) < currL:
                # find a shorter path
                currPath = currPath_r
                currL = len(currPath_r)
            return (currPath_r, currL)
        elif len(currPath_r) > currL:
            # more than the minimal length we have, stop searching
            return (currPath_r, -1)
        elif len(currPath_r) > maxL:
            # a path takes half of the map is stupid
            return (currPath_r, -1)
        else:
            neighbors = getNeighbors(accessMap, i, j, 
                getDirection(currPath_r[-1], endPoint))
            if len(neighbors) == 0:
                return (currPath_r, -1)
            totalResult = (currPath_r, -1)
            for nextStep in neighbors:
                if nextStep in currPath_r:
                    continue
                thePath, theL = find_recursion(currPath_r + [nextStep], currL)
                if theL != -1:
                    totalResult = (thePath, theL) 
                    currL = theL
            return totalResult

    currPath, currLength = find_recursion([startPoint], maxL)
    if currLength == -1:
        return None
    else:
        return currPath

def find(mapString, startPoint, endPoint, interval = 4):
    """
    @ Usage:
        Wrapper function for findPath. Main function for pathFinder.
        Difference between find, findPath and findOnePath:
            find is the "biggest" function that calls findPath and 
            findOnePath following some certain strategies as described
            by the comments in this function. findPath return the 
            shortest possible path within the given limitations. 
            findOnePath return a possible path but not necessarily the
            shortest.
    @ Parameter: 
        mapString    str
            the string that uses 0 and 1 to indicate the accessibility
        startPoint   (int,int)
            coord of starting point
        endPoint     (int,int)
            coord of ending point
    @ Return:
        None if no path exists.
        A tuple list if path exists. 
    """
    # first we process the mapString by calling parseMapString to parse
    # it. 
    theMap = parseMapString(mapString)
    r,c = startPoint
    assert(0 <= r < len(theMap) and 0 <= c < len(theMap[r]))
    r,c = endPoint
    assert(0 <= r < len(theMap) and 0 <= c < len(theMap[r]))
    print "parsing finished"
    print 

    # do a lazy pathFinder by calling findOnePath to ensure there at
    # least exist one path from the start to the end. This procedure
    # produces onePath, which is a possible path but usually not the 
    # shortest way to the end point.
    onePath = findOnePath(startPoint, endPoint, theMap)
    if onePath == None:
        return None
    print "find one path"
    printMap(onePath,mapString)

    # after we find onePath, we cut onePath into several pieces.
    # Typically the more pieces you have, the shorter time it will take
    # to find a path in general. But often times this can mean we can
    # have a path almost as long as onePath. So you got to choose a 
    # balancing point between those trade-offs.
    # put the sequence of starting/ending points of these small 
    # sections into the list pointList.
    n = len(onePath)
    m = n / interval # the amount of middle points
    pointList = [startPoint]
    for i in xrange(1,m):
        pointList += [onePath[i * interval - 1]]
    pointList += [endPoint]

    # within the starting/ending points of these smaller sections
    # we find shorter paths.
    pathList = []
    for i in xrange(len(pointList)-1):
        if i == len(pointList)-2:
            thePath = findPath(pointList[i], pointList[i+1], 
                               theMap, interval * 2)
        else:
            thePath = findPath(pointList[i], pointList[i+1], 
                               theMap, interval + 1)
        if not thePath:
            print pointList[i], pointList[i+1]
        pathList += thePath[:-1]
    pathList += [endPoint]

    print "pathSections"
    printMap(pathList, theMap)

    # This part is no longer necessary b/c we have the neighbor filter
    # below.
    # Since this can produce some U turns we want to ensure we are 
    # doing the smallest path. Ensure no cycles in the path.
    # newMap = theMap + []
    # for r in xrange(len(theMap)):
    #     newMap[r] = string.replace(theMap[r], '0','1')
    # for (r,c) in pathList:
    #     newStr = list(newMap[r])
    #     newStr[c] = "0"
    #     newMap[r] = "".join(newStr)
    # pathList = findPath(startPoint, endPoint, newMap, len(pathList))

    # print "no U turns"
    # printMap(pathList, theMap)

    # check if the pathList contains any points that do not have index
    # difference within 2 (i.e., pathList[3] and pathList[5] have
    # the index difference of 2 but pathList[3] and pathList[6] don't)
    # and see if we actually have a shorter path for that.
    neighborRange = 3
    while i < len(pathList):
        row, col = pathList[i]
        for r in xrange(row - neighborRange, row + neighborRange + 1):
            for c in xrange(col - neighborRange, col + neighborRange + 1):
                if ((r,c) in pathList[i+neighborRange+1:]):
                    j = (pathList[i+neighborRange+1:].index((r,c)) 
                         + i + neighborRange + 1)
                    newPath = findPath((row,col), pathList[j],
                        theMap, neighborRange * 2 + 3)
                    if newPath and len(newPath[:-1]) < len(pathList[i:j]):
                        pathList = pathList[:i] + newPath[:-1] + pathList[j:]
        i += 1
        if i >= len(pathList):
            break


    return pathList


if __name__ == '__main__':
    # 0 = safe
    # anything else = not accessible
    # the map is not necessarily a square
    # but do not use space in the middle. Use 1 instead.
    environment = (
    """
    00110000100000000000
    00100111001000000000
    00101000001000000000
    00100000001000100000
    00000000011001111111
    00000000000100100000
    00010000001001000000
    00010000001001000000
    00000010000001011110
    00000100000001000000
    00000100000000100000
    00000100011110001000
    00010000111000000000
    00010001111111101111
    11100111111101100000
    00010000000010000000
    00010000100000011000
    00000000100011011000
    00001000100011010000
    00001000100011001111
    """
    )

    # coordinate on where they start
    start, end = (19, 0), (0, 19)

    # the smaller, the faster to find the path, and longer the path is.
    # the bigger, the slower to find the path, and shorter the path is.
    # This is just a general rule.
    # must be a positive integer. 
    # suggested value: between 4 and 7. 
    interval = 7

    path = find(environment, start, end, interval)
    print "final path"
    printMap(path, environment)
    print path
