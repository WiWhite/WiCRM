$('#update').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget)
          var correction = button.data('correction')
          var correction_desc = button.data('desc')
          var correction_status = button.data('status')
          var correction_id = button.data('id')
          var modal = $(this)
          modal.find('.modal-body input[name="correction"]').val(correction)
          modal.find('.modal-body textarea[name="description"]').val(correction_desc)
          modal.find('.modal-body select[name="status"]').val(correction_status)
          modal.find('.modal-footer input.form-control').val(correction_id)
        })