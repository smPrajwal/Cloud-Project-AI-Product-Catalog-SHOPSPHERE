// Main JavaScript File - Simple, Short, and Functional
const API_BASE = '/api/products';
const CATEGORIES = ['tech', 'fashion', 'home', 'lifestyle', 'office', 'audio', 'furniture', 'kitchen'];

// Helpers
function formatPrice(price) { return price ? Number(price).toLocaleString('en-IN') : "0"; }
function createSlug(name) { return name.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-'); }

// Create Product Card HTML
function createProductCard(product, isRecommendation = false) {
    let priceHtml = `<span class="fw-bold fs-5">₹${formatPrice(product.price)}</span>`;
    if (product.original_price > product.price) {
        let discount = Math.round(((product.original_price - product.price) / product.original_price) * 100);
        priceHtml = `<span class="text-danger fw-bold me-2">-${discount}%</span><span class="fw-bold fs-5">₹${formatPrice(product.price)}</span><span class="text-muted text-decoration-line-through ms-2 small">₹${formatPrice(product.original_price)}</span>`;
    }

    let deleteBtn = (typeof IS_ADMIN !== 'undefined' && IS_ADMIN && !isRecommendation) ?
        `<div class="mt-2 text-center"><button class="btn btn-sm btn-outline-danger" onclick="deleteProduct('${product.id}', event)">Delete</button></div>` : '';

    return `
        <div class="${isRecommendation ? 'col-4 me-3' : 'col-md-3 col-6 mb-4'}" style="${isRecommendation ? 'min-width: 250px;' : ''}">
            <div class="card product-card h-100"><a href="/product/${createSlug(product.name)}" class="text-decoration-none">
                <img src="${product.thumbnail_url}" class="card-img-top" alt="${product.name}" style="height: 260px; object-fit: contain; padding: 0;">
                <div class="card-body"><h5 class="card-title text-dark text-truncate">${product.name}</h5><div class="mb-2">${priceHtml}</div>${deleteBtn}</div>
            </a></div>
        </div>`;
}

// Home Page: Load Products
async function loadProducts(query = '') {
    const grid = document.getElementById('productGrid');
    if (!grid) return;

    let url = API_BASE + '?_t=' + Date.now();
    if (CATEGORIES.includes(query)) url += '&tag=' + query;
    else if (query) url += '&q=' + query;

    try {
        const response = await fetch(url);
        const products = await response.json();

        grid.innerHTML = products.length ? '' : '<p class="text-center mt-5">No products found.</p>';
        for (let product of products) grid.innerHTML += createProductCard(product);
    } catch (error) { grid.innerHTML = '<p class="text-center text-danger">Failed to load.</p>'; }
}
function searchProducts() { loadProducts(document.getElementById('searchInput').value); }

// Product Details Page
async function loadProductDetails(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}?_t=${Date.now()}`);
        if (!response.ok) return;
        const product = await response.json();

        document.getElementById('pName').textContent = product.name;
        document.getElementById('pDesc').textContent = product.description;
        document.getElementById('pTags').innerHTML = (product.tags || []).map(tag => `<span class="badge-minimal me-1">${tag}</span>`).join('');

        let priceHtml = `<span class="fw-bold fs-3">₹${formatPrice(product.price)}</span>`;
        if (product.original_price > product.price) {
            let discount = Math.round(((product.original_price - product.price) / product.original_price) * 100);
            priceHtml = `<span class="text-danger fw-bold fs-4 me-2">-${discount}%</span><span class="fw-bold fs-3 text-dark">₹${formatPrice(product.price)}</span><span class="text-muted text-decoration-line-through ms-2 fs-5">₹${formatPrice(product.original_price)}</span>`;
        }
        document.getElementById('pPrice').innerHTML = priceHtml;

        let hasImage = product.thumbnail_url && !product.thumbnail_url.includes('placeholder');
        document.getElementById('mainImage').src = hasImage ? product.thumbnail_url : '';
        document.getElementById('mainImage').style.display = hasImage ? 'block' : 'none';
        document.getElementById('imgPlaceholder').style.display = hasImage ? 'none' : 'block';

        renderReviews(product.reviews);
        loadRecommendations(product.id);
    } catch (error) { console.error(error); }
}

// Reviews & Recommendations
function renderReviews(reviews) {
    const list = document.getElementById('reviewsList');
    if (!reviews || !reviews.length) {
        list.innerHTML = '<p class="text-muted">No reviews yet.</p>';
        document.getElementById('reviewCount').textContent = '(0)';
        return;
    }

    list.innerHTML = '';
    let totalScore = 0;
    for (let review of reviews) {
        totalScore += review.sentiment_score;
        let badge = review.sentiment_label === 'Positive' ? 'bg-success' : 'bg-secondary';
        let deleteBtn = (typeof IS_ADMIN !== "undefined" && IS_ADMIN) ? `<button class="btn btn-sm btn-link text-danger ms-2 p-0 text-decoration-none" style="font-size: 0.9em;" onclick="deleteReview(${review.id})">Delete</button>` : "";

        list.innerHTML += `<div class="mb-2 border-bottom pb-1"><div class="d-flex justify-content-between align-items-center">
            <div><strong>${review.reviewer}</strong><span class="badge ${badge} ms-2">${review.sentiment_label}</span></div>${deleteBtn}</div>
            <p class="mb-0 small mt-1">${review.review_text}</p></div>`;
    }
    document.getElementById('reviewCount').textContent = `(${reviews.length})`;
    if (document.getElementById('sentimentBadge')) document.getElementById('sentimentBadge').textContent = `Avg Sentiment: ${(totalScore / reviews.length * 100).toFixed(0)}%`;
}

async function loadRecommendations(id) {
    const response = await fetch(`${API_BASE}/${id}/recommendations`);
    const products = await response.json();
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';
    for (let product of products) container.innerHTML += createProductCard(product, true);
}

// Actions
async function apiAction(url, method, body = null) {
    await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : null });
    loadProductDetails(PRODUCT_ID);
}

function submitReview(e) {
    e.preventDefault();
    const name = document.getElementById('reviewerName').value;
    const text = document.getElementById('reviewText').value;
    if (name && text) {
        apiAction(`/api/products/${PRODUCT_ID}/reviews`, 'POST', { reviewer: name, review_text: text });
        document.getElementById('reviewerName').value = '';
        document.getElementById('reviewText').value = '';
    } else alert("Enter name and review.");
}

function deleteReview(id) { apiAction(`/api/reviews/${id}`, 'DELETE'); }

// Init
document.addEventListener('DOMContentLoaded', () => typeof PRODUCT_ID !== 'undefined' ? loadProductDetails(PRODUCT_ID) : loadProducts());
