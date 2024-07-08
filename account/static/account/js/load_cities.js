// Load cities for each province
$(document).on("change", "#id_province", function () {
    const url = $('#address_form').data('url');
    $('#id_city').load(url + '?id_province=' + $(this).val());
});