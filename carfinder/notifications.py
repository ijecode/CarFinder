import winotify
import urllib
import http.client
import webbrowser

def notify(notificationsParameters, newCars, db):
    if notificationsParameters['pushover']:
        pushoverNotify(notificationsParameters, newCars, db)
    if notificationsParameters['windows']:
        windowsNotify(newCars, db)

def windowsNotify(newCars, db):
    for car in newCars:
        print('notifying')
        #toast = winotify.Notification(app_id="windows app",
                     #title="Winotify Test Toast",
                     #msg="New Notification!")
        #toast.add_actions(label='Open website', launch='%(url)s' % db[car])

        #toast.show()

        toast = winotify.Notification(app_id='windows app', title='New car located', msg='New Car Located on %(site)s: %(make)s, %(price)s' % db[car],
                     icon=r"c:\path\to\icon.png")

        #toast.show()

def pushoverNotify(notificationsParameters, newCars, db):
    for car in newCars:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": notificationsParameters['pushover']['apiKey'],
            "user": notificationsParameters['pushover']['userKey'],
            "message": "New Car Located on %(site)s: %(make)s, %(price)s" % db[car],
            "url" : "%(url)s" % db[car]
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

def open_url(url):
    try: 
        webbrowser.open_new(url)
    except: 
        print('Failed to open URL. Unsupported variable type.')
