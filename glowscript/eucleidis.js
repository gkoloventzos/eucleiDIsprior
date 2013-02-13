GlowScript 1.0

scene.width = scene.height = 500
scene.range = 2.2

scene.caption.text("From VPython to Glowscript")


sphere( {pos:vec(0,0,0), size:1*vec(1,1,1),visible:false}) // display a box for context
var points =0;
var allpoints = [];

function Point_2(locate){
    this.location=locate;
    this.point = sphere ({pos:locate, size:0.1*vec(1,1,1)} );
    this.x =function (){return this.locate.pos.x;};
    this.y =function (){return this.locate.pos.y;};
    this.z =function (){return this.locate.pos.z;};
    this.ll = function(){return this.location};
    }
Point_2.prototype.add = function(p2){
    //var xa = this.x+p2.x;
//    var ya = this.y+p2.y;
  //  var za = this.z+p2.z;
    return Point_2({pos:(this.ll+p2.ll)});
}

Point_2.prototype.equal = function(p2){
    return this.x == p2.x && this.y == p2.y && this.z == p2.z;
}


function Segment_2(start,end){
    this.s = start;
    this.e = end;
    this.segment= curve({radius:.005});
    this.segment.push(start.location);
    this.segment.push(end.location);
    this.source =function (){return this.s};
    this.target =function (){return this.e};
    this.opposite =function(){return Segment_2(this.e,this.s)};
    this.middle =function(){ 
        var xm = start.x+end.x;
        var ym = start.y+end.y;
        var zm = start.z+end.z;
        return Point_2({pos:vec(xm,ym,zm)});
    };
    
}
function Line_2(){
    
}

    scene.waitfor("click",wait)
    var loc = scene.mouse.pos  
    allpoints[0] = new Point_2(loc);
    scene.waitfor("click",wait)
    var loc1 = scene.mouse.pos
    allpoints[1] = new Point_2(loc1);
    var s = allpoints[0].add(allpoints[1])
    var seg = new Segment_2(allpoints[0],allpoints[1]);