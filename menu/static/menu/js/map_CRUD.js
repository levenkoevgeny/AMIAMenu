$('#map_add_form').submit(function (e) {
    e.preventDefault();

    let new_obj = {}
    let rest_url = ''

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    if ($('#id_has_parents').is(':checked')) {
        new_obj = {
            'map_number': $(`#id_map_number_`).val(),
            'map_name': $(`#id_map_name_`).val(),
            'description': null,
            'map_parent': $(`#id_map_parent_select`).val(),
        }
        rest_url = '/menu/make_map_clone/'
    } else {
        new_obj = {
            'map_number': $(`#id_map_number_`).val(),
            'map_name': $(`#id_map_name_`).val(),
            'description': null,
        }
        rest_url = '/api/maps/'
    }

    console.log(new_obj);

    // show_spinner();

    fetch(rest_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(new_obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message)).finally(() => window.location.href=window.location.href);
});


$('#id_has_parents').click(function (e) {

    if ($(this).is(':checked')) {
        $('#id_map_parent_select').prop('disabled', false).prop('required', true);
    } else {
        $('#id_map_parent_select').prop('disabled', true).prop('required', false);
    }
});