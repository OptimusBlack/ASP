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

placeOrder = () =>{
    console.log("Placing order");
    $.ajax({
        url: "/clinic_manager/place_order/",
        method: "GET",
        type: "GET",
        headers:{
            "X-CSRFToken": '{{csrf_token}}',
            "Content-type" : 'application/json'
        },
    });
};
