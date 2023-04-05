$(document).ready(function() {

//  bulma navbar toast toggle
  $(".navbar-burger").click(function() {
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });

//  bulma close button
  $(".delete").click(function() {
    $(this).parent('div').remove();
  });

//  profile forms switch
  $(".data-form").change(function() {
    this.form.submit();
  });

});