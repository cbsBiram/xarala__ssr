$(window).on('load', function () { // makes sure the whole site is loaded 
  $('#status').fadeOut(); // will first fade out the loading animation 
  $('#preloader').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website. 
  $('body').delay(350).css({
    'overflow': 'visible'
  });
})

$(document).ready(function () {
  "use strict";
  // home contact info
  $(".trggericon").on("click", function (e) {
    $(this).parent('.top-contact').addClass('togglecontact');
  });
  $(".top-contact .close").on("click", function (e) {
    $(this).parent('.top-contact').removeClass('togglecontact');
  });
});

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



setTimeout(function () {
  $('#message').fadeOut('slow');
}, 3000);


$(document).on('click', '.panel-heading span.clickable', function (e) {
  var $this = $(this);
  if (!$this.hasClass('panel-collapsed')) {
    $this.parents('.panel').find('.panel-body').slideUp();
    $this.addClass('panel-collapsed');
    $this.find('i').removeClass('fa-chevron-down').addClass('fa-chevron-up');

  } else {
    $this.parents('.panel').find('.panel-body').slideDown();
    $this.removeClass('panel-collapsed');
    $this.find('i').removeClass('fa-chevron-up').addClass('fa-chevron-down');

  }
})