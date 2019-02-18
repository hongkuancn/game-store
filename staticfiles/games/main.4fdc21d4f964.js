

$(function () {
    // Short Document Ready
    $('#delete').on('click', function (e) {
        if (!confirm($(this).data('confirm'))) {
            e.stopImmediatePropagation();
            e.preventDefault();
        }
    });

    let url = window.location.href;
    let encodeURL = encodeURIComponent(url)
    $('.shareFacebook').attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + encodeURL);
    $('.shareTwitter').attr("href", "https://twitter.com/home?status=" + encodeURL);
});
