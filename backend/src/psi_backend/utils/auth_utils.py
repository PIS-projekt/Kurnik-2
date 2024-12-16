import random


def get_current_user_id() -> (
    int
):  # TODO If we want user authentication, this should return the id of an authenticated user.
    """Mock function to simulate an authenticated user.

    Returns:
        int: ID of the currently logged user.
    """
    return random.randint(1000, 9999)
