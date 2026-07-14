import pytest
from app.utils import generate_short_key, calculate_expiration
from datetime import datetime, timezone, timedelta
import string

class TestGenerateShortKey:

    def test_returns_string(self):
        key = generate_short_key()
        assert isinstance(key, str)

    def test_default_length_is_six(self):
        key = generate_short_key()
        assert len(key) == 6

    def test_respects_custom_length(self):
        key = generate_short_key(length=10)
        assert len(key) == 10

    def test_only_urlsafe_characters(self):
        key = generate_short_key()
        allowed = string.digits + string.ascii_lowercase + string.ascii_uppercase + "-" + "_"
        allowed = set(allowed)
        assert set(key).issubset(allowed)


class TestCalculateExpiration:

    def test_returns_none_for_none_input(self):
        result = calculate_expiration(None)
        assert result == None

    def test_returns_datetime_for_positive_days(self):
        result = calculate_expiration(30)
        assert isinstance(result, datetime)
        expected = datetime.now(timezone.utc) + timedelta(days=30)
        assert expected - timedelta(seconds=5) < result < expected + timedelta(seconds=5)

    def test_behavior_for_negative_days(self):
        result = calculate_expiration(-5)
        assert result < datetime.now(timezone.utc)