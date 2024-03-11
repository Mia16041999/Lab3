// scripts.js

// Function to fetch and display products
function fetchProducts() {
    fetch('/products') // Adjust if your backend API is at a different endpoint
        .then(response => response.json())
        .then(products => {
            const productList = document.getElementById('product-list');
            productList.innerHTML = ''; // Clear existing products
            products.forEach(product => {
                productList.innerHTML += `<div>${product.name} - ${product.price}</div>`;
            });
        })
        .catch(error => console.error('Error fetching products:', error));
}

// Call fetchProducts on page load
window.onload = fetchProducts;
