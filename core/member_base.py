import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path





class Member:
    member_database = "database/members.json"
    member_data = []
    try:
        if Path(member_database).exists():
            with open(member_database) as fs:
                member_data = json.loads(fs.read())
        else:
            print("No such data found!")
    except Exception as err:
        print(f"An error occurred as {err}")

    @classmethod
    def __update(cls):
        with open(cls.member_database, "w") as fs:
            fs.write(json.dumps(Member.member_data, indent=4))

    @classmethod
    def __unique_id(cls):
        while True:
            alpha = random.choices(string.ascii_letters, k=3)
            nums = random.choices(string.digits, k=8)

            id = alpha + nums
            random.shuffle(id)
            new_id = "MEM." + "".join(id)
            idcheck = [i for i in Member.member_data if i["Member-ID"] == new_id]
            if len(idcheck) > 0:
                continue
            return new_id

    @classmethod
    def __generatepass(cls):
        password = string.ascii_letters + string.digits + "@#$&*"
        return "".join(random.choices(password, k=8))

    @classmethod
    def autopassword(cls):
        return cls.__generatepass()

    @classmethod
    def update(cls):
        cls.__update()

    @classmethod
    def uniqueid(cls):
        return cls.__unique_id()

    @classmethod
    def usernamegenerate(cls, name):
        cleanname = name.lower().replace(" ", "")
        symbols = ["_", "-", "."]
        while True:
            namechars = random.choices(cleanname, k=random.randint(4, 6))
            nums = random.choices(string.digits, k=random.randint(2, 3))
            syms = random.choices(symbols, k=random.randint(1, 2))
            username = namechars + nums + syms
            random.shuffle(username)
            newusername = "".join(username)
            checkusername = [i for i in cls.member_data if i["Username"] == newusername]
            if len(checkusername) == 0:
                return newusername
