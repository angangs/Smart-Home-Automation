# import RPi.GPIO as GPIO
import os
import web
from web import form
# from homeoperations import Home
import logging
# import sysemail
import base64

port = 8080
relay1 = 7
relay2 = 6
relay3 = 5
relay4 = 4
relay5 = 3
relay6 = 2
relay7 = 1
relay8 = 0
in1 = 4
in2 = 17
in3 = 27
in4 = 23
in5 = 22
in6 = 24
in7 = 11
in8 = 7
in9 = 8
in10 = 9
in11 = 25
in12 = 10
out1 = 18
inputlist = [in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12]
outputlist = [out1]
relaylist = [relay1, relay2, relay3, relay4, relay5, relay6, relay7, relay8]
# myhome = Home(inputlist, outputlist, relaylist, port)
# io = myhome.initializerelays()
# pwm = myhome.setpwm(out1)
dinlist = []

logging.getLogger("web").setLevel(logging.WARNING)
urls = ('/', 'login',
        '/changepass','changepass',
        '/logout', 'logout',
        '/loggedinout', 'loggedinout',
        '/index', 'index',
        '/readlastvo', 'readlastvo',
        '/statusdigitalinput', 'statusdigitalinput',
        '/statusanaloginput', 'statusanaloginput',
        '/statusrelay1', 'statusrelay1',
        '/statusrelay2', 'statusrelay2',
        '/statusrelay3', 'statusrelay3',
        '/statusrelay4', 'statusrelay4',
        '/statusrelay5', 'statusrelay5',
        '/statusrelay6', 'statusrelay6',
        '/statusrelay7', 'statusrelay7',
        '/statusrelay8', 'statusrelay8',
        '/changerelay1', 'changerelay1',
        '/changerelay2', 'changerelay2',
        '/changerelay3', 'changerelay3',
        '/changerelay4', 'changerelay4',
        '/changerelay5', 'changerelay5',
        '/changerelay6', 'changerelay6',
        '/changerelay7', 'changerelay7',
        '/changerelay8', 'changerelay8',

        '/images/(.*)', 'images')

web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'logged_in': False})
render = web.template.render('./templates/')

def readpassword():
    f = open('pass.txt', 'rb')
    st = str(f.readline())
    f.close()
    return base64.b64decode(st)

def updatepass(newpass):
    f = open('pass.txt', 'wb')
    f.write(base64.b64encode(newpass))
    f.close()

def readallowedusername():
    f = open('users.txt', 'rb')
    userlist = []
    for word in f.read().split():
        userlist.append(word)
    f.close()
    return userlist

def getinfo():
    # return myhome, io, relaylist
    pass

# validators Login
username_required = form.Validator("Username not provided", bool)
password_required = form.Validator("Password not provided", bool)
oldpassword_required = form.Validator("Wrong Password", lambda i: str(i.oldpass)==readpassword())
password_length = form.Validator("Password length should be minimum 7 characters", lambda p: p is None or len(p) >= 7)
login_details_required = form.Validator("Please Enter Login Details", lambda f: f["username"] or f["password"])
valid_credentials = form.Validator("Invalid username or password", lambda i: str(i.password) == readpassword() and
                                                                             str(i.username) in readallowedusername())
login_form = form.Form(
    form.Textbox('username', username_required, description=''),
    form.Password('password', password_required, password_length, description=''),
    form.Button('Login'),
    validators=[login_details_required, valid_credentials, ],
)

changepass_form = form.Form(
    form.Password('oldpass', description=''),
    form.Password('newpass', password_required, password_length, description=''),
    form.Button('Update'),
    validators=[oldpassword_required,],
)

# validators Index
analoginput_required = form.Validator("Invalid input, range must be between 0-10",
                                  lambda i: float(i)>=0 and float(i)<=10)

analogoutput = form.Form(
    form.Dropdown('AO', ['0V', '1V', '2V',
                         '3V', '4V', '5V',
                         '6V', '7V', '8V',
                         '9V', '10V'], description="Output Voltage: "),
    form.Button('Submit')
)

# class for images
class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"}

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

class loggedinout:
    def POST(self):
        if session.get('logged_in'):
            return True
        else:
            return False

class readlastvo:
    def POST(self):
        f = open('status.txt', 'rb')
        st = str(f.readline())
        f.close()
        return st

class statusdigitalinput:
    def POST(self):
        dinlistnew = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
        #
        # if dinlistnew[10] == 1 and dinlist[10] == 0:
        #     dinlist[10] = 1
        #
        # if dinlistnew[10] == 0 and dinlist[10] == 1:
        #     dinlist[10] = 0
        #     sysemail.main(11,"aaggelidakis@gmail.com")
        #     sysemail.main(11,"vangelidakis@hotmail.com")
        #
        # if dinlistnew[11] == 1 and dinlist[11] == 0:
        #     dinlist[11] = 1
        #
        # if dinlistnew[11] == 0 and dinlist[11] == 1:
        #     dinlist[11] = 0
        #     sysemail.main(12, "aaggelidakis@gmail.com")
        #     sysemail.main(12, "vangelidakis@hotmail.com")
        #
        return dinlistnew
        pass

class statusanaloginput:
    def POST(self):
        analoglist = [5,0]
        # analoglist.append(str(myhome.readanaloginput(0)))
        # analoglist.append(str(myhome.readanaloginput(1)))

        return analoglist

class statusrelay1:
    def POST(self):
        # return myhome.readrelay(io,7)
        return True

class statusrelay2:
    def POST(self):
        # return myhome.readrelay(io,6)
        return False

class statusrelay3:
    def POST(self):
        # return myhome.readrelay(io,5)
        return False

class statusrelay4:
    def POST(self):
        # return myhome.readrelay(io,4)
        return False

class statusrelay5:
    def POST(self):
        # return myhome.readrelay(io,3)
        pass

class statusrelay6:
    def POST(self):
        # return myhome.readrelay(io,2)
        return False

class statusrelay7:
    def POST(self):
        # return myhome.readrelay(io,1)
        return False

class statusrelay8:
    def POST(self):
        # return myhome.readrelay(io,0)
        return True

class changerelay1:
    def POST(self):
        # if not myhome.readrelay(io,7):
        #     myhome.turnrelayon(io,7)
        # else:
        #     myhome.turnrelayoff(io, 7)
        pass

class changerelay2:
    def POST(self):
        # if not myhome.readrelay(io, 6):
        #     myhome.turnrelayon(io, 6)
        # else:
        #     myhome.turnrelayoff(io, 6)
        pass

class changerelay3:
    def POST(self):
        # if not myhome.readrelay(io, 5):
        #     myhome.turnrelayon(io, 5)
        # else:
        #     myhome.turnrelayoff(io, 5)
        pass

class changerelay4:
    def POST(self):
        # if not myhome.readrelay(io, 4):
        #     myhome.turnrelayon(io, 4)
        # else:
        #     myhome.turnrelayoff(io, 4)
        pass

class changerelay5:
    def POST(self):
        # if not myhome.readrelay(io, 3):
        #     myhome.turnrelayon(io, 3)
        # else:
        #     myhome.turnrelayoff(io, 3)
        pass

class changerelay6:
    def POST(self):
        # if not myhome.readrelay(io, 2):
        #     myhome.turnrelayon(io, 2)
        # else:
        #     myhome.turnrelayoff(io, 2)
        pass

class changerelay7:
    def POST(self):
        # if not myhome.readrelay(io, 1):
        #     myhome.turnrelayon(io, 1)
        # else:
        #     myhome.turnrelayoff(io, 1)
        pass

class changerelay8:
    def POST(self):
        # if not myhome.readrelay(io, 0):
        #     myhome.turnrelayon(io, 0)
        # else:
        #     myhome.turnrelayoff(io, 0)
        pass

# class for login
class login(object):
    def GET(self):
        if session.get('logged_in') == False:
            f = login_form()
            return render.login(f)
        else:
            raise web.seeother('/index')

    def POST(self):
        # Validation
        f = login_form()
        if not f.validates():
            return render.login(f)
        else:
            session.logged_in = True
            raise web.seeother('/index')

# class for logout
class logout:
    def GET(self):
        session.logged_in = False
        session.kill()
        raise web.seeother('/')

# class for index
class index(object):
    def GET(self):
        if session.get('logged_in') == True:
            return render.index(analogoutput)
        else:
            raise web.seeother('/')

    def POST(self):
        i = web.input(form_action='foo1')
        if session.get('logged_in') == False:
            raise web.seeother('/')
        else:
            analogout = analogoutput()
            if analogout.validates():
                outvolt = str(i.AO).replace('V','')
                f = open('status.txt', 'wb')
                f.write(outvolt)
                f.close()
                return render.index(analogout)
            else:
                raise web.seeother('/index')

class changepass(object):
    def GET(self):
        print "Changepass GET, session.logged_in: "+str(session.get('logged_in'))
        if session.get('logged_in') == False:
            raise web.seeother('/')
        else:
            changepwd = changepass_form()
            return render.changepass(changepwd)

    def POST(self):
        i = web.input(form_action='foo2')
        changepwd = changepass_form()
        if session.get('logged_in') == False:
                raise web.seeother('/changepass')
        else:
            if changepwd.validates():
                updatepass(i.newpass)
                return render.index(analogoutput)
            else:
                return render.changepass(changepwd)

if __name__ == "__main__":
    # myhome.turnrelayoff(io, relay1)
    # myhome.turnrelayoff(io, relay2)
    # myhome.turnrelayoff(io, relay3)
    # myhome.turnrelayoff(io, relay4)
    # myhome.turnrelayoff(io, relay5)
    # myhome.turnrelayoff(io, relay6)
    # myhome.turnrelayoff(io, relay7)
    # myhome.turnrelayoff(io, relay8)
    # myhome.changepwm(0, pwm)
    # sysemail.main(0, "aaggelidakis@gmail.com")
    # sysemail.main(0, "vangelidakis@hotmail.com")
    # dinlist = myhome.readdigitalinput()
    app.run()