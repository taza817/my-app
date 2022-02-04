// active nav
$(function() {

  var pageURL = location.pathname,
  pageURLArr = pageURL.split('/'),      //ページのパスを分割して配列化
  pageURLArrCategory = pageURLArr[1];   //第1階層を取得

  $('.navbar-nav li a').each(function() {
    var selfhref = $(this).attr('href'),
    hrefArr = selfhref.split('/'),   //aタグのhref属性の値を分割して配列化
    hrefArrCategory = hrefArr[1];    //第1階層を取得

    //パスの第1階層とhrefの第1階層を比較して同じであればcurrentを付与する
    if (pageURLArrCategory == hrefArrCategory) {
      $(this).addClass('current');
    } else {
      $(this).removeClass('current');
    }
  });

});

$(function() {

  var pageURL = location.pathname,
  pageURLArr = pageURL.split('/'),      //ページのパスを分割して配列化
  pageURLArrCategory = pageURLArr[1];   //第1階層を取得

  $('.bottom-nav ul li a').each(function() {
    var selfhref = $(this).attr('href'),
    hrefArr = selfhref.split('/'),   //aタグのhref属性の値を分割して配列化
    hrefArrCategory = hrefArr[1];    //第1階層を取得

    //パスの第1階層とhrefの第1階層を比較して同じであればcurrentを付与する
    if (pageURLArrCategory == hrefArrCategory) {
      $(this).addClass('current');
    } else {
      $(this).removeClass('current');
    }
  });

});


// input length count
function ShowLength(str) {
  document.getElementById("inputlength").innerHTML = str.length;
}

// modal
$(function() {
  // follow-list
  $('.js-modal-open-follow').click(function() {
    $("html,body").css("overflow", "hidden");
    $(".js-modal-follow").show();
    return false;
  });
  $(".js-modal-close-follow").click(function() {
    $("html,body").removeAttr("style");
    $(".js-modal-follow").hide();
    return false;
  });
});

$(function() {
  // follower-list
  $('.js-modal-open-follower').click(function() {
    $("html,body").css("overflow", "hidden");
    $(".js-modal-follower").show();
    return false;
  });
  $(".js-modal-close-follower").click(function() {
    $("html,body").removeAttr("style");
    $(".js-modal-follower").hide();
    return false;
  });
});


// keep scroll posision
$(function() {
  $(".like-btn").click(function() {
    var scrollPosition = $(window).scrollTop();
    localStorage.setItem('key', scrollPosition);
  });
  $(document).ready(function() {
    var position = localStorage.getItem('key');
    // $(this).location.href(position)
    $(window).scrollTop(position);
    localStorage.clear();
  });
});


// good signal
$(".like-btn").submit(function(event) {
  event.preventDefault();
  var likebtn = $(this);
  $.ajax({
    url
  })
})
