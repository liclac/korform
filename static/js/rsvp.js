$(document).ready(function() {
  /*
   * Handle RSVP answer changes.
   */
  $('.rsvp-panel input[type=radio][name$=-answer]').change(function(e) {
    var panel = $(this).closest('.rsvp-panel');
    var comment = panel.find('div[id$=-comment]');
    var value = $(this).val();
    
    // Set the correct highlight class on the parent panel
    panel.removeClass('panel-default panel-success panel-danger panel-warning');
    if (value === '1') {
      panel.addClass('panel-success');
    } else if (value === '0') {
      panel.addClass('panel-danger');
    } else if (value === '2') {
      panel.addClass('panel-warning');
    } else {
      console.log("Unknown value", value);
    }
    
    // Focus the comment field if the answer is not Yes
    if (value != '1') {
      comment.show();
      comment.find('textarea').focus();
    } else {
      comment.hide();
    }
  });
})
