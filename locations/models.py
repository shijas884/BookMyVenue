from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class District(models.Model):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="districts"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("state", "name")
    
    def __str__(self):
        return self.name
    
    
