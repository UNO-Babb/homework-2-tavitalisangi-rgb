#BusSchedule.py
#Name:
#Date:
#Assignment:

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    content = driver.find_element(By.XPATH, "/html/body").text
    driver.quit()
    return content


def loadTestPage():
    with open("testPage.txt", 'r') as page:
        contents = page.read()
    return contents


def getHours(time):
    return datetime.datetime.strptime(time, "%I:%M %p").hour


def getminutes(time):
    return datetime.datetime.strptime(time, "%I:%M %p").minute


def isLater(time1, time2):
    return time1 > time2


def minutesUntil(target, current):
    diff = (target - current).total_seconds() / 60
    if diff < 0:
        diff += 24 * 60
    return round(diff)


def findTimes(content):
    words = content.split()
    times = []
    for w in words:
        w = w.strip()
        if ":" in w and ("AM" in w or "PM" in w):
            if w[-2:] in ("AM", "PM") and w[-3] != " ":
                w = w[:-2] + " " + w[-2:]
            times.append(w)
    return times




def Nextbus(content):
    times = findTimes(content)
    if not times:
        print("No times found on this page.")
        return None, None

    now = datetime.datetime.now() - datetime.timedelta(hours=5)
    print("Current time:", now.strftime("%I:%M %p"))

    bustimes = []
    for t in times:
        bustime = datetime.datetime.strptime(t, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        bustimes.append(bustime)

    upcoming = [bt for bt in bustimes if isLater(bt, now)]

    if len(upcoming) < 2:
        print("Fewer than two future bus times found.")
        return None, None

    nextbus = upcoming[0]
    followingbus = upcoming[1]

    minsnext = minutesUntil(nextbus, now)
    minsfollow = minutesUntil(followingbus, now)

    return minsnext, minsfollow


def main():
    direction = "West"
    routenumber = "00"
    stopcode = "6023"

    #url = f"https://myride.ometro.com/Schedule?stopCode={stopcode}&routeNumber={routenumber}&directionName={direction}"
    #c1 = loadURL(url)
    c1 = loadTestPage()  # for testing instead of live site

    print("Route", routenumber ,"- Direction", direction,".")
    minsnext, minsfollow = Nextbus(c1)

    if minsnext is not None and minsfollow is not None:
        print("The next bus will arrive in", minsnext ,"minutes.")
        print("The following bus will arrive in", minsfollow ,"minutes.")
    else:
        print("Could not determine upcoming bus times.")



if __name__ == "__main__":
    main()