window.onload = function () {
    $('.basket-list').on('change', 'input[type=number]', function (event) {
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                $('.basket-list').html(data.result)
            }
        });
    })
};