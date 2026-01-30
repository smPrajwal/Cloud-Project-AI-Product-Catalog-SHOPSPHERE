// Cloud-Friendly API URL
var API_URL = "/api";
const API_BASE = API_URL + "/products";

// Convert product name to URL slug (e.g. "Wireless Headphones" -> "wireless-headphones")
function toSlug(name) { return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, ''); }

function formatIndianCurrency(value) {
    if (!value) return "0";
    value = parseFloat(value).toFixed(0);
    const s = value.toString();
    if (s.length <= 3) return s;
    const lastThree = s.slice(-3);
    const rest = s.slice(0, -3);
    let lastThreeWithComma = "," + lastThree;
    const formattedRest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    return formattedRest + lastThreeWithComma;
}

// Index Page
async function loadProducts(query = '') {
    // Rely on global IS_ADMIN from template
    const isAdmin = (typeof IS_ADMIN !== 'undefined' && IS_ADMIN);

    console.log(`LOG: loadProducts query=${query}, isAdmin=${isAdmin}`);
    const grid = document.getElementById('productGrid');
    if (!grid) return;

    let url = `${API_BASE}`;
    // Precise category matching
    const validCategories = ['tech', 'fashion', 'home', 'lifestyle', 'office', 'audio', 'furniture', 'kitchen'];

    if (validCategories.includes(query)) {
        url += `?tag=${encodeURIComponent(query)}`;
    } else if (query) {
        url += `?q=${encodeURIComponent(query)}`;
    }

    // Prevent API caching
    url += (url.includes('?') ? '&' : '?') + `_t=${new Date().getTime()}`;

    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('Failed to load products');

        const products = await res.json();

        grid.innerHTML = products.map(p => {
            let priceHtml = `₹${formatIndianCurrency(p.price)}`;
            if (p.original_price && p.original_price > p.price) {
                const discount = Math.round((1 - p.price / p.original_price) * 100);
                priceHtml = `
                    <span class="text-danger fw-bold me-2">-${discount}%</span>
                    <span class="fw-bold fs-5">₹${formatIndianCurrency(p.price)}</span>
                    <span class="text-muted text-decoration-line-through ms-2 small">₹${formatIndianCurrency(p.original_price)}</span>
                `;
            } else {
                priceHtml = `<span class="fw-bold fs-5">₹${formatIndianCurrency(p.price)}</span>`;
            }

            let adminControls = '';
            if (isAdmin) {
                adminControls = `
                    <div class="mt-2 d-flex justify-content-center">
                        <button class="btn btn-sm btn-outline-danger w-50" onclick="deleteProduct('${p.id}', event)">Delete</button>
                    </div>
                `;
            }

            return `
            <div class="col-md-3 col-6 mb-4">
                <div class="card product-card h-100">
                    <a href="/product/${toSlug(p.name)}" class="text-decoration-none">
                        <img src="${p.thumbnail_url}" alt="${p.name}" loading="lazy" onload="this.style.opacity=1" style="display: block; width: 100%; height: 250px; object-fit: contain; background: #f9f9f9; padding: 1rem; opacity: 0;">
                        <div class="card-body">
                            <h5 class="card-title text-dark">${p.name}</h5>
                            <div class="card-price mb-2">${priceHtml}</div>
                            <div>${p.tags.map(t => `<span class="badge rounded-pill bg-light text-dark border me-1" style="font-weight:400">${t}</span>`).join('')}</div>
                            ${adminControls}
                        </div>
                    </a>
                </div>
            </div>
        `}).join('') || '<div class="col-12 text-center text-muted mt-5 pt-5"><p class="fs-5">No products found.</p></div>';
    } catch (error) {
        console.error("Error loading products:", error);
        grid.innerHTML = `<div class="col-12 text-center text-danger mt-5"><p>Failed to load products. Please try again later.</p></div>`;
    }
}

function searchProducts() {
    const q = document.getElementById('searchInput').value;
    loadProducts(q);
}

// Handle browser 'Back' button cache (BFCache)
window.addEventListener('pageshow', (event) => {
    if (event.persisted || (performance.getEntriesByType("navigation")[0] && performance.getEntriesByType("navigation")[0].type === "back_forward")) {
        // Force reload products if page is restored from cache
        console.log("LOG: Restored from cache, reloading products...");
        loadProducts();
    }
});

// Load products and scroll to product grid (used by ad banners)
async function loadProductsAndScroll(category) {
    await loadProducts(category);
    const productGrid = document.getElementById('productGrid');
    if (productGrid) {
        // Get the position and account for sticky header + leave some breathing room
        const headerOffset = 180;
        const elementPosition = productGrid.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// Detail Page
async function loadProductDetails(id) {
    console.log(`LOG: loadProductDetails ${id}`);
    // Add timestamp to prevent caching
    const res = await fetch(`${API_BASE}/${id}?_t=${new Date().getTime()}`);
    if (!res.ok) return;
    const p = await res.json();

    document.getElementById('pName').textContent = p.name;

    // Price display logic
    let priceHtml = `₹${formatIndianCurrency(p.price)}`;
    if (p.original_price && p.original_price > p.price) {
        const discount = Math.round((1 - p.price / p.original_price) * 100);
        priceHtml = `
            <span class="text-danger fw-bold fs-4 me-2">-${discount}%</span>
            <span class="fw-bold fs-3 text-dark">₹${formatIndianCurrency(p.price)}</span>
            <span class="text-muted text-decoration-line-through ms-2 fs-5">₹${formatIndianCurrency(p.original_price)}</span>
         `;
    } else {
        priceHtml = `<span class="fw-bold fs-3">₹${formatIndianCurrency(p.price)}</span>`;
    }

    document.getElementById('pPrice').innerHTML = priceHtml; // Changed to innerHTML standard
    document.getElementById('pDesc').textContent = p.description;
    document.getElementById('pTags').innerHTML = p.tags.map(t => `<span class="badge-minimal me-1">#${t}</span>`).join('');

    if (p.thumbnail_url && !p.thumbnail_url.includes('placeholder')) {
        document.getElementById('mainImage').src = p.thumbnail_url;
        document.getElementById('mainImage').style.display = 'block';
        document.getElementById('imgPlaceholder').style.display = 'none';
    } else if (p.thumbnail_url) {
        // Fallback for placeholder
        document.getElementById('mainImage').src = p.thumbnail_url;
        document.getElementById('mainImage').style.display = 'block';
        document.getElementById('imgPlaceholder').style.display = 'none';
    } else {
        document.getElementById('mainImage').style.display = 'none';
        document.getElementById('imgPlaceholder').style.display = 'block';
    }

    // Render reviews
    renderReviews(p.reviews);
}

// Global state for images is managed differently now, so no complex logic needed here.

async function submitReview(event) {
    if (event) event.preventDefault();
    const name = document.getElementById('reviewerName').value;
    const text = document.getElementById('reviewText').value;

    if (!name || !text) {
        alert('Name and Review are required!');
        return;
    }

    try {
        const res = await fetch(`${API_URL}/products/${PRODUCT_ID}/reviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reviewer: name, review_text: text })
        });

        if (res.ok) {
            // Clear inputs
            document.getElementById('reviewerName').value = '';
            document.getElementById('reviewText').value = '';

            // Reload details to update List and Avg Badge
            loadProductDetails(PRODUCT_ID);

        } else {
            const err = await res.json();
            alert(err.error || 'Failed to submit review');
        }
    } catch (e) {
        console.error(e);
        alert('Error submitting review');
    }
}

async function deleteReview(id, event) {
    if (event) event.preventDefault();

    try {
        const res = await fetch(`${API_URL}/reviews/${id}`, { method: 'DELETE' });
        if (res.ok) {
            // Dynamic Remove
            if (event && event.target) {
                // Just reload the entire product details
                // This will re-fetch reviews and re-calculate the Avg Sentiment automatically
                await loadProductDetails(PRODUCT_ID);
            } else {
                window.location.reload(); // Fallback
            }
        } else {
            const err = await res.json();
            alert(err.error || 'Failed to delete');
        }
    } catch (e) {
        console.error(e);
        alert('Error deleting review');
    }
}

function renderReviews(reviews) {
    const list = document.getElementById('reviewsList');
    if (!reviews || reviews.length === 0) {
        list.innerHTML = '<p class="text-muted">No reviews yet.</p>';
        const countSpan = document.getElementById('reviewCount');
        if (countSpan) countSpan.textContent = '(0)';
        return;
    }

    let totalScore = 0;
    list.innerHTML = reviews.map(r => {
        totalScore += r.sentiment_score;
        // Show delete only if isAdmin
        const deleteBtn = (typeof IS_ADMIN !== 'undefined' && IS_ADMIN)
            ? `<button class="btn btn-sm btn-link text-danger p-0 ms-2" onclick="deleteReview(${r.id}, event)" style="font-size: 0.8rem;">Delete</button>`
            : '';

        return `
        <div class="mb-3 border-bottom pb-2">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="fw-bold small">${r.reviewer || 'Guest'}</span> 
                    <span class="badge bg-${r.sentiment_label === 'Positive' ? 'success' : 'secondary'} ms-2" style="font-size: 0.7em;">${r.sentiment_label}</span>
                </div>
                ${deleteBtn}
            </div>
            <p class="mb-0 small mt-1">${r.review_text}</p>
        </div>`;
    }).join('');

    const avg = totalScore / reviews.length;
    const badge = document.getElementById('sentimentBadge');
    if (badge) badge.textContent = `Avg Sentiment: ${(avg * 100).toFixed(0)}%`;

    const countSpan = document.getElementById('reviewCount');
    if (countSpan) countSpan.textContent = `(${reviews.length})`;
}

async function loadRecommendations(id) {
    console.log(`LOG: loadRecommendations for ${id}`);
    const res = await fetch(`${API_BASE}/${id}/recommendations`);
    const recs = await res.json();
    document.getElementById('recommendationsList').innerHTML = recs.map(r => {
        let priceHtml = `<span class="fw-bold">₹${formatIndianCurrency(r.price)}</span>`;
        if (r.original_price && r.original_price > r.price) {
            const discount = Math.round((1 - r.price / r.original_price) * 100);
            priceHtml = `
                <span class="text-danger fw-bold me-1">-${discount}%</span>
                <span class="fw-bold">₹${formatIndianCurrency(r.price)}</span>
                <span class="text-muted text-decoration-line-through ms-1 small">₹${formatIndianCurrency(r.original_price)}</span>
            `;
        }
        return `
        <div class="col-4 me-3" style="min-width: 250px;">
            <div class="card h-100 product-card">
                 <a href="/product/${toSlug(r.name)}" class="text-reset text-decoration-none">
                    <img src="${r.thumbnail_url}" alt="${r.name}" loading="lazy" onload="this.style.opacity=1" style="display: block; width: 100%; height: 180px; object-fit: contain; background: #f9f9f9; padding: 1rem; opacity: 0;">
                    <div class="card-body">
                        <h6 class="card-title text-truncate">${r.name}</h6>
                        <div class="small">${priceHtml}</div>
                    </div>
                </a>
            </div>
        </div>
    `}).join('');
}
