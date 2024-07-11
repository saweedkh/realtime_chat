document.addEventListener("DOMContentLoaded", function() {

    if (typeof django !== "undefined" && typeof django.jQuery !== "undefined") {
      var $ = django.jQuery;
  
      var userElement = $('#id_user');
      var groupElement = $('#id_group'); 
  
      userElement.change(function() {
        var newValue = $(this).val();
        console.log("New value: " + newValue);

        if (newValue)
  
            $.ajax({
            url: '/chat/api/user-groups/' + newValue + "/", 
            method: 'GET',

            success: function(response) {
                console.log("Success:", response);

                groupElement.empty();

                $.each(response, function(index, group) {
                    console.log(group.uuid)
                    groupElement.append('<option value="' + group.uuid + '">' + group.name + '</option>');
                });
            },
            error: function(xhr, status, error) {
                console.log("Error:", error);
            }
            });
      });
    } else {
      console.log("Django jQuery is not loaded.");
    }
  });
  