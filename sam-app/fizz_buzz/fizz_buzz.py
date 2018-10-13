class FizzBuzz:
    @staticmethod
    def generate(number):
        value = number

        if value % 3 == 0:
            value = 'Fizz'
        elif value % 5 == 0:
            value = 'Buzz'
        elif value % 3 == 0 and value % 5 == 0:
            value = 'FizzBuzz'

        return value
    