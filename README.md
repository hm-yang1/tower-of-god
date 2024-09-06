# [Choice](https://tower-of-god-frontend.vercel.app/) - Product Recommendation Website (Backend)

## Features

### 1. Authentication
- Users can log in using a username/password or Google OAuth.

### 2. Product Search & Filtering
- Users can search for products with full-text search and fuzzy search.
- Products can be filtered by category, price, brand, and more.
- Additional features: sorting, autocomplete, and infinite scrolling.

### 3. Web Scrapers
- Web scrapers collect product data from review sites (e.g., [Rtings](https://www.rtings.com), [PCMag](https://www.pcmag.com), [Reddit](https://www.reddit.com)).
- Selenium is used for precise scraping.
- Found in scrapers folder

### 4. Product Recommendation Cards
- Summarized product cards with key details like name, rating, and image.
- Features wishlist and compare buttons.

### 5. Detailed Product Pages
- Detailed view includes summary of reviews, pros and cons
- Also contain analysis of Reddit comments about the product

### 6. Search History
- Logged-in users can view and manage their search history.
- Search results can be saved and accessed later.

### 7. Wishlist
- Users can save products to a wishlist and manage items.
- Similar products are recommended based on the wishlist.

### 8. Product Comparison
- Compare two products side-by-side, including pros, cons, and reviews.

### 9. AI Summarizer & Sentiment Analysis
- Use of Gemini API
- AI used to summarise reviews and perform sentiment analysis on Reddit comments

### 10. Miscellaneous Features
- Debounced search bars and smart overlay closing.
- Cron job to keep the backend online.

## Use
- This is the Internet, there are no rules.

### Django API
- [Live backend](https://tower-of-god.onrender.com/api/). Will shutdown under heavy traffic.
- Used DRF to implement a REST API
- The backend folder is the Django project. The api folder is the actual Django app

## Scrapper
- Selenium webdrivers that navigate thorugh review sites. Navigates through pre-determined path.
- Used Selenium to interact with web elements. Much slower than if used BeautifulSoup4.
- Some may longer work as websites change everyday. Will not fix.
