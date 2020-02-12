#!/home/drrago/anaconda3/bin/python3.7m

import typing
import requests

from encryption import dec
from mail_utility import send_mail
from mysql_connection import MySQL


def check_task():
    """
    Check whether grades of a specific user have changed and send an email to the recipient list
    """
    mysql = MySQL()
    check_targets = mysql.query("SELECT * FROM course WHERE valid", ())

    for check_target in check_targets:
        # 0: ID 1: username 2: password 3: valid
        username = check_target[1]
        print("checking for %s" % username)

        mail_recipients = mysql.query("SELECT * FROM subscription WHERE course = ?", (check_target[0],))

        password = dec(check_target[2])
        data = {
            "username": username.lower(),
            "password": password
        }
        response = make_request(data).json()

        # validate response
        if (response.get("code") != 200):
            print("Error response: " + str(response.get("code")) + "\n invalidating account")
            mysql.query("UPDATE course SET valid = FALSE WHERE ID = ?", (check_target[0],))  # make entry invalid
            continue

        changed_modules = filter(lambda m: m.get("updated"), response.get("data").get("modules"))
        mail_message = "".join(
            map(lambda m: f'<li>{m.get("module_name")} ({m.get("module_no")}){get_grade_html(m)}</li>', changed_modules)
        )

        # will be empty if nothing has changed... hopefully
        if (mail_message):
            mail_message = f'<ul>{mail_message}</ul>'
            mail_message = mail_message.encode("ascii", "xmlcharrefreplace").decode("utf-8")
            print(mail_message)
            for recipient in mail_recipients:
                # 0: username 1: email 2: name 3: course
                send_mail(recipient[1], recipient[2], mail_message)
        print()

    mysql.close()


def get_grade_html(module: typing.Dict[str, any]) -> str:
    """
    Generate a list of the grades inside a module, if existing

    :param module: the module
    :return: the html list of the grade names
    """
    message = "".join(map(lambda g: f'<li>{g.get("name")}</li>', module.get("grades")))
    if (message):
        return f'<ul>{message}</ul>'
    return ""


def make_request(data: typing.Dict[str, str]) -> requests.Response:
    """
    Perform the get request to update the users data

    :param data: dict containing username and password as plain text
    :return: the GET-response
    """
    return requests.get(
        f'https://api.drrago.de/dualis/user/{data.get("username")}',
        headers={"Private-Token": data.get("password")}
    )


if __name__ == "__main__":
    check_task()
