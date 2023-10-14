
$(document).ready(function() {
    $('.btn-layout').click(function(e) {
        e.preventDefault();
        $('.btn-layout').removeClass('active');
        $(this).addClass('active');

        // Get the layout class (e.g., 'layout-1', 'layout-2', etc.)
        var layoutClass = $(this).attr('class').split(' ').find(function(className) {
            return className.startsWith('layout-');
        });

        // Apply the selected layout class to your content container
        $('.your-content-container').removeClass().addClass('your-content-container ' + layoutClass);
    });
});

