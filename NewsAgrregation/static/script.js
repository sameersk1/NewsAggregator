let selectedCategory = ''; // Variable to store the selected category
let searchQuery = ''; // Variable to store the search query

document.getElementById('search-button').addEventListener('click', searchArticles);
document.getElementById('apply-filter').addEventListener('click', applyDateFilter);
document.getElementById('remove-filter').addEventListener('click', removeDateFilter);
document.getElementById('all').addEventListener('click', () => selectCategory(''));
document.getElementById('politics').addEventListener('click', () => selectCategory('Politics'));
document.getElementById('crime').addEventListener('click', () => selectCategory('Crime'));
document.getElementById('sports').addEventListener('click', () => selectCategory('Sports'));

// Function to select a category
function selectCategory(category) {
    selectedCategory = category; // Update the selected category
    getArticles(selectedCategory); // Fetch articles for the selected category
}

// Fetch all articles or filter by category
function getArticles(category = '', query = '') {
    let url = '/articles?';

    // Include category if provided
    if (category) {
        url += `category=${encodeURIComponent(category)}&`;
    }

    // Include search query if provided
    if (query) {
        url += `q=${encodeURIComponent(query)}&`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched articles:', data); // Log the fetched articles
            displayArticles(data);
        })
        .catch(error => console.error('Error fetching articles:', error));
}

// Apply date filter
function applyDateFilter() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    let url = '/articles?';

    // Include selected category in the URL
    if (selectedCategory) {
        url += `category=${encodeURIComponent(selectedCategory)}&`;
    }

    // Add date filters
    if (startDate) {
        url += `start_date=${startDate}&`;
    }
    if (endDate) {
        url += `end_date=${endDate}&`;
    }

    // Include the search query if it exists
    if (searchQuery) {
        url += `q=${encodeURIComponent(searchQuery)}&`;
    }

    console.log('Fetching articles from URL:', url); // Debugging

    // Fetch the filtered articles
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Filtered articles:', data);
            displayArticles(data);
        })
        .catch(error => console.error('Error applying date filter:', error));
}

// Remove date filter but keep the category and the date inputs
function removeDateFilter() {
    // Keep the current date values, do not reset them
    getArticles(selectedCategory, searchQuery); // Fetch articles based on the current category and search query
}

// Search for articles based on query
function searchArticles() {
    const query = document.getElementById('search').value;
    searchQuery = query; // Store the search query for future reference
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    console.log('Searching for:', query); // Log the search query
    let url = `/search?q=${encodeURIComponent(query)}`;

    // Include selected category in the URL
    if (selectedCategory) {
        url += `&category=${encodeURIComponent(selectedCategory)}`;
    }

    // Add date filters if they exist
    if (startDate) {
        url += `&start_date=${encodeURIComponent(startDate)}`;
    }
    if (endDate) {
        url += `&end_date=${encodeURIComponent(endDate)}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Search results:', data); // Log search results
            displayArticles(data);
        })
        .catch(error => console.error('Error searching articles:', error));
}

// Display the list of articles
function displayArticles(articles) {
    const articlesDiv = document.getElementById('articles');
    articlesDiv.innerHTML = ''; // Clear previous articles

    if (articles.length > 0) {
        articles.forEach(article => {
            const articleElement = document.createElement('div');
            articleElement.classList.add('article');
            articleElement.innerHTML = `
                <h3><a href="${article.URL}" target="_blank">${article.Title}</a></h3>
                <p>${article.Summary || 'No summary available'}</p>
                <small><b>Source:</b> ${article.Source || 'Unknown'}</small>
                <small><b>Publication Date:</b> ${article['Publication Date'] || 'Unknown'}</small>
                <small><b>Category:</b> ${article.Category || 'General'}</small>
            `;
            articlesDiv.appendChild(articleElement);
        });
    } else {
        articlesDiv.innerHTML = '<p>No articles found</p>';
    }
}
