from copy import copy
from AppKit import NSPoint
from GlyphsApp import GSIntersectLineLineUnlimited

def middlePos(p1, p2):
	middle = addPoints(p1, scalePoint(subtractPoints(p2, p1), 0.5))
	return middle

def twoThirdPos(p1, p2):
	twothirds = addPoints(p1, scalePoint(subtractPoints(p2, p1), 2/3))
	return twothirds

def segmentFromSelection(layer):
	for n in layer.selection:
		if type(n)==GSNode and n.type==GSOFFCURVE:
			return segmentOfOffCurve(n)
	return None
	
def segmentOfOffCurve(offCurve):
	segment = []
	path = offCurve.parent
	if any([n.type!=GSOFFCURVE for n in path.nodes]):
		currentNode = offCurve
		while currentNode.type==GSOFFCURVE:
			currentNode = currentNode.prevNode
		segment.append(currentNode)
		while currentNode.nextNode.type==GSOFFCURVE:
			currentNode = currentNode.nextNode
			segment.append(currentNode)
	return segment

def offCurvesAndImpliedOnCurves(segment):
	coordinates = [segment[0].position]
	for node in segment:
		nextNode = node.nextNode
		if node.type==GSOFFCURVE and nextNode.type==GSOFFCURVE:
			impliedOnCurve = middlePos(node.position, nextNode.position)
			coordinates.append(impliedOnCurve)
		coordinates.append(nextNode.position)
	return coordinates

def duplicateOffcurvesOnSegment(offCurve):
	path = offCurve.parent
	segment = segmentOfOffCurve(offCurve)
	if segment:
		coordinates = offCurvesAndImpliedOnCurves(segment)
		newOffCurves = []
		for i in range(1, len(coordinates)):
			pos1 = coordinates[i-1]
			pos2 = coordinates[i]
			newOffCurve = GSNode()
			newOffCurve.type = GSOFFCURVE
			newOffCurve.position = middlePos(pos1, pos2)
			newOffCurves.append(newOffCurve)
		lowestIndex = min([n.index for n in segment])
		path.removeNodes_(segment[1:])
		insertIndex = path.nodes[lowestIndex].nextNode.index
		while newOffCurves:
			path.insertNode_atIndex_(newOffCurves.pop(), insertIndex)

def increaseOffCurves(segment):
	# segment lacks the last on-curve: segment[-1].nextNode
	if len(segment)%2 == 0:
		middleIndex = len(segment)//2
		middelNode = segment[middleIndex]
		
	elif len(segment)%2 == 1:
		half = len(segment)//2
		middlePair = segment[half:half+2]

def bezierQ(p1, p2, p3, t):
	"""
	Returns coordinates for t (=0.0...1.0) on curve segment.
	x1,y1 and x3,y3: coordinates of (implied) on-curve nodes
	x2,y2: coordinates of off-curve
	"""
	x1,y1 = p1.x, p1.y
	x2,y2 = p2.x, p2.y
	x3,y3 = p3.x, p3.y
	x = x1*(1-t)**2 + x2*2*t*(1-t) + x3*t**2
	y = y1*(1-t)**2 + y2*2*t*(1-t) + y3*t**2
	return NSPoint(x, y)

