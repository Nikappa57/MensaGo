from django.db import models


class Review(models.Model):
    """"
    Review(Mensa, User, Stars, text*)
     f.k Review[User] ⊆ User[Email]
     f.k. Review[Mensa] ⊆ Mensa[UUID]
    Stars: 1-5
    p.k Review[mensa, user]
    """

    STARS = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    stars = models.IntegerField(choices=STARS)
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey("core.CustomUser", on_delete=models.CASCADE)
    mensa = models.ForeignKey(
        "mensa.Mensa",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    class Meta:
        costraints = [
            models.UniqueConstraint(
                fields=["mensa", "user"], name="unique_mensa_user_review"
            )
        ]

    def __str__(self):
        return f"Review(mensa={self.mensa}, user={self.user}, stars={self.stars}, text={self.text})"

    def __repr__(self) -> str:
        return self.__str__()
