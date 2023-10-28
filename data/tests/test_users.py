import data.users as usrs


"""
    Ensure:
        - get_users() returns a dict with at least 1 user
        - each user key, or ID, is an int
        - each user is a dict with a name member
        - each user name is an alphabetical str with at least two letters
"""
def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for key in users:
        assert isinstance(key, int)
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.NAME in user
        user_name = user[usrs.NAME]
        assert isinstance(user_name, str)
        assert user_name.isalpha()
        assert len(user_name) >= usrs.MIN_USER_NAME_LEN