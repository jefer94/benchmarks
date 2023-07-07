from .object import object_generator


SHORT_OBJECT = 3
MEDIUM_OBJECT = 10
BIG_OBJECT = 30

short_object_generator = object_generator(SHORT_OBJECT)
medium_object_generator = object_generator(MEDIUM_OBJECT)
big_object_generator = object_generator(BIG_OBJECT)