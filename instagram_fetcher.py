import instaloader
import browser_cookie3


def get_loader():

    L = instaloader.Instaloader(
        download_videos=False,
        download_pictures=False,
        quiet=True
    )

    try:
        cookies = browser_cookie3.chrome()
        L.context._session.cookies.update(cookies)
        print("✅ Browser cookies loaded")
    except Exception as e:
        print("❌ Cookie load failed:", e)

    return L


def fetch_reels_from_handle(handle, limit=50):

    L = get_loader()

    profile = instaloader.Profile.from_username(L.context, handle.replace("@", ""))

    reels = []

    for post in profile.get_posts():

        if post.is_video:
            reels.append(f"https://www.instagram.com/reel/{post.shortcode}/")

        if len(reels) >= limit:
            break

    return reels