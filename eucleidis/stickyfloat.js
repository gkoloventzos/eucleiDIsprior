/*
 * stickyfloat - jQuery plugin for verticaly floating anything in a constrained area
 * 
 * Example: jQuery('#menu').stickyfloat({duration: 400});
 * parameters:
 * 		duration 	(200)	 - the duration of the animation
 *		startOffset (number) - the amount of scroll offset after the animations kicks in
 *		offsetY		(number) - the offset from the top when the object is animated
 *		lockBottom	(true)	 - set to false if you don't want your floating box to stop at parent's bottom
 *		delay		(0)		 - delay in milliseconds  until the animnations starts
		easing		(linear) - easing function (jQuery has by default only 'swing' & 'linear')
 * $Version: 08.10.2011 r2
 * $Version: 05.16.2009 r1
 * Copyright (c) 2009 Yair Even-Or
 * vsync.design@gmail.com
 */
/*
* jQuery easing functions (for this demo)
*/
jQuery.extend( jQuery.easing,{
	def: 'easeOutQuad',
	swing: function (x, t, b, c, d) {
		//alert(jQuery.easing.default);
		return jQuery.easing[jQuery.easing.def](x, t, b, c, d);
	},
	easeInQuad: function (x, t, b, c, d) {
		return c*(t/=d)*t + b;
	},
	easeOutQuad: function (x, t, b, c, d) {
		return -c *(t/=d)*(t-2) + b;
	},
	easeInOutQuad: function (x, t, b, c, d) {
		if ((t/=d/2) < 1) return c/2*t*t + b;
		return -c/2 * ((--t)*(t-2) - 1) + b;
	},
	easeOutElastic: function (x, t, b, c, d) {
		var s=1.70158;var p=0;var a=c;
		if (t==0) return b;  if ((t/=d)==1) return b+c;  if (!p) p=d*.3;
		if (a < Math.abs(c)) { a=c; var s=p/4; }
		else var s = p/(2*Math.PI) * Math.asin (c/a);
		return a*Math.pow(2,-10*t) * Math.sin( (t*d-s)*(2*Math.PI)/p ) + c + b;
	},
	easeInOutElastic: function (x, t, b, c, d) {
		var s=1.70158;var p=0;var a=c;
		if (t==0) return b;  if ((t/=d/2)==2) return b+c;  if (!p) p=d*(.3*1.5);
		if (a < Math.abs(c)) { a=c; var s=p/4; }
		else var s = p/(2*Math.PI) * Math.asin (c/a);
		if (t < 1) return -.5*(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
		return a*Math.pow(2,-10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )*.5 + c + b;
	},
	easeInBack: function (x, t, b, c, d, s) {
		if (s == undefined) s = 1.70158;
		return c*(t/=d)*t*((s+1)*t - s) + b;
	},
	easeOutBack: function (x, t, b, c, d, s) {
		if (s == undefined) s = 1.70158;
		return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
	},
	easeInOutBack: function (x, t, b, c, d, s) {
		if (s == undefined) s = 1.70158; 
		if ((t/=d/2) < 1) return c/2*(t*t*(((s*=(1.525))+1)*t - s)) + b;
		return c/2*((t-=2)*t*(((s*=(1.525))+1)*t + s) + 2) + b;
	}
});

(function($){
	$.fn.stickyfloat = function(options, lockBottom){
		var $obj 				= this,
			doc					= $(document),
			opts, bottomPos, pastStartOffset, objFartherThanTopPos, objBiggerThanWindow, newpos, checkTimer, lastDocPos = doc.scrollTop(),
			parentPaddingTop 	= parseInt($obj.parent().css('padding-top')),
			startOffset 		= $obj.parent().offset().top;
		
		$.extend( $.fn.stickyfloat.opts, options, { startOffset:startOffset, offsetY:parentPaddingTop} );
		opts = $.fn.stickyfloat.opts;
		$obj.css({ position: 'absolute' });
		
		if(opts.lockBottom){
			bottomPos = $obj.parent().height() - $obj.outerHeight() + parentPaddingTop; //get the maximum scrollTop value
			if( bottomPos < 0 )
				bottomPos = 0;
		}
		
		function checkScroll(){
			if( opts.duration > 40 ){
				clearTimeout(checkTimer);
				checkTimer = setTimeout(function(){
					if( Math.abs(doc.scrollTop() - lastDocPos) > 0 ){
						lastDocPos = doc.scrollTop();
						initFloat();
					}
				},40);
			}
			else initFloat();
		}
		
		function initFloat(){
			$obj.stop(); // stop all calculations on scroll event
			
			pastStartOffset			= doc.scrollTop() > opts.startOffset;	// check if the window was scrolled down more than the start offset declared.
			objFartherThanTopPos	= $obj.offset().top > startOffset;	// check if the object is at it's top position (starting point)
			objBiggerThanWindow 	= $obj.outerHeight() < $(window).height();	// if the window size is smaller than the Obj size, then do not animate.
			
			// if window scrolled down more than startOffset OR obj position is greater than
			// the top position possible (+ offsetY) AND window size must be bigger than Obj size
			if( (pastStartOffset || objFartherThanTopPos) && objBiggerThanWindow ){ 
				newpos = (doc.scrollTop() -startOffset + opts.offsetY );

				if ( newpos > bottomPos )
					newpos = bottomPos;
				if ( doc.scrollTop() < opts.startOffset ) // if window scrolled < starting offset, then reset Obj position (opts.offsetY);
					newpos = parentPaddingTop;
				
				$obj.delay(opts.delay).animate({ top: newpos }, opts.duration , opts.easing );
			}
		}
		
		$(window).scroll(checkScroll);
	};
	
	$.fn.stickyfloat.opts = { duration:700, lockBottom:true , delay:0, easing:'easeInOutElastic' };
})(jQuery);

			
// init the pluging and bind it to the #menu element
$('#sidebar').stickyfloat();

// binds for this demo
$('#sidebar').delegate('button', 'click', function(){
	$.extend( $.fn.stickyfloat.opts, { easing:this.innerHTML });
});

$('#duration').change(function(){
	var val = this.value|0 || 0;
	$.extend( $.fn.stickyfloat.opts, { duration:val });
});

$('#delay').change(function(){
	var val = this.value|0 || 0;
	$.extend( $.fn.stickyfloat.opts, { delay:val });
});

$('#lock').change(function(){
	var val = this.checked ? true : false; 
	$('#sidebar').stickyfloat({ lockBottom:val });
});
