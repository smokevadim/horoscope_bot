from django.db import models


class Zodiac(models.IntegerChoices):
    Aries = 1  # The Ram
    Taurus = 2  # The Bull
    Gemini = 3  # The Twins
    Cancer = 4  # The Crab
    Leo = 5  # The Lion
    Virgo = 6  # The Maiden
    Libra = 7  # The Scales
    Scorpio = 8  # The Scorpion
    Sagittarius = 9  # The (Centaur) Archer
    Capricorn = 10  # "Goat-Horned" (The Sea-Goat)
    Aquarius = 11  # The Water-Bearer
    Pisces = 12  # The Fishes
