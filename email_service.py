import os
import requests

BIRD_API_KEY = os.getenv("BIRD_API_KEY")


def send_email(to_email, subject, html):
    print("BIRD KEY EXISTS:", bool(BIRD_API_KEY))
    print(
    "BIRD KEY PREFIX:",
    BIRD_API_KEY[:7] if BIRD_API_KEY else "MISSING"
)


    url = "https://us1.platform.bird.com/v1/email/messages"

    headers = {
       "Authorization": f"Bearer {BIRD_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {
            "email": "onboarding@messagebird.dev",
            "name": "Bird"
        },
        "to": [to_email],
        "subject": subject,
        "html": html
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )

        print("BIRD STATUS:", response.status_code)
        print("BIRD RESPONSE:", response.text)

        response.raise_for_status()

        return True
    

    except requests.RequestException as e:
        print("BIRD EMAIL ERROR:", repr(e))
        return False
