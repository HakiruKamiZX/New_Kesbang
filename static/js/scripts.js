// Function to create a news item element
function createNewsItem(news) {
    return `
    <div class="news-item">
        <div class="news-image" style="background-image: url('${news.imageUrl}');"></div>
        <div class="news-content">
            <h2>${news.title}</h2>
            <div class="meta">
                <span class="date">${news.date} | ${news.author}</span>
                <span class="category">${news.category}</span>
            </div>
            <p class="description">${news.description}</p>
            <a href="${news.link}" class="read-more">Read more</a>
        </div>
    </div>`;
}

function loadNews() {
    fetch('/api/news')
        .then(response => response.json())
        .then(data => {
            // Sort the data by date in descending order
            data.sort((a, b) => new Date(b.date) - new Date(a.date));

            // Slice the array to get the top 5 most recent articles
            const topFiveArticles = data.slice(0, 5);

            const articlesDiv = document.getElementById('news-articles');
            articlesDiv.innerHTML = ''; // Clear existing content

            topFiveArticles.forEach(article => {
                articlesDiv.innerHTML += createNewsItem({
                    imageUrl: article.image,
                    title: article.title,
                    date: article.date,
                    author: article.author,
                    category: article.category,
                    description: article.content,
                    link: `/article/${article._id}`
                });
            });
        })
        .catch(error => console.error('Error fetching news:', error));
}

// Load news when the page is loaded
window.onload = loadNews;

// Intersection Observer for fade-in/fade-out effect
function handleSlideIn(entries) {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        } else {
            entry.target.classList.remove('visible');
        }
    });
}

// Create an Intersection Observer
const slideObserver = new IntersectionObserver(handleSlideIn, {
    threshold: 0.1 // Adjust threshold as needed
});

// Select elements to observe
const slideElements = document.querySelectorAll('.slide-in');
slideElements.forEach((el) => slideObserver.observe(el));

// Load news when the page is loaded
window.onload = loadNews;
