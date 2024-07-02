from FoodyAuth.model import User


def Search_In_Users(option: str, data: str) -> User:
    """
        this function take a search option and search Data and
        search in users by base on option that passed
    :param option:
    :param data:
    :return:
    """
    match option:
        case "NationalCode":
            return User.query.filter(User.NationalCode == data).all() or None

        case "PhoneNumber":
            return User.query.filter(User.PhoneNumber == data).all() or None

        case "EmployeeCode":
            return User.query.filter(User.EmployeeCode == data).all() or None

        case _:
            return None
