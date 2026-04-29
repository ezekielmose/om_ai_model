import instaloader


def get_reels_from_profile(username, max_reels=12):

    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_comments=False,
        save_metadata=False
    )

    # 🔥 IMPORTANT FIX: LOGIN REQUIRED
    try:
        L.load_session_from_file("your_instagram_username")  # optional but best
    except:
        pass

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        reels = []

        for post in profile.get_posts():

            if post.is_video:

                reels.append({
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "caption": post.caption or "",
                    "likes": post.likes,
                    "views": post.video_view_count
                })

            if len(reels) >= max_reels:
                break

        return {
            "success": True,
            "reels": reels
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }