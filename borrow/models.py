from django.db import models

# Create your models here.

class Borrow(models.Model):
    toy_id = models.CharField(max_length=20)  # 玩具id
    name = models.CharField(max_length=20)  # 玩具名
    type = models.CharField(max_length=20)  # 玩具类型
    toy_borrow = models.CharField(max_length=20)  # 玩具借用人
    advance_time = models.DateTimeField(auto_now_add=True)  # 预借时间
    borrow_time = models.DateTimeField(null=True, blank=True)  # 借用时间，允许为空
    return_time = models.DateTimeField(null=True, blank=True)  # 归还时间，允许为空

    class Meta:
        unique_together = ('toy_id', 'advance_time')  # 设置联合主键

    def __str__(self):
        return f"{self.toy_id} borrowed by {self.toy_borrow} at {self.advance_time}"