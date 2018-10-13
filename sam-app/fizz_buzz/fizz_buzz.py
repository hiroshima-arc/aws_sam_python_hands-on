class FizzBuzz:
    @staticmethod
    def generate(number):
        value = number

        if value % 3 == 0:
            value = 'Fizz'

        return value
    