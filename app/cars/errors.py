from cars.error_handler import InvalidApiUsage


class CarApiErrors:
    class ExternalApiCarNotFound(InvalidApiUsage):
        message = 'Car not found'

    class CarNotUnique(InvalidApiUsage):
        message = 'The fields make, model must make a unique set.'


class RateApiErrors:
    class InvalidRateType(InvalidApiUsage):
        message = 'Rating must be an integer'

    class InvalidRateMin(InvalidApiUsage):
        message = 'Rating must be greater or equal then 1'

    class InvalidRateMax(InvalidApiUsage):
        message = 'Rating must be lower or equal then 5'

    class InvalidCarId(InvalidApiUsage):
        message = 'Car with provided id does not exists'
