// Admin JavaScript File - Simple and Easy to Understand
// Used for: Adding products, Deleting products, and Uploading images.

// 1. Open the "Add New Product" Modal
function openAddModal() {
    // Reset the form so it is empty
    document.getElementById('addProductForm').reset();

    // Show the modal window
    const modal = new bootstrap.Modal(document.getElementById('addProductModal'));
    modal.show();
}

// 2. Delete a Product
async function deleteProduct(id, event) {
    if (event) event.preventDefault(); // Stop clicking link

    // Ask for confirmation
    if (confirm("Are you sure you want to delete this product?")) {
        // Send DELETE command to server
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE',
            credentials: 'include' // Needed for admin check
        });

        if (response.ok) {
            // If successful, reload page to update list
            window.location.reload();
        } else {
            alert("Failed to delete product.");
        }
    }
}

// 3. Add a New Product (Form Submit)
const addForm = document.getElementById('addProductForm');
if (addForm) {
    addForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Stop normal submit

        // Step A: Get data from inputs
        const name = document.getElementById('pName').value;
        const price = document.getElementById('pPrice').value;
        const desc = document.getElementById('pDesc').value;
        const origPrice = document.getElementById('pOriginalPrice').value;

        // Step B: Send Product Data to Server
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                price: parseFloat(price),
                description: desc,
                original_price: origPrice ? parseFloat(origPrice) : null
            }),
            credentials: 'include'
        });

        const result = await response.json();

        // Step C: If success, upload image (if selected)
        if (response.ok) {
            const fileInput = document.getElementById('pImages');
            if (fileInput.files.length > 0) {
                // Prepare image data
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);

                // Send image
                await fetch(`${API_BASE}/${result.data.id}/image`, {
                    method: 'POST',
                    body: formData,
                    credentials: 'include'
                });
            }
            // All done, reload page
            window.location.reload();
        } else {
            alert("Error creating product: " + result.error);
        }
    });
}

// 4. Upload Image (from Product Details page)
async function uploadImage() {
    const fileInput = document.getElementById('imageUploadInput');

    // Check if file is selected
    if (fileInput.files.length === 0) {
        alert("Please pick a file first.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Send to Server
    const response = await fetch(`/api/products/${PRODUCT_ID}/image`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
    });

    if (response.ok) {
        // Reload page to show new image
        window.location.reload();
    } else {
        alert("Upload failed.");
    }
}
