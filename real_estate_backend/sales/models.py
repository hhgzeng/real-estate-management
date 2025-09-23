from django.db import models

class Sales(models.Model):
    property_name = models.CharField(max_length=200, verbose_name='房产名称')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='销售价格')
    sale_date = models.DateField(verbose_name='销售日期')
    buyer_name = models.CharField(max_length=100, verbose_name='买家姓名')
    seller_name = models.CharField(max_length=100, verbose_name='卖家姓名')
    commission = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='佣金', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '销售记录'
        verbose_name_plural = '销售记录'
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.property_name} - {self.sale_date}"
