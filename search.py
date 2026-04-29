import requests


def get_instagram_from_google(hotel_name, city, country):

    # ===============================
    # 🔍 PRIMARY SEARCH (STRICT)
    # ===============================
    query = f"{hotel_name} {city} {country} site:instagram.com"

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": query,
        "key": "YOUR_GOOGLE_API_KEY",
        "cx": "YOUR_SEARCH_ENGINE_ID",
        "num": 5
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        result = extract_instagram(data)

        if result:
            return result

        # ===============================
        # 🔄 FALLBACK SEARCH (LOOSER)
        # ===============================
        fallback_query = f"{hotel_name} {city} {country} Instagram"

        params["q"] = fallback_query

        response = requests.get(url, params=params)
        data = response.json()

        result = extract_instagram(data)

        if result:
            return result

        return {"instagram": None}

    except Exception as e:
        return {
            "instagram": None,
            "error": str(e)
        }


# ===============================
# 🧠 CLEAN EXTRACTION LOGIC
# ===============================
def extract_instagram(data):

    items = data.get("items", [])

    for item in items:

        link = item.get("link", "").lower()

        # must be instagram
        if "instagram.com" not in link:
            continue

        # ❌ skip irrelevant IG pages
        if "/reel/" in link:
            continue

        if "/p/" in link:
            continue

        if "explore" in link:
            continue

        # ✅ likely hotel page
        return {
            "instagram": item.get("link", ""),
            "title": item.get("title", ""),
            "snippet": item.get("snippet", "")
        }

    return None