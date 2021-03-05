$('#update').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var person = button.data('person')
          var person_id = button.data('id')
          var person_firstname = button.data('firstname')
          var person_lastname = button.data('lastname')
          var person_phonenumber = button.data('phonenumber')
          var person_birthdate = button.data('birthdate')
          var person_position = button.data('position')
          var person_sex = button.data('sex')
          var person_dismissal = button.data('dismissal')
          var modal = $(this)
          modal.find('.modal-header').text('Update ' + person + ':')
          modal.find('.modal-body input[name="first_name"]').val(person_firstname)
          modal.find('.modal-body input[name="last_name"]').val(person_lastname)
          modal.find('.modal-body select[name="phone_number_0"]').val(person_phonenumber.slice(0, 4))
          modal.find('.modal-body input[name="phone_number_1"]').val(person_phonenumber.slice(4))
          modal.find('.modal-body input[name="birthdate"]').val(person_birthdate)
          modal.find('.modal-body select[name="position"]').val(person_position)
          modal.find('.modal-body select[name="sex"]').val(person_sex)
          modal.find('.modal-body select[name="dismissal"]').val(person_dismissal)
          modal.find('.modal-footer input.form-control').val(person_id)
        })