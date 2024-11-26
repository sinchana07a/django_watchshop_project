document.getElementById('search-bar').addEventListener('input', function() {
    const query = this.value.trim();

    if (!query) {
        // Clear the product list if the search bar is empty
        document.getElementById("product_list").innerHTML = "";
        return;
    }

    fetch(`/search_product?query=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Unable to connect to search product.");
            }
            return response.json();
        })
        .then(data => {
            const watchContainer = document.getElementById("product_list");
            watchContainer.innerHTML = ""; // Clear previous results

            data.forEach(watch => {
                const watchCard = `
                    <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                        <div class="card h-100">
                            <img src="uploads/${watch.image}" class="img-thumbnail" style="height: 250px;" alt="${watch.name}">
                            <div class="card-body">
                                <p class="card-text"><strong>Id: </strong>${watch.id}</p>
                                <p class="card-title"><strong>Name:</strong> ${watch.name}</p>
                                <p class="card-text"><strong>Description:</strong> ${watch.desc}</p>
                                <p class="card-text"><strong>Price:</strong> ${watch.price}</p>
                                <a href="/product/${watch.id}" class="btn btn-primary btn-sm">View</a>
                                <a href="/edit/${watch.id}" class="btn btn-secondary btn-sm">Edit</a>
                                <a href="/delete/${watch.id}" class="btn btn-danger btn-sm">Delete</a>
                            </div>
                        </div>
                    </div>
                `;
                watchContainer.innerHTML += watchCard;
            });
        })
        .catch(error => console.error('Error:', error));
});


// ........ new 

document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");
    const toggleButton = document.querySelector(".navbar-toggler");

    toggleButton.addEventListener("click", () => {
        sidebar.classList.toggle("active");
    });
});



    // JavaScript function to update price range display
    function updatePriceRange() {
        var minPrice = document.getElementById("priceRangeMin").value;
        var maxPrice = document.getElementById("priceRangeMax").value;
        
        if (parseInt(minPrice) > parseInt(maxPrice)) {
            // Ensure min is always less than or equal to max
            document.getElementById("priceRangeMax").value = minPrice;
            maxPrice = minPrice;
        }
        
        document.getElementById("minPrice").textContent = minPrice;
        document.getElementById("maxPrice").textContent = maxPrice;
    }

    // Initialize with default values on load
    document.addEventListener("DOMContentLoaded", updatePriceRange);


//   filter 


    function toggleAll(allCheckbox) {
        const checkboxes = document.querySelectorAll('.brand-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = allCheckbox.checked;
        });
    }

    document.querySelectorAll('.brand-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const allCheckbox = document.getElementById('brandAll');
            const allChecked = [...document.querySelectorAll('.brand-checkbox')].every(cb => cb.checked);
            allCheckbox.checked = allChecked;
        });
    });

