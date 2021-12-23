window.onload = function () {
    $('.basket-list').on('change', 'input[type=number]', function (event) {
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                $('.basket-list').html(data.result)
            }
        });
    });

    // $('.add_to_cart').click(function (event) {
    //     $.ajax({
    //         url: '/basket/add/' + event.target.name + '/',
    //         type: 'POST',
    //         success: function (data) {
    //             alert('Item added');
    //             console.log(event.target);
    //         }
    //     });
    // })
};