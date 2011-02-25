p= None

class A(object):
    def p_get(self):
        return p
    def p_set(self, value):
        global p
        p= value
    p= property(p_get, p_set, doc="your property")
    def jump(self):
        print "yes sir", self.p

class B(A):
    def jump(self):
        print "prits", self.p

a= A(); b= B()
a.jump()
b.jump()
a.p= "my arse"
a.jump()
b.jump()
