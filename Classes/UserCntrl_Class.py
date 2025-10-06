from Classes.User_Class import User

class UserCntrl(User):

    def login(self, email, password):
        """
        Verify if the email and password match a record in the users table.
        Returns user data if successful, False if failed.
        """
        users = self._view_users()  # fetch all users
        if not users:
            return False

        for user in users:
            # Compare with DB column names
            if user['email'] == email and user['password'] == password:
                return user  # login successful
        return False  # login failed
