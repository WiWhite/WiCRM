$('#update').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var customer = button.data('customer')
          var customer_id = button.data('id')
          var customer_firstname = button.data('firstname')
          var customer_lastname = button.data('lastname')
          var customer_company = button.data('company')
          var customer_phonenumber = button.data('phonenumber')
          var customer_email = button.data('email')
          var customer_instagram = button.data('instagram')
          var customer_curator = button.data('curator')// Extract info from data-* attributes
          // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
          // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
          var modal = $(this)
          modal.find('.modal-header').text('Update ' + customer + ':')
          modal.find('.modal-body input[name="first_name"]').val(customer_firstname)
          modal.find('.modal-body input[name="last_name"]').val(customer_lastname)
          modal.find('.modal-body input[name="company"]').val(customer_company)
          modal.find('.modal-body input[name="phone_number"]').val(customer_phonenumber)
          modal.find('.modal-body input[name="email"]').val(customer_email)
          modal.find('.modal-body input[name="instagram"]').val(customer_instagram)
          modal.find('.modal-body select[name="curator"]').val(customer_curator)
        })