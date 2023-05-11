from Utils.GeneralTools import response, run_query


class ValidateAuth():

    def validate_permission(username, module_id):

        sql = "select u.user_id, pm.module_id from users u inner join permissions_module pm on u.user_id = pm.user_id\
            where u.username ='{}' and pm.module_id = {} and pm.active = 1".format(username, module_id)

        user_id = run_query(sql, 'get')

        if user_id == []:
            return False
        return True

    def insert_permission(user_id: int, module_list, data):

        for module in module_list:

            verifi = run_query("select user_id from permissions_module where user_id = {} and module_id = {}".format(
                user_id, module), 'get')

            if verifi != []:
                pass
            else:
                run_query("insert into permissions_module(user_id, module_id, active, created_at) values({}, {}, 1, now())".format(
                    user_id, module), 'post')

        return response(200, "permission assigned successfully", data)
