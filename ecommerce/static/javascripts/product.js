// product.js


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
                    <button class="btn btn-sm btn-warning edit-btn" data-id="${product.pk}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${product.pk}">Delete</button>
                </td>
            </tr>
        `;
        productTable.innerHTML += row;
        console.log(product.pk)
        
    });

    // Attach event listeners after populating the table
    attachEventListeners();
}

// Attach event listeners to the edit and delete buttons
function attachEventListeners() {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            console.log('this is inside getAttribute'+productId)
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
export async function editProduct(productId) {
    try {
        const response = await fetch(`/api/products/${productId}/`, {
            headers: {
                'Authorization': `Token ${getToken()}`
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const product = await response.json();

        // Populate form fields with the product data
        document.getElementById('title').value = product.title;
        document.getElementById('content').value = product.content;
        document.getElementById('price').value = product.price;
        document.getElementById('quantity').value = product.quantity;
        document.getElementById('productId').value = product.pk;  // Hidden field to track product ID
        document.getElementById('submitBtn').innerText = 'Update Product';  // Change button text
    } catch (error) {
        console.error('Error editing product:', error);
    }
}

function getToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'authToken') {
            return value;
        }
    }
    return null;  // Return null if no token is found
}

// Fetch and display products
export async function fetchProducts() {
    try {
        const token = getToken();  // Get token from cookie
        const response = await fetch('/api/products/', {
            headers: {
                'Authorization': `Token ${token}`  // Pass token in Authorization header
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateProductTable(data);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Update product
export async function updateProduct(productId) {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const price = document.getElementById('price').value;
    const quantity = document.getElementById('quantity').value;
    const token = getToken();  // Get token from cookie

    try {
        const response = await fetch(`/api/products/${productId}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,  // Pass token in Authorization header
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
export async function deleteProduct(productId) {
    const token = getToken();  // Get token from cookie

    if (confirm('Are you sure you want to delete this product?')) {
        try {
            const response = await fetch(`/api/products/${productId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,  // Pass token in Authorization header
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
