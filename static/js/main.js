/* jslint browser: true */
/* global $, jQuery, alert */

$(".cta-btn--email").on("click", function(){

  $("body").removeClass("overlay-success--visible")

  var DEST_EMAIL = $(this).data("emails"),
      DEST_NAME = $(this).data("nom");

  $(".placeholder-name").text(DEST_NAME);
  $("body").addClass("overlay-sign--visible");

  var form = $('#main_subscribe');

  $(form).submit(function(event) {
    event.preventDefault();

    var EMAIL = this.EMAIL.value,
        NAME = this.NAME.value;

    if ($(form).find('.optin').is(':checked')) {
      var OPTIN = 'true';
    } else {
      var OPTIN = 'false';
    }

    $(form)
      .find('input, .submit')
      .prop('disabled', true);
    $(form)
      .find('.submit')
      .button('loading');

    $.ajax({
      type: 'POST',
      url: $(form).attr('action'),
      data: `EMAIL=${  EMAIL  }&NAME=${  NAME  }&DEST_EMAIL=${  DEST_EMAIL  }&DEST_NAME=${  DEST_NAME  }&OPTIN=${  OPTIN  }`
    })

    .done(data => {
      ga('send', 'event', 'Action', 'Interpellation', 'Email', DEST_NAME);
      $("body").removeClass("overlay-sign--visible").addClass("overlay-success--visible");
      $(form).find('input, .submit').prop('disabled', false);
      $(form).find('.submit').button('reset');
    })
  });
});

$(".close-sign--btn").on("click", function(){
  $("body").removeClass("overlay-sign--visible")
});

$(".close-success--btn").on("click", function(){
  $("body").removeClass("overlay-success--visible")
});

$(".cta-btn--twitter").on("click", function(){
  $("body").addClass("overlay-success--visible");
  ga('send', 'event', 'Action', 'Interpellation', 'Twitter', $(this).data("nom"));
});

$('.social .button').on('click', function() {
  ga(
    'send',
    'event',
    'Action',
    'Share',
    $(this)
      .parent()
      .attr('class')
  );
});

function initstep(container) {
  $(container).height($(`${container} .active`).height());
}

initstep('.steps');

function step(container, step) {
  $(container)
    .find('.step.active')
    .removeClass('active');
  $(container)
    .find('.step.step--'+step)
    .addClass('active');
  $(container).height($(container + '.step.active').height());
}

$('#cp').on( "keyup", function(){
  var queryDpt = $(this).val();
  if(
  (queryDpt == "2A") ||
  (queryDpt == "2B") ||
  (queryDpt > 95 && queryDpt.length === 3) ||
  (queryDpt <= 95 && queryDpt.length === 2)
  ){
    $(".dep-" + queryDpt).addClass("active");

    if ( $('.list-deputes__already').children(".active").length == 0 ) {
      $('.list-deputes__already').hide();
    }
    if ( $('.list-deputes__primary').children(".active").length == 0 ) {
      $('.list-deputes__primary').hide();
      $('.list-deputes__secondary h2').text("Les député·es de votre département à interpeller en priorité");
    }

    step('.steps', 2);

    $(".depute.active .card-parlement__image").Lazy();
  }
});
