$(function () {
    $(".img-w").each(function () {
      $(this).wrap("<div class='img-c'></div>");
      let imgSrc = $(this).find("img").attr("src");
      $(this).css("background-image", "url(" + imgSrc + ")");
    });

    $(".img-c").click(function () {
      let imgSrc = $(this).find("img").attr("src");
      let $overlay = $("<div class='overlay'><img src='" + imgSrc + "'></div>");
      $("body").append($overlay);

      $overlay.click(function () {
        $(this).fadeOut(function () {
          $(this).remove();
        });
      });
    });
  });
