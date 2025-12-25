// Modal Helpers
function openAddModal() {
    document.getElementById('addProductForm').reset();

    document.getElementById('productModalTitle').textContent = 'New Item';
    document.getElementById('modalSubmitBtn').textContent = 'Create Product';
    const modal = new bootstrap.Modal(document.getElementById('addProductModal'));
    modal.show();
}

async function deleteProduct(id, event) {
    if (event) { event.preventDefault(); event.stopPropagation(); }

    if (!confirm('Delete this product? This cannot be undone.')) return;

    try {
        const res = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
        const result = await res.json();

        if (res.ok && result.success) {
            // Efficient: Remove element instead of reload
            const card = event.target.closest('.col-6') || event.target.closest('.col-md-3'); // Safer selector
            if (card) card.remove();
            else window.location.reload(); // Fallback
        }
        else alert('Failed to delete product: ' + (result.error || 'Error'));
    } catch (e) {
        console.error(e);
        alert('Network error');
    }
}

document.getElementById('addProductForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById('pName').value,
        price: parseFloat(document.getElementById('pPrice').value),
        original_price: document.getElementById('pOriginalPrice').value ? parseFloat(document.getElementById('pOriginalPrice').value) : null,
        description: document.getElementById('pDesc').value,
        tags: document.getElementById('pTags').value.split(',').map(t => t.trim()).filter(Boolean)
    };

    try {
        const res = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (res.ok && result.success) {
            const productId = result.data.id;

            // Upload images if any
            const imageInput = document.getElementById('pImages');
            if (imageInput.files.length > 0 && productId) {
                const formData = new FormData();
                const file = imageInput.files[0];
                formData.append('file', file);

                // Use the singular endpoint
                await fetch(`${API_BASE}/${productId}/image`, {
                    method: 'POST',
                    body: formData
                });
            }

            window.location.reload();
        } else {
            alert('Error: ' + (result.error || 'Unauthorized'));
        }
    } catch (err) { console.error(err); }
});

// Consolidated uploadImage from product.html
async function uploadImage() {
    const input = document.getElementById('imageUploadInput');
    if (!input.files || input.files.length === 0) {
        alert('Please select a file first.');
        return;
    }

    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const btn = document.querySelector('button[onclick="uploadImage()"]');
    if (btn) {
        var originalText = btn.innerText;
        btn.innerText = 'Uploading...';
        btn.disabled = true;
    }

    try {
        // Use PRODUCT_ID as slug/id
        const res = await fetch(`/api/products/${PRODUCT_ID}/image`, {
            method: 'POST',
            body: formData
        });

        const result = await res.json();

        if (res.ok && result.success) {
            // Update image on page immediately
            const img = document.getElementById('mainImage');
            const timestamp = new Date().getTime(); // Cache buster
            // Backend returns: { success: true, data: { url: "..." } }
            const newUrl = result.data.url;

            // Check for existing query params in newUrl
            const separator = newUrl.includes('?') ? '&' : '?';
            img.src = newUrl + separator + 't=' + timestamp;
            img.style.display = 'block';
            document.getElementById('imgPlaceholder').style.display = 'none';

            // Clear input
            input.value = '';
        } else {
            alert('Error: ' + (result.error || 'Upload failed'));
        }
    } catch (e) {
        console.error(e);
        alert('Network error during upload.');
    } finally {
        if (btn) {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    }
}
