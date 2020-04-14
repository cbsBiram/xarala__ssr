// Navbar Toggle
document.addEventListener('DOMContentLoaded', function () {

  // Get all "navbar-burger" elements
  var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach(function ($el) {
      $el.addEventListener('click', function () {

        // Get the "main-nav" element
        var $target = document.getElementById('main-nav');

        // Toggle the class on "main-nav"
        $target.classList.toggle('hidden');

      });
    });
  }

});

// course tabs
var myRadios = document.getElementsByName("tabs2");
var setCheck;

var x = 0;
for (x = 0; x < myRadios.length; x++) {
  myRadios[x].onclick = function () {
    if (setCheck != this) {
      setCheck = this;
    } else {
      this.checked = false;
      setCheck = null;
    }
  };
}

// less tabs
var myLessons = document.getElementsByName("tabs");
var setCheck;

var x = 0;
for (x = 0; x < myLessons.length; x++) {
  myRadios[x].onclick = function () {
    if (setCheck != this) {
      setCheck = this;
    } else {
      this.checked = false;
      setCheck = null;
    }
  };
}

// course lesson

document.getElementById('menuBtn').addEventListener('click', function () {
  document.getElementById('app').classList.add('opened');
});

document.getElementById('sideNavBg').addEventListener('click', function () {
  document.getElementById('app').classList.remove('opened');
});