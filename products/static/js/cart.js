$(document).ready(function () {
    // Function to update the cart count
    function updateCartCount() {
        $.ajax({
            url: '/cart/count/',
            method: 'GET',
            success: function (data) {
                if (data.cart_count !== undefined) {
                    $("#cart-count").text(data.cart_count);
                }
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error("Error:", errorThrown);
            }
        });
    }

// Function to update the cart items
// Function to update the cart items
function updateCartItems() {
    $.ajax({
        url: '/cart/items/',
        method: 'GET',
        success: function (data) {
            var cartItemsContainer = $('.dropdown-cart-products');
            cartItemsContainer.empty();
            data.cart_items.forEach(function (item) {
                console.log(item.product_uuid); // Check if the product UUID is correctly extracted
                var productHtml = `
                    <div class="product">
                        <div class="product-cart-details">
                            <h4 class="product-title">
                                <a href="${item.product_url}">${item.title}</a>
                            </h4>
                            <span class="cart-product-info">
                                <span class="cart-product-qty">${item.quantity}</span>
                                x ${item.price}
                            </span>
                        </div><!-- End .product-cart-details -->
                        <figure class="product-image-container">
                            <a href="${item.product_url}">
                                <img src="${item.image_url}" alt="cover">
                            </a>
                        </figure>
                        <a href="#" class="btn-remove" title="Remove Product" data-product-uuid="${item.product_uuid}">
                            <i class="icon-close"></i>
                        </a>
                    </div><!-- End .product -->
                `;
                cartItemsContainer.append(productHtml);
            });
            var totalCartPrice = $('.cart-total-price');
            totalCartPrice.text('$' + data.total_price);

            // Update subtotal and total in the summary table
            var summarySubtotal = $('.summary-subtotal td:last-child');
            summarySubtotal.text('$' + data.total_price);

            var summaryTotal = $('.summary-total td:last-child');
            summaryTotal.text('$' + data.total_price);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", errorThrown);
        }
    });
}

    // Call the updateCartCount function initially to set the cart count
    updateCartCount();

    // Call the updateCartItems function initially to set the cart items
    updateCartItems();

    // Event handler for adding a product to the cart
    $(document).on("submit", ".add-to-cart-form", function (e) {
        e.preventDefault();
        var form = $(this);
        var productUuid = form.data("product-uuid");
        var quantity = form.find("input[name=quantity]").val();
        var override = false;
        var csrfToken = form.find("input[name=csrfmiddlewaretoken]").val();
        var addButton = form.find("#add-to-cart-button");
        var loader = addButton.find(".loader");
        addButton.attr("disabled", true);
        loader.addClass("active");

        // Send an AJAX request to add the product to the cart
        $.ajax({
            url: `/cart/add/${productUuid}/`,
            method: "POST",
            data: {
                quantity: quantity,
                override: override,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (data) {
                if (data.cart_count !== undefined) {
                    updateCartCount();
                    updateCartItems();
                }
                addButton.find("span").first().text("Already Added");
                    // Display the message on your template
                //var messageDiv = $('.message-div'); // Change this selector to match your template structure
                //messageDiv.text(data.message); // Display the message
                alert(data.message);
            },

            error: function (xhr, textStatus, errorThrown) {
                console.error("Error:", errorThrown);
            },
            complete: function () {
                addButton.attr("disabled", false);
                loader.removeClass("active");
            }
        });
    });

// Event handler for removing a product from the cart
$(document).on("click", ".btn-remove", function (e) {
    e.preventDefault();
    var productUUID = $(this).data("product-uuid");
    var removeButton = $(this);
    var productUUID = $(this).data('product-uuid');
    $('[data-product-uuid="' + productUUID + '"]').remove(); // Check if the productUUID is correctly extracted.

    if (productUUID) {
        // Get the CSRF token value
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();

        // Send an AJAX request to remove the product from the cart
        $.ajax({
            url: `/cart/remove/${productUUID}/`,
            method: "POST",
            data: {
                csrfmiddlewaretoken: csrfToken  // Include the CSRF token
            },
            success: function (data) {
                if (data.cart_count !== undefined) {
                    updateCartCount();
                    updateCartItems();
                }
                alert(data.message);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error("Error:", errorThrown);
            },
            complete: function () {
                removeButton.closest(".product").remove();
                updateCartCount();
            }
        });
    } else {
        console.log("Product UUID is undefined or missing.");
    }
});



});