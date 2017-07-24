/* PRELOADER STARTS
	========================================================================= */
function handlePreloader() {
	"use strict";
	if($('.preloader').length){
		$('.preloader').delay(500).fadeOut(500);
	}
}
handlePreloader();
/* PRELOADER ENDS
	========================================================================= */
/* ICONS STARTS
	========================================================================= */
$(".triggerone").on("click",function(){
	"use strict";
	$(".one").slideToggle(750);
	$(".two").slideUp();
	$(".three").slideUp();
	$(".four").slideUp();
	$(".five").slideUp();
	$(".six").slideUp();
});
$(".triggertwo").on("click",function(){
	"use strict";
	$(".two").slideToggle(750);
	$(".one").slideUp();
	$(".three").slideUp();
	$(".four").slideUp();
	$(".five").slideUp();
	$(".six").slideUp();
});
$(".triggerthree").on("click",function(){
	"use strict";
	$(".three").slideToggle(750);
	$(".two").slideUp();
	$(".one").slideUp();
	$(".four").slideUp();
	$(".five").slideUp();
	$(".six").slideUp();

});
$(".triggerfour").on("click",function(){
	"use strict";
	$(".four").slideToggle(750);
	$(".two").slideUp();
	$(".three").slideUp();
	$(".one").slideUp();
	$(".five").slideUp();
	$(".six").slideUp();
});
$(".triggerfive").on("click",function(){
	"use strict";
	$(".five").slideToggle(750);
	$(".two").slideUp();
	$(".three").slideUp();
	$(".four").slideUp();
	$(".one").slideUp();
	$(".six").slideUp();
});
$(".triggersix").on("click",function(){
	"use strict";
	$(".six").slideToggle(750);
	$(".two").slideUp();
	$(".three").slideUp();
	$(".four").slideUp();
	$(".five").slideUp();
	$(".one").slideUp();
});
/* ICONS ENDS
	========================================================================= */
/* SMOOTH SCROLL STARTS
	========================================================================= */
$('.main-navigation a').on('click', function() {
	"use strict";
	if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
		var target = $(this.hash);
		target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
		if (target.length) {
			$('html, body').animate({
				scrollTop: (target.offset().top - 80)
			}, 1000);
			return false;
		}
	}
});
/* SMOOTH SCROLL ENDS
	========================================================================= */
/* TESTIMONIALS STARTS
	========================================================================= */
$('.testimonials-slider').owlCarousel({
	navigation: false,
	slideSpeed: 300,
	paginationSpeed: 400,
	singleItem: true,
	transitionStyle: "fade",
	autoPlay: 7000
});
/* TESTIMONIALS ENDS
	========================================================================= */
$(window).scroll(function() {
	"use strict";
	if ($(this).scrollTop() >= 100) {
		$('#menu').addClass('stickytop');
		$('#button-search').hide();
		$('#logo img').css("position", "relative");
		$('#logo img').css("left", "15px");
	}
	else {
		$('#menu').removeClass('stickytop');
		$('#button-search').show();
		$('#logo img').css("position", "relative");
		$('#logo img').css("left", "0px");
	}
	if ($(this).scrollTop() > 100) {
		$('.scroll-to').fadeIn();
	} else {
		$('.scroll-to').fadeOut();
	}
	$('.scroll-to').on('click', function(){
	"use strict";
	$('html, body').animate({scrollTop : 0},800);
	return false;
});
});
/* SEARCH STARTS
	========================================================================= */
$(".search").on('click', function() {
	"use strict";
	$("#site-search").slideToggle(250);
});
/* SEARCH ENDS
	========================================================================= */
/* MOBILE MENU STARTS
	========================================================================= */
$('nav#mobile-navigation').mmenu({
	offCanvas: {
	position: 'right'
},
	header	: {
		add		: true,
		update	: true,
		title	: 'Menu'
	}
});
var $mobile_menu = $('nav#mobile-navigation'),
$html = $('html, body');
$mobile_menu.mmenu({classes:'mm-slide'});
$mobile_menu.find('li > a').on('click', function() {
	"use strict";
	var e = $(this).attr('href');if(e.slice(0,1) === "#") {
		$mobile_menu.one('closed.mm',function() {
			"use strict";
			setTimeout(function() {
				"use strict";
				$html.animate({scrollTop:$(e).offset().top});}, 10);
			}
		)
	}
});
/* MOBILE MENU ENDS
	========================================================================= */