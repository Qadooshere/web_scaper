from flask import Flask, render_template, request, redirect, url_for
from main import GoogleScraper, parse
from ExtractEmail import EmailScraper

app = Flask(__name__)
app.secret_key = 'Samaq'


@app.route('/', methods=['GET', 'POST'])
def index():
    languages = [
        {'code': 'en', 'name': 'English'},
        {'code': 'ar', 'name': 'Arabic'},
        {'code': 'ur', 'name': 'Urdu'},
        {'code': 'hi', 'name': 'Hindi'},
        {'code': 'fr', 'name': 'French'},
        {'code': 'de', 'name': 'German'},
        {'code': 'it', 'name': 'Italian'}
        # Add other languages as needed
    ]
    countries = [
        {'code': 'us', 'name': 'United States'},
        {'code': 'ae', 'name': 'United Arab Emirates'},
        {'code': 'uk', 'name': 'United Kingdom'},
        {'code': 'PK', 'name': 'Pakistan'},
        {'code': 'QA', 'name': 'Qatar'},
        {'code': 'SA', 'name': 'Saudi Arabia'},
        {'code': 'EG', 'name': 'Egypt'},
        {'code': 'JO', 'name': 'Jordan'},
        {'code': 'IN', 'name': 'India'}
        # Add other countries as needed
    ]
    if request.method == 'POST':
        query = request.form.get('query')
        selected_country = request.form.get('country')
        selected_language = request.form.get('language')

        # Initialize GoogleScraper with selected country and language
        scraper = GoogleScraper(country=selected_country, language=selected_language)
        extracted_links = scraper.run(query)
        return render_template('index.html', results=extracted_links, languages=languages, countries=countries)

    return render_template('index.html', languages=languages, countries=countries)


@app.route('/extract_emails', methods=['POST'])
def extract_emails():
    if request.method == 'POST':
        selected_links = request.form.getlist('selected_links')
        email_scraper = EmailScraper()
        extracted_emails = {}

        for link in selected_links:
            emails = email_scraper.extract_valid_emails_from_url(link)
            extracted_emails[link] = emails

        return render_template('email_results.html', extraction_results=extracted_emails)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
