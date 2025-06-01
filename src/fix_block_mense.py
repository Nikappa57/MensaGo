import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.mensa.models.Mensa import Mensa

if __name__ == "__main__":
    mense = Mensa.objects.all()

    for mensa in mense:
        mensa.save()
        print(mensa.capacity)
        print("0 ==", mensa.capacity % 40)
        print(mensa.block_nbr, "==", mensa.capacity // 40)
