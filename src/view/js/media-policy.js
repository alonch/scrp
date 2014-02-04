$(document).ready(function(){
    $('#acceptance').validate({
      rules: {
         today: {
          	required: true
        },
     	initials: {
          	required: true

        },
        email: {
          	required: true,
          	email: true
        },
        agree: {
            required: true
        }
      },
      highlight: function(element) {
        $(element).closest('.control-group').removeClass('success').addClass('error');
      },
      success: function(element) {
        element
        .text('OK!').addClass('valid')
        .closest('.control-group').removeClass('error').addClass('success');
      }
    });

    if (typeof reload != 'undefined'){
  		for (var key in reload){
  	  		$("#{0}".format(key)).val(reload[key])
  		}
  		$('#acceptance').valid()
  		for (var key in errors){
  			$('label[for={0}][generated=true'.format(key))
  				.text(errors[key])
  				.removeClass('valid')
  				.addClass('error')
  				.focus()
  			$('input[name={0}]'.format(key)).select()
  		}
	  }
}); // end document.ready

