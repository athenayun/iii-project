
$(function(){
    var h = $(window).height();
    $('#loader-bg ,#loader').height(h).css('display','block');
});

$(window).load(function () { 
	stopload();
});

function stopload(){
	
        $('#first_content_wrapper').delay(900).fadeOut(800);
        $('#loader-bg').delay(900).fadeOut(800);
        $('#loader').delay(1000).fadeOut(600);
        
    
}