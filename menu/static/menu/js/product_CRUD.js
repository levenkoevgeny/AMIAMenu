$('#add_product_form').submit(function (e) {
    e.preventDefault();
    $('#add_product_form_button').prop('disabled', true);

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    let new_obj = {
        'product_name': $(`#id_product_name_`).val(),
        'energy_value': $(`#id_energy_value`).val(),
        'proteins': $(`#id_proteins`).val(),
        'fats': $(`#id_fats`).val(),
        'carbohydrates': $(`#id_carbohydrates`).val(),
    }

    // show_spinner();

    fetch('/api/products/', {
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


$('.product_modal_update_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'product_name': $(`#id_product_name_${form_id}`).val(),
        'energy_value': $(`#id_energy_value_${form_id}`).val(),
        'proteins': $(`#id_proteins_${form_id}`).val(),
        'fats': $(`#id_fats_${form_id}`).val(),
        'carbohydrates': $(`#id_carbohydrates_${form_id}`).val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    // show_spinner();
    fetch(`/api/products/${form_id}/`, {
        method: 'PATCH',
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


$('.wastage_modal_update_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'percent': $(`#id_percent_${form_id}`).val() == "" ? null : $(`#id_percent_${form_id}`).val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    // show_spinner();
    fetch(`/api/wastage-by-date-range/${form_id}/`, {
        method: 'PATCH',
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