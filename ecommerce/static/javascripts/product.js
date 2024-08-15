// product.js

// Fetch and display products
export async function fetchProducts() {
    try {
        const response = await fetch('/api/products/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateProductTable(data);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Populate product table
function populateProductTable(products) {
    const productTable = document.getElementById('productTable');
    productTable.innerHTML = '';  // Clear existing rows
    products.forEach(product => {
        const row = `
            <tr>
                <td>${product.title}</td>
                <td>${product.content}</td>
                <td>${product.price}</td>
                <td>${product.quantity}</td>
                <td>
                    <button class="btn btn-sm btn-warning edit-btn" data-id="${product.id}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${product.id}">Delete</button>
                </td>
            </tr>
        `;
        productTable.innerHTML += row;
    });

    // Attach event listeners after populating the table
    attachEventListeners();
}

// Attach event listeners to the edit and delete buttons
function attachEventListeners() {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            if (productId) {
                editProduct(productId);
            } else {
                console.error('Product ID is undefined.');
            }
        });
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            if (productId) {
                deleteProduct(productId);
            } else {
                console.error('Product ID is undefined.');
            }
        });
    });
}

// Edit product
export async function editProduct(id) {
    try {
        const response = await fetch(`/api/products/${id}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const product = await response.json();

        // Populate form fields with the product data
        document.getElementById('title').value = product.title;
        document.getElementById('content').value = product.content;
        document.getElementById('price').value = product.price;
        document.getElementById('quantity').value = product.quantity;
        document.getElementById('productId').value = product.id;  // Hidden field to track product ID
        document.getElementById('submitBtn').innerText = 'Update Product';  // Change button text
    } catch (error) {
        console.error('Error editing product:', error);
    }
}

// Update product
export async function updateProduct(id) {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const price = document.getElementById('price').value;
    const quantity = document.getElementById('quantity').value;

    try {
        const response = await fetch(`/api/products/${id}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify({
                title: title,
                content: content,
                price: price,
                quantity: quantity
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        alert('Product updated successfully!');
        fetchProducts();  // Refresh product list
        resetForm();  // Reset form fields
    } catch (error) {
        console.error('Error updating product:', error);
    }
}

// Delete product
export async function deleteProduct(id) {
    if (confirm('Are you sure you want to delete this product?')) {
        try {
            const response = await fetch(`/api/products/${id}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            alert('Product deleted successfully!');
            fetchProducts();  // Refresh product list
        } catch (error) {
            console.error('Error deleting product:', error);
        }
    }
}

// Reset the form after update
function resetForm() {
    document.getElementById('addProductForm').reset();
    document.getElementById('productId').value = '';  // Clear hidden product ID field
    document.getElementById('submitBtn').innerText = 'Add Product';  // Reset button text
}

// Initial fetching of products when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
});
