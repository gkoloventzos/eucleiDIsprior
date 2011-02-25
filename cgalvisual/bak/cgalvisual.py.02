import CGAL
import visual

def prepareScene():
	visual.scene.range = 10
	visual.scene.width = 400
	visual.scene.height = 300
	visual.scene.exit_on_close(1)

# Default values for visual representations of CGAL objects
#TODO: Check if this is always suitable for sphere radius
RADIUS = visual.scene.range.x/visual.scene.width
COLOR = visual.color.white
# Default value for an unspecified visual point label
DEF_POINT_LABEL = 'X'
DEF_POINT_REPR = 'sphere'
# Default value for an unspecified visual segment label
DEF_SEGMENT_LABEL = 'XY'

VisualPoints = None
VisualSegments = None

class  cgalScene(visual.display):
	"""
	docstring
	"""
	def __init__(self, title='CGAL-Python Visual scene', width=400, 
		height=400, range=10):
			super(cgalScene, self).__init__(title=title, width=width, \
				height=height, range=range)
			self.w = width
			self.h = height
			self.r = range
			self.VPoints_2 = None
			self.VSegments_2 = None
			
	def insertVPoints_2(self, vpoint_2):
		if self.VPoints_2 is not None:
			self.VPoints_2[vpoint_2] = vpoint_2
		else:
			self.VPoints_2 = {}
			self.VPoints_2[vpoint_2] = vpoint_2
			
	def insertVSegments_2(self, vsegment_2):
		if self.VSegments_2 is not None:
			self.VSegments_2[vsegment_2] = {'start' : vsegment_2.start(), \
				'end' : vsegment_2.end()}
		else:
			self.VSegments_2 = {}
			self.VSegments_2[vsegment_2] = {'start' : vsegment_2.start(), \
				'end' : vsegment_2.end()}
			
	def updateVPoints_2(self, vpoint_2):
		try:
			existingPoint = self.VPoints_2[vpoint_2]
			print existingPoint
		except:
			existingPoint = None
			
		if existingPoint:
			self.updateVSegments_2(existingPoint)
			del self.VPoints_2[existingPoint]
			self.VPoints_2[vpoint_2] = vpoint_2
			
	def updateVSegments_2(self, changedPoint):
		affectedSegments = []
		if self.VSegments_2:
			for segment, endpoints in self.VSegments_2.iteritems():
				for endpoint, value in endpoints.iteritems():
					if value is changedPoint:
						affectedSegments.append(segment)
		for segment in affectedSegments:
			segment.hide()
			self.VSegments_2[VSegment_2(self.VSegments_2[segment]['start'], \
				self.VSegments_2[segment]['end'])] = self.VSegments_2[segment]
			del self.VSegments_2[segment]

DEFAULT_SCENE = cgalScene()

class mouseClick(object):
	"""
	click = mouseClick(which_button=None)
	"""
	def __init__(self, which_button=None, display=DEFAULT_SCENE):
		self.button = None
		self.pos = None
		self.pick = None
		self.display = display
		self.get(which_button)
		
	def getEvent(self):
		self.display.select()
		if self.display.mouse.events:
			event = self.display.mouse.getevent()
			if event.press:
				self.button = event.button
				self.pos = event.pos
				self.pick = event.pick
		
	def get(self, which_button):
		if which_button is not None:
			while self.button <> which_button:
				self.getEvent()
		else:
			while self.button is None:
				self.getEvent()
		
	def __str__(self):
		return "%s button pressed at position %s" % (self.button, self.pos)


class VPoint_2(CGAL.Point_2):
	
	def __init__(self, point_2=None, label=None, display=DEFAULT_SCENE):
		super(VPoint_2, self).__init__(point_2.x(), point_2.y())
		self.__textLabel = label
		self.__pos = visual.vector(point_2.x(), point_2.y())
		self.__color = visual.color.white
		self.show()

		self.display = display			
		self.display.insertVPoints_2(self)
		
	def getPoint_2(self):
		return 
	def setPoint_2(self, point_2):
		super(VPoint_2, self).__init__(point_2.x(), point_2.y())
		
	def getVPos(self):
		return 
		
	def visualRepresentation(self):
		self.vpoint = 
		
	def getLabel(self):
		return self.__label
		
	def setLabel(self, label):
		self.__label = label
		self.repr = 'label'
	
	label = property(getLabel, setLabel, doc='VPoint_2 label property')
	
	def getColor(self):
		return self.__color
		
	def setColor(self, color):
		self.__color = color
		if self.__repr is not None:
			self.__repr.color = color
			if self.__reprstr == 'label':
				self.__repr.linecolor = color
		
	color = property(getColor, setColor, doc='VPoint_2 color property')
		
	def getPos(self):
		return self.__pos
		
	def setPos(self, pos):
		# parameter pos is a (x,y) tuple
		x, y = pos[0], pos[1]
		# self.__pos is a CGAL.Vector_2()
		self.__pos = CGAL.Vector_2(x, y)
		# self.__vpos is a visual.vector(). Used for visual representation
		self.__vpos = visual.vector(x, y)
		# TOCHECK: CGAL.Point_2 has no setter ?!
		super(VPoint_2, self).__init__(x, y)
		# self.__repr.pos is visual.vector(x,y)
		if self.__repr is not None:
			self.__repr.pos = visual.vector(x, y)
			
		self.display.updateVPoints_2(self)

	pos = property(getPos, setPos, doc='VPoint_2 position property')
		
	def getRepr(self):
		return self.__reprstr

	def setRepr(self, repr):
		self.display.select()
		self.__reprstr = repr
		if self.__repr is not None:
			self.__repr.visible = False
		if repr == 'sphere':
			if self.display.range.x/self.display.w < 1:
				RADIUS = 1
			else:
				RADIUS = self.display.range.x/self.display.w
			self.__repr = visual.sphere(pos=self.__vpos, radius=RADIUS, color=self.__color)
		else:
			self.__repr = visual.label(pos=self.__vpos, text=self.__label, color=self.__color)
			self.__repr.linecolor = self.__color

	repr = property(getRepr, setRepr, doc='VPoint_2 representation property')

# class VPoint_2 ends here

class VSegment_2(CGAL.Segment_2):
	def __init__(self, start=CGAL.Point_2(), end=CGAL.Point_2(), label=None, display=DEFAULT_SCENE):
		super(VSegment_2, self).__init__(start, end)
		self.__repr = None
		self.__line = visual.curve(pos=[(start.x(), start.y()), (end.x(), end.y())])
		#self.color = visual.color.white
		#if label is not None:
		#	self.label = label
		#else:
		#	self.__label = DEF_SEGMENT_LABEL
		
		display.insertVSegments_2(self)	
			
	def label():
		doc = 'label property of VSegment_2: a tuple with the endpoints'' labels'
		def fget(self):
			return self.__label
		def fset(self, label):
			# label is a tuple with the endpoint's labels
			self.__label = label[0]  + label[1]
			self.__start.label = label[0]
			self.__end.label = label[1]
		return locals()
	label = property(**label())
	
	def color():
		doc = 'color property of VSegment_2: visual.color'
		def fget(self):
			return self.__color
		def fset(self, color):
			self.__color = color
			self.__start.color = color
			self.__end.color = color
			self.__line.color = color
		return locals()
	color = property(**color())
	
	def repr():
		doc = ''
		def fget(self):
			return self.__repr
		def fset(self, repr):
			if repr == 'plain':
				self.__start.repr = 'sphere'
				self.__end.repr = 'sphere'
			elif repr == 'labeled':
				self.__start.label
		return locals()
	repr = property(**repr())
	
	def hide(self):
		self.__line.visible = False
			
def getVisualPoints():
	points = []
	click = mouseClick()
	while click.button <> 'right':
		point = VPoint_2(click.pos.x, click.pos.y)
		points.append(point)
		click = mouseClick()
	return points
	
def getVisualPointsLabeled():
	points = []
	label = 0
	click = mouseClick()
	while click.button <> 'right':
		point = VPoint_2(click.pos.x, click.pos.y, label=str(label))
		points.append(point)
		click = mouseClick()
		label += 1
	return points
	

a = VPoint_2()
b = VPoint_2(4,4)
c = VPoint_2(-4,4)
d = VPoint_2(0,4)
a.label='A'
b.label='B'
c.label='C'
d.label='D'
s1 = VSegment_2(a,b)
s2 = VSegment_2(a,c)
