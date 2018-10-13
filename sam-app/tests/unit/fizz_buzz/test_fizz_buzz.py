import pytest
from fizz_buzz.fizz_buzz import FizzBuzz


class TestFizzBuzz(object):
    def test_3ならばFizzを返す(self):
        assert FizzBuzz.generate(3) == 'Fizz'   

    def test_6ならばFizzを返す(self):
        assert FizzBuzz.generate(6) == 'Fizz'

    def test_30ならばFizzを返す(self):
        assert FizzBuzz.generate(30) == 'Fizz'
