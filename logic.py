from book_data import BOOK_DATA


def get_book_data(title):
    return BOOK_DATA.get(title)


def calculate_average_rating(ratings):
    if len(ratings) == 0:
        return 0

    return sum(ratings) / len(ratings)


def is_top_rated(rating):
    return rating >= 9