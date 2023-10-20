const user_input = $("#user-input");
const search_icon = $("#search-icon");
const products_div = $("#replaceable-content");
const search_results_container = $("#search-results-container");
const endpoint = "/";
const delay_by_in_ms = 700;
let scheduled_function = false;
let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done((response) => {
            if (response["html_from_view"].trim() !== "") {
                // If there are results, show the search results container
                search_results_container.show();
            } else {
                // If no results, hide the search results container
                search_results_container.hide();
            }
            // fade out the products_div, then:
            products_div.fadeTo("slow", 0).promise().then(() => {
                // replace the HTML contents
                products_div.html(response["html_from_view"]);
                // fade-in the div with new contents
                products_div.fadeTo("slow", 1);
                // stop animating search icon
                search_icon.removeClass("blink");
            });
        });
};
user_input.on("keyup", function () {
    const request_parameters = {
        q: $(this).val(), // value of user_input: the HTML element with ID user-input
    };
    // start animating the search icon with the CSS class
    search_icon.addClass("blink");
    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function);
    }
    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(
        ajax_call,
        delay_by_in_ms,
        endpoint,
        request_parameters
    );
});