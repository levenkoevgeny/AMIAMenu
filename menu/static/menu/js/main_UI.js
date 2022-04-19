function show_spinner() {
    $('#id_main_div').css('height', '100vh')
        .addClass('d-flex justify-content-center align-items-center')
        .html('<div class="d-flex justify-content-center">\n' +
            '  <div class="spinner-border text-secondary" style="width: 3rem; height: 3rem;" role="status">\n' +
            '    <span class="visually-hidden">Loading...</span>\n' +
            '  </div>\n' +
            '</div>');
}