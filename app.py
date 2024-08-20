from flask import Flask, request, jsonify, render_template
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def open_browser_with_cookies(url, cookies):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch the browser
        context = browser.new_context()

        # Iterate over each cookie and set 'sameSite' to 'Lax' if it doesn't exist
        for cookie in cookies:
            if 'sameSite' not in cookie or cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
                cookie['sameSite'] = 'Lax'  # Default to 'Lax' if not provided or invalid
            context.add_cookies([cookie])

        page = context.new_page()
        page.goto(url)

        # Keep the browser open by running an event loop
        try:
            while True:
                # Keep the server running or use other mechanism to keep it open
                input("Press Enter to close the browser...\n")  # Wait for user input
        except KeyboardInterrupt:
            print("Browser closed.")
        finally:
            browser.close()  # Ensure the browser closes


@app.route('/open-browser', methods=['POST'])
def open_browser():
    data = request.json
    url = data.get('url', 'https://www.example.com/')
    cookies = data.get('cookies', [])
    open_browser_with_cookies(url, cookies)

    return jsonify({"message": "Browser opened with cookies!"})

if __name__ == '__main__':
    app.run(debug=True)
