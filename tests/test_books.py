from logic import get_book_data, calculate_average_rating, is_top_rated

def test_get_book_data_existing_book():
    book = get_book_data("Crime and Punishment")

    assert book is not None
    assert book["author"] == "Fyodor Dostoevsky"
    assert book["category"] == "Classic"
    assert book["rating"] == 10


def test_get_book_data_unknown_book():
    book = get_book_data("Unknown Book")

    assert book is None


def test_calculate_average_rating():
    ratings = [10, 8, 6]

    result = calculate_average_rating(ratings)

    assert result == 8


def test_calculate_average_rating_empty_list():
    result = calculate_average_rating([])

    assert result == 0


def test_is_top_rated_true():
    assert is_top_rated(9) is True
    assert is_top_rated(10) is True


def test_is_top_rated_false():
    assert is_top_rated(8) is False