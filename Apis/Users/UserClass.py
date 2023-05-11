from Utils.GeneralTools import run_query
import re
from jwt import decode
from decouple import config


class ValidateUser():

    def validate_email(data: str) -> str:
        email = data.lower()

        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(regex, email):
            return True
        return False

    def validate_new_email(data: str) -> str:

        email = run_query(
            "select email from users where active = 1 and email = '{}'".format(data), "get")

        if email:
            return True
        return False

    def validate_old_password(user, old_password):

        sql = "select password from users where user_id = {}".format(user)
        dato = run_query(sql, 'get')
        
        passw = decode(str(dato[0][0]).encode(), key=config("SECRET"), algorithms=["HS256"])
       
        if passw['key'] == old_password:
            return passw
        return False

    def validate_new_password(user, old_password, new_password):

        old_pw = ValidateUser.validate_old_password(user, old_password)        

        if old_pw['key'] == new_password:
            return False
        return True

    def validate_existence(user:int) -> int:

        sql = "select user_id, username from users where active = 1 and user_id = {}".format(
            user)
        exist = run_query(sql, 'get')

        if exist:
            return True
        return False

    def validate_username(username: str) -> str:

        sql = "select user_id, username, password from users where active = 1 and username = '{}'".format(
            username)
        exist = run_query(sql, 'get')

        if exist:
            return {
                "user_id": exist[0][0],
                "password": exist[0][2]
            }
        return False

    def password_lenght(password):

        if len(password) < 8 or len(password) > 16:
            return False
        return True


class validate_fields_input():

    def validate_created_user(data):

        fields = ("username", "password", "email", "name", "last_name","age", "phone", "document")
        missing_list = []

        for f in fields:
            try:
                if data[f] == "":
                    missing_list.append(f)

            except Exception as err:
                missing_list.append(str(err))

        if missing_list == []:
            return (True,)
        return (False, missing_list)

    def validate_update_user(data):

        fields = ("email", "name", "last_name", "age", "phone")
        missing_list = []

        for f in fields:
            try:
                if data[f] == "":
                    missing_list.append(f)

            except Exception as err:
                missing_list.append(str(err))

        if missing_list == []:
            return (True,)
        return (False, missing_list)
