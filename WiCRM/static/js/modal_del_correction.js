$('#delete').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget)
          var correction_id = button.data('id')
          var modal = $(this)
          modal.find('.modal-footer input.form-control').val(correction_id)
        })