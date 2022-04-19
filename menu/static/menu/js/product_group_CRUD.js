$('#add_product_group_form').submit(function (e) {
    e.preventDefault();
    $('#add_product_group_form_button').prop('disabled', true);

    let new_obj = {}

    if ($('#is_main_checkbox').is(':checked')) {
        new_obj = {
            'group_name': $(`#id_group_name_add`).val(),
            'norm_per_day': $(`#id_norm_per_day`).val(),
            'replacement_for': null,
            'in_count': 100,
        }

    } else {
        new_obj = {
            'group_name': $(`#id_group_name_add`).val(),
            'norm_per_day': null,
            'replacement_for': $(`#id_replacement_for`).val(),
            'in_count': $(`#id_norm_for_replacement`).val(),
        }

    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    // show_spinner();

    fetch('/api/product-groups/', {
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


$('.product_update_group_form_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'group_name': $(`#id_group_name_${form_id}`).val(),
        'norm_per_day': $(`#id_norm_per_day_${form_id}`).val() == undefined ? null : $(`#id_norm_per_day_${form_id}`).val(),
        'replacement_for': $(`#id_replacement_for_${form_id}`).val() == undefined ? null : $(`#id_replacement_for_${form_id}`).val(),
        'in_count': $(`#id_norm_for_replacement_${form_id}`).val() == undefined ? 100 : $(`#id_norm_for_replacement_${form_id}`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    // show_spinner();
    fetch(`/api/product-groups/${form_id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(obj)
    }).then(response => {
        if (response.status >= 200 && response.status < 300) {
        } else {
            throw new Error("Ошибка записи!")
        }
    }).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href);

});


function delete_product_group(id) {
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    // show_spinner();
    fetch(`/api/product-groups/${id}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrftoken,
        },
    }).then(response => {
            if (response.status >= 200 && response.status < 300) {
            } else {
                throw new Error("Ошибка удаления!")
            }
        }
    ).catch((e) => alert(e.message)).finally(() => window.location.href = window.location.href)
}


$('#is_main_checkbox').click(function (e) {

    if ($(this).is(':checked')) {
        $('#id_replacement_for').prop('disabled', true).prop('required', false);
        $('#id_norm_for_replacement').prop('disabled', true).prop('required', false);
        $('#id_norm_per_day').prop('disabled', false).prop('required', true);
    } else {
        $('#id_replacement_for').prop('disabled', false).prop('required', true);
        $('#id_norm_for_replacement').prop('disabled', false).prop('required', true);
        $('#id_norm_per_day').prop('disabled', true).prop('required', false);

    }
});