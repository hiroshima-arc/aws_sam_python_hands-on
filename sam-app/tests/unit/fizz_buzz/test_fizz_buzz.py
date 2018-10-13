import pytest
from fizz_buzz.fizz_buzz import FizzBuzz


class TestFizzBuzz(object):
    def test_3ならばFizzを返す(self):
        assert FizzBuzz.generate(3) == 'Fizz'

    def test_6ならばFizzを返す(self):
        assert FizzBuzz.generate(6) == 'Fizz'

    def test_5ならばBuzzを返す(self):
        assert FizzBuzz.generate(5) == 'Buzz'

    def test_10ならばBuzzを返す(self):
        assert FizzBuzz.generate(10) == 'Buzz'

    def test_50ならばBuzzを返す(self):
        assert FizzBuzz.generate(50) == 'Buzz'

    def test_15ならばFizzBuzzを返す(self):
        assert FizzBuzz.generate(15) == 'FizzBuzz'

    def test_30ならばFizzBuzzを返す(self):
        assert FizzBuzz.generate(30) == 'FizzBuzz'

    def test_1ならば1を返す(self):
        assert FizzBuzz.generate(1) == 1

    def test_101ならば101を返す(self):
        assert FizzBuzz.generate(101) == 101
