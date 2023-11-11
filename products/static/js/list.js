jQuery(function ($) {
    var $list = $('.item-list');
    var $loader = $('script[type="text/template"].loader');
    $list.jscroll({
        loadingHtml: $loader.html(),
        padding: 100,
        pagingSelector: '.pagination',
        nextSelector: 'a.next-page:last',
        contentSelector: '.item,.pagination'
    });
});

jQuery(function ($) {
    var $list = $('.item-list');
    var $modal = $('#modal');
    $modal.on('click', '.close', function (event) {
        $modal.modal('hide');
        // do something when dialog is closed
    });
    $list.on('click', 'a.item', function (event) {
        var $link = $(this);
        var url = $link.data('modal-url');
        var title = $link.data('modal-title');
        if (url && title) {
            event.preventDefault();
            $('.modal-title', $modal).text(title);
            $('.modal-body', $modal).load(url, function () {
                $modal.on('shown.bs.modal', function () {
                    // do something when dialog is shown
                }).modal('show');
            });
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Get references to the navigation elements
    const prevButton = document.querySelector(".product-pager-prev");
    const nextButton = document.querySelector(".product-pager-next");
    const productDetail = document.querySelector(".product-detail");

    // Add event listeners to the "Prev" and "Next" buttons
    prevButton.addEventListener("click", function (e) {
        e.preventDefault();
        // Implement logic to load the previous product detail
        // For example, you can fetch the data via AJAX and update the productDetail content
    });

    nextButton.addEventListener("click", function (e) {
        e.preventDefault();
        // Implement logic to load the next product detail
        // For example, you can fetch the data via AJAX and update the productDetail content
    });
});
