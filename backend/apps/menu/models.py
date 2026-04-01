from django.db import models

class MenuCategory(models.Model):
    name = models.CharField("Название категории", max_length=150, unique=True)
    description = models.CharField("Описание", max_length=255, blank=True)

    class Meta:
        verbose_name = "Категория меню"
        verbose_name_plural = "Категории меню"
        ordering = ["name"]

class Dish(models.Model):
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.PROTECT,
        related_name="dishes",
        verbose_name="Категория",
    )

    name = models.CharField("Название блюда", max_length=200)
    description = models.TextField("Описание", blank=True)
    is_active = models.BooleanField("Доступно", default=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_dish_name_in_category",
            )
        ]
    
    def __str__(self):
        return self.name