from faker import Faker
fake = Faker()

def object_generator(n) -> callable:
    def wrapper():
        return {fake.name(): fake.text() for _ in range(n)}
    return wrapper