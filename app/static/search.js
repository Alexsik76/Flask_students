$(document).ready(function () {
        // $('#searchModal').modal('show');
        $('#gr').on('input change', function () {
            if ($(this).val() !== '') {
                $('[id=st]').prop('disabled', true);
            }
            else {
                $('[id=st]').prop('disabled', false);
            }
        });
        $('[id=st]').on('input change', function () {
            if ($(this).val() !== '') {
                $('#gr').prop('disabled', true);
            }
            else {
                $('#gr').prop('disabled', false);
            }
        });
    });
