$(document).ready(function(){       
   var scroll_start = 0;
   var actual = $('body');
   var offset = actual.offset();   

   //For navbar change-color
  if (actual.length){
   $(document).scroll(function() { 
      scroll_start = $(this).scrollTop();
	  if(scroll_start > (offset.top)) {
          $(".navbar-default").css('background-color', '#000');
	  }
	   else {
          $('.navbar-default').css('background-color', 'transparent');
       }
      });
    }//Navbbar change-color
});