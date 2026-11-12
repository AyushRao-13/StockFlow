from django.db import models
from django.db.models import Sum


DEPARTMENT_CHOICES = [
    ('BCA', 'BCA'),
    ('BBA', 'BBA'),
    ('B.COM', 'B.COM'),
    ('BSC', 'BSC'),
    ('B.ED', 'B.ED'),
]

class Department(models.Model):
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.department


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    faculty_id=models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.faculty_id}"

class Items(models.Model):
    name = models.CharField(max_length=50)
    totalPurchased= models.IntegerField(default=0)
    QuantityInInventory= models.IntegerField(default=0)
    ItemsIssued = models.IntegerField(default = 0)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Purchase(models.Model):
    ItemName = models.ForeignKey(Items,max_length=50,on_delete=models.PROTECT,related_name='purchase_itemname')
    Quantity = models.IntegerField()
    Rate = models.IntegerField(default=0)
    Invoice_Number = models.CharField(max_length=50)
    Billing_Date = models.DateField()
    Date_of_Entry = models.DateField()
    Total_Amount = models.IntegerField()
    Seller_Name = models.CharField(max_length=50)
    CGST = models.IntegerField(default=0)
    SGST = models.IntegerField(default=0)
    Extra_charges = models.IntegerField(default=0)
    GST = models.IntegerField(default=0)
    Invoice=models.FileField(upload_to='invoice',null=True,blank=True)

    def __str__(self):
        return f"{self.ItemName.name} - {self.Invoice_Number}"
    

class IssuedItem(models.Model):
    ItemName = models.ForeignKey(Items, on_delete=models.PROTECT, related_name='issued_item_itemname') 
    Quantity = models.IntegerField()
    Name_of_Employee = models.ForeignKey(Faculty,max_length=50,on_delete=models.PROTECT,related_name='issued_item_name_of_employee')
    Issue_Date = models.DateField()
    Department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    Refrence_No = models.CharField(max_length=50,default="Not Found")
    Location = models.CharField(max_length=50)
    physical_verification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ItemName} - {self.Name_of_Employee} - {self.Department}"
    