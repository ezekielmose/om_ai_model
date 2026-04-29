import requests


def check_instagram_username(username):

    url = f"https://www.instagram.com/{username}/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)

        html = response.text.lower()

        # ❌ Detect "page not found"
        if "sorry, this page isn't available" in html:
            return {"exists": False, "url": None}

        if "page not found" in html:
            return {"exists": False, "url": None}

        # ❌ Detect login wall (valid page)
        if "login" in html or "log in" in html:
            return {"exists": True, "url": url}

        # ✅ Detect real profile indicators
        if "profile picture" in html or "followers" in html:
            return {"exists": True, "url": url}

        # fallback
        return {"exists": False, "url": None}

    except Exception:
        return {"exists": False, "url": None}