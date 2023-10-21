import data.users as usrs


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