$(document).ready(function(){
  document.select = function select(e){
    //clear tabs pane
    $(".tab-pane").each(function(){$(this).removeClass("active")})
    //selecting pane
    $(e).addClass("active");
    id = $(e).text().toLowerCase();
    id = "#{0}".format(id); 
    $(id).each(function(){
      $('input[name=personType]').val($(e).text());
      $(this).addClass("active")
    })

    //clear other button's selecction
    $(".btn-group button").each(function(){$(this).removeClass("active")})
  }

  $('#mentor-registration').validate({
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
        	required: true,
          phone: true
        },
        reference_name1:{
        	required: true
        },
        reference_phone1:{
        	required: true,
          phone: true
        },
        reference_email1:{
        	required: true,
        	email: true
        },
        reference_name2:{
          required: true
        },
        reference_phone2:{
          required: true,
          phone: true
        },
        reference_email2:{
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
  $('#mentee-registration').validate({
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
          required: true,
          phone: true
        },
        reference_name1:{
          required: true
        },
        reference_phone1:{
          required: true,
          phone: true
        },
        reference_email1:{
          required: true,
          email: true
        },
        reference_name2:{
          required: true
        },
        reference_phone2:{
          required: true,
          phone: true
        },
        reference_email2:{
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
      document.select($('#{0}'.format(reload['personType'])).first())
      form_id = '{0}-registration'.format(reload['personType'].toLowerCase())
      for (var key in reload){
        // form[id=mentee-registration]
        $("form[id={0}] #{1}".format(form_id,key)).val(reload[key])
      }
      $("#{0}".format(form_id)).valid()
      for (var key in errors){
        $('label[for={0}][generated=true'.format(key))
          .text(errors[key])
          .removeClass('valid')
          .addClass('error')
          .focus()
        $('input[name={0}]'.format(key)).select()
      }
    }else{
      person = $('input[name=personType]').first().val();
      document.select($('#{0}'.format(person)).first())
    }
    

    
	
  }); // end document.ready


