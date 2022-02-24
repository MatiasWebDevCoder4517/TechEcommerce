$(document).ready(function () {
  //like ajax call
  $(".like-form").submit(function (e) {
    e.preventDefault();
    const product_id = $(".like-btn").val();
    const token = $("input[name=csrfmiddlewaretoken]").val();
    const url = $(this).attr("action");
    $.ajax({
      method: "POST",
      url: url,
      headers: { "X-CSRFToken": token },
      data: {
        product_id: product_id,
      },
      success: function (response) {
        if (response.liked === true) {
          $(".like-icon").addClass("text-blue-700");
        } else {
          $(".like-icon").removeClass("text-blue-700");
        }

        like = $("#like-count").text(response.likes_count);
        parseInt(like);
      },
      error: function (response) {
        console.log("Failed ", response);
      },
    });
  });

  //dislike ajax call
  $(".dislike-form").submit(function (e) {
    e.preventDefault();
    const product_id = $(".dislike-btn").val();
    const token = $("input[name=csrfmiddlewaretoken]").val();
    const url = $(this).attr("action");
    $.ajax({
      method: "POST",
      url: url,
      headers: { "X-CSRFToken": token },
      data: {
        product_id: product_id,
      },
      success: function (response) {
        console.log(response);
        if (response.disliked === true) {
          $(".dislike-icon").addClass("text-blue-700");
        } else {
          $(".dislike-icon").removeClass("text-blue-700");
        }

        dislikes = $("#dislike-count").text(response.dislike_count);
        parseInt(dislikes);
      },
      error: function (response) {
        console.log("failed", response);
      },
    });
  });
});
