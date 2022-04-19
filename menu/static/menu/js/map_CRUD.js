$('#map_add_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'map_number': $(`#id_map_number_`).val(),
        'map_name': $(`#id_map_name_`).val(),
        'description': null,
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    // show_spinner();

    fetch('/api/maps/', {
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
    }).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href);
});