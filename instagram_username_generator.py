def generate_usernames(hotel_name, city=None):

    base = hotel_name.lower()

    clean = "".join(c for c in base if c.isalnum() or c == " ")
    clean = clean.replace(" ", "")

    usernames = []

    # 🔥 CORE (MOST IMPORTANT FIRST)
    usernames.append(clean)

    # slight variations
    usernames.append(clean + "hotel")
    usernames.append(clean + "official")

    usernames.append(clean + "_hotel")
    usernames.append(clean + "_official")

    # with city (LOW PRIORITY)
    if city:
        city_clean = city.lower().replace(" ", "")
        usernames.append(clean + city_clean)
        usernames.append(clean + "_" + city_clean)

    return list(set(usernames))