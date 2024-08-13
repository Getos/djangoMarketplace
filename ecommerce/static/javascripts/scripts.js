export function increaseQuantity(button) {
    const input = button.parentNode.querySelector('input');
    let currentValue = parseInt(input.value);
    if (currentValue < 100) {
        input.value = currentValue + 1;
    }
}

export function decreaseQuantity(button) {
    const input = button.parentNode.querySelector('input');
    let currentValue = parseInt(input.value);
    if (currentValue > 0) {
        input.value = currentValue - 1;
    }
}

// Attach functions to the window object to make them globally accessible
window.increaseQuantity = increaseQuantity;
window.decreaseQuantity = decreaseQuantity;
