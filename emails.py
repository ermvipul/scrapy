import requests
import time

def solve_captcha(api_key, captcha_image_url):
    # API endpoint for 2Captcha
    api_url = "http://2captcha.com/in.php"

    # Send the CAPTCHA image URL to 2Captcha for solving
    response = requests.post(api_url, data={
        'key': api_key,
        'method': 'download',
        'file': captcha_image_url,
    })

    # Parse the response to get the CAPTCHA ID
    captcha_id = response.text.split('|')[1]

    # Check if the CAPTCHA has been solved every 5 seconds
    while True:
        response = requests.get('http://2captcha.com/res.php', params={
            'key': api_key,
            'action': 'get',
            'id': captcha_id,
        })
        if 'OK' in response.text:
            # If solved, return the CAPTCHA solution
            return response.text.split('|')[1]
        elif 'CAPCHA_NOT_READY' in response.text:
            # If not solved yet, wait 5 seconds and check again
            time.sleep(5)
        else:
            # Handle other error cases
            return None

# Example usage
# Example usage
api_key = 'bc290f0226a8b82f20f542451b7ad352'
captcha_image_url = 'https://www.zoominfo.com/companies-search/location-usa--florida-industry-construction?pageNum=1'
captcha_solution = solve_captcha(api_key, captcha_image_url)
print("CAPTCHA Solution:", captcha_solution)
