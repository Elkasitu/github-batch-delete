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


def prompt_confirm_delete():
    while True:
        ans = input("Are you sure you want to delete these repos? (y/n) ")
        if ans:
            if ans[0].lower() == 'y':
                return True
            elif ans[0].lower() == 'n':
                return False

        print("%s is not a valid answer, type 'y' or 'n'" % ans)


def prompt_filter():
    return input("Enter a url-form filter: ")


def main():
    # Prompt user for credentials
    username, password = prompt_credentials()

    # Init, access login page
    driver = webdriver.Chrome()
    driver.get("http://www.github.com/login")

    # Login
    usr = driver.find_element_by_name("login")
    usr.clear()
    usr.send_keys(username)

    pwd = driver.find_element_by_name("password")
    pwd.clear()
    pwd.send_keys(password)
    pwd.send_keys(Keys.RETURN)

    query = prompt_filter()
    driver.get(
        "https://github.com/%s?%s" % (username, query)
    )

    repos = set()

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

    if len(repos) > 0:
        for repo in repos:
            print(repo)

        if prompt_confirm_delete():
            delete_repos(driver, username, password, repos)
    else:
        print("No repositories found, did you enter a good filter?")

    driver.quit()


def delete_repos(driver, username, password, repos):
    """
    Permanently deletes all the repos found in repo_list
    """
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


if __name__ == '__main__':
    main()
