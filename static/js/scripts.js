$("form[name=regForm]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find("#regError");
  var data = $form.serialize();


  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("d-none");
    }
  });

  e.preventDefault();
});

$("form[name=loginForm]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find("#loginError");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signin",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("d-none");
    }
  });

  e.preventDefault();
});