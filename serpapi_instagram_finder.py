import requests
import os


def normalize(text):
    return text.lower().replace(" ", "")


def get_instagram_from_serpapi(hotel_name, city, country=None):

    # 🔥 Better flexible query (less strict = better results)
    query = f'"{hotel_name}" instagram {city}'

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google",
        "q": query,
        # ✅ use environment variable (safer)
        "api_key": os.getenv("SERPAPI_API_KEY", "YOUR_SERPAPI_API_KEY"),
        "num": 10
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        items = data.get("organic_results", [])

        if not items:
            return {
                "instagram": None,
                "reason": "No results from SerpAPI"
            }

        best_match = None
        best_score = 0

        hotel_norm = normalize(hotel_name)

        for item in items:

            link = item.get("link", "")
            title = item.get("title", "")
            snippet = item.get("snippet", "")

            if not link:
                continue

            link_clean = link.split("?")[0].lower()

            # ❌ must be instagram
            if "instagram.com" not in link_clean:
                continue

            # ❌ skip posts/reels/stories
            if any(x in link_clean for x in ["/reel/", "/p/", "/tv/", "/stories/"]):
                continue

            score = 0

            title_norm = normalize(title)
            snippet_norm = normalize(snippet)
            hotel_words = hotel_norm.split()

            # =========================
            # 🔥 LIGHTWEIGHT MATCHING
            # =========================

            # full match
            if hotel_norm in title_norm:
                score += 3

            if hotel_norm in snippet_norm:
                score += 2

            # word-level fuzzy match
            for word in hotel_words:
                if word in title_norm:
                    score += 1
                if word in snippet_norm:
                    score += 1

            # instagram profile boost
            if "/p/" not in link_clean and "/reel/" not in link_clean:
                score += 1

            # official signal
            if "official" in title.lower() or "official" in snippet.lower():
                score += 1

            # hotel keyword
            if "hotel" in title.lower():
                score += 1

            # profile-like URL
            if link_clean.count("/") <= 4:
                score += 1

            # =========================
            # BEST MATCH SELECTION
            # =========================
            if score > best_score:
                best_score = score
                best_match = {
                    "instagram": link_clean,
                    "title": title,
                    "snippet": snippet,
                    "score": best_score
                }

        # =========================
        # LOWERED THRESHOLD (IMPORTANT)
        # =========================
        if best_match and best_score >= 1:
            return best_match

        return {
            "instagram": None,
            "reason": "No usable match found"
        }

    except Exception as e:
        return {
            "instagram": None,
            "error": str(e)
        }