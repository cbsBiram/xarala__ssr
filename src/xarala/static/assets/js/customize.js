$(document).ready(function () {


  // subscribe to mailchimp
  $('#subscribe').submit(function (e) {
    e.preventDefault();
    var email_id = $("#email_id").val();
    if (email_id) {
      var csrfmiddlewaretoken = csrftoken;
      var email_data = {
        "email_id": email_id,
        "csrfmiddlewaretoken": csrfmiddlewaretoken
      };
      $.ajax({
        type: 'POST',
        url: "/subscribe/",
        data: email_data,
        success: function (response) {
          $('#email_id').val('');
          if (response.status == "404") {
            alert("Cet email est déjà inscrit!");
          } else {
            alert("Merci de vous être abonné! S'il vous plaît vérifier votre e-mail pour la confirmation");
          }
        },
        error: function (response) {
          alert("Désolé, quelque chose s'est mal passé");
          $('#email_id').val('');
        }
      });
      return false;
    } else {
      alert("S'il vous plaît fournir un email correct!");
    }
  });

  // get token
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  })


});