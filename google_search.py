import requests


def get_instagram_from_serpapi(hotel_name, city, country=None):

    query = f'site:instagram.com "{hotel_name}" "{city}"'

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google",
        "q": query,
        "api_key": "c8e0fb2951ecb7f988a06e141ba0318c76749e8bf548e25468f3eba84ea242bc",
        "num": 5
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        items = data.get("organic_results", [])

        best_match = None
        best_score = 0

        hotel_name_lower = hotel_name.lower()

        for item in items:

            link = item.get("link", "").lower()
            title = item.get("title", "").lower()
            snippet = item.get("snippet", "").lower()

            # ❌ must be instagram
            if "instagram.com" not in link:
                continue

            # ❌ skip non-profile pages
            if any(x in link for x in ["/reel/", "/p/", "/tv/", "/stories/"]):
                continue

            score = 0

            # 🔥 matching rules
            if hotel_name_lower in title:
                score += 3

            if hotel_name_lower in snippet:
                score += 2

            # profile strength (short URL = likely profile)
            if link.count("/") <= 4:
                score += 2

            if "official" in title or "official" in snippet:
                score += 2

            if "hotel" in title:
                score += 1

            if score > best_score:
                best_score = score
                best_match = {
                    "instagram": link,
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "score": best_score
                }

        return best_match if best_match else {"instagram": None}

    except Exception as e:
        return {
            "instagram": None,
            "error": str(e)
        }