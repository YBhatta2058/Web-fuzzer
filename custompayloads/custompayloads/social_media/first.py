import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

def get_website_content(url):
    """
    Crawl the website and extract up to 500 words of paragraph content.
    """
    try:
        # Make a request to the website
        response = requests.get(url, timeout=10,verify=False)
        response.raise_for_status()  # Raise error for HTTP issues

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all paragraph content
        paragraphs = soup.find_all('p')
        content = []

        # Collect text from paragraphs up to 500 words
        word_count = 0
        for p in paragraphs:
            text = p.get_text(strip=True)
            words = text.split()
            word_count += len(words)
            if word_count <= 300:
                content.append(text)
            else:
                # Include only enough words to reach 500
                remaining_words = 500 - (word_count - len(words))
                content.append(" ".join(words[:remaining_words]))
                break

        return " ".join(content)  # Join all collected paragraphs into a single string
    except Exception as e:
        print(f"Error crawling website: {e}")
        return None

def classify_content_with_gemini(content, api_key="AIzaSyBYpNf7L0sPbuRkr7FlLu0p8ZigNljY5Io"):
    """
    Classify the website content using Gemini API.
    """
    try:
        # Configure Generative AI with the API key
        genai.configure(api_key=api_key)

        # Initialize the GenerativeModel for Gemini 1.5 Flash
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Prepare the prompt to classify the content
        prompt = f"portfolio, corporate, ecommerce, blogs, news, social_media, educational, government, entertainment, test_dummy. Based on the above mentioned list classify the following content into any one category. only give the classified category name as response. The content is: {content}"

        # Call the model to classify the content
        response = model.generate_content(prompt)

        # Return the classified category
        return response.text.strip()  # Strip whitespace or newline characters
    except Exception as e:
        print(f"Error classifying content: {e}")
        return None

# Example usage
url = "https://coursera.com"  # Replace with the website URL to classify
content = get_website_content(url)

if content:
    classification = classify_content_with_gemini(content)
    print(classification)
else:
    print("Failed to extract content from the website.")
