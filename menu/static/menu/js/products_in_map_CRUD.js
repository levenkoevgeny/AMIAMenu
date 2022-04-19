$('#id_product_in_map_add').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'map': $(`#id_map`).val(),
        'product': $(`#id_product`).val(),
        'product_count_gross': $(`#id_product_count_gross`).val(),
        'dish_category': $(`#id_dish_category`).val(),
        'treatments': $(`#id_treatments`).val(),
        'group': $(`#id_group`).val(),
    }

    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    show_spinner();

    fetch('/api/products-in-map/', {
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


function delete_product_in_map(id) {
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/products-in-map/${id}/`, {
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


$('.product_in_map_update_class').submit(function (e) {
    e.preventDefault();
    let form_id = e.target.id;
    let obj = {
        'map': $(`#id_map`).val(),
        'product': $(`#id_product_${form_id}`).val(),
        'product_count_gross': $(`#id_product_count_gross_${form_id}`).val(),
        'dish_category': $(`#id_dish_category_${form_id}`).val(),
        'treatments': $(`#id_treatments_${form_id}`).val() == "" ? [] : $(`#id_treatments_${form_id}`).val(),
        'group': $(`#id_group_${form_id}`).val() == "" ? null : $(`#id_group_${form_id}`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    show_spinner();
    fetch(`/api/products-in-map/${form_id}/`, {
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


$('#id_menu_date').change(function () {
    let new_date = $(`#id_menu_date`).val();
    let new_url = window.location.pathname + `?menu_date=${new_date}`;
    window.location.href = new_url;
});

$('#description_update_form').submit(function (e) {
    e.preventDefault();
    let map_id = $(`#id_map`).val();
    let obj = {
        'description': $(`#id_description`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    show_spinner();
    fetch(`/api/maps/${map_id}/`, {
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

$('#map_data_update_form').submit(function (e) {
    e.preventDefault();
    let map_id = $(`#id_map`).val();
    let obj = {
        'map_number': $(`#id_map_number`).val(),
        'map_name': $(`#id_map_name`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    show_spinner();
    fetch(`/api/maps/${map_id}/`, {
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

