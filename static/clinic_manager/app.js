addToCart = (id) => {
    let order_qty = $(`#qty${id}`).val();
    if(isNaN(order_qty)){
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
        });
    }
};

checkout = () =>{
    $.ajax({
        url: "/clinic_manager/checkout/",
        method: "GET",
        type: "GET",
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });
};

placeOrder = () =>{
    console.log("Placing order");
    let priority = $('#priority').val();
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
};
