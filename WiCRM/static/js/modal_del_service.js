$('#delete').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget)
          var service_id = button.data('id')
          var service = button.data('service')
          var modal = $(this)
          modal.find('.modal-title').text('Are you sure you want to delete ' + service + '?')
          modal.find('.modal-footer input.form-control').val(service_id)
        })