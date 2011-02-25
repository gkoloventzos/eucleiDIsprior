from __future__ import division
from visual import *
from visual.controls import *
from time import sleep

VisualPoints = None
VisualSegments = None
control = None

CLOCKWISE = -1
COUNTERCLOCKWISE = 1
COLLINEAR = 0

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

	f = VisualPoints.keys()
	for ke in f:
		if VisualPoints[ke]._point.visible == False:
			del VisualPoints[ke]

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

class Point_2(object):
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
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return True
		return (self.x()==other.x()) and (self.y()==other.y())
	def __ne__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return True
		return (self.x()!=other.x()) or (self.y()!=other.y())
	def __gt__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return True
		return self.x() < other.x() or ( self.x() == other.x() and self.y() < other.y() )
	def __lt__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return True
		return self.x() > other.x() or ( self.x() == other.x() and self.y() > other.y() )
	def __ge__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return True
		return self.x() >= other.x()
	def __le__(self,other):
		if type(self).__name__=='NoneType' or type(other).__name__=='NoneType':
			return True
		return self.x() <= other.x()
	def __getitem__(self,i):
		if i>=0 and i<=1:
			return self._point.pos[i]

"""
	kanei swsta thn anathesi omws dn allazei to xrwma :'(
	def get_color(self):
		return self._point.color
	def set_color(self,color):
		self._point.color = color
	color = property(get_color,set_color)
"""

class Vector_2(object):
	def __init__(self,x=None,y=None):
		if type(x).__name__==type(y).__name__=='NoneType':
			self._vector=None
		if type(x).__name__==type(y).__name__== 'Point_2':
			self._vector=vector(y.x()-x.x(),y.y()-x.y())
		if (type(x).__name__==type(y).__name__=='int') or(type(x).__name__==type(y).__name__=='float'):
			self._vector=(x,y)
		if type(y).__name__ == 'NoneType':
			if type(x).__name__=='Segment_2':
				self._vector=vector(x._point_end.pos[0] - x._point_start.pos[0],x._point_end.pos[1] - x._point_start.pos[1])
			elif type(x).__name__=='Ray_2':
				pass
			elif type(x).__name__=='Line_2':
				pass
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
		return self._vector == other._vector
	def __ne__(self,other):
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
		
		
class Direction_2(object):
	def __init__(self,x,y=None):
		self._d=[]
		if type(y).__name__=='NoneType':
			if type(x).__name__=='Vector_2':
				self._direction=x.y()/x.x()
				self._d.append(x.x())
				self._d.append(x.y())				
			if type(x).__name__=='Line_2':
				pass
			if type(x).__name__=='Ray_2':
				pass
			if type(x).__name__=='Segment_2':
				s=x.source()
				t=x.target()
				self._d.append(t.x()-s.x())
				self._d.append(t.y()-s.y())
				self._direction= self._d[1]/self._d[0]
		else:
			self._direction=x/y
			self._d.append(x)
			self._d.append(y)
	def delta(self,i):
		if i>=0 and i<=1:
			self._d[i]
	def direction(self):
		return self._direction
	def dx(self):
		return self._d[0]
	def dy(self):
		return self._d[1]
	def __neg__(self):
		return Direction_2(-self._d[0],self._d[1])
	def vector(self):
		return Vector_2(self._d[0],self._d[1])
	def __eq__(self,other):
		return self.vector() == other.vector()
	def __ne__(self,other):
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
				
			
class Line_2(object):
	"""
	Line in 2d
	"""
	def __init__(self,a,b=None,c=None):
		self._a=None
		self._b=None
		self._c=None
		if b == None and c == None:
			if type(a).__name__ == 'Segment_2':
				x=a.source()
				y=a.target()
				self._b=-1
				self._a=(y.y() - x.y())/(y.x() - x.x())
				self._c=y.y() - (self._a*y.x())
			if type(a).__name__ == 'Ray_2':
				pass
		if c == None:
			if type(a).__name__ == 'Point_2' and type(b).__name__ =='Vector_2':
				x=a
				y=b.directio()
				self._b=-1
				self._a=b.direction()
				self._c=x.y() - (self._a*x.x())
			if type(a).__name__ == 'Point_2' and type(b).__name__ =='Direction_2':
				x=a
				y=b
				self._b=-1
				self._a=b.direction()
				self._c=x.y() - (self._a*x.x())
			if type(a).__name__ == 'Point_2' and type(b).__name__ =='Point_2':
				x=a
				y=b
				self._b=-1
				self._a=(y.y() - x.y())/(y.x() - x.x())
				self._c=y.y() - (self._a*y.x())				
		if (isinstance(a,float) or isinstance(a,int)) and (isinstance(b,float) or isinstance(b,int)) and (isinstance(c,float) or isinstance(c,int)):
			if b == 0:
				self._b = None
			self._b=-1
			self._a=-(a/b)
			self._c=-(c/b)
	def a(self):
		return self._a			
	def b(self):
		return self._b
	def c(self):
		return self._c
	def is_degenerate(self):
		return a == b == 0
	def is_horizontal():
		return self._a ==0
	
#class Ray_2(object):
class Segment_2(object):
	"""
	Segment in 2d
	"""
	def __init__(self,start1,end1):
		self._segment=curve(pos=[(start1.x(), start1.y()),(end1.x(), end1.y())])
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
		return Segment_2(self.target(),self.source())
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
		return (self.source() == other.source()) and (self.target() == other.target())
	def __ne__(self,other):
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
		return Vector_2(self._point_end,self._point_start)
	def has_on(self,other):
		if type(other).__name__== 'Point_2':
			if ((self._point_start.x()-other.x())*(self._point_end.y()-other.y()))-((self._point_start.y()-other.y())*(self._point_end.x()-other.x())) == 0:
				return self.min() <= other <= self.max()

	
#class Triangle_2(object):
#class Iso_rectangle_2(object):
#class Circle_2(object):
def orientation(a,b,c):
		orie = ((a.x()-c.x())*(b.y()-c.y()))-((a.y()-c.y())*(b.x()-c.x()))
		if orie == 0:
			return COLLINEAR
		elif orie < 0:
			return CLOCKWISE
		else:
			return COUNTERCLOCKWISE

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
      print hull
      return hull

prepareScene()
prepareControls()
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
