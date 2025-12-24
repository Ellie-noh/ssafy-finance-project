from django.db import models

class DepositProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=50, unique=True)  # 상품코드 (PK 역할)
    kor_co_nm = models.CharField(max_length=100)              # 금융회사명
    fin_prdt_nm = models.CharField(max_length=200)             # 상품명
    etc_note = models.TextField(blank=True, null=True)
    join_deny = models.IntegerField()                         # 가입제한 (1,2,3)
    join_member = models.TextField(blank=True, null=True)        # 가입대상
    join_way = models.TextField(blank=True, null=True)         # 가입방법
    spcl_cnd = models.TextField(blank=True, null=True)         # 우대조건
    max_rate = models.FloatField(null=True, blank=True)       # 최대 우대금리

    def __str__(self):
        return self.fin_prdt_nm


class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    intr_rate_type_nm = models.CharField(max_length=20)   # 단리/복리
    save_trm = models.CharField(max_length=10)           # 저축기간(개월)
    intr_rate = models.FloatField(null=True, blank=True)    # 기본금리
    intr_rate2 = models.FloatField(null=True, blank=True)  # 우대금리

    def __str__(self):
        return self.save_trm
