import pickle
from selenium import webdriver
import time


def save_instagram_session():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # 🔥 keeps browser open

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.instagram.com/accounts/login/")

    print("\n==============================")
    print("👉 LOGIN IN THE OPEN BROWSER")
    print("👉 DO NOT CLOSE IT")
    print("==============================\n")

    # 🔥 HARD WAIT LOOP (prevents script exit)
    while True:
        user_input = input("Type 'done' after login is complete: ").strip().lower()

        if user_input == "done":
            break
        else:
            print("Waiting... type 'done' when finished login")

    time.sleep(3)

    # Save cookies AFTER login
    pickle.dump(driver.get_cookies(), open("instagram_cookies.pkl", "wb"))

    print("✅ Session saved successfully!")

    # IMPORTANT: do NOT force close immediately
    print("You can now close the browser manually.")