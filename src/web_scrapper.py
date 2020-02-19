from selenium import webdriver
from time import sleep
import json

def save_relations_to_json(relations, file_path):
    json_obj = json.dumps(relations)
    f = open(file_path, "w")
    f.write(json_obj)
    f.close()

def load_relations_from_json(file_path):
    file = open(file_path)
    relations = json.load(file)
    file.close()
    return relations

# returns a dictionary
# where key is a unique friend from "root_friends"
#   and the value is a list of users that are friends of root and unique friend
def get_relations(username, password):
    driver = __get_root_profile(username, password)
    # delete password after use
    del password

    print("Collected data will be saved to default file: \"relations.json\"")
    print("Collecting root friends")
    root_friends = __get_user_friends(driver)
    print(str(len(root_friends)) + " users to scrapp")

    # open following pop-up
    driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()

    relations = {}
    for friend in root_friends:
        print("Collecting " + friend + " friends")
        # open friend profile
        driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(friend)).click()
        sleep(4)
        friend_friends = __get_user_friends(driver)
        # go back to root profile with following pop-up open
        driver.back()
        driver.back()
        driver.back()
        driver.back()
        driver.back()
        sleep(4)
        # transformed to list because of .json
        relations[friend] = list(root_friends.intersection(friend_friends))
        save_relations_to_json(relations, "relations.json")

    return relations

# returns the set of users that follow and are being followed
def __get_user_friends(driver):
    # open following pop-up
    driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
    following = set(__get_names(driver))

    # open followers pop-up
    driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
    followers = set(__get_names(driver))

    return following.intersection(followers)

# returns all usernames from current pop-up and closes it
def __get_names(driver):
    sleep(5)
    scroll_box = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
    # scroll while there are things to scroll to
    last_height, height = 0, 1
    count = 0
    while last_height != height:
        last_height = height
        sleep(2)
        height = driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
        # "count" exists just to prevent the *slow* collection
        #   of hundreds of thousands of usernames
        #   it can be remove if desired
        count += 1
        if count > 1000:
            break
    links = scroll_box.find_elements_by_tag_name('a')
    names = [name.text for name in links if name.text != '']

    # close button
    driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
    sleep(2)

    return names

# creates a webdriver goes to user profile and returns
def __get_root_profile(username, password):
    driver = webdriver.Firefox()
    driver.get("https://www.instagram.com/")
    sleep(2)
    # click "Log in" button
    driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
    sleep(2)
    # fill "username" input box
    driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
    # fill "password" input box
    driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
    # delete password after use
    del password
    # click "Log In" button
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    sleep(4)
    # click "Not Now" button from notifications pop-up
    driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    sleep(2)
    # go to profile
    driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(username)).click()
    sleep(2)

    return driver
