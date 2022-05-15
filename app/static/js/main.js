$(document).ready(function () {
    $('#contact form').on('submit', function (e) {
        e.preventDefault();
        var $form = $(e.currentTarget),
            $email = $form.find('#contact-email'),
            $button = $form.find('button[type=submit]');
        // console.log($email.val())

        if ($email.val().indexOf('@') == -1) {
            console.log('tes')
            $email.closest('.form-control').addClass('is-invalid');
        } else {
            $form.find('.form-control').addClass('is-valid').
                removeClass('is-invalid');
            $button.attr('disabled', 'disabled');
            $button.after('<span>Message sent. We will contact you soon.</span > ');
        }
    });



    
    // rest of the JavaScript code
    $('#sign-btn').on('click', function(e) {
        $(e.currentTarget).closest('ul').hide();
        $('form#signin').fadeIn('fast');
        });
});


   