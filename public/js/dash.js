count = 1;

function startClick(){

	var div = $('div#flow1');
	div.fadeIn();
		$('html,body').animate({scrollTop:$('div#flow1').offset().top},'slow');

}
