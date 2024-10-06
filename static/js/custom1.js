$(document).ready(function () {

    /* increment and decrement */
    $('.increment-btn').click(function (e) {
        e.preventDefault();
        var incre_value = $(this).parent('.quantity').find('.qty-input').val();
        var value = parseInt(incre_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value<10){
            value++;
            $(this).parent(".quantity").find(".qty-input").val(Number(value));
        }

    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();
        var decre_value = $(this).parent('.quantity').find('.qty-input').val();
        var value = parseInt(decre_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value>1){
            value--;
            $(this).parent('.quantity').find('.qty-input').val(value);
        }
    });


    /* add to cart */
    $('.addToCartBtn').click(function (e) { 
        e.preventDefault();
        var product_id = $('.product_id').val();
        var product_qty = $('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id' : product_id,
                'product_qty' : product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                //console.log(response)
                alertify.success(response.status)
            }
        });
        
    });

    /* Move to wishlist */
    $('.moveToWishlistBtn').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: "POST",
            url: "/move-to-wishlist",
            data: {
                'product_id' : product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                //console.log(response)
                alertify.success(response.status)
            }
        });
        
    });


    /* update cart */
    //$('.change_qty').on('click', function (e) {
    $('.change_qty').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.product_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id' : product_id,
                'product_qty' : product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                //console.log(response)
                alertify.success(response.status)
                location.reload()
                //$('.cartList').load(location.href + " .cartList");
            }
        });
        
    });

    /* delete-cart-item */
    $(document).on('click','.delete-cart-item', function (e) {    
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken : token,
            },
            success: function (response) {
                location.reload();
                //console.log(response)
                alertify.success(response.status)
                //$('.cartList').load(location.href + " .cartList");
                
            }
        });


    });


    /* delete-wishlist-item */
    $(document).on('click','.delete-wishlist-item', function (e) {    
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken : token,
            },
            success: function (response) {
                //location.reload();
                //console.log(response)
                alertify.success(response.status)
                $('.wishlist').load(location.href + " .wishlist");
                
            }
        });


    });



    /* message */
    window.setTimeout(function() {
        $(".alert").fadeTo(400, 0).slideUp(400, function(){
            $(this).remove(); 
        });
    }, 2000);

});

