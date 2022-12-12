from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    kingdom = Set(lambda: Kingdom)

class Spell(models.Model):
    name = models.CharField(max_length=50)

class Kingdom(models.Model):
    age = models.IntegerField()
    name = models.IntegerField()
    ruler = models.ForeignKey(Player, on_delete=models.CASCADE)
    diffMult = models.FloatField()
    population = models.IntegerField()
    relationship = models.IntegerField()

    soldiers = models.IntegerField()
    soldierPrice= models.IntegerField()
    
    points = models.IntegerField()
    level = models.IntegerField()
    levelUp = models.IntegerField()
    
    popGrowth = models.IntegerField()
    popDeath = models.IntegerField()
    
    buildMaterials = models.IntegerField()
    buildMaterialsPro = models.IntegerField()
    
    money = models.IntegerField()
    land = models.IntegerField()
    
    buildProUpgradePrice = models.IntegerField()
    buildProLevel = models.IntegerField()
    
    moneyPro = models.IntegerField()
    moneyProLevel = models.IntegerField()
    moneyProUpgradePrice = models.IntegerField()
    
    defenseLevel = models.IntegerField()
    defenseUpgradePrice = models.IntegerField()
    defenseUpgradeBuildCost = models.IntegerField()

    mortars = models.IntegerField()
    mortarprice = models.IntegerField()

    missiles = models.IntegerField()
    missileprice = models.IntegerField()

    nukes = models.IntegerField()
    nukeprice = models.IntegerField()

    hbombs = models.IntegerField()
    hbombPrice = models.IntegerField()
    
    bhbombs=models.IntegerField()
    bhbombPrice=models.IntegerField()

    food = models.IntegerField()
    foodProCan = models.BooleanField()
    foodPro = models.IntegerField()
    foodDaysUntil = models.IntegerField()
    foodres = models.IntegerField()
    foodProUpgradePrice = models.IntegerField()
    foodProLevel = models.IntegerField()

    spells = models.ManyToManyField(Spell)
    birth = models.IntegerField()
    death = models.IntegerField()

    daysUntil = models.IntegerField()
    birthRes = models.IntegerField()









db.bind(provider='mysql', host='localhost', user='root', passwd='', db='clash_of_clans')

db.generate_mapping(create_tables=True)