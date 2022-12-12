class Kingdoms:
    def __init__(self, name, diffMult, relationship, popDeath, soldiers, soldierPrice, points, level, levelUp, popGrowth, buildMaterials, buildMaterialsPro, money, rulerName = None, population = 300, land = 1, age = "Stone Age", buildProUpgradePrice = 10, buildProLevel = 1, moneyPro = 1, moneyProLevel = 1, moneyProUpgradePrice = 10, defenseLevel = 1, defenseUpgradePrice = 10, defenseUpgradeBuildCost = 10, spells = []):
        self.age = age
        self.name = name
        self.rulerName = rulerName
        self.diffMult = diffMult
        self.population = population
        self.relationship = relationship

        self.soldiers = soldiers
        self.soldierPrice= soldierPrice
        
        self.points = points
        self.level = level
        self.levelUp = levelUp
        
        self.popGrowth = popGrowth
        self.popDeath = popDeath
        
        self.buildMaterials = buildMaterials
        self.buildMaterialsPro = buildMaterialsPro
        
        self.money = money
        self.land = land
        
        self.buildProUpgradePrice = buildProUpgradePrice
        self.buildProLevel = buildProLevel
        
        self.moneyPro = moneyPro
        self.moneyProLevel = moneyProLevel
        self.moneyProUpgradePrice = moneyProUpgradePrice
        
        self.defenseLevel = defenseLevel
        self.defenseUpgradePrice = defenseUpgradePrice
        self.defenseUpgradeBuildCost = defenseUpgradeBuildCost

        self.mortars = 0
        self.mortarprice = 500

        self.missiles = 0
        self.missileprice = 2000

        self.nukes = 0
        self.nukeprice = 7000

        self.hbombs = 0
        self.hbombPrice = 10000
        
        self.bhbombs=0
        self.bhbombPrice=20000

        self.food = 300
        self.foodProCan = True
        self.foodPro = 300
        self.foodDaysUntil = 0
        self.foodres = 0
        self.foodProUpgradePrice = 50
        self.foodProLevel = 1

        self.spells = spells
        self.birth = True
        self.death = True

        self.daysUntil = 0
        self.birthRes = 0
    
    def upLevel(self):
        self.level += 1
        self.points -= self.levelUp

        self.levelUp = int(self.levelUp * 1.5)
        print("\n\n\n\n-----------\n|LEVEL UP!|\n-----------\n\n\n\n")
    
    def downLevel(self):
        self.points = 0
        self.level -= 1
        self.levelUp //= 2
        print("\n\n\n\n-------------\n|Level down.|\n-------------\n\n\n\n")

    def changeAge(self, newAge):
        # age : unlocked-unit
        dict_ages = {
            "Copper Age":"Soldier",
            "Bronze Age":"Mortar",
            "Iron Age":"Missile",
            "Middle Ages":"Nuke",
            "Modern Age":"H-bomb",
            "Future Age":"Black Hole Bomb"
        } 
        self.age = newAge
        print(f"You have entered the {newAge}!\nYou gain a new unit: {dict_ages[newAge]}!\n")
        
        if self.age == "Future Age":
            print("Wow. You've made it this far. I salute you, and give you 2 of every spell as a reward)\n\n")
        else:
            print("\n\n")
    
    def addSpells(self, arrSpell):
        self.spells += arrSpell
    
    def upBuildMaterials(self, prodmult):     
        self.buildMaterials += int(prodmult * self.buildMaterialsPro)
    
    def changePopGrowth(self, divNumber):
        self.popGrowth //= divNumber
    
    def changePopDeath(self, divNumber):
        self.popDeath //= divNumber
    
    def prodMoney(self, prodmult: int):
        self.money += int(prodmult * self.moneyPro)
    
    def growthPop(self, divNumber, birthmult=1):
        if self.birth:
            self.popGrowth //= divNumber
            self.population += int(birthmult*self.popGrowth)
            self.birth = False
        else:
            if self.daysUntil>=self.birthRes:
                self.birth = True
                self.daysUntil = 0
                self.birthRes = 0
            else:
                self.daysUntil += 1
    
    def deathPop(self):
        if self.death:
            popdeath = int(population/200)
            population -= popdeath
    
    def prodFood(self):
        if self.foodProCan:
            self.food += self.foodPro
        else:
            if self.foodDaysUntil>= self.foodRes:
                self.foodProCan = True
                self.foodPro *= 2
                self.food += self.foodpro
            else:
                self.foodDaysUntil += 1
    
    def consumeFood(self, consumpmult):
        consumption = int(consumpmult * self.population)
        if self.food < consumption:
            starved = self.population - (food // consumpmult)
            self.population -= starved
            food = 0
            print(f"You did not have enough food, so {starved} people died of hunger.")
        else:
            food -= consumption