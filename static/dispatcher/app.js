execute_pop = () => {
    $.ajax({
        url: "/dispatcher/pop/",
        method: "GET",
        type: "GET",
    });
};

execute_dispatch = () => {
    $.ajax({
        url: "/dispatcher/dispatch/",
        method: "GET",
        type: "GET",
        success: function(result){
            console.log(result);
            let url = window.URL.createObjectURL(new Blob([result], {type: 'text/csv'}));
            let $a = $('<a />', {
            'href': url,
            'download': 'download.csv',
            'text': "click"
            }).hide().appendTo("body")[0].click();
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