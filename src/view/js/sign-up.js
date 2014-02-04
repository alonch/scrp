$(document).ready(function(){
    $('#registration').validate({
      rules: {
         first_name: {
          	required: true
        },
      
     	last_name: {
          	required: true
        },
        email: {
          	required: true,
          	email: true
        },
        phone:{
        	required: true
        },
        reference_name1:{
        	required: true
        },
        reference_phone1:{
        	required: true
        },
        reference_email1:{
        	required: true,
        	email: true
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
		$('#registration').valid()
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

document.select = function select(e){
	//clear tabs pane
	$(".tab-pane").each(function(){$(this).removeClass("active")})
	//selecting pane
	id = $(e).text().toLowerCase();
	id = "#{0}".format(id); 
	$(id).each(function(){
		$('input[name=personType]').val($(e).text());
		$(this).addClass("active")
	})

	//clear other button's selecction
	$(".btn-group button").each(function(){$(this).removeClass("active")})
}
