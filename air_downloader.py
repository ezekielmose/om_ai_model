from playwright.sync_api import sync_playwright
import os

def download_air_video(page_url, save_path):
    os.makedirs(save_path, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        video_url = None

        def capture_response(response):
            nonlocal video_url
            url = response.url

            if ".mp4" in url or "video" in response.headers.get("content-type", ""):
                if response.status == 200:
                    video_url = url

        page.on("response", capture_response)

        # Open Air page
        page.goto(page_url, wait_until="networkidle")

        # Try clicking download button
        try:
            page.click("text=Download")
        except:
            pass

        # wait for network to settle
        page.wait_for_timeout(8000)

        if not video_url:
            browser.close()
            return None

        # Download actual file
        response = context.request.get(video_url)
        file_name = video_url.split("?")[0].split("/")[-1]

        full_path = os.path.join(save_path, file_name)

        with open(full_path, "wb") as f:
            f.write(response.body())

        browser.close()
        return full_path