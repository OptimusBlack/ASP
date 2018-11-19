process_queue_pop = () => {
    $.ajax({
        url: "/warehouse/pop/",
        method: "GET",
        type: "GET",
    });
};

execute_process = () => {
    $.ajax({
        url: "/warehouse/process/",
        method: "GET",
        type: "GET",
        success: function(result){
            console.log(result);
            let url = window.URL.createObjectURL(new Blob([result], {type: 'application/pdf'}));
            let $a = $('<a />', {
            'href': url,
            'download': 'shipping_label.pdf',
            'text': "click"
            }).hide().appendTo("body")[0].click();
        }
    });
};
