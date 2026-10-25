import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path




class Admin:
    admin_database = "database/admins.json"
    admin_data = []
    try:
        if Path(admin_database).exists():
            with open(admin_database) as fs:
                admin_data = json.loads(fs.read())
        else:
            print("No such data found!")
    except Exception as err:
        print(f"An error occurred as {err}")

    @classmethod
    def update(cls):
        with open(cls.admin_database, "w") as fs:
            fs.write(json.dumps(Admin.admin_data, indent=4))

    @classmethod
    def unique_id(cls):
        while True:
            alpha = random.choices(string.ascii_letters, k=3)
            nums = random.choices(string.digits, k=10)

            id = alpha + nums
            random.shuffle(id)
            new_id = "ADMIN." + "".join(id)
            idcheck = [i for i in Admin.admin_data if i["Amin-ID"] == new_id]
            if len(idcheck) > 0:
                continue
            return new_id
        