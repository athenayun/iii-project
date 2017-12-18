/*
    page loading javascript
    from http://miwa-komatsu.jp
*/



$(function() {
	
  var h = $(window).height();
//    $('html,body').css({overflow:'scroll',height : 'auto' /*,height:$(window).height()*/});
//    $('#container_sp').css({'cssText':'display: none !important;'});
    $('#loader-bg ,#loader').height(h).css('display','block');
    //$("#movie_content_btn").click(function(){
		//move_toppage(800);
		//return false;

	//});
//	move_toppage = function(fadetime){
//		$('html,body').css({overflow:'auto',height:'auto'});
//		$('#container_sp').css({'cssText':''});
//		//$('#movie_content').fadeOut(fadetime);
//		Cookies.set('isPlayMovie', 'true');
//	}
});

/*
function set_movie_resize(){
	var tarvideo = $("#my-video");
	$("#movie_content").height($(window).height());
	var m_scale_fH = 1920 / 1080;
	var m_scale_fW = 1080 / 1920;
	// 最大の縦長倍率
	var max_m_scale_fH = 700 / 800;
	function m_resize_functions(){
		var wH = $(window).height();
		var wW = $(window).width();
		var mH = 0;
		var mW = 0;
		if(wH*m_scale_fH < wW){ // 横長時
			mW = wW;
			mH = wW * m_scale_fW;
		}else{// 縦長時
			mH = wH;
			mW = wH * m_scale_fH;
			//縦長すぎる時は横基準で
			if( wW / wH < max_m_scale_fH ){
				mW = wH*max_m_scale_fH;
				mH = (wH*max_m_scale_fH) * m_scale_fW;
			}
		}
		var m_mt = (wH-mH)/2;
		var m_ml = (wW-mW)/2;
		tarvideo.width(mW).height(mH).css({marginTop:m_mt,marginLeft:m_ml});
	}
	$(window).resize(function() {
		m_resize_functions();
	});
	m_resize_functions();
}
*/

$(window).load(function () { 
	stopload();
});
//$(function(){
//  setTimeout('stopload()',10000);
//});
 
// var isLoadEnded = false
function stopload(){
	if(!isLoadEnded){
        $('#first_content_wrapper').delay(900).fadeOut(800);
        $('#loader-bg').delay(900).fadeOut(800);
        $('#loader').delay(900).fadeOut(800);
//        if(Cookies.get('isPlayMovie') == "true"){
//            move_toppage(0);
//            //set_movie_resize();
//        }else{
//            $('html,body').css({overflow:'auto',height:'auto'});
//            //set_movie_resize();
//        }
//        isLoadEnded = true;
//    }
}
