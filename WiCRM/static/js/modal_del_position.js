$('#delete').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget)
          var position_id = button.data('id')
          var position = button.data('service')
          var modal = $(this)
          modal.find('.modal-title').text('Are you sure you want to delete ' + position + '?')
          modal.find('.modal-footer input.form-control').val(position_id)
        })