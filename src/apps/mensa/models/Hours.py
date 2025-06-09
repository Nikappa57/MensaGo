from django.db import models


class Hours(models.Model):
    """"
    Hours(WeekDay, DayPart, OpenTime, CloseTime, Mensa)
        f.k. Hours[Mensa] ⊆ Mensa[Name]
    """

    WEEKDAY = [
        (0, "Lunedi"),
        (1, "Martedi"),
        (2, "Mercoledi"),
        (3, "Giovedi"),
        (4, "Venerdi"),
        (5, "Sabato"),
        (6, "Domenica"),
    ]
    DAYPART = [
        (0, "Pranzo"),
        (1, "Cena"),
    ]

    mensa = models.ForeignKey("mensa.Mensa", on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY)
    daypart = models.IntegerField(choices=DAYPART)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.mensa} {self.weekday} {self.daypart}"

    def __repr__(self) -> str:
        return (
            f"Hours(mensa={self.mensa}, weekday={self.weekday}, daypart={self.daypart}, open_time={self.open_time}, close_time={self.close_time})"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mensa", "weekday", "daypart"],
                name="hours_unique_mensa_weekday_daypart",
            )
        ]
