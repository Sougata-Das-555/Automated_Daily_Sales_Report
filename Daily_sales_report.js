
let productCount = 0;
let saleCount = 0;

// Frontend and Input Management
function addProduct() {
    productCount++;

    const div = document.createElement("div");
    div.className = "form-grid product-row";

    div.innerHTML = `
        <div>
            <label>Product ID</label>
            <input class="pid" placeholder="Enter product ID">
        </div>

        <div>
            <label>Product Name</label>
            <input class="pname" placeholder="Enter product name">
        </div>

        <div>
            <label>Product Price</label>
            <input class="price" type="number" min="0"
                   step="0.01" placeholder="Enter price">
        </div>

        <div>
            <label>Product Quantity</label>
            <input class="quantity" type="number" min="0"
                   step="1" placeholder="Enter quantity">
        </div>
    `;

    document.getElementById("products").appendChild(div);
    updateProductOptions();
}

function addSale() {
    saleCount++;

    const div = document.createElement("div");
    div.className = "sale-grid sale-row";

    div.innerHTML = `
        <div>
            <label>Product</label>
            <select class="sale-product"></select>
        </div>

        <div>
            <label>Quantity Sold</label>
            <input class="sold-quantity"
                   type="number"
                   min="1"
                   step="1"
                   placeholder="Enter quantity">
        </div>
    `;

    document.getElementById("sales").appendChild(div);
    updateProductOptions();
}

function updateProductOptions() {
    const productRows = document.querySelectorAll(".product-row");
    const options = [];

    productRows.forEach(row => {
        const id = row.querySelector(".pid").value.trim();
        const name = row.querySelector(".pname").value.trim();

        if (id && name) {
            options.push({
                id: id,
                name: name
            });
        }
    });

    document.querySelectorAll(".sale-product").forEach(select => {
        const previousValue = select.value;

        select.innerHTML = '<option value="">Select Product</option>';

        options.forEach(product => {
            const option = document.createElement("option");
            option.value = product.id;
            option.textContent = product.name;
            select.appendChild(option);
        });

        if (options.some(p => p.id === previousValue)) {
            select.value = previousValue;
        }
    });
}

document.getElementById("products").addEventListener(
    "input",
    updateProductOptions
);

function showMessage(message, type) {
    const box = document.getElementById("message");
    box.className = type;
    box.textContent = message;
}

function escapeCSV(val) {
    const str = String(val ?? "");
    if (str.includes(",") || str.includes('"') || str.includes("\n")) {
        return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
}

