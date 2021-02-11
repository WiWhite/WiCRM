$('#delete').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget)
          var order_id = button.data('id')
          var modal = $(this)
          modal.find('.modal-footer input.form-control').val(order_id)
        })