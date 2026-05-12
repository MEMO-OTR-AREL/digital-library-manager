def calculate_average_rating(ratings):

    if len(ratings) == 0:
        return 0

    return sum(ratings) / len(ratings)


def test_average_rating():

    ratings = [10, 8, 6]

    result = calculate_average_rating(ratings)

    assert result == 8