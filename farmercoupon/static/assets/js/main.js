// $( "#adduser" ).click(function() {
//     url_endpoint = '/manageusers/add'
//     button_id = $( "#adduser" ).attr( "name")
//     alert(button_id)
//     $.ajax({
//         method:"POST",
//         url:url_endpoint,
//         data:{
//             'add_id':button_id,
//             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//         },
//         success: function(data){
//         }
//     })
//   });