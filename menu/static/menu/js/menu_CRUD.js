$('#menu_day_add_form').submit(function (e) {
    e.preventDefault();
    let new_obj = {
        'menu_day_date': $(`#id_menu_day_date`).val(),
    }
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    // show_spinner();

    fetch('/api/menu-days/', {
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

$('.menu_day_update_class').submit(function (e) {
    e.preventDefault();
    let menu_day_id = e.target.id;
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let meals = $(`#meals_select_hidden_${menu_day_id}`).val();
    let obj = {
        'menu_day_id': menu_day_id
    }

    meals.forEach(id => {
        obj[id] = $(`#meal_select_${menu_day_id}_${id}`).val();
    });

    fetch('/menu/menu-day-update-maps/', {
        method: 'POST',
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
    }).catch((e) => alert(e.message))
        .finally(() => window.location.href = window.location.href);
});

$('#id_menu_day_date_start, #id_menu_day_date_end').change(function () {
    let current_date = $(`#current_date`).val();
    $(`#id_menu_day_date_start`).val() == '' ? $(`#id_menu_day_date_start`).val(current_date) : $(`#id_menu_day_date_start`).val();
    $(`#id_menu_day_date_end`).val() == '' ? $(`#id_menu_day_date_end`).val(current_date) : $(`#id_menu_day_date_end`).val();

    $('#id_filter_form').submit();
    show_spinner();
});


