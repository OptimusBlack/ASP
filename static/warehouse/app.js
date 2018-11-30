process_queue_pop = () => {
    $.ajax({
        url: "/warehouse/pop/",
        method: "GET",
        type: "GET",
        success: function (res) {
            data = $.parseJSON(res);
            if (data.msg == 1){
                alert('One order being processed');
            }
            else{
                window.location.href = window.location.origin + '/warehouse/home/';
            }
        }
    });
};

execute_process = () => {
    $.ajax({
        url: "/warehouse/process/",
        method: "GET",
        type: "GET",
        success: function(result){
            console.log(result);
;
            if (result == "0"){
                alert('Nothing in process');
            }
            else {
                let url = window.URL.createObjectURL(new Blob([result], {type: 'application/pdf'}));
                let $a = $('<a />', {
                    'href': url,
                    'download': 'shipping_label.pdf',
                    'text': "click"
                }).hide().appendTo("body")[0].click();
                window.location.href = window.location.origin + '/warehouse/home/';
            }
        }
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