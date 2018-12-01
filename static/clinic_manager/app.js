var priority = null;

addToCart = (id) => {
    let order_qty = $(`#qty${id}`).val();
    if(order_qty == '' || order_qty == null || isNaN(order_qty)){
        alert("Invalid quantity");
    }
    else{
        //Place order
        let data = {
            'product_id': id,
            'qty': order_qty,
        };

        $.ajax({
            url: "/clinic_manager/add_to_cart/",
            method: "POST",
            type: "POST",
            dataType: "json",
            data: JSON.stringify(data),
            headers:{
                "X-CSRFToken": '{{csrf_token}}',
                "Content-type" : 'application/json'
            },
            success: function (res) {
                if (res['msg'] == "overweight"){
                    alert('The order has already crossed the weight limit of 23.8kg');
                }
                if (res['msg'] == "done"){
                    $.notify('Added to cart', 'success');
                }
            }
        });
    }
};

viewCart = () =>{
   /* $.ajax({
        url: "/clinic_manager/show_cart/",
        method: "GET",
        type: "GET",
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });*/
    window.location.href = window.location.origin + '/clinic_manager/show_cart/';
};

placeOrder = () =>{
    console.log("Placing order");
    if (priority == null){
        alert('Please select priority');
        return;
    }
    $.ajax({
        url: "/clinic_manager/place_order/",
        method: "POST",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({'priority': priority}),
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });
    $.notify('Order Placed!', 'success');

    setTimeout(function() {
                window.location.href = window.location.origin + '/clinic_manager/home/';
                }, 2000);
};


logout = () => {
    $.ajax({
        url: "/logout/",
        method: "GET",
        type: "GET",
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });
    window.location.replace(`${window.location.origin}/`);
};

$(document).ready(function () {
    $('.dropdown-item').click(function () {
       priority = $(this).attr('value');
       $('#dropdownMenuButton').html($(this).html().toUpperCase());
       console.log(priority);
    });
});

notifyDelivery = (e) =>{
    /**
     * Cancel an order
     * @type {object}  e.id gives "cancel-<id>
     */

    let order_id = parseInt(e.id.substring(8));
    $.ajax({
        url: "/clinic_manager/notify_delivery/",
        method: "POST",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({'order_id' : order_id}),
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });

    console.log("Delivery Notified");
    window.location.href = window.location.origin + '/clinic_manager/orders/';
};

cancelOrder = (e) =>{
    /**
     * Cancel an order
     * @type {object}  e.id gives "cancel-<id>
     */

    let order_id = parseInt(e.id.substring(7));
    $.ajax({
        url: "/clinic_manager/cancel_order/",
        method: "POST",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({'order_id' : order_id}),
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });

    console.log("Order Cancelled");
    window.location.href = window.location.origin + '/clinic_manager/orders/';
};
