

$(function () {
    // Short Document Ready
    $('#delete').on('click', function (e) {
        if (!confirm($(this).data('confirm'))) {
            e.stopImmediatePropagation();
            e.preventDefault();
        }

        // if(confirm("Are you sure")){
        //     // e.stopImmediatePropagation();
        //     e.preventDefault();
        // }
    });
});
