from __future__ import division
from visual import *
from visual.controls import *
from time import sleep

VisualPoints = None
VisualSegments = None
control = None


orien = {"CLOCKWISE":-1,"COLLINEAR":0,"COUNTERCLOCKWISE":1}
rorien = {-1:"CLOCKWISE",0:"COLLINEAR",1:"COUNTERCLOCKWISE"}
sides = {"ON_NEGATIVE_SIDE":-1,"ON_ORIENTED_BOUNDARY":0,"ON_POSITIVE_SIDE":1}
rsides = {-1:"ON_NEGATIVE_SIDE",0:"ON_ORIENTED_BOUNDARY",1:"ON_POSITIVE_SIDE"}
CLOCKWISE = ON_NEGATIVE_SIDE = -1
COUNTERCLOCKWISE = ON_POSITIVE_SIDE = 1
COLLINEAR = ON_ORIENTED_BOUNDARY = 0
EP = 15	#Extreme Point for creating lines and rays which does not have a particulary end

class No_Constructor(Exception):
	def __init__(self,value):
		self.name = type(value[0]).__name__
		self.parameters = value[1:]
	def repr(self):
		print '{self.name} has no constructor with this arguments' .format(self=self),
		for i in range(self.parameters):
			if self.parameters[i] != None:
				print '{self.parameters[i]}' .format(self=self),
			print ""
class Is_Degenerate(Exception):
	def __init__(self,value):
		self.name = type(value).__name__
	def repr(self): 
		print 'The {self.name} is degenerate' .format(self=self)
def prepareScene():
	#scene.userspin = False #Gia na exoume k deksi koumpi sto pontiki
	scene.range = 10
	scene.width = 800
	scene.height = 700
	scene.title = "eukleiDIs"
	scene.exit=1
	
class mouseClick(object):
	"""
	click = mouseClick(which_button=None)
	"""
	def __init__(self, which_button=None):
		self.button = None
		self.pos = None
		self.pick = None
		self.get(which_button)
		
	def getEvent(self):
		if scene.mouse.clicked:
			event = scene.mouse.getclick()
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
		
def getVisualPoints():
	points =[]
	while True:
		if scene.kb.keys:
			s = scene.kb.getkey()
			if s == 'backspace':
				break
		if scene.mouse.clicked:
			click =	scene.mouse.getclick()
			point = Point_2(click.pos.x,click.pos.y)
#			stri = str(click.pos.x) + "," + str(click.pos.y)
#			point.label(stri)
			points.append(point)
	return points
	
def movePoints():
	pick = None # no object picked out of the scene yet
	global VisualSegments
	if VisualSegments:
		f = VisualSegments.keys()
		for ke in f:
			VisualSegments[ke]._segment.visible=False
	while True:
		if scene.kb.keys:
			s = scene.kb.getkey()
			if s == 'backspace':
				break		
		if scene.mouse.events:
			m1 = scene.mouse.getevent() # get event
			global VisualPoints
			for poin in VisualPoints:
				if m1.drag and m1.pick == poin.pos(): # if touched ball
					drag_pos = m1.pickpos # where on the ball
					pick = m1.pick # pick now true (not None)
				elif m1.drop: # released at end of drag
					pick = None # end dragging (None is false)
		if pick:
			# project onto xy plane, even if scene rotated:
			new_pos = scene.mouse.project(normal=(0,0,1))
			if new_pos != drag_pos: # if mouse has moved
				# offset for where the ball was clicked:
				pick.pos += new_pos - drag_pos
				drag_pos = new_pos # update drag position


def prepareControls():
	w = 380
	global control
	global VisualPoints
	control = controls(title='Controlling eukleiDIs',x=800, y=0, width=w, height=w, range=60)
	mv = button(pos=(-30,40), height=20, width=50, text='Move Points', action=lambda: movePoints())
	gp = button(pos=(30,40), height=20, width=50, text='Insert Points', action=lambda: getVisualPoints())
	dap = button(pos=(-30,10), height=20, width=50, text='Del Points', action=lambda: getVisualPoints())
	das = button(pos=(30,10), height=20, width=50, text='Del Segments', action=lambda: getVisualPoints())
	ru = button(pos=(0,-20), height=20, width=50, color = (1,0,0), text='Run', action=lambda: run(VisualPoints))
	while 1:
		control.interact()

def is_permute(l1,l2):
	"""
	Returning True if l2 is a cyclic permutation of l1
	"""
	if l1 == l2:
		return true
	for i in range(0,len(l1)-1):
		list1 = l1[1:len(l1)]
		list1.append(l1[0])
		if list1 == l2:
			return True
		l1 = list1
	return False
	

class Point_2(object):#all clear
	"""
	Point in 2d
	"""
	def __init__(self,x=0,y=0,color=(1,1,1),visible=True): #using visible not opacity for older versions
		self._point=sphere(pos=(x,y,0),radius=0.1,color=color,visible=visible) 
		global VisualPoints
		if VisualPoints is not None:
			VisualPoints[self]=self
		else:
			VisualPoints = {}
			VisualPoints[self]=self
	def __repr__(self):
		return 'Point_2({self._point.pos[0]},{self._point.pos[1]})' .format(self=self)
	def x(self):
		return self._point.pos[0]
	def y(self):
		return self._point.pos[1]
	def pos(self):
		return self._point
	def label(self,string):
		self._label=label(pos=self._point.pos,text=string,xoffset=0,yoffset=5,space=self._point.radius,height=10,border=1,font='sans')
	def color(self,x=0,y=0,z=0):
		if(x==0 and y==0 and z==0):
			print self._point.color
			return
		if type(x).__name__=='tuple':
			self._point.color=x
			return
		self._point.color=(x,y,z)
	def cartesian(self,i):
		if i>=0 and i<=1:
			return self._point.pos[i]
	def dimension(self):
		return 2
#generator gia na ulopoihsw tous iterators ths CGAL
	def iter(self):
		for index in range(2):
			yield self._point.pos[index]
	def __add__(self,other):
		return Point_2(other.x()+self.x(),other.y()+self.y())
	def __sub__(self,other):
			if type(self).__name__==type(other).__name__:
				return Vector_2(self,other)
			return Point_2(self.x()-other.x(),self.y()-other.y())
	def __eq__(self,other):
		if other == None:
			return False
		return (self.x()==other.x()) and (self.y()==other.y())
	def __ne__(self,other):
		if other==None:
			return False
		return (self.x()!=other.x()) or (self.y()!=other.y())
	def __gt__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return False
		return self.x() < other.x() or ( self.x() == other.x() and self.y() < other.y() )
	def __lt__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return False
		return self.x() > other.x() or ( self.x() == other.x() and self.y() > other.y() )
	def __ge__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return False
		return self.x() >= other.x()
	def __le__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return False
		return self.x() <= other.x()
	def __getitem__(self,i):
		if i>=0 and i<=1:
			return self._point.pos[i]
	def visual(self,visible=None): #argue how will work
		if visible == None:
			self._point.visible = not self._point.visible
		else:
			self._point.visible = visible
		return self._point.visible


"""
	kanei swsta thn anathesi omws dn allazei to xrwma :'(
	def get_color(self):
		return self._point.color
	def set_color(self,color):
		self._point.color = color
	color = property(get_color,set_color)
"""

class Vector_2(object):
	"""
	Vector in 2d
	"""
	def __init__(self,x=None,y=None,visible=True):
		if type(x).__name__==type(y).__name__=='NoneType':
			raise No_Constructor([self,x,y])
		if type(x).__name__==type(y).__name__== 'Point_2':
			self._vector=vector(y.x()-x.x(),y.y()-x.y())
		if (type(x).__name__==type(y).__name__=='int') or(type(x).__name__==type(y).__name__=='float'):
			self._vector=(x,y)
		if type(y).__name__ == 'NoneType':
			if type(x).__name__=='Segment_2':
				a = x.source()
				b = x.target()
				self._vector=vector(b.x() - a.x(),b.y() - a.y())
			elif type(x).__name__=='Ray_2':
				s = x.direction()
				self._vector=vector(s.dx(),s.dy())
			elif type(x).__name__=='Line_2':
				self._vector=vector(x.b(),-x.a())
		#self._vvector=arrow(pos=(0,0,0),axis=(self._vector[0],self._vector[1],0),visible=visible,shaftwidth = 0)
	def __repr__(self):
		return 'Vector_2({self._vector[0]},{self._vector[1]})' .format(self=self)
	def x(self):
		return self._vector[0]
	def y(self):
		return self._vector[1]
	def dimension(self):
		return 2
	def cartesian(self,i):
		if i>=0 and i<=1:
			return self._vector[i]
	def direction(self):
		return Direction_2(self)
	def __eq__(self,other):
		if other == None:
			return False
		return self._vector == other._vector
	def __ne__(self,other):
		if other == None:
			return False
		return self._vector != other._vector
	def cartesian(self,i):
		if i>=0 and i<=1:
			return self._vector[i]
	def __getitem__(self,i):
		if i>=0 and i<=1:
			return self._vector[i]
	def squared_length(self):
		return mag2(self)
	def __neg__(self):
		return Vector_2(-self.x(),-self.y())
	def __mul__(self,other):
		if type(other).__name__=='Vector_2':
			return dot(self,other)
		else:
			return Vector_2(other*self.x(),other*self.y())
	def __div__(self,other):
		return Vector_2(self.x()/other,self.y()/other)
	def __add__(self,other):
		return Vector_2(self.x()+other.x(),self.y()+other.y())
	def __sub__(self,other):
		return Vector_2(self.x()-other.x(),self.y()-other.y())
	def angle(self):
		angle = degrees(atan2(self[1],self[0]))
		if angle < 0:
			return 360 + angle
		else:
			return angle
	def visual(self,visible=None): #argue how will work
		if visible == None:
			self._vector.visible = not self._vector.visible
		else:
			self._vector.visible = visible
		return self._vector.visible
		
		
class Direction_2(object):#all clear
	"""
	Direction in 2d
	"""
	def __init__(self,x,y=None):
		self._d=[]
		if type(y).__name__=='NoneType':
			if type(x).__name__=='Vector_2':
				if x.x() == 0:
					self._direction = None
				else:
					self._direction=x.y()/x.x()
				self._d.extend([x.x(),x.y()])				
			if type(x).__name__=='Line_2':
				self._direction=x.direction()
				self._d.extend[-x.a(),x.b()]
			if type(x).__name__=='Ray_2':
				f = x.to_vector()
				self = Direction_2(f)
			if type(x).__name__=='Segment_2':
				s=x.source()
				t=x.target()
				self._d.extend([t.x()-s.x(),t.y()-s.y()])
				if self._d[0] == 0:
					self._direction = None
				else:
					self._direction= self._d[1]/self._d[0]
		elif (isinstance(x,float) or isinstance(x,int)) and (isinstance(y,float) or isinstance(y,int)):
			if x == 0:
				self._direction = None
			else:
				self._direction=y/x
			self._d.extend([x,y])
		else:
			raise No_Constructor([self,x,y])
	def delta(self,i):
		if i>=0 and i<=1:
			return self._d[i]
	def direction(self):
		return self._direction
	def dx(self):
		return self._d[0]
	def dy(self):
		return self._d[1]
	def __neg__(self):
		return Direction_2(-self._d[0],self._d[1])
	def vector(self):
		return Vector_2(self._d[0],self._d[1],visible=False)
	def __eq__(self,other):
		if other == None:
			return False
		return self.vector() == other.vector()
	def __ne__(self,other):
		if other == None:
			return False
		return self.vector() != other.vector()
	def __gt__(self,other):
		s = self.vector()
		o = other.vector()
		return s.angle > o.angle
	def __lt__(self,other):
		s = self.to_vector()
		o = other.to_vector()
		return s.angle < o.angle	
	def __ge__(self,other):
		s = self.vector()
		o = other.vector()
		return s.angle >= o.angle
	def __le__(self,other):
		s = self.vector()
		o = other.vector()
		return s.angle <= o.angle	
	def counterclockwise_in_between(self,d1,d2):
		s = self.vector()
		dd1 = d1.vector()
		dd2 = d2.vector()
		sa = s.angle()
		dd1a = dd1.angle()
		dd2a = dd2.angle()
		if dd1a < sa and sa < dd2a:
			return True
		if dd1a == sa:
			return False
		return False
	def __repr__(self):
		return 'Direction_2({self._d[0]},{self._d[1]})' .format(self=self)
				
			
class Line_2(object):
	"""
	Line in 2d
	"""
	def __init__(self,a,b=None,c=None,color=(1,1,1),visible=True):
		self._line=None
		self._a=None
		self._b=None
		self._c=None
		if b == None and c == None:
			if type(a).__name__ == 'Segment_2':
				x=a.source()
				y=a.target()
				if a.is_degenerate():
					raise Degenetate_Segment
				self._b=(y.x() - x.x()) # y = -(y2-y1)/(x2-x1)*x +c
				self._a=-(y.y() - x.y())
				self._c=-(self._b*x.y()+self._a*x.x())
			if type(a).__name__ == 'Ray_2':
				self = Line_2(a.source(),a.direction())
		elif c == None:
			if type(a).__name__ == 'Point_2' and type(b).__name__ =='Vector_2':
				self._b=b.x()
				self._a=-b.y()
				self._c=-(self._b*a.y()+self._a*a.x())
			if type(a).__name__ == 'Point_2' and type(b).__name__ =='Direction_2':
				self._b=b.delta(0)
				self._a=-b.delta(1)
				if a.y() != None and a.x() != None:
					self._c=-(self._b*a.y()+self._a*a.x())
				else:
					self._c=0
			if type(a).__name__ == 'Point_2' and type(b).__name__ =='Point_2':
				p=Segment_2(a,b)
				x=p.source()
				y=p.target()
				if p.is_degenerate():
					raise Degenetate_Segment
				self._b=(y.x() - x.x())
				self._a=-(y.y() - x.y())
				self._c=-(self._b*y.y()+self._a*y.x())				
		if (isinstance(a,float) or isinstance(a,int)) and (isinstance(b,float) or isinstance(b,int)) and (isinstance(c,float) or isinstance(c,int)):
				self._b=b
				self._c=c
				self._a=a
		print self._a,self._b,self._c
		print self.y_at_x(-EP),self.y_at_x(EP),"\n"
		if self.is_vertical():
			f = self._c/self._a
			self._line=curve(pos=[(-f, -EP),(-f,EP)],color=color,visible=visible)
		elif self.is_horizontal():
			f = self._c/self._b
			self._line=curve(pos=[(-EP,-f),(EP,-f)],color=color,visible=visible)
		else:
			self._line=curve(pos=[(-EP, self.y_at_x(-EP)),(EP,self.y_at_x(EP))],color=color,visible=visible)
	def a(self):
		return self._a			
	def b(self):
		return self._b
	def c(self):
		return self._c
	def is_degenerate(self):
		return a == b == 0
	def is_horizontal(self):
		return self._a == 0
	def is_vertical(self):
		return self._b == 0
	def direction(self):
		return Direction_2(self._b,-self._a)
	def opposite(self):
		return Line_2(-self._a,-self._b,-self._c,visible=False)
	def to_vector(self):
		return Vector_2(self.direction(),visible=False)
	def x_at_y(self,y):
		if not self.is_horizontal():
			return ((-self._b*y)-self._c)/self._a
	def y_at_x(self,x):
		if not self.is_vertical():
			return ((-self._a*x)-self._c)/self._b
	def __repr__(self):
		return 'Line_2({self._a} x + {self._b} y + {self._c} = 0)' .format(self=self)
	def visual(self,visible=None): #argue how will work
		if visible == None:
			self._line.visible = not self._line.visible
		else:
			self._line.visible = visible
		return self._line.visible
	def oriented_side(self,c):
		x1 = self.x_at_y(1)
		y1 = self.y_at_x(x1+1)
		a = Point_2(x1,1,visible=False)
		b = Point_2(x1+1,y1,visible=False)
		orie = ((a.x()-c.x())*(b.y()-c.y()))-((a.y()-c.y())*(b.x()-c.x()))
		if orie == 0:
			return rsides[0]
		elif orie < 0:
			return rsides[-1]
		else:
			return rsides[1]
	def point(self,i):
		x=1+self._b*i
		y=self.y_at_x(x)
		return Point_2(x,y,visible=False)
	def perpendicular(self,p):
		d = self.direction()
		x=d.dx()
		y=d.dy()
		if (x >=0 and y>=0) or (x <=0 and y<=0):
			d1=Direction_2(-y,x)
		else:
			d1=Direction_2(y,-x)
		return Line_2(p,d1,visible=False)
	def has_on(self,p):
		return self.oriented_side(p) == 0
	def has_on_positive_side(self,p):
		return self.oriented_side(p) == 1
	def has_on_negative_side(self,p):
		return self.oriented_side(p) == -1
	def __eq__(self,other):
		if other == None:
			return False
		return (self._a == other.a()) and (self._b == other.b()) and (self._c==other.c())
	def __ne__(self,other):
		if other == None:
			return False
		return (self._a != other.a()) or (self._b != other.b()) or (self._c != other.c())
	def color(self,x=0,y=0,z=0):
		if(x==0 and y==0 and z==0):
			print self._line.color
			return
		if type(x).__name__=='tuple':
			self._line.color=x
			return
		self._line.color=(x,y,z)
			
class Ray_2(object):
	"""
	Ray in 2d
	"""
	def __init__(self,x,y,color=(1,1,1),visible=True):
		if type(y).__name__ == 'Point_2':
			#y.visual()
			self._direction = Direction_2(Segment_2(x,y))
		if type(y).__name__ == 'Direction_2':
			self._direction = y
		if type(y).__name__ == 'Vector_2':
			self._direction = y.direction()
		if type(y).__name__ == 'Line_2':
			self._direction = y.direction()
		d = self._direction
		l = Line_2(x,d,visible=False)
		if d.dx() > 0 and d.dy() >0:
			p = Point_2(EP,l.y_at_x(EP),visible=False)
		if d.dx() < 0 and d.dy() >0:
			p = Point_2(-EP,l.y_at_x(-EP),visible=False)
		if d.dx() > 0 and d.dy() <0:
			p = Point_2(EP,l.y_at_x(EP),visible=False)
		if d.dx() < 0 and d.dy() <0:
			p = Point_2(-EP,l.y_at_x(-EP),visible=False)
		if d.dx() == 0:
			if d.dy() <0:
				p = Point_2(-EP,x.y(),visible=False)
			elif d.dy()>0:
				p = Point_2(EP,x.y(),visible=False)
		if d.dy() == 0:
			if d.dx() <0:
				p = Point_2(x.x(),-EP,visible=False)
			elif d.dx()>0:
				p = Point_2(x.x(),EP,visible=False)
		self._source=x
		self._ray=curve(pos=[(x.x(), x.y()),(p.x(), p.y())],color=color,visible=visible)
	def color(self,x=0,y=0,z=0):
		if(x==0 and y==0 and z==0):
			print self._ray.color
			return
		if type(x).__name__=='tuple':
			self._ray.color=x
			return
		self._ray.color=(x,y,z)
	def source():
		return self._source
	def __eq__(self,other):
		if other == None:
			return False
		return self._source == other.source() and self._direction == other.direction()
	def __ne__(self,other):
		if other == None:
			return False
		return self._source != other.source() or self._direction != other.direction()
	def direction(self):
		return self._direction
	def supporting_line(self):
		return Line_2(self._source,self._direction,visible=False)
	def to_vector(self):
		return Vector_2(self.supporting_line())
	def opposite(self):
		l=self.supporting_line()
		p=l.point(-1)
		return Ray_2(self._source,p,visible=False)
	def point(self,i):
		if i>0:
			l=self.supporting_line()
			l.point(i)
		if i==0:
			return self._source
		
		

class Segment_2(object):#all clear
	"""
	Segment in 2d
	"""
	def __init__(self,start1,end1,color=(1,1,1),visible=True):
		self._segment=curve(pos=[(start1.x(), start1.y()),(end1.x(), end1.y())],color=color,visible=visible)
		self._point_start=start1
		self._point_end=end1
		self._middle = None
		global VisualSegments
		if VisualSegments is not None:
			VisualSegments[self]=self
		else:
			VisualSegments = {}
			VisualSegments[self]=self
	def __repr__(self):
		return 'Segment_2({self._point_start[0]},{self._point_start[1]}),({self._point_end[0]},{self._point_end[1]})' .format(self=self)	
	def color(self,x=0,y=0,z=0):
		if(x==0 and y==0 and z==0):
			print self._segment.color
			return
		if type(x).__name__=='tuple':
			self._segment.color=x
			return
		self._segment.color=(x,y,z)
	def source(self):
		return self._point_start
	def target(self):
		return self._point_end
	def opposite(self):
		return Segment_2(self.target(),self.source(),visible=False)
	def squared_length(self):
		return pow((fabs(self._point_start.x()-self._point_end.x())),2)+pow((fabs(self._point_start.y()-self._point_end.y())),2)
	def middle(self):
		if self._middle == None:
			self._middle = Point_2((self._point_start.x()+self._point_end.x())/2,(self._point_start.y()+self._point_end.y())/2,visible=False)
		return self._middle
	def label(self,string):
		self._label=label(pos=self._middle._point.pos,text=string,xoffset=0,yoffset=-6,space=3,height=10,border=1,font='sans')        
	def is_degenerate(self):
		return self.source() == self.target()
	def is_horizontal(self):
		return self._point_start.y() == self._point_end.y()
	def is_vertical(self):
		return self._point_start.x() == self._point_end.x()
	def __eq__(self,other):
		if other == None:
			return False
		return (self.source() == other.source()) and (self.target() == other.target())
	def __ne__(self,other):
		if other == None:
			return False
		return (self.source() != other.source()) or (self.target() != other.target())
	def vertex(self,i):
		if i>=0 and i<=1:
			return self._segment[i]
	def point(self,i):
		if i>=0 and i<=1:
			return self._segment[i]	
	def __getitem__(self,i):
		if i>=0 and i<=1:
			return self._segment[i]
	def min(self):
		if (self._point_start <= self._point_end):
			return self._point_start
		else:
			return self._point_end
	def max(self):
		if (self._point_start >= self._point_end):
			return self._point_start
		else:
			return self._point_end
	def to_vector(self):
		return Vector_2(self._point_end,self._point_start,visible=False)
	def has_on(self,other):
		if type(other).__name__== 'Point_2':
			if ((self._point_start.x()-other.x())*(self._point_end.y()-other.y()))-((self._point_start.y()-other.y())*(self._point_end.x()-other.x())) == 0:
				return self.min() <= other <= self.max()
	def supporting_line(self):
		return Line_2(self._point_start,self._point_end,visible=False)
	def visual(self,visible=None): #argue how will work
		if visible == None:
			self._segment.visible = not self._segment.visible
		else:
			self._segment.visible = visible
		return self._segment.visible
	def color(self,x=0,y=0,z=0):
		if(x==0 and y==0 and z==0):
			print self._segment.color
			return
		if type(x).__name__=='tuple':
			self._segment.color=x
			return
		self._segment.color=(x,y,z)
	def direction(self):
		return Direction_2(self)

	
class Triangle_2(object):
	def __init__(self,x,y,z):
		if type(x).__name__ == type(y).__name__ == type(z).__name__ == 'Point_2':
			self._vertex=[]
			self._segments=[]
			self._vertex.extend([x,y,z])
			self._segments.extend([Segment_2(x,y),Segment_2(y,z),Segment_2(z,x)])
			self._orientation = orien[orientation(x,y,z)]
		else:
			raise No_Constructor([self,x,y,z])
	def __eq__(self,other):
		if other == None:
			return False
		return is_permute(self._vertex,other.vertexs()) and self._orientation == other.orientation()
	def __ne__(self,other):
		if other == None:
			return False
		return not is_permute(self._vertex,other.vertexs()) or self._orientation != other.orientation()
	def vertex(self,i):
		return self._vertex[i%3]
	def __getitem__(self,i):
		return self.vertex(i)
	def is_degenerate(self):
		return self.orientation() == COLLINEAR
	def orientation(self):
		return self._orientation
	def oriented_side(self,p):
		if self.is_degenerate():
			raise Is_Degenerate(self)
		x =[]
		for i in range(3):
			x.append(orientation(self._segments[i].source(),self._segments[i].target(),p))
			if x[-1] == "COLLINEAR":
				return 0
		if x[0] == x[1] == x[2]:
			return -1
		else:
			return 1
	def bounded_side(self,p):
		if self.is_degenerate():
			raise Is_Degenerate(self)
		o = self.oriented_side(p)
		if o == 0:
			return 0
		if o < 0 and self._orientation <0:
			return 1
		if o < 0 and self._orientation>0:
			return -1
		if o > 0 and self._orientation <0:
			return -1
		if o > 0 and self._orientation>0:
			return 1		
	def opposite(self):
		return Triangle_2(self._vertex[2],self._vertex[1],self._vertex[0])
	def area(self):
		"""
		From Heron formula
		"""
		a = self._vertex[0].squared_length()
		b = self._vertex[1].squared_length()
		c = self._vertex[2].squared_length()
		s = (a+b+c)/2
		return sqrt(s*(s-a)*(s-b)*(s-c))
		
	
#class Iso_rectangle_2(object):
class Circle_2(object):
	def __init__(self,x,y,z="COUNTERCLOCKWISE",color=(1,1,1),visible=True):
		if type(x).__name__ == type(y).__name__ == type(z).__name__ == 'Point_2':
			o = orientation(x,y,z)
			if o != COLLINEAR:
				self._orientation = orien[o]
			l1 = Line_2(x,y,visible=False)
			l2 = Line_2(y,z,visible=False)
			self._center = intersection(l1.perpendicular(),l2.perpendicular())
			s = Segment_2(self._center,x,visible=False)
			self._sqradius = s.squared_length()
		elif type(x).__name__ == type(y).__name__ == 'Point_2' and type(z).__name__ == 'str':
			if z != "COLLINEAR":
				self._orientation = orien[z]
				s = Segment_2(p,q)
				self._center = s.middle()
				self._sqradius = s.squared_length()/2
		elif type(x).__name__ == 'Point_2' and type(y).__name__ == 'str':
			if y != "COLLINEAR":
				self._center =x
				self._sqradius =0
		elif type(x).__name__ =='Point_2' and (type(y).__name__ == 'int' or type(y).__name__ == 'float') and type(z).__name__ == 'str':
				if z != "COLLINEAR" and y >= 0:
					self._center =x
					self._orientation = orien[z]
					self._sqradius = y
		else:
			raise No_Constructor([self,x,y,z])
		self._circle = ring(pos = (self._center.x(),self._center.y(),0), axis=(0,0,1),thickness=0.02,radius = sqrt(self._sqradius),color=color,visible=visible)
	def center(self):
		return self._center
	def squared_radius(self):
		return self._sqradius
	def orientation(self):
		return self._orientation
	def is_degenerate(self):
		return self._sqradius == 0
	def opposite(self):
		ori = rorien[-self._orientation]
		return Circle_2(self._center,self._sqradius,ori)
	def oriented_side(self,p):
		s = Segment_2(self._center,p,visible=False)
		ori = s.squared_length() - self._sqradious
		if ori == 0:
			return ori
		if ori < 0:
			return -1
		if ori > 0:
			return 1
	def bounded_side(self,p):
		s = Segment_2(self._center,p,visible=False)
		ori = s.squared_length() - self._sqradious
		if ori == 0:
			return ori
		if ori < 0:
			return -1
		if ori > 0:
			return 1		
	
			
			
def orientation(a,b,c):
		orie = ((a.x()-c.x())*(b.y()-c.y()))-((a.y()-c.y())*(b.x()-c.x()))
		if orie == 0:
			return "COLLINEAR"
		elif orie < 0:
			return "CLOCKWISE"
		else:
			return "COUNTERCLOCKWISE"
def intersection(a,b):
	"""
	Intersection in 2d
	"""
	if type(a).__name__ == type(b).__name__ =='Line_2':
		p = (a.a()*b.b()) - (a.b()*b.a())
		if p != 0:
			return Point_2((-a.c()*b.b()+a.b()*b.c())/p,(-(a.a()*b.c())+a.c()*b.a())/p)
	elif type(a).__name__ == type(b).__name__ =='Segment_2':
		max1 = a.max()
		min1 = a.min()
		max2 = b.max()
		min2 = b.min()
		r = intersection(a.supporting_line(),b.supporting_line())
		if r >= min1 and r>=min2 and r <=max1 and r<=max2:
			return r
		else:
			return None
	else:
		return None
		

def run(Vpoints):
      """
      Jarvis Convex Hull algorithm.
      points is a list of CGAL.Point_2 points
      """
      points = Vpoints.values()
      import random
      r0 = min(points)
      hull = [r0]
      r,u = r0,None
      remainingPoints = [x for x in points if x not in hull]
      while (u != r0) and remainingPoints:
            u = random.choice(remainingPoints)
            for t in points:
                  if t != u and \
                     (orientation(r,u,t) == CLOCKWISE or \
                     (orientation(r,u,t) == COLLINEAR and \
                     (u-r).direction() == (t-u).direction())):
                        u = t
            r = u
            if r != r0:
				points.remove(r)
				hull.append(r)
				remainingPoints.remove(r)
      for t in range(len(hull)):
       if t != len(hull)-1:
        Segment_2(hull[t],hull[t+1])
       else:
		Segment_2(hull[-1],hull[0])
      return hull

prepareScene()
#prepareControls()
#m=[]
#m=getVisualPoints()
#print m
#t = jarvis(m)
#print t 
#print VisualPoints
#a = Segment_2(VisualPoints[m[0]],VisualPoints[m[1]])
#b = Segment_2(VisualPoints[m[0]],VisualPoints[m[2]])
#sleep(5)
#movePoints()
#print VisualPoints
#if orientation(VisualPoints[m[0]],VisualPoints[m[1]],VisualPoints[m[2]]) == CLOCKWISE:
#if orientation(Point_2(1,1),Point_2(2,2),Point_2(3,3)) == COLLINEAR:
#	print "NiCe"
#################Line_2##################
#l=Line_2(3,4,29)
#x=l.x_at_y(0)
#c = Point_2(l.x_at_y(0),0,visible=True,color=(1,0,0))
#print l.oriented_side(c)
################Ray_2######################
a = Point_2(1,1)
b = Point_2(3,3)
c = Point_2(3,8)
d = Point_2(1,4)
e = Point_2(2,5,color=(1,0,0))
f = Point_2(0,0,color=(0.4,1,0.7))
g = Point_2(3,-2)


tr = Triangle_2(c,f,g)
print tr.bounded_side(a)
print tr.bounded_side(b)
print tr.bounded_side(d)
print tr.bounded_side(e)
tr1 = tr.opposite()
print tr1.bounded_side(a)
print tr1.bounded_side(b)
print tr1.bounded_side(d)
print tr1.bounded_side(e)
#s1 = Segment_2(b,c)
#s2 = Segment_2(a,d)
#s3 = Segment_2(a,b)
#s4 = Segment_2(c,a)
#print orientation(c,a,e)
'''
v1 = Vector_2(0,5)
v2 = Vector_2(3,0)
v3 = Vector_2(s3)
v4 = Vector_2(s4)
v5 = Vector_2(2,6)

d1 = Direction_2(1,2)
d2 = Direction_2(0,5)
d3 = Direction_2(s1)
d4 = Direction_2(7,0)
d5 = Direction_2(0,0)
d6 = Direction_2(s2)



l1 = Line_2(s2,color=(0,0,1))


l2 = Line_2(s3)
print l2.a()
print l2.b()
print l2.c()
print l2.direction()
wl = l2.perpendicular(d)
wl.visual()
print wl.point(1)
print wl.point(100)
print wl.direction()
print l2.point(1)
print l2.point(100)
print l2.x_at_y(4)
print l2.y_at_x(3)


print l2.oriented_side(c)
print l2.oriented_side(f)
print l2.oriented_side(g)

sleep(5)
l3 = Line_2(s1,color=(0,1,1))

sleep(5)
l4 = Line_2(d,v2,color=(1,0,0))

sleep(5)
l5 = Line_2(b,v1,color=(1,0,1))

sleep(5)
l6 = Line_2(c,d2,color=(1,1,0))

sleep(5)
l7 = Line_2(a,d4,color=(0.5,0.5,0.5))

sleep(5)
l8 = Line_2(a,c,color=(0,0.5,0.5))

sleep(5)
l9 = Line_2(b,d)

a.color(color.red)
b.color(color.red)
c.color(color.red)
d.color(color.red)

r1 = Ray_2(b,e,color=color.green)
sleep(5)
ss = Segment_2(b,e)
sleep(5)
ll = ss.supporting_line()
ll.visual()
print ll.direction()
sleep(5)
lr1 = r1.supporting_line()
print lr1.direction()
lr1.visual()
print lr1.direction()
sleep(5)
r2 = Ray_2(b,v5,color=(0,0,1))
sleep(5)
l = Line_2(b,v5,color = (1,0,0))
sleep(5)
r3 = Ray_2(b,d1,color=(1,0,1))
sleep(5)
re = Line_2(b,d1,color = (0,1,0))
'''


#l = Line_2(3,3,4,color = (1,0,0))
#re = Line_2(3,3,9,color = (0,1,0))

#s1 = Segment_2(e,b)
#s2 = Segment_2(e,f)
#r = intersection(s1,s2)
#if r :
#	r.color(1,0,1)

#c = Circle_2(f,2)

"""
a = Point_2(1,1)
b = Point_2(3,3)
c = Point_2()

#g = mouseClick()
#t=Point_2(g.pos.x,g.pos.y)
#print "mouse click pos ",g.pos.x, "lalalal ",g.pos.y
#t.color(1,1,0)
##orientation
#print ((a.x-c.x)*(b.y-c.y))-((a.y-c.y)*(b.x-c.x))
##

rod = Segment_2(a,b)
rod.color(0,0,1)
rod.label("ert")
d= rod.source()
e= rod.target()
d.color(1,0,1)
a.color()
#for seeing the difference
scene.mouse.getclick()
a.color(color.cyan)
#point
a.color()
print a.x()
print a.y()
print a
print a[0]
print a[1]
print a.dimension()
print a == d
print a == e
print d != e
print d < e
print a < d
print a <= d
print a >= d
print a >= e
print a <= e
for poin in e.iter():
	print poin
dd = d+e
print dd
#vector
r = d-e
print r
print -r
#segment
print rod
print rod.min()
print rod.max()
f=rod.middle()
print rod.has_on(f)
print rod.has_on(dd)
print rod.has_on(c)
print f
rod.color()
print rod.squared_length()
"""
