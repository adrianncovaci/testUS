$(function () {

    $(".js-create-book").click(function () {
      $.ajax({
        url: '/add',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-book").modal("show");
        },
        success: function (data) {
          $("#modal-book .modal-content").html(data.html_form);
        }
      });
    });

    $("#modal-book").on("submit", ".js-book-create-form", function () {
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
          url: form.attr("action"),
          data: formData,
          type: form.attr("method"),
          dataType: 'json',
          async: true,
            cache: false,
            contentType: false,
            enctype: form.attr("enctype"),
            processData: false,
          success: function (data) {
            if (data.form_is_valid) {
              alert("Submited!"); 
              $("#modal-book").modal("hide"); 
            }
            else {
              $("#modal-book .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      });
  
  });