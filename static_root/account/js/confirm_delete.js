// Confirm delete
$(document).ready(function () {
    $(".delete-button").on("click", function () {
        var url = $(this).data('delete-url');
        $("#confirm_delete").attr("href", url)
    });
});