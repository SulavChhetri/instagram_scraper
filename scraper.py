"""
    This module is used to scrape the instagram data using a playwright bot
"""
import os
import re
import time
import json
from pathlib import Path
from random import uniform
from playwright_stealth import stealth
from playwright.sync_api import sync_playwright


files_path = os.path.join(Path(__file__).parent, "files", "config.json")

about_url = 'https://www.instagram.com/api/v1/users/web_profile_info/?username=sulavthapachhetri'
comments = "https://www.instagram.com/api/v1/media/3101263999732594425/comments/?can_support_threading=true&permalink_enabled=false"


def sleep_random_time(low, high):
    """
        This function is used to sleep the program for a random time between
        the interval low and high
    """
    return time.sleep(uniform(low, high))


def _get_response_body(response, final_dict):
    regex = r'/api/v1/[.]*'
    pattern = re.compile(regex)
    if bool(re.search(pattern, response.url)):
        pass


def login(username, password, user_agent, viewport_size):
    """
        This function takes username and password to login using playwright
        It uses user_agent and viewport size that are unique to each account
    """
    cookie_dict = {}
    cookies = None

    response_dict = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': viewport_size[0],
                      'height': viewport_size[1]},
            user_agent=user_agent
        )
        stealth.stealth_sync(context)
        _cookie = cookie_dict.get(username, None)
        if _cookie:
            print("Cookies added!!")
            context.add_cookies(_cookie)

        page = context.new_page()
        sleep_random_time(1,3)
        response = page.goto("https://www.instagram.com/")
        sleep_random_time(1,4)
        page.get_by_role("textbox", name="username").type(username)
        sleep_random_time(1,2)
        page.get_by_role("textbox", name="password").type(password)
        sleep_random_time(1,2)
        keyboard = page.keyboard
        keyboard.press('Enter')
        sleep_random_time(5,10)
        page.on(
            "response", lambda response: _get_response_body(
                response, response_dict)
        )

        cookie_dict[username] = context.cookies()

        page.close()
        context.close()

        browser.close()


if __name__ == "__main__":
    with open(files_path, "r", encoding="utf-8") as file:
        user_files = json.load(file)
    USERNAME = 'harithapaparajuli'
    PASSWORD, USER_AGENT, VIEWPORT_SIZE = user_files[USERNAME]

    login(USERNAME, PASSWORD, USER_AGENT, VIEWPORT_SIZE)
