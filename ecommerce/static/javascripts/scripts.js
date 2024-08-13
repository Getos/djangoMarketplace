// Function to increase the quantity
export function increaseQuantity(button) {
    const input = button.parentNode.querySelector('input[name="quantity"]');
    let currentValue = parseInt(input.value);
    if (currentValue < 100) {
        input.value = currentValue + 1;
    }
}

// Function to decrease the quantity
export function decreaseQuantity(button) {
    console.log("downclicked")
    const input = button.parentNode.querySelector('input[name="quantity"]');
    let currentValue = parseInt(input.value);
    if (currentValue > 1) {
        input.value = currentValue - 1;
    }
}

// Attach functions to the window object to make them globally accessible
window.increaseQuantity = increaseQuantity;
window.decreaseQuantity = decreaseQuantity;

// Function to get CSRF token from cookies
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-outline-dark').forEach(button => {
        button.addEventListener('click', addToCart);
    });
});
// Function to add product to cart
export function addToCart(e) {
    const button = e.target;
    console.log("inside addToCart")

    const productId = button.getAttribute('data-product-id');
    const quantityInput = button.parentNode.querySelector('input[name="quantity"]');
    console.log('Quantity Input:', quantityInput);
    const quantity = parseInt(quantityInput.value);
    console.log('Quantity:', quantity);

    if (quantity > 0) {
        const url = "/add_to_cart/";

        const data = {
            id: productId,
            quantity: quantity
        };
    console.log(productId, quantity)

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("num_of_items").innerHTML = data.num_of_items;
        console.log(data);
    })
    .catch(error => {
        console.log(error);
    });
        console.log(data)
        console.log(quantityInput);  // Inspect the element
        console.log(quantity);  // Check the value being retrieved

} else {
    console.log("Quantity must be greater than 0.");
}
}
export function updateCartItemCount(count) {
    const numItemsElement = document.getElementById("num_of_items");
    if (numItemsElement) {
        numItemsElement.textContent = count;
    }
}

