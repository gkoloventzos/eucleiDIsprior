import CGAL
import visual

DEFAULT_SCENE = 1

class VPoint_2(CGAL.Point_2):
	"""
	VPoint_2 subclasses CGAL.Point_2 adding a visual representation
	of visual.sphere or visual.label to the 2D point that CGAL.Point_2
	refers to. The constructor accepts the mandatory parameter point_2,
	an instance of CGAL.Point_2 and an optional parameter label.
	"""	
	def __init__(self, point_2=None, label=None):
		# sanitise the point_2 parameter
		try:
			# is point_2 a x,y tuple?
			x, y = point_2[0], point_2[1]
			# it is!
			point_2 = CGAL.Point_2(x,y)
		except:
			if point_2 is not None:
				assert point_2.__class__ is CGAL.Point_2
			else:
				point_2 = CGAL.Point_2()
		self.label = label
		self.color = visual.color.white
		self.point_2 = point_2
		# update the global catalog of visual points
		global gc
		gc.insert(self)
		
	def __add__(self, vector):
		"""
		We overload the super class's method as it returns an
		instance of CGAL.Point_2. We need an instance of 
		cgalvisual.VPoint_2 in order to update the global VPoints_2
		dictionary.
		"""
		self.pos = self.x()+vector.x(), self.y()+vector.y()
		return self

	def __sub__(self, other):
		"""
		We overload the super class's method in order to handle
		properly the case where the subtraction returns a CGAL.Point_2.
		As in __add__ we need an instance of cgalvisual.VPoint_2 in 
		order to update the global VPoint_2 dictionary.
		"""
		x, y = self.x()-other.x(), self.y()-other.y()
		if other.__class__ is CGAL.Kernel.Vector_2:
			self.pos = x, y
			return self
		else:
			return CGAL.Vector_2(x, y)
		
	def getPoint_2(self):
		return self
		
	def setPoint_2(self, point_2):
		self.pos = point_2.x(), point_2.y()
		
	point_2 = property (getPoint_2, setPoint_2, \
		doc = 'point_2 property')
	
	def getLabel(self):
		return self.__label
		
	def setLabel(self, label):
		# if the label parameter is None we use the dummy value of X
		self.__label = label or 'X'
		try:
			# self.__reprObj could be undefined if we just created
			# an instance of VPoint_2
			self.__reprObj.text = self.__label
		except:
			pass
		
	label = property (getLabel, setLabel, doc = 'label property')
	
	def getColor(self):
		return self.__color
		
	def setColor(self, color):
		self.__color = color
		try:
			# self.__reprObj could be undefined if we just created
			# an instance of VPoint_2
			self.__reprObj.color = color
			self.__reprObj.linecolor = color
		except:
			pass
			
	color = property (getColor, setColor, doc = 'color property')
	
	def getPos(self):
		return self.__pos
		
	def setPos(self, pos):
		x, y = pos[0], pos[1]
		# CGAL.Point_2 has no setter so we instantiate again the
		# super class
		super(VPoint_2, self).__init__(x, y)
		# Set the visual object's position
		self.__pos = visual.vector(x, y)
		try:
			self.__reprObj.visible = False
			self.show()
			
			global gc
			gc.update(pos, self)
		except:
			self.repr = 'sphere'
			
	pos = property (getPos, setPos, doc = 'pos property')
	
	def getRepr(self):
		return self.__repr
		
	def setRepr(self, value):
		try:
			self.__reprObj.visible = False
		except:
			pass
		if value == 'sphere':
			self.__repr = 'sphere'
		elif value == 'label':
			self.__repr = 'label'
		self.show()
			
	repr = property (getRepr, setRepr, doc = 'repr property')
	
	def show(self):
		if self.__repr == 'sphere':
			self.__reprObj = visual.sphere(pos=self.__pos, \
				radius=RADIUS, color=self.__color)
		elif self.__repr == 'label':
			self.__reprObj = visual.label(pos=self.__pos, \
				text=self.__label, color=self.__color)
			self.__reprObj.linecolor = self.__color

# VPoint_2 class ends here

class VSegment_2(CGAL.Segment_2):
	"""
	"""
	def __init__(self, segment_2):
		# sanitise the segment_2 parameter
		try:
			# is segment_2 a start,end tuple of CGAL.Point_2 points?
			start, end = segment_2[0], segment_2[1]
			# it is a tuple, make sure that consists of two
			# CGAL.Point_2 instances
			assert start.__class__ is VPoint_2, \
				end.__class__ is VPoint_2
			segment_2 = CGAL.Segment_2(start, end)
		except:
			# segment_2 should not be None (must be a segment)
			assert segment_2 is not None, segment_2.__class__ is \
				CGAL.Segment_2
		self.color = visual.color.white
		self.segment_2 = segment_2
		global gc
		gc.insert(self)
		
		
	def getSegment_2(self):
		return self
		
	def setSegment_2(self, segment_2):
		self.__start = segment_2.start()
		self.__end = segment_2.end()
		self.pos = [(segment_2.start().x(), segment_2.start().y()), \
			(segment_2.end().x(), segment_2.end().y())]
			
	segment_2 = property (getSegment_2, setSegment_2, \
		doc = 'segment_2 property')
		
	def getPos(self):
		return self.__pos
		
	def setPos(self, pos):
		self.__pos = pos
		super(VSegment_2, self).__init__(self.__start, self.__end)
		try:
			self.__reprObj.visible = False
			self.show()
		except:
			self.repr = 'curve'
			
	pos = property (getPos, setPos, doc = 'pos property')
	
	def getRepr(self):
		return self.__repr
		
	def setRepr(self, value):
		try:
			self.__reprObj.visible = False
		except:
			pass
		if value == 'curve':
			self.__repr = 'curve'
		self.show()
		
	repr = property (getRepr, setRepr, doc = 'repr property')
	
	def show(self):
		if self.__repr == 'curve':
			self.__reprObj = visual.curve(pos=self.__pos)
			
# VSegment_2 class ends here

def prepareScene():
	visual.scene.range=RANGE
	visual.scene.width=WIDTH
	visual.scene.height=HEIGHT
	visual.scene.exit_on_close(1)

class GlobalCatalog(object):
	def __init__(self):
		self.VPoints_2={}
		self.VSegments_2={}
	def insert(self, visualObj):
		if visualObj.__class__ is VPoint_2:
			self.VPoints_2[visualObj]=visualObj
		elif visualObj.__class__ is VSegment_2:
			self.VSegments_2[visualObj] = { \
				'start': visualObj.start(), 'end': visualObj.end()}
	def update(self, pos, visualObj):
		print 'VPoints_2', self.VPoints_2
		print 'visualObj', visualObj
		if visualObj.__class__ is VPoint_2:
			try:
				existingPoint = self.VPoints_2[visualObj]
				print 'index', self.VPoints_2[visualObj]
			except:
				existingPoint = None
			if existingPoint:
				print 'existingPoint', existingPoint
				affectedSegments = []
				for segment, endpoints in self.VSegments_2.iteritems():
					for endpoint, value in endpoints.iteritems():
						print 'value', value
						if value is existingPoint:
							print 'skatakis'
							affectedSegments.append(segment)
							
				print 'going to delete', self.VPoints_2[existingPoint]
				del self.VPoints_2[existingPoint]
				self.VPoints_2[visualObj] = visualObj
				
				for segment in affectedSegments:
					self.VSegments_2[VSegment_2((self.VSegments_2[segment]['start'], self.VSegments_2[segment]['end']))] = self.VSegments_2[segment]
					del self.VSegments_2[segment]
			

RANGE=100.0
WIDTH=400
HEIGHT=300
RADIUS=RANGE/WIDTH
if RADIUS < .5:
	RADIUS = .5

prepareScene()
gc = GlobalCatalog()

a=VPoint_2()
b=VPoint_2((40,40))
s=VSegment_2((a,b))

