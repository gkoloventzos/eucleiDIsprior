#!/usr/local/bin/python
from __future__ import division
from visual import *
from visual.controls import *
import time,operator
from decimal import *
from math import pow,fabs,sqrt

PrepareScene = False
VisualPoints = None
VVPoint = []
VisualSegments = None
control = None

orien = {"CLOCKWISE":-1,"COLLINEAR":0,"COUNTERCLOCKWISE":1}
rorien = {-1:"CLOCKWISE",0:"COLLINEAR",1:"COUNTERCLOCKWISE"}
sides = {"ON_NEGATIVE_SIDE":-1,"ON_ORIENTED_BOUNDARY":0,"ON_POSITIVE_SIDE":1}
rsides = {-1:"ON_NEGATIVE_SIDE",0:"ON_ORIENTED_BOUNDARY",1:"ON_POSITIVE_SIDE"}
CLOCKWISE = ON_NEGATIVE_SIDE = -1
COUNTERCLOCKWISE = ON_POSITIVE_SIDE = 1
COLLINEAR = ON_ORIENTED_BOUNDARY = 0
EP = 15 #Extreme Point for creating lines and rays which does not have a particulary end

#Exception if someone tries to create an object with false input
class No_Constructor(Exception):
    """
    Exception if someone tries to create an object with false input
    """
    def __init__(self,value):
        self.name = type(value[0]).__name__
        self.parameters = value[1:]
    def repr(self):
        print '{self.name} has no constructor with this arguments' .format(self=self),
        for i in xrange(self.parameters):
            if self.parameters[i] != None:
                print '{self.parameters[i]}' .format(self=self),
            
#Exception for the degenarate objects there are in CGAL
class Is_Degenerate(Exception):
    """
    If an object is degenarate
    """
    def __init__(self,value):
        self.name = type(value).__name__
    def repr(self): 
        print 'The {self.name} is degenerate' .format(self=self)
        
class Wrong_Arguments(Exception):
    """
    If wrong argument given to a function
    """
    def __init__(self,value):
        self.name = type(value).__name__
    def repr(self):
        print '{self.name} cannot take this arguments' .format(self=self),
        for i in xrange(self.parameters):
            if self.parameters[i] != None:
                print '{self.parameters[i]}' .format(self=self),
        
def prepareScene():
    """
    Creates the scene with some default values
    """
    global PrepareScene
    PrepareScene = True
    scene.range = 10
    scene.width = 800
    scene.height = 700
    scene.title = "eukleiDIs"
    scene.exit=0

def quadratic(a, b, c=None):
    """
    Solution of a quadratic equatation
    Is used for the Circle_2 object
    """
    if c: # (ax^2 + bx + c = 0) 
        a, b = b / float(a), c / float(a) 
        t = a / 2.0 
        r = t**2 - b 
        y1 = math.sqrt(r) 
        return y1 - t, y2 - t 

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
    global PrepareScene
    if (not PrepareScene):
        prepareScene()
    points =[]
    while True:
        if scene.kb.keys:
            s = scene.kb.getkey()
            if s == 'backspace':
                break
        if scene.mouse.clicked:
            click = scene.mouse.getclick()
            point = Point_2(str(click.pos.x),str(click.pos.y))
#           stri = str(click.pos.x) + "," + str(click.pos.y)
#           point.label(stri)
            if point not in points:
                points.append(point)
#    print VVPoint
    return points
    
def getPolygon():
    """
    Function for getting a polygon from the user.
    In order to stop inserting points the user must 
    hit the backspace button
    """
    global PrepareScene
    if not PrepareScene:
        prepareScene()
    points =[]
    segments =[]
    while True:
        if scene.kb.keys:
            s = scene.kb.getkey()
            if s == 'backspace':
                break
        if scene.mouse.clicked:
            click = scene.mouse.getclick()
            point = Point_2(str(click.pos.x),str(click.pos.y))
            points.append(point)
            if len(points)>1:
                segment = Segment_2(points[-2],points[-1])
                segments.append(segment)
    segment = Segment_2(points[-1],points[0])
    segments.append(segment)
    return points,segments
            
def movePoints():
    """
    Function for moving points from the plane.
    """
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
                    global VVPoint
                    drag_pos = m1.pickpos # where on the ball
                    pick = m1.pick # pick now true (not None)
                elif m1.drop: # released at end of drag
                    poin.set_xy(str(m1.pos.x),str(m1.pos.y))
                    pick = None # end dragging (None is false)
        if pick:
            # project onto xy plane, even if scene rotated:
            new_pos = scene.mouse.project(normal=(0,0,1))
            if new_pos != drag_pos: # if mouse has moved
                # offset for where the ball was clicked:
                pick.pos += new_pos - drag_pos
                drag_pos = new_pos # update drag position
                #run()  #run the function.
#    print VVPoint
    return VVPoint
        


def prepareControls():
    """
        Preparing the buttons for controling the schene.
    """
    w = 380
    global control
    global VisualPoints
    control = controls(title='Controlling eukleiDIs',x=800, y=0, width=w, height=w, range=60)
    mv = button(pos=(-30,40), height=20, width=50, text='Move Points', action=lambda: movePoints())
    gp = button(pos=(30,40), height=20, width=50, text='Insert Points', action=lambda: getVisualPoints())
    dap = button(pos=(-30,10), height=20, width=50, text='Del Points', action=lambda: getVisualPoints())
    das = button(pos=(30,10), height=20, width=50, text='Del Segments', action=lambda: getVisualPoints())
    ru = button(pos=(0,-20), height=20, width=50, color = (1,0,0), text='Run', action=lambda: run(VVPoint))
    while 1:
        control.interact()

def is_permute(l1,l2):
    """
    Returning True if l2 is a cyclic permutation of l1
    """
    if l1 == l2:
        return true
    for i in xrange(0,len(l1)-1):
        list1 = l1[1:len(l1)]
        list1.append(l1[0])
        if list1 == l2:
            return True
        l1 = list1
    return False

def isgood(x):
    """
        Returns if the instance x is good for inserting as value for coordinates
    """
    return (isinstance(x,float) or isinstance(x,int) or isinstance(x,str) or isinstance(x,Decimal))

def issame(x,y):
    """
        Return if the 2 objects are the same class
    """
    return type(x) == type(y)
    
def incone(i, j, P):
    n = len(P)
    i1 = (i+1)%n					# i+1
    in1 = (i+n-1)%n					# i-1
    cc = orien[orientation(P[in1], P[i], P[i1])]
    if cc >= 0 :			# CCW or collinear
        if orien[orientation(P[in1], P[i], P[j])] == 1 and orien[orientation(P[i], P[j], P[i1])] == -1:
            return True
    else:						# CW
        if orien[orientation(P[in1], P[i], P[j])] == 1 or orien[orientation(P[i], P[i1], P[j])] ==1:
            return True
    return False

def diagonalie(i, j, P):
	n = len(P)
	s = Segment_2(P[i], P[j],visible=False)
	for k in range(n):				# intersection of two segments
		p = intersection(s, Segment_2(P[k], P[(k+1)%n]))
		if isinstance(p,Point_2) and p not in P:	# exlude Points i, j
			return False
	return True
    
#########################################################################################
class Point_2(object):#all clear
    """
    Point in 2d
    """
    def __init__(self,x=0,y=0,color=(1,1,1),visible=True): #using visible not opacity for older versions
        global PrepareScene
        if (not PrepareScene):
            prepareScene()
        if (not isgood(x)) and (not isgood(y)):
            raise No_Constructor([self,x,y])
        self._pos=[]
        add_string = "0."
        add_string += "0" * getcontext().prec
        self._x = Decimal(str(x)) + Decimal(add_string) # http://docs.python.org/release/2.5.2/lib/node130.html
        self._y = Decimal(str(y)) + Decimal(add_string)
        self._pos.append(self._x)
        self._pos.append(self._y)
        self._point=sphere(pos=(float(x),float(y),0),radius=0.1,color=color,visible=visible)
        self._color=color
        self._visible=visible
#        global VisualPoints
#        if VisualPoints is not None:
#            VisualPoints[self]=self
#        else:
#            VisualPoints = {}
#            VisualPoints[self]=self
#        global VVPoint
#        VVPoint.append(self)
    def __repr__(self):
        return "Point_2 (%s,%s)" % (self._x, self._y)
    """
    def set_x(self,x):
        self._x = Decimal(str(x)) + Decimal('0.000000000000000000000000000')
        self._pos[0]=self._x
        self._color=self._point.color
        self._visible=self._point.visible
        self._point.visible =False # deleteing the point
        self._point=sphere(pos=(float(self._x),float(self._y),0),radius=0.1,color=self._color,visible=self._visible)
    def set_y(self,y):
        self._y = Decimal(str(y)) + Decimal('0.000000000000000000000000000')
        self._pos[1]=self._y
        self._color=self._point.color
        self._visible=self._point.visible
        self._point.visible=False # deleteing the point
        self._point=sphere(pos=(float(self._x),float(self._y),0),radius=0.1,color=self._color,visible=self._visible)
    def set_xy(self,x,y):
        self._x = Decimal(str(x)) + Decimal('0.000000000000000000000000000')
        self._y = Decimal(str(y)) + Decimal('0.000000000000000000000000000')
        self._pos[0]=self._x
        self._pos[1]=self._y
        self._color=self._point.color
        self._visible=self._point.visible
        self._point.visible=False # deleteing the point
        self._point=sphere(pos=(float(self._x),float(self._y),0),radius=0.1,color=self._color,visible=self._visible)
    """
    def x(self):
        return self._x
    def y(self):
        return self._y
    def pos(self):
        return self._point
    def label(self,string):
        self._label=label(pos=self._point.pos,text=string,xoffset=0,yoffset=5,space=self._point.radius,height=10,border=1,font='sans')
    def color(self,x=0,y=0,z=0):
        if(x==0 and y==0 and z==0):
            print self._point.color
            return
        if isinstance(x,tuple):
            self._point.color=x
            return
        self._point.color=(x,y,z)
    def cartesian(self,i):
        if i>=0 and i<=1:
            return self._pos[i]
    def dimension(self):
        return 2
#generator in order to emulate th iterators of CGAL
    def iter(self):
        for index in xrange(2):
            yield self._pos[index]
    def __add__(self,other):
        if isinstance(other,Vector_2):
            return Point_2(other.x()+self.x(),other.y()+self.y())
        else:
            raise Wrong_Arguments([self,self,other])
    def __sub__(self,other):
            if type(self)==type(other):
                return Vector_2(self,other)
            elif isinstance(other,Vector_2):
                return Point_2(self.x()-other.x(),self.y()-other.y())
            else:
                raise Wrong_Arguments([self,self,other])                
    def __eq__(self,other):
        if other == None:
            return False
        elif issame(self,other):
            return (self.x()==other.x()) and (self.y()==other.y())
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other==None:
            return True
        elif issame(self,other):
            return (self.x()!=other.x()) or (self.y()!=other.y())
        else:
            raise Wrong_Arguments([self,self,other])
    def __gt__(self,other):
        if other==None:
            return False
        elif issame(self,other):
            return self.x() > other.x() or ( self.x() == other.x() and self.y() > other.y() )
        else:
            raise Wrong_Arguments([self,self,other])
    def __lt__(self,other):
        if self==None or other==None:
            return False
        elif issame(self,other):
            return self.x() < other.x() or ( self.x() == other.x() and self.y() < other.y() )
        else:
            raise Wrong_Arguments([self,self,other])
    def __ge__(self,other):
        if other==None:
            return False
        if issame(self,other):
            if self == other:
                return True
            return self.x() > other.x() or ( self.x() == other.x() and self.y() > other.y() )
        else:
            raise Wrong_Arguments([self,self,other])
    def __le__(self,other):
        if other==None:
            return False
        if issame(self,other):
            if self == other:
                return True
            return self.x() < other.x() or ( self.x() == other.x() and self.y() < other.y() )
        else:
            raise Wrong_Arguments([self,self,other])
    def __getitem__(self,i):
        if i>=0 and i<=1:
            return self._pos[i]
    def visual(self,visible=None): #argue how will work
        if visible == None:
            self._point.visible = not self._point.visible
        else:
            self._point.visible = visible
        return self._point.visible


class Vector_2(object):
    """
    Vector in 2d
    """
    def __init__(self,x=None,y=None,visible=True):
        if x==y==None:
            raise No_Constructor([self,x,y])
        if isinstance(x,Point_2) and isinstance(y,Point_2):
            self._vector=vector(y.x()-x.x(),y.y()-x.y())
        if (isgood(x)) and (isgood(y)):
            self._vector=vector(Decimal(str(x)),Decimal(str(y)))
        if y==None:
            if isinstance(x,Segment_2):
                a = x.source()
                b = x.target()
                self._vector=vector(b.x() -a.x(),b.y() - a.y())
            elif isinstance(x,Ray_2):
                s = x.direction()
                self._vector=vector(s.dx(),s.dy())
            elif isinstance(x,Line_2):
                self._vector=vector(x.b(),-x.a())
            else:
                raise No_Constructor([self,x,y])
    def __repr__(self):
        return 'Vector_2({self._vector[0]},{self._vector[1]})' .format(self=self)
    def x(self):
        return Decimal(str(self._vector[0]))
    def y(self):
        return Decimal(str(self._vector[1]))
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
        elif issame(self,other):
            return self._vector == other._vector
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other == None:
            return True
        elif issame(self,other):
            return self._vector != other._vector
        else:
            raise Wrong_Arguments([self,self,other])
    def __getitem__(self,i):
        if i>=0 and i<=1:
            return self._vector[i]
    def squared_length(self):
        return mag2(self._vector)
    def __neg__(self):
        return Vector_2(-self.x(),-self.y())
    def __mul__(self,other):
        if isinstance(other,Vector_2):
            return dot(self,other)
        elif isinstance(other,Point_2):
            return Vector_2(other*self.x(),other*self.y())
        else:
            raise Wrong_Arguments([self,self,other])
    def __div__(self,other): #if want exception
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
        if y==None:
            if isinstance(x,Vector_2):
                if x.x() == 0:
                    self._direction = None
                else:
                    self._direction=x.y()/x.x()
                self._d.extend([x.x(),x.y()])               
            elif isinstance(x,Line_2):
                self._direction=x.direction()
                self._d.extend[-x.a(),x.b()]
            elif isinstance(x,Ray_2):
                f = x.to_vector()
                self = Direction_2(f)
            elif isinstance(x,Segment_2):
                s=x.source()
                t=x.target()
                self._d.extend([t.x()-s.x(),t.y()-s.y()])
                if self._d[0] == 0:
                    self._direction = None
                else:
                    self._direction= self._d[1]/self._d[0]
            else:
                raise No_Constructor([self,x,y])
        elif (isgood(x)) and (isgood(y)):
            if x == 0:
                self._direction = None
            else:
                self._direction=Decimal(str(y))/Decimal(str(x))
            self._d.extend([Decimal(str(x)),Decimal(str(y))])
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
        if self._direction==None:
            return self
        if self._d[0]!= 0:
            return Direction_2(-self._d[0],self._d[1])
        return Direction_2(self._d[0],-self._d[1])
    def vector(self):
        return Vector_2(self._d[0],self._d[1],visible=False)
    def __eq__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            return self._direction == other
        if isinstance(other,Direction_2) and isinstance(self,Direction_2):
            if (self._d[0] == other._d[0] == 0):
                if (self._d[1] < 0 and other._d[1]<0) or (self._d[1] > 0 and other._d[1] > 0):
                    return True
                else:
                    return False
            if (self._d[1] == other._d[1] == 0):
                if (self._d[0] < 0 and other._d[0]<0) or (self._d[0] > 0 and other._d[0] > 0):
                    return True
                else:
                    return False                
        if other == None and self._direction == None:
            return True
        return False
    def __ne__(self,other):
        if other == None:
            return True
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
        if not isinstance(b,Direction_2) and b == None and c == None:
            if isinstance(a,Segment_2):
                x=a.source()
                y=a.target()
                if a.is_degenerate():
                    raise Degenetate_Segment([self,a,b,c])
                self._b=(y.x() - x.x()) # y = -(y2-y1)/(x2-x1)*x +c
                self._a=-(y.y() - x.y())
                self._c=-(self._b*x.y()+self._a*x.x())
            elif isinstance(a,Ray_2):
                self = Line_2(a.source(),a.direction())
            else:
                raise No_Constructor([self,a,b,c])
        elif c == None:
            if isinstance(a,Point_2) and isinstance(b,Vector_2):
                self._b=b.x()
                self._a=-b.y()
                self._c=-(self._b*a.y()+self._a*a.x())
            if isinstance(a,Point_2) and isinstance(b,Direction_2):
                self._b=b.delta(0)
                self._a=-b.delta(1)
                if a.y() != None and a.x() != None:
                    self._c=-(self._b*a.y()+self._a*a.x())
                else:
                    self._c=0
            if isinstance(a,Point_2) and isinstance(b,Point_2):
                p=Segment_2(a,b,visible=False)
                x=p.source()
                y=p.target()
                if p.is_degenerate():
                    raise Degenetate_Segment
                self._b=(y.x() - x.x())
                self._a=-(y.y() - x.y())
                self._c=-(self._b*y.y()+self._a*y.x())
                del p
        elif (isgood(a)) and (isgood(b)) and (isgood(c)):
                self._b=Decimal(str(b))
                self._c=Decimal(str(c))
                self._a=Decimal(str(a))
                if self._a == None and self._b == None and self._c == None:
                    raise No_Constructor([self,a,b,c])
        if self.is_vertical():
            f = self._c/self._a
            self._line=curve(pos=[(float(-f), -EP),(float(-f),EP)],color=color,visible=visible)
        elif self.is_horizontal():
            f = self._c/self._b
            self._line=curve(pos=[(-EP,float(-f)),(EP,float(-f))],color=color,visible=visible)
        else:
            self._line=curve(pos=[(-EP, float(self.y_at_x(-EP))),(EP,float(self.y_at_x(EP)))],color=color,visible=visible)
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
        else:
            return 
    def __repr__(self):
        return 'Line_2({self._a} x + {self._b} y + {self._c} = 0)' .format(self=self)
    def visual(self,visible=None): #argue how will work
        if visible == None:
            self._line.visible = not self._line.visible
        else:
            self._line.visible = visible
        return self._line.visible
    def oriented_side(self,c):
        if self.is_vertical():
            a = Point_2(-self.c(),0,visible=False)
            b = Point_2(-self.c(),1,visible=False)
        elif self.is_horizontal():
            a = Point_2(0,-self.c(),visible=False)
            b = Point_2(1,-self.c(),visible=False)
        else:
            x1 = self.x_at_y(1)
            y1 = self.y_at_x(x1+1)
            a = Point_2(x1,1,visible=False)
            b = Point_2(x1+1,y1,visible=False)
        s1 = Decimal(a.x()-c.x())*(b.y()-c.y())
        s2 = Decimal(a.y()-c.y())*(b.x()-c.x())
        s1 = s1.quantize(Decimal('1.00000000000000000000000000'))
        s2 = s2.quantize(Decimal('1.00000000000000000000000000'))
        orie = s1-s2
        del a,b
        if orie == 0:
            return rsides[0]
        elif orie < 0:
            return rsides[-1]
        else:
            return rsides[1]
    def point(self,i):
        if self.is_horizontal():
            return Point_2(i,self.c(),visible=False)
        if self.is_vertical():
            return Point_2(self.c(),i,visible=False)
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
        return sides[self.oriented_side(p)] == 0
    def has_on_positive_side(self,p):
        return sides[self.oriented_side(p)] == 1
    def has_on_negative_side(self,p):
        return sides[self.oriented_side(p)] == -1
    def __eq__(self,other):
        if other == None:
            return False
        elif issame(self,other):
            l = intersection(self,other,False)
            return isinstance(l,Line_2)
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other == None:
            return True
        elif issame(self,other):
            return not (self==other)
        else:
            raise Wrong_Arguments([self,self,other])
    def color(self,x=0,y=0,z=0):
        if(x==0 and y==0 and z==0):
            print self._line.color
            return
        if isinstance(x,tuple):
            self._line.color=x
            return
        self._line.color=(x,y,z)
            
class Ray_2(object):
    """
    Ray in 2d
    """
    def __init__(self,x,y,color=(1,1,1),visible=True):
        self._direction=None
        if not isinstance(x,Point_2):
            raise No_Constructor([self,x,y])
        if isinstance(y,Point_2):
            #y.visual()
            self._direction = Direction_2(Segment_2(x,y,visible=False))
        elif isinstance(y,Direction_2):
            self._direction = y
        elif isinstance(y,Vector_2):
            self._direction = y.direction()
        elif isinstance(y,Line_2):
            self._direction = y.direction()
        else :
            raise No_Constructor([self,x,y])
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
                p = Point_2(x.x(),-EP,visible=False)
            elif d.dy()>0:
                p = Point_2(x.x(),EP,visible=False)
        if d.dy() == 0:
            if d.dx()<0:
                p = Point_2(-EP,x.y(),visible=False)
            elif d.dx()>0:
                p = Point_2(EP,x.y(),visible=False)
        self._source=x
        self._out=p
        self._ray=curve(pos=[(float(x.x()), float(x.y())),(float(p.x()), float(p.y()))],color=color,visible=visible)
        del l
    def color(self,x=0,y=0,z=0):
        if(x==0 and y==0 and z==0):
            print self._ray.color
            return
        if isinstance(x,tuple):
            self._ray.color=x
            return
        self._ray.color=(x,y,z)
    def source(self):
        return self._source
    def out(self):
        return self._out
    def __eq__(self,other):
        if other == None:
            return False
        elif issame(self,other):
            return self._source == other.source() and self._direction == other.direction()
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other == None:
            return True
        elif issame(self,other):
            return self._source != other.source() or self._direction != other.direction()
        else:
            raise Wrong_Arguments([self,self,other])
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
            return l.point(i)
        if i==0:
            return self._source
    def is_degenerate(self):
        return self.point(0) == self.point(1)
    def is_horizontal(self):
        l = sel.supporting_line()
        return l.is_horizontal()
    def is_vertical(self):
        l = sel.supporting_line()
        return l.is_vertical()
    def has_on(self,point):
                s1 = Segment_2(self.source(),self.out(),visible=False)
                ret = s1.has_on(point)
                del s1
                return ret
    def visual(self,visible=None): #argue how will work
        if visible == None:
            self._ray.visible = not self._ray.visible
        else:
            self._ray.visible = visible
        return self._ray.visible
#        l = self.supporting_line()
#        if l.has_on(point):
#            print "here"
#            p = self.source()
#            s = Segment_2(p,point,visible=False)
#            print s.direction()
#            print self.direction()
#            return s.direction() == self.direction()
#        else:
#            return False
        
        

class Segment_2(object):#all clear
    """
    Segment in 2d
    """
    def __init__(self,start1,end1,color=(1,1,1),visible=True):
        if not isinstance(start1,Point_2) and not isinstance(end1,Point_2):
            raise No_Constructor([self,start1,end1])
        self._segment=curve(pos=[(float(start1.x()), float(start1.y())),(float(end1.x()), float(end1.y()))],color=color,visible=visible)
        self._point_start=start1
        self._point_end=end1
        self._middle = None
        self._color = color
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
        if isinstance(x,tuple):
            self._segment.color=x
            self._color=x
            return
        self._segment.color=(x,y,z)
        self._color=(x,y,z)
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
        if self._middle == None:
            self.middle()
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
        elif issame(self,other):
            return (self.source() == other.source()) and (self.target() == other.target())
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other == None:
            return True
        elif (self,other):
            return (self.source() != other.source()) or (self.target() != other.target())
        else:
            raise Wrong_Arguments([self,self,other])
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
        if isinstance(other,Point_2):
            if ((self._point_start.x()-other.x())*(self._point_end.y()-other.y()))-((self._point_start.y()-other.y())*(self._point_end.x()-other.x())) == 0:
                return self.min() <= other <= self.max()
    def supporting_line(self):
        return Line_2(self,color=self._segment.color,visible=False)
    def visual(self,visible=None): #argue how will work
        if visible == None:
            self._segment.visible = not self._segment.visible
        else:
            self._segment.visible = visible
        return self._segment.visible
    def direction(self):
        return Direction_2(self)

    
class Triangle_2(object):
    """
    Triangle_2
    """
    def __init__(self,x,y,z,color=(1,1,1),visible=True):
        if isinstance(x,Point_2) and isinstance(y,Point_2) and isinstance(z,Point_2):
            self._vertex=[]
            self._segments=[]
            self._vertex.extend([x,y,z])
            self._segments.extend([Segment_2(x,y,color =color,visible=visible),Segment_2(y,z,color =color,visible=visible),Segment_2(z,x,color =color,visible=visible)])
            self._orientation = orien[orientation(x,y,z)]
            r=[]
            z1=(z.x(),z.y(),0)
            x1=(x.x(),x.y(),0)
            y1=(y.x(),y.y(),0)
            if self._orientation == -1:
                r.extend([z1,y1,x1])
            else:
                r.extend([x1,y1,z1])
            self._face= faces(pos=r,normal=[(1,1,0),(1,1,0),(1,1,0)],visible=False)
        else:
            raise No_Constructor([self,x,y,z])
    def __eq__(self,other):
        if other == None:
            return False
        elif issame(self,other):
            return is_permute(self._vertex,other.vertexs()) and self._orientation == other.orientation()
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other == None:
            return True
        elif (self,other):
            return not is_permute(self._vertex,other.vertexs()) or self._orientation != other.orientation()
        else:
            raise Wrong_Arguments([self,self,other])
    def vertex(self,i):
        return self._vertex[i%3]
    def edge(self,i):
        return self._segments[i%3]
    def __getitem__(self,i):
        return self.vertex(i)
    def is_degenerate(self):
        return self.orientation() == COLLINEAR
    def orientation(self):
        return self._orientation
    def bounded_side(self,p): # more tests no good understanding
        if self.is_degenerate():
            raise Is_Degenerate(self)
        x =[]
        for i in xrange(3):
            x.append(orientation(self._segments[i].source(),self._segments[i].target(),p))
            if x[-1] == "COLLINEAR":
                return 0
        if x[0] == x[1] == x[2]:
            return -1
        else:
            return 1
    def oriented_side(self,p):
        if self.is_degenerate():
            raise Is_Degenerate(self)
        o = self.bounded_side(p)
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
        a = self._segments[0].squared_length()
        b = self._segments[1].squared_length()
        c = self._segments[2].squared_length()
        s = (a+b+c)/2
        return sqrt(fabs(s*(s-a)*(s-b)*(s-c)))
    def seg_color(self,x=0,y=0,z=0):
        if(x==0 and y==0 and z==0):
            print "Segment {self._segments[0]} {self._segments[0]._color} Segment {self._segments[1]} {self._segments[1]._color} Segment {self._segments[2]} {self._segments[2]._color}" .format(self=self)
            print "\n"
            return
        if type(x).__name__=='tuple':
            for i in xrange(3):
                self._segments[i].color(x)
            return
        for i in xrange(3):
            self._segments[i].color(x,y,z)          
    def poi_color(self,x=0,y=0,z=0): #strange None output
        if(x==0 and y==0 and z==0):
            for i in xrange(3):
                print "Vertex" ,self._vertex[i], "color",self._vertex[i].color()
            return
        if type(x).__name__=='tuple':
            for i in xrange(3):
                self._vertex[i].color(x)
            return
        for i in xrange(3):
            self._vertex[i].color(x,y,z)
    def fill(self,x=0,y=0,z=0):
        if(x==0 and y==0 and z==0):
            print self._face.color
            return
        if type(x).__name__=='tuple':
            self._face.color=x
            self._face.visible=True
            return
        self._face.color=(x,y,z)
        
    
class Circle_2(object):
    def __init__(self,x,y,z="COUNTERCLOCKWISE",color=(1,1,1),visible=True):
        if isinstance(x,Point_2) and isinstance(y,Point_2) and isinstance(z,Point_2):
            o = orientation(x,y,z)
            if o != COLLINEAR:
                self._orientation = orien[o]
            l1 = Line_2(x,y,visible=False)
            l2 = Line_2(y,z,visible=False)
            self._center = intersection(l1.perpendicular(),l2.perpendicular())
            s = Segment_2(self._center,x,visible=False)
            self._sqradius = s.squared_length()
            del l1,l2,s
        elif isinstance(x,Point_2) and isinstance(y,Point_2) and isinstance(z,str):
            if z != "COLLINEAR":
                self._orientation = orien[z]
                s = Segment_2(p,q,visible=False)
                self._center = s.middle()
                self._sqradius = s.squared_length()/2
                del s
        elif isinstance(x,Point_2) and isinstance(y,str):
            if y != "COLLINEAR":
                self._center =x
                self._sqradius =0
        elif isinstance(x,Point_2) and isgood(y) and isinstance(z,str):
                if z != "COLLINEAR" and y >= 0:
                    self._center =x
                    self._orientation = orien[z]
                    self._sqradius = y
        else:
            raise No_Constructor([self,x,y,z])
        self._circle = ring(pos = (float(self._center.x()),float(self._center.y()),0), axis=(0,0,1),thickness=0.02,radius = sqrt(self._sqradius),color=color,visible=visible)
    def center(self):
        return self._center
    def __eq__(self,other):
        if other == None:
            return False
        elif isinstance(other,Circle_2):
            return self.center()==other.center() and self.squared_radius() == other.squared_radius() and other.orientaion() == self.orientation()
        else:
            raise Wrong_Arguments([self,self,other])
    def __ne__(self,other):
        if other == None:
            return True
        elif issame(self,other):
            return not (self==other)
        else:
            raise Wrong_Arguments([self,self,other])
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
        del s
        if ori == 0:
            return ori
        if ori < 0:
            return -1
        if ori > 0:
            return 1
    def bounded_side(self,p):
        s = Segment_2(self._center,p,visible=False)
        ori = s.squared_length() - self._sqradious
        del s
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

def intersection(a,b,c=True):
    """
    Intersection in 2d
    Every Segment, Ray trasformed as Line for intersection
    If there is interesection then we look if it is inside
    the Segment or Ray
    Triangle,Polygon returns list (if empty returns None)
    Circle return either list, Point_2,None
    The c parameter is if we want to depict the intersection.
    """
    if isinstance(a,Line_2): #If it is Line
        if isinstance(b,Line_2):
            if a.direction().direction() != None and b.direction().direction() != None:
                if ((a.direction().direction() == b.direction().direction() or a.direction().direction() == -b.direction().direction()) and a.c()==b.c()): # If it is the same line(not with == because will fail in direction)
                    a.visual(c)#return a line
                    return a
                p = (a.a()*b.b()) - (a.b()*b.a())
                if p != 0:
                    return Point_2((-a.c()*b.b()+a.b()*b.c())/p,(-(a.a()*b.c())+a.c()*b.a())/p,visible=c)
            else:
                if (a.direction().direction() == b.direction().direction() and a.c()==b.c()): # If it is the same line(not with == because will fail in direction)
                    a.visual(c)#return a line
                    return a
                p = (a.a()*b.b()) - (a.b()*b.a())
                if p != 0:
                    return Point_2((-a.c()*b.b()+a.b()*b.c())/p,(-(a.a()*b.c())+a.c()*b.a())/p,visible=c)                
            return None
        if isinstance(b,Ray_2) or isinstance(b,Segment_2): #if it is ray or segment
            lin = b.supporting_line()
            ret = intersection(a,lin,False)
            if ret == None:
                return ret
            if isinstance(ret,Point_2):# if the intersection with the line returns a point
                if isinstance(b,Ray_2):
                    seg = Segment_2(b.source(),ret,visible=False)   #create a segment with the source an the inter point
                    if seg.direction() == b.direction() : #check if segment and ray has same direction
                        ret.visual(c)
                        del seg
                        return ret
                    else:
                        del seg
                        return None
                if isinstance(b,Segment_2):
                    if b.has_on(ret):   #check if the point is inside segment
                        ret.visual()
                        return ret
                    else:
                        return None
            return b
        if isinstance(b,Triangle_2): #if it is triangle
            ret = []
            for i in xrange(3): #for every edge find interseciont point(s), line
                lin = b.edge(i).supporting_line()
                retu = intersection(a,lin,False)
                if retu != None:
                    ret.append(retu)
            if len(ret) >0:
                for i in ret:
                    i.visual()
                return ret
            else:
                return None
        if isinstance(b,Circle_2):
            """
            In the circle intersecion we have 3 possibilities
            No intersection, single point, two points.
            First we create the perpendicular line form center of circle
            to the line. We find the intersection of this lines 
            (they have a point intersection). We create the
            segment between center and intersection point(segment seq).
            If seq length is bigger than the radius then we have no intersection.
            If they are equal we have one point intersection, with this point is
            the inesection point we have found before.
            If it is smaller then we have 2 points intersection
            """
            lin = a.perpendicular(b.center(),visible=False)
            f = intersection(a,lin,False)
            if not isinstance(f,Point_2):
                exit(-34)
            seq = Segment_2(f,b.center(),visible=False)
            if seq.squared_length() == b.squared_radius():
                f.visual()
                del seq
                return f
            if seq.squared_length() < b.squared_radius():
                g = b.center()
                if a.is_vertical():
                    x = -a.c()/a.a()
                    y1,y2 = quadratic(1,(-2*g.y()),((g.y()**2)+((x-g.x())**2)),(-b.squared_radius()))
                    del seq
                    return [Point_2(x,y1),Point_2(x,y2)]
                if a.is_horizontal():
                    y = -a.b()/a.a()
                    x1,x2 = quadratic(1,(-2*g.x()),((g.x()**2)+((y-g.y())**2)),(-b.squared_radius()))
                    del seq
                    return [Point_2(x1,y),Point_2(x2,y)]
                aaa = (((a.b()**2)/a.a()**2)+1)
                bbb = ((2*a.b()/(a.a()**2))+(2*a.b()*g.x()/a.a()) -2)
                ccc = (((a.c()**2)+a.c())/(a.a()**2)) + (g.x()**2) + (2*a.c()*g.x()/a.a()) + (g.y()**2) - g.squared_radius()
                y1,y2 = quadratic(aaa,bbb,ccc)  #function to solve quadratic equatations
                del seq
                return [Point_2(a.x_at_y(y1),y1),Point_2(a.x_at_y(y2),y2)]
            del seq
            return None
    if isinstance(a,Segment_2):
        if isinstance(b,Segment_2):
            max1 = a.max()
            min1 = a.min()
            max2 = b.max()
            min2 = b.min()
            r = intersection(a.supporting_line(),b.supporting_line(),False)
            if r == None:
                return None
            if isinstance(r,Point_2):
                if r >= min1 and r>=min2 and r <=max1 and r<=max2:
                    r.visual(c)
                    return r
                else:
                    return None
            if  isinstance(r,Line_2):
                if min1 <= min2:
                    min = min2
                else:
                    min = min1
                if max1 <= max2:
                    max = max1
                else:
                    max = max2
                if min != max:
                    return Segment_2(min,max,visible=c)
                else:
                    return Point_2(min.x(),min.y(),visible=c)
        if isinstance(b,Ray_2):
            r = intersection(a.supporting_line(),b.supporting_line(),False)
            if r == None:
                return None
            if isinstance(r,Point_2):
                if r >= a.min() and r <= a.max() and b.has_on(r):
                    r.visual(c)
                    return r
                else:
                    return None
            if  isinstance(r,Line_2):
                s = b.point(300)
                if b.source() > a.min() and b.source() < a.max():
                    if s < a.min():
                        return Segment_2(b.source(),a.min(),visible=c)
                    else:
                        return Segment_2(b.source(),a.max(),visible=c)
                if b.source() > a.max():
                    if s > a.max():
                        return None
                    else:
                        return a
                if b.source() < a.min():
                    if s < a.min():
                        return None
                    else:
                        return a
                if b.source() == a.min():
                    if s<a.min():
                        return a.min()
                    else:
                        return a
                if b.source() == a.max():
                    if s>a.max():
                        return a.max()
                    else:
                        return a
        if isinstance(b,Line_2):
            return intersection(b,a,c)
        if isinstance(b,Triangle_2):
            ret = []
            for i in xrange(3):
                lin=b.edge(i)
                retu = intersection(lin,a,False)
                if retu != None:
                    retu.visual(c)
                    ret.append(retu)
            if len(ret) >0:
                return ret
            else:
                return None
        if isinstance(b,Circle_2):
            r = intersection(a.supporting_line(),b,c)
            if r == None:
                return None
            if isinstance(r,Point_2):
                if r >=a.min() and r <=a.max():
                    r.visual(c)
                    return r
            else:
                ret = []
                if r[0] >=a.min() and r[0] <=a.max():
                    r[0].visual(c)
                    ret.append(r)
                if r[1] >=a.min() and r[1] <=a.max():
                    r[0].visual(c)
                    ret.append(r)
                le = len(ret)
                if le == 0:
                    return None
                if le ==1:
                    return ret[0]
                else:
                    return ret                  
    if isinstance(a,Ray_2):
        ret = []
        s = a.point(300)
        seg = Segment_2(a.source(),s,visible=False)
        if isinstance(b,Triangle_2):
            for i in xrange(3):
                lin = b.edge(i)
                retu = intersection(lin,seg,False)
                if retu != None:
                    retu.visual(c)
                    ret.append(retu)
            if len(ret)>0:
                del seg
                return ret
            else:
                del seg
                return None
        if isinstance(b,Circle_2):
            return intersection(seg,b,c)
        return intersection(b,a,c)
    if isinstance(a,Circle_2):
        if isinstance(b,Circle_2):
            seq=Segment_2(a.center(),b.center(),visible=False)
            dis_square = a.squared_radius() + b.squared_radius()
            if a.center() == b.center() and a.squared_radius == b.squared_radius():
                del seq
                return a
            if seq.squared_length() > dis_square.squared_length():
                del seq
                return None
            if seq.squared_length() == dis_square.squared_length():
                l = intersection(a,seq.supporting_line(),False)
                l1 = intersection(b,seq.supporting_line(),False)
                del seq
                for t in l:
                    if t in l1:
                        t.visual(c)
                        return t
            else:
                ca = (a.squared_radius - b.squared_radius() + seq.squared_length())/(2*sqrt(seq.squared_length()))
                h = sqrt(a.squared_radius() - (ca**2))
                p2 = a.center() + ca*(b.center() - a.center())/sqrt(dis_square)
                c1 = Point_2(p2.x()+h*(b.center().y()-a.center().y()),p2.y()-h*(b.center().x()-a.center().x()))
                c2 = Point_2(p2.x()-h*(b.center().y()-a.center().y()),p2.y()+h*(b.center().x()-a.center().x()))
                del seq
                return c1,c2
        if isinstance(b,Triangle_2):
            ret = []
            for i in xrange(3):
                lin = b.edge(i)
                retu = intersection(lin,a)
                if retu != None:
                    retu.visual(c)
                    ret.append(retu)
                if len(ret)>0:
                    return ret
                else:
                    return None         
        return intersection(b,a,c)
    if isinstance(a,Triangle_2):
        if isinstance(b,Triangle_2):
            ret = []
            for i in xrange(3):
                for j in xrange(3):
                    lin = b.edge(i)
                    lin1 = a.edge(j)
                    retu = intersection(lin,lin1,c)
                    if retu != None:
                        ret.extend(retu)
            if len(ret)>0:
                return ret
            else:
                return None   
        return intersection(b,a,c)
                
                
def run(Vpoints):
      """
      Jarvis Convex Hull algorithm.
      points is a list of Point_2 points
      
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
      for t in xrange(len(hull)):
       if t != len(hull)-1:
        Segment_2(hull[t],hull[t+1])
       else:
        Segment_2(hull[-1],hull[0])
      return hull
      """
      print Vpoints
      p = Polygon_2(Vpoints)
      t= p.is_simple()
      print t 
      print "The polygon is",
      if not t:
          print "not",
      print "simple"
      
class Polygon_2(object):
    def __init__(self,points,segments=None,color=(1,1,1),visible=True):
        self._simple=self._convex=self._orientation =2
        self._points=[]
        self._segments=[]
        if segments !=None:
            self._points=points[:]
            self._segments=segments[:]
        else:
            if len(points)>1:
                for i in xrange(len(points)-1):
                    segment = Segment_2(points[i],points[i+1],color=color,visible=visible)
                    self._segments.append(segment)
                segment = Segment_2(points[-1],points[0],color=color,visible=visible)
                self._segments.append(segment)
                self._points=points[:]
            else:
                raise No_Constructor([self,points,segments])
    def create(self):
        for s in self._segments:
            del s
        self._segments=[]
        if len(self._points)>1:
                for i in xrange(len(self._points)-1):
                    segment = Segment_2(self._points[i],self._points[i+1])
                    self._segments.append(segment)
                segment = Segment_2(self._points[-1],self._points[0],visible=True)
                self._segments.append(segment)      
    def clear(self):
        for s in self._segments:
            del s
        self._segments=[]
        for t in self._points:
            del t
        self._points=[]
    def size(self):
        return len(self._points)
    def is_empty(self):
        return self.size() == 0
    def insert(self,i,p):
        if p is not list:
            self._points.insert(i,p)
        else:
            for x in p:
                self._points.insert(i,x)
                i+=1
        self.create()
    def push_back(self,p):
        self._points.insert(p)
        self.create()
    def erase(self,i,j=None):
        if j==None:
            del self._points[i]
        else:
            del self._points[i:j]
        self.create()
    def reverse_orientation(self):
        self._points.reverse()
        s = self._points.pop()
        self._points.insert(0,s)
    def vertex(self,i):# 1<i<self.size()
        return self._points[i-1]
    def edge(self,i):
        return self._segments[i-1]
    def __getitem__(self,i):
        return self.vertex(i)
    def is_simple(self):
        if self._simple != 2:
            return self._simple
        for i in xrange(len(self._segments)-1):
            for j in xrange(i+2,len(self._segments)):
                if i == 0 and j == len(self._segments)-1: #for not find intersection between the first and the last segment
                    continue
                p = intersection(self._segments[i],self._segments[j])
                if isinstance(p,Point_2):
#                    print self._segments[i],self._segments[j]
#                    if not (p == self._segments[i].source() and p == self._segments[j].target()) and not (p == self._segments[j].source() and p == self._segments[i].target()):
                        print i,j
                        print p
                        self._simple = 0
                        return self._simple
        self._simple = 1
        return self._simple
    def is_convex(self): #Find if the diagon is inside the polygon.(exercise 1 2008-09)
        if self._convex != 2:
            return self._convex
        conv = self._points[:]
        n = len(conv)
        i = conv.index(max(conv))
        if orien[orientation(conv[(i+n-1)%n],conv[i],conv[(i+1)%n])] == -1:
            conv.reverse()
        while len(conv) > 3:
           n = len(conv)
           for i in range(n):
               i1 = (i+1)%n
               i2 = (i+2)%n
               if not incone(i, i2, conv) and diagonalie(i, i2, conv):
                   self._convex = 0
                   return self._convex   
           self._convex = 1
           return self._convex    
    def orientation(self):
        if self._orientation != 2:
            return self._orientation
        if self.is_simple():
            if self.size() < 3:
                self._orientation =0
                return 0
            else:
                self._orientation = orientation(self._points[0],self._points[1],self._points[2])
                return self._orientation
    def area(self):
        n = len(self._points)
        sum =0
        for i in xrange(n+1):
            x=i%n
            y=(i+1)%n
            sum += (self._points[x].x()*self._points[y].y() - self._points[x].y()*self._points[y].x())
            total_area = sum/2
        if self.orientation == 1:
            return total_area
        else:
            return -total_area
    def is_counterclockwise_oriented(self):
        return self.orientation() == 1
    def is_clockwise_oriented(self):
        return self.orientation() == -1
    def is_collinear_oriented(self):
        return self.orientation() == 0
    def return_points(self):
        return self._points
    def __eq__(self,other):
        return is_permute(self._points,other.return_points())
    def __ne__(self,other):
        return not is_permute(self._points,other.return_points())
    def left_vertex(self):
        s = sorted(self._points)
        return s[-1]
    def right_vertex(self):
        s = sorted(self._points)
        return s[0]
    def top_vertex(self):
        s = sorted(self._points,key=operator.itemgetter(1))
        return s[-1]
    def bottom_vertex(self):
        s = sorted(self._points,key=operator.itemgetter(1))
        return s[0]
    def seg_color(self,x=0,y=0,z=0): #strange None output
        if(x==0 and y==0 and z==0):
            for i in xrange(len(self._segments)):
                print "Segment" ,self._segments[i], "color",self._segments[i].color()
            return
        if type(x).__name__=='tuple':
            for i in xrange(len(self._segments)):
                self._segments[i].color(x)
            return
        for i in xrange(len(self._segments)):
                self._segments[i].color(x,y,z)      
    def poi_color(self,x=0,y=0,z=0): #strange None output
        if(x==0 and y==0 and z==0):
            for i in xrange(len(self._points)):
                print "Vertex" ,self._points[i], "color",self._points[i].color()
            return
        if type(x).__name__=='tuple':
            for i in xrange(len(self._points)):
                self._points[i].color(x)
            return
        for i in xrange(len(self._points)):
                self._points[i].color(x,y,z)
    def bounded_side(self,other):
        if not (isinstance(other,Point_2)) and not self.is_simple():
            print "Precondition failed.Either not point given or not simple polygon"
            return -2
        int = []
        line = False
        ray = Ray(other,Line(0,1,-other.x(),visible=False),visible=False)
        for seg in self._segments:
            if seg.has_on(other):
                return 0
            inter = intersection(seg,ray)
            if isinstance(inter,Point_2) and not line:
                    int.push_back(inter)
            elif (isinstance(inter,Point_2) and line):
                int.pop()
                line = not line
                continue
            elif (isinstance(inter,Segment_2) and not line):
                line = not line
                continue
            else :
                continue
        if (len(int)%2) ==0:
            return -1
        else:
            return 1
    def oriented_side(self,other):
        if not (isinstance(other,Point_2)) and not self.is_simple():
            print "Precondition failed.Either not point given or not simple polygon"
            return -2
        where = self.bounded_side(other)
        if where == 0:
            return 0
        elif where == -1:
            if self.orientation == 1:
                return -1
            else:
                return 1
        else:
            if self.orientation == 1:
                return 1
            else:
                return  -1
    def has_on_positive_side(self,other):
        return self.oriented_side(other) == 1
    def has_on_negative_side(self,other):
        return self.oriented_side(other) == -1
    def has_on_boundary(self,other):
        return self.bounded_side(other) == 0
    def has_on_bounded_side(self,other):
        return self.bounded_side(other) == 1
    def has_on_unbounded_side(self,other):
        return self.bounded_side(other) == -1       
    
            

#prepareScene()
#getcontext().prec = 21
#controls
#prepareControls()
#/controls

#m,s = getPolygon()
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
#   print "NiCe"
#a = Point_2()
#time.sleep(2)

#a.set_x(3)
"""
problem on floating point arithmetics

a=Point_2('-6.12163446856','5.85814348872',color=(0,0,1))
b=Point_2('4.09376340605','5.68062339084',color=(0,1,0))
c=Point_2('5.74140812056','-5.45238405818',color=(1,0,0))
d=Point_2('-1.73636404529','-2.02879406816',color=(1,1,0))

time.sleep(5)
m = [a,b,c,d]
print m
p=Polygon_2(m)
print p.is_simple()
print p.is_convex()


"""
"""
d = Point_2('2.3245235','6.4685768')
c = Point_2('-3.257347','4.236526')
f = Point_2('0.1542667','6.6375367')
g = Point_2('1.386425376','2.97843')

s1 = Segment_2(c,d)
s2 = Segment_2(f,g)
i1 = intersection(s1,s2)
if i1 != None:
    i1.color(color.yellow)
    print i1

a = Point_2(0,1)
b = Point_2(-3,3)
c = Point_2(3,4)
d = Point_2(2,6)
e = Point_2()
f = Point_2(0,2)
h = Point_2(1,1)
f.color(0,255,0)
e.color(0,0,255)
g = Point_2(0,4)
s1 = Ray_2(h,a)
s2 = Segment_2(c,e)
#s1.color(0,255,0)
#s2.color(255,0,0)
#t1 = Triangle_2(a,d,e)
i1 = intersection(s1,s2)
if i1 != None:
    i1.color(color.yellow)
    print i1
"""
"""
a.color()
t = Triangle_2(a,b,c,color=color.red)
t.poi_color()
t.poi_color(color.green)
t.poi_color()

v2=Vector_2(a,b)
print v2
print v2.squared_length()

d = Point_2(1,4)
e = Point_2(2,5,color=(1,0,0))
f = Point_2(0,0,color=(0.4,1,0.7))
g = Point_2(3,-2)
h=g
print "a < b == %s" %str(a < b)
print "a<=b == %s" %str(a<=b)
print "b<c == %s" %str(b<c)

#############Triangle_2#####################
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

s1 = Segment_2(b,c)
s2 = Segment_2(a,d)
s3 = Segment_2(a,b)
s4 = Segment_2(c,a)
print orientation(c,a,e)


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


#################Line_2##################

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

#sleep(5)
l3 = Line_2(s1,color=(0,1,1))

#sleep(5)
l4 = Line_2(d,v2,color=(1,0,0))

#sleep(5)
l5 = Line_2(b,v1,color=(1,0,1))

#sleep(5)
l6 = Line_2(c,d2,color=(1,1,0))

#sleep(5)
l7 = Line_2(a,d4,color=(0.5,0.5,0.5))

#sleep(5)
l8 = Line_2(a,c,color=(0,0.5,0.5))

#sleep(5)
l9 = Line_2(b,d)

a.color(color.red)
b.color(color.red)
c.color(color.red)
d.color(color.red)

##################Ray_2#############################
r1 = Ray_2(b,e,color=color.green)
#sleep(5)
ss = Segment_2(b,e)
#sleep(5)
ll = ss.supporting_line()
ll.visual()
print ll.direction()
#sleep(5)
lr1 = r1.supporting_line()
print lr1.direction()
lr1.visual()
print lr1.direction()
#sleep(5)
r2 = Ray_2(b,v5,color=(0,0,1))
#sleep(5)
l = Line_2(b,v5,color = (1,0,0))
#sleep(5)
r3 = Ray_2(b,d1,color=(1,0,1))
#sleep(5)
re = Line_2(b,d1,color = (0,1,0))



#l = Line_2(3,3,4,color = (1,0,0))
#re = Line_2(3,3,9,color = (0,1,0))

#s1 = Segment_2(e,b)
#s2 = Segment_2(e,f)
#r = intersection(s1,s2)
#if r :
#   r.color(1,0,1)

#c = Circle_2(f,2)
###################various Point_2 staff######################

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

 rod.max()
f=rod.middle()
print rod.has_on(f)
print rod.has_on(dd)
print rod.has_on(c)
print f
rod.color()
print rod.squared_length()
"""
#intersection
"""
l = Line_2(3,4,6)
l1 = Line_2(3,4,6)
l2 = l.perpendicular(Point_2())
l2.visual()
l3 = Line_2(6,8,4)
#print intersection(l,l1)

s = intersection(l,l2)
s.color(1,1,0)
#print intersection(l,l3)
d = Point_2(0,-3)
d1=Point_2(3,0)
seg = Segment_2(Point_2(-1,0),d1)
#e = -seg.direction()
#print seg.direction()
#we = Ray_2(Point_2(),-seg.direction())
seg1 = Segment_2(Point_2(0,1),d,visible=False)
ss= seg1.supporting_line()
r = intersection(seg,ss)
print r
if isinstance(r,Point_2):
    r.color(1,0,1)
"""
if __name__ == "__main__":
    main()

