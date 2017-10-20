#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def prompt_credentials():
    username = input("Username: ")
    password = getpass.getpass()

    return username, password


def main():
    # TODO: Ask for filter or list of repo names to delete
    # Init, access login page
    driver = webdriver.Chrome()
    driver.get("http://www.github.com/login")

    username, password = prompt_credentials()

    # Login
    usr = driver.find_element_by_name("login")
    usr.clear()
    usr.send_keys(username)

    pwd = driver.find_element_by_name("password")
    pwd.clear()
    pwd.send_keys(password)
    pwd.send_keys(Keys.RETURN)

    # Find to-delete repos
    # TODO: Generalize
    driver.get(
        "https://github.com/%s?tab=repositories&q=cb-gh&type=fork" % username
    )

    repos = set()

    # TODO: Atomize code

    while True:
        p = driver.find_elements_by_xpath(
            "//a[@itemprop='name codeRepository']"
        )

        for elem in p:
            repos.add(elem.text)

        try:
            next = driver.find_element_by_xpath("//a[@class='next_page']")
            next.click()
        except Exception:
            break

    # TODO: Display the list of repos to be deleted and ask the user for
    # confirmation before proceeding

    i = 1
    for repo in list(repos):
        driver.get("https://github.com/%s/%s/settings" % (username, repo))
        delete = driver.find_element_by_xpath(
            "//button[text()='Delete this repository']"
        )
        delete.click()

        # The verify modal is created on the fly, so we need to hack shit up
        # in order to inject the repo's name into the input box
        action = ActionChains(driver)
        action.send_keys(repo + Keys.RETURN)
        action.perform()

        try:
            pwd = driver.find_element_by_name("sudo_password")
            pwd.send_keys(password)
            pwd.send_keys(Keys.RETURN)
        except Exception:
            pass

        max = len(repos)
        print("Repository %s successfully deleted! (%d/%d)" % (repo, i, max))
        i += 1

    driver.quit()


if __name__ == '__main__':
    main()
