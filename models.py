import time
import playsound
import random

from sqlalchemy import Column, Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import select

from sqlalchemy.orm import Session


engine = create_engine("mysql+pymysql://root:@localhost/clash_of_clans", echo=True)

Base = declarative_base()

session = Session(engine)

class Player(Base):
    __tablename__ = "player_account"

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(30))
    is_online = Column(Boolean)

    kingdom = relationship("Kingdom", back_populates="ruler", uselist=False)


class KingdomSpellRelation(Base):
    __tablename__ = "spell_kingdom_relation"

    kingdom_id = Column(ForeignKey("kingdom.id"), primary_key=True)
    spell_id = Column(ForeignKey("spell.id"), primary_key=True)

    kingdom = relationship("Kingdom", back_populates="spell_rellations")

    spell = relationship("Spell", back_populates="kingdoms_relation")


class Spell(Base):
    __tablename__ = "spell"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    kingdoms_relation = relationship("KingdomSpellRelation", back_populates="spell")

    def __str__(self):
        return self.name


class KingdomBuildingRelation(Base):
    __tablename__ = "building_kingdom_relation"
    
    kingdom_id = Column(ForeignKey("kingdom.id"), primary_key=True)
    building_id = Column(ForeignKey("building.id"), primary_key=True)

    kingdom = relationship("Kingdom", back_populates="building_relations")
    building = relationship("Building", back_populates="kingdoms_relation")


class Building(Base):
    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    kingdoms_relation = relationship("KingdomBuildingRelation", back_populates="building")

    def __str__(self):
        return self.name


class Kingdom(Base):
    __tablename__ = "kingdom"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String(30))
    player_id = Column(Integer, ForeignKey("player_account.id"))

    endGame = Column(Boolean, default=False)

    ruler = relationship("Player", back_populates="kingdom")

    day = Column(Integer, default=1)    
    age = Column(String(50), default="Zaman Batu")
    diffMult = Column(Float, default=1)
    prodMult = Column(Float, default=1)

    # Diubah menjadi many to many
    kingdom_relationship = Column(Integer, default=5) 

    birth = Column(Boolean, default=True)
    birthMult = Column(Float, default=1)
    death = Column(Integer, default=1)
    deathCan = Column(Boolean, default=True)
    deathAdd = Column(Integer, default=2)

    daysUntil = Column(Integer, default=0)
    birthRes = Column(Integer, default=0)

    attack = Column(Float, default=1)
    warMult = Column(Float, default=1)
    soldiers = Column(Integer, default=0)
    soldierPrice= Column(Integer, default=100)
    sword = Column(Float, default=1)
    
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    levelUp = Column(Integer, default=200)

    population = Column(Integer, default=300)
    popGrowth = Column(Integer, default=5)
    popDeath = Column(Integer, default=1)
    popAdd = Column(Integer, default=0)
    
    buildMaterials = Column(Integer, default=50)
    buildMaterialsPro = Column(Integer, default=1)
    buildProUpgradePrice = Column(Integer, default=10)
    buildProLevel = Column(Integer, default=1)

    explorePrice = Column(Integer, default=10)
    land = Column(Integer, default=1)

    money = Column(Integer, default=50)    
    moneyPro = Column(Integer, default=1)
    moneyProLevel = Column(Integer, default=1)
    moneyProUpgradePrice = Column(Integer, default=10)
    
    destruction = Column(Float, default=1)
    defense = Column(Integer, default=1)
    waste = Column(Float, default=1)
    defenseLevel = Column(Integer, default=1)
    defenseUpgradePrice = Column(Integer, default=10)
    defenseUpgradeBuildCost = Column(Integer, default=10)
    defenseUpgradeLandCost = Column(Integer, default=1)

    mortars = Column(Integer, default=0)
    mortarPrice = Column(Integer, default=500)

    missiles = Column(Integer, default=0)
    missilePrice = Column(Integer, default=2000)

    nukes = Column(Integer, default=0)
    nukePrice = Column(Integer, default=700)

    hbombs = Column(Integer, default=0)
    hbombPrice = Column(Integer, default=10000)
    
    bhbombs=Column(Integer, default=0)
    bhbombPrice=Column(Integer, default=20000)

    consumpMult = Column(Float, default=1)
    food = Column(Integer, default=300)
    foodProCan = Column(Boolean, default=True)
    foodPro = Column(Integer, default=300)
    foodDaysUntil = Column(Integer, default=0)
    foodRes = Column(Integer, default=0)
    foodProUpgradePrice = Column(Integer, default=50)
    foodProLevel = Column(Integer, default=1)

    spell_rellations = relationship("KingdomSpellRelation", back_populates="kingdom")

    building_relations = relationship("KingdomBuildingRelation", back_populates="kingdom")


    def getAllSpells(self):
        return [ spell_relation.spell for spell_relation in self.spell_rellations ]


    def getAllBuildings(self):
        return [ building_relation.building for building_relation in self.building_relations ]


    def __str__(self):
        spellsS     = "\n".join([f"- {spell.name}" for spell in self.getAllSpells()])
        buildingsLS = "\n".join([f"- {building.name}" for building in self.getAllBuildings()])
        
        return f"""\nHari {self.day:,} : 
{self.age}
Level\t: {self.level:,}
Poin\t: {self.points:,}
Poin yang dibutuhkan untuk level berikutnya: {self.levelUp:,}
Bahan bangunan: {self.buildMaterials:,}
Produksi bahan bangunan: {int(self.prodMult*self.buildMaterialsPro):,}/hari
Uang: ${self.money:,}
Produksi uang: ${int(self.prodMult*self.moneyPro):,}/hari
Makanan: {self.food:,}
Produksi makanan: {self.foodPro:,}/hari
Angka kelahiran: {int(self.birthMult*self.popGrowth):,}/hari
Angka kematian: {int(self.birthMult*self.popGrowth):,} (pertumbuhan populasi secara keseluruhan saat ini: {(self.birthMult*self.popGrowth)-self.popDeath:,})
Lahan: {self.land:,}
Populasi: {self.population:,}
Sihir: 
{spellsS}

Bangunan: 
{buildingsLS}

"""


    def addSpell(self, spellName):
        spell = session.execute(
            select(Spell).where(Spell.name == spellName)
            ).fetchone()[0]
        
        relation = KingdomSpellRelation(spell=spell)

        self.spell_rellations.append(relation) 

        session.commit()


    def removeSpell(self, spellName):
        relation = session.execute(
            select(KingdomSpellRelation).where(
                KingdomSpellRelation.spell.name==spellName)
        ).fetchone()[0]

        self.spell_rellations.remove(relation)

        session.commit()


    def checkBuildingExist(self, buildingName):
        for relation in self.building_relations:
            if relation.building.name == buildingName:
                return True
        return False


    def addBuilding(self, buildingName):
        building = session.execute(
            select(Building).where(Building.name == buildingName)
            ).fetchone()[0]
        
        relation = KingdomBuildingRelation(building=building)

        self.building_relations.append(relation) 

        session.commit()


    def showDecision(self):
        print("Apa yang ingin Anda lakukan, {}?".format(self.ruler))
        print("A: Tingkatkan produksi bahan bangunan seharga ${:,} (level saat ini: {:,})".format(self.buildProUpgradePrice, self.buildProLevel))
        print("B: Tingkatkan produksi uang seharga {:,} bahan bangunan (level saat ini: {:,})".format(self.moneyProUpgradePrice, self.moneyProLevel))
        print("C: Tingkatkan pertahanan seharga ${:,} dan {:,} bahan bangunan dan {:,} lahan (level saat ini: {:,})".format(self.defenseUpgradePrice, self.defenseUpgradeBuildCost, self.defenseUpgradeLandCost, self.defenseLevel))
        print("D: Tingkatkan produksi makanan seharga ${:,} (level saat ini: {:,}".format(self.foodProUpgradePrice, self.foodProLevel))
        print("E: Coba berdagang")
        print("F: Nyatakan perang")
        print("G: Jelajahi lahan baru seharga ${:,}".format(self.explorePrice))
        print("H/kunci lainnya: Hari berikutnya")
        print("I: Kejadian Random")
        print("J: Mengeluarkan Sihir")
        print("K: Mengatur hukum lahan")
        print("L: Membangun sesuatu")
        
        if self.level>=5:
            print("M: Latih Prajurit seharga ${:,} (saat ini Anda memiliki {:,})".format(self.soldierPrice, self.soldiers))
        if self.level>=10:
            print("N: Buat Mortir seharga ${:,} (saat ini Anda memiliki {:,})".format(self.mortarPrice, self.mortars))
        if self.level>=15:
            print("O: Buat Rudal seharga ${:,} (saat ini Anda memiliki {:,})".format(self.missilePrice, self.missiles))
        if self.level>=20:
            print("P: Buat Nuklir seharga ${:,} (saat ini Anda memiliki {:,})".format(self.nukePrice, self.nukes))
        if self.level>=25:
            print("Q: Buat Bom H seharga ${:,} (saat ini Anda memiliki {:,})".format(self.hbombPrice, self.hbombs))
        if self.level>=30:
            print("R: Buat Bom Lubang Hitam seharga ${:,} (saat ini Anda memiliki {:,})".format(self.bhbombPrice, self.bhbombs))
        
        print("\nX: Exit")


    def prodMaterials(self):
        self.buildMaterials = int(self.buildMaterials+(self.prodMult*self.buildMaterialsPro))
        session.commit()
    

    def makeMoney(self):
        self.money = int(self.money+(self.prodMult*self.moneyPro))
        session.commit()


    def birthPopulation(self):
        if self.birth:
            self.popGrowth   = int(self.population/95) + self.popAdd
            self.population  = int(self.population + (self.birthMult*self.popGrowth) + self.popAdd)
        else:
            if self.daysUntil >= self.birthRes:
                self.birth = True
                self.daysUntil = 0
                self.birthRes = 0
            else:
                self.daysUntil += 1
        session.commit()


    def deathPopulation(self):
        if self.deathCan:
            self.popDeath = int(self.population/200) + self.deathAdd
            self.population -= self.popDeath
        else:
            self.population -= self.deathAdd
        session.commit()


    def prodFood(self):
        if self.foodProCan:
            self.food += self.foodPro
        else:
            if self.foodDaysUntil >= self.foodRes:
                self.foodProCan = True
                self.foodPro *= 2
                self.food += self.foodPro
            else:
                self.foodDaysUntil += 1
        session.commit()


    def consumeFood(self):
        consumption = int(self.consumpMult*self.population)
        if self.food < consumption:
            starved = int((consumption-food)/self.consumpMult)
            self.population -= starved
            self.food = 0
            print("Anda tidak memiliki cukup makanan, jadi {} orang meninggal karena kelaparan.".format(starved))
            time.sleep(1)
        else:
            food = int(food-consumption)
        session.commit()


    def upgradeBuild(self):
        if self.buildProUpgradePrice > self.money:
            print("Tidak cukup uang!\n\n")
            self.points -= self.level*50
        else:
            playsound('sounds/palu.wav')
            self.money -= self.buildProUpgradePrice
            self.buildProLevel += 1
            self.buildMaterialsPro += int((1.5*self.buildProLevel))
            self.buildProUpgradePrice += (25*self.buildProLevel)
            print("Berhasil ditingkatkan!\n\n")
            self.points += self.level*100
        session.commit()


    def upgradeMoneyProd(self):
        if self.moneyProUpgradePrice > self.buildMaterials:
            print("Bahan bangunan tidak cukup!\n\n")
            self.points -= self.level*50
        else:
            playsound('sounds/palu.wav')
            self.buildMaterials         -= self.moneyProUpgradePrice
            self.moneyProLevel          += 1
            self.moneyPro               += int((1.5*self.moneyProLevel))
            self.moneyProUpgradePrice   += (25*self.moneyProLevel)
            
            print("Berhasil ditingkatkan!\n\n")
            
            self.points += self.level*100
        session.commit()

    
    def upgradeDefense(self):
        if self.defenseUpgradePrice > self.money:
            print("Tidak cukup uang!\n\n")
            self.points -= self.level*50
        elif self.defenseUpgradeBuildCost > self.buildMaterials:
            print("Bahan bangunan tidak cukup!\n\n")
            self.points -= self.level*50
        elif self.defenseUpgradeLandCost > self.land:
            print("Tidak cukup lahan!\n\n")
            self.points -= self.level*50
        else:
            playsound('sounds/palu.wav')
            self.buildMaterials -= self.defenseUpgradeBuildCost
            self.money -= self.defenseUpgradePrice
            self.land -= self.defenseUpgradeLandCost
            self.defenseLevel += 1
            self.defenseUpgradePrice += (25*self.defenseLevel)
            self.defenseUpgradeBuildCost += (25*self.defenseLevel)
            print("Berhasil ditingkatkan!\n\n")
            self.points += self.level*100
        session.commit()


    def upgradeFoodProd(self):
        if self.foodProUpgradePrice > self.money:
            print("Tidak cukup uang!\n\n")
            self.points -= self.level*50
        else:
            playsound('sounds/palu.wav')
            self.money -= self.foodProUpgradePrice
            self.foodProLevel += 1
            self.foodPro += (100*self.foodProLevel)
            self.foodProUpgradePrice +=(15*self.foodProLevel)
            print("Berhasil ditingkatkan!\n\n")
            self.points += self.level*100
        session.commit()


    def tradeBuilding(self, tradenum):
        if tradenum == 0:
            print("Anda tidak dapat melakukan perdagangan untuk 0 uang/bahan bangunan!\n\n")
        elif tradenum > self.money:
            print("Tidak cukup uang!\n\n")
            self.points -= self.level*50
        else:
            playsound('sounds/cha-ching-7053_1.wav')
            self.money -= tradenum
            self.buildMaterials += tradenum
            print("Anda berhasil memperdagangkan {:,} bahan bangunan!\n\n".format(tradenum))
            self.points += self.level*100
        session.commit()


    def tradeMoney(self, tradenum):
        if tradenum == 0:
            print("Anda tidak dapat melakukan perdagangan untuk 0 uang/bahan bangunan!\n\n")
        elif tradenum > self.buildMaterials:
            print("Bahan bangunan tidak cukup!\n\n")
            self.points -= self.level*50
        else:
            playsound('sounds/cha-ching-7053_1.wav')
            self.money += tradenum
            self.buildMaterials -= tradenum
            print("Anda berhasil melakukan perdagangan seharga ${:,}!\n\n".format(tradenum))
            self.points += self.level*100
        session.commit()


    def war(self):
        # Cari musuh secara random
        query = select(Kingdom).where(Kingdom.id != self.id)
        enemies = session.execute(query).scalars().all()

        enemy = random.choice(enemies)

        enemyWarPoints = int((7*enemy.defenseLevel) + (0.25*enemy.population) 
            + (7*enemy.soldiers) 
            + (15*enemy.mortars) 
            + (30*enemy.missiles)
            + (50*enemy.nukes)
            + (100*enemy.hbombs)
            + (200*enemy.bhbombs))

        warPoints = int(self.sword*self.warMult*self.attack*self.defense*self.destruction*self.waste*self.death*(
            (7*self.defenseLevel)
            + (0.25*self.population)
            + (7*self.soldiers)
            + (15*self.mortars)
            + (30*self.missiles)
            + (50*self.nukes)
            + (100*self.hbombs)
            + (200*self.bhbombs)))
        
        if warPoints > enemyWarPoints:
            playsound('sounds/success-fanfare-trumpets-6185.wav')
            winBy = warPoints - enemyWarPoints
            print("\n\nKamu menang! Kamu menjarah kota mereka dan mendapatkan banyak item:")
            
            moneyAdd    = int(0.5*winBy)
            buildAdd    = int(0.5*winBy)+11
            landAdd     = int((0.5*winBy))
            foodAdd     = int((0.5*winBy))+50
            
            enemy.population        -= (0.5*enemy.population)
            self.money              += moneyAdd
            self.buildMaterials     += buildAdd
            self.land               += landAdd
            self.food               += foodAdd
            self.points             += self.level*100
            self.population         -= (0.1*self.population)
            
            print("- ${:,}".format(moneyAdd))
            print("- {:,} bahan bangunan".format(buildAdd))
            print("- {:,} lahan baru".format(landAdd))
            print("- {:,} lebih banyak makanan\n".format(foodAdd))
            print("Namun, Anda telah kehilangan {:,} orang-orang dalam perang.\n\n".format(int(0.1*self.population)))
            time.sleep(2)
        elif warPoints < enemyWarPoints:
            playsound('sounds/piano-crash-sound-37898.wav')
            loseBy = enemyWarPoints-warPoints
            print("\n\nKamu kalah. Mereka menjarah kotamu dan mendapatkan banyak item:")
            
            moneySubtract   = int(0.5*loseBy)
            buildSubtract   = int(0.5*loseBy)
            landSubtract    = int(0.5*self.land)
            foodSubtract    = int(0.5*loseBy)
            
            self.food -= foodSubtract
            if self.food < 0:
                foodSubtract += self.food
                self.food = 0
            
            self.land -= landSubtract
            enemy.population -= (0.1*enemy.population)
            self.population = int(0.5*self.population)
            self.money -= moneySubtract
            if self.money < 0:
                moneySubtract += self.money
                self.money = 0
            
            self.buildMaterials -= buildSubtract
            if self.buildMaterials < 0:
                buildSubtract += self.buildMaterials
                self.buildMaterials = 0
            
            self.points -= (self.level*100)

            print("- ${:,}".format(moneySubtract))
            print("- {:,} bahan bangunan".format(buildSubtract))
            print("- {:,} lahan".format(landSubtract))
            print("- {:,} makanan\n".format(foodSubtract))
            print("Anda juga telah kehilangan {:,} orang dalam perang.".format(int(0.5*self.population)))
            time.sleep(2)
        else:
            print("Kalian seri. Tidak ada di antara kalian yang kehilangan apapun.")
            time.sleep(1)
        
        session.commit()


    def exploreLand(self):
        if self.explorePrice > self.money:
            print("Tidak cukup uang!\n\n")
            self.points -= self.level*50
        else:
            landGain = int((0.5*self.land)+1)
            self.money -= self.explorePrice
            self.land +=landGain
            self.explorePrice = int(1.8*self.explorePrice)
            exploreGainNum = random.randint(1,9)
            if exploreGainNum == 1:
                self.addSpell("Sihir Kemakmuran")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kemakmuran!\n\n".format(landGain))
            elif exploreGainNum == 2:
                self.addSpell("Sihir Kesuburan")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kesuburan!\n\n".format(landGain))
            elif exploreGainNum == 3:
                self.addSpell("Sihir Kekayaan")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kekayaan!\n\n".format(landGain))
            elif exploreGainNum == 4:
                self.addSpell("Sihir Kerja")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kerja!\n\n".format(landGain))
            elif exploreGainNum == 5:
                if self.level < 5:
                    self.addSpell("Sihir Pedang")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Pedang!\n\n".format(landGain))
                elif self.level < 10:
                    self.addSpell("Sihir Perang")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Perang!\n\n".format(landGain))
                elif self.level < 15:
                    self.addSpell("Sihir Serangan")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Serangan!\n\n".format(landGain))
                elif self.level < 20:
                    self.addSpell("Sihir Pertahanan")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Pertahanan!\n\n".format(landGain))
                elif self.level < 25:
                    self.addSpell("Sihir Kehancuran")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kehancuran!\n\n".format(landGain))
                elif self.level < 30:
                    self.addSpell("Sihir Kebusukan")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kebusukan!\n\n".format(landGain))
                else:
                    self.addSpell("Sihir Kematian")
                    print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kematian!\n\n".format(landGain))
            else:
                print("Anda pergi menjelajah dan menemukan {:,} lahan.".format(landGain))
            self.points += self.level*50
        
        session.commit()


    def randomEvent(self):
        wildCard = random.randint(1,9)
        
        if wildCard == 1:
            moneyGain = int(0.7*self.money)+1
            print("Beberapa petani menemukan peti harta karun tersembunyi yang berisi {:,} di dalam lahan ketika sedang membajak ladang mereka.\n\n".format(moneyGain))
            self.money += moneyGain
        elif wildCard == 2:
            buildLoss = int(0.3*self.buildMaterials)
            print("Seorang pekerja yang kikuk menjatuhkan {:,} bahan bangunan ke dalam lubang tak berujung yang tak berujung, di mana bahan bangunan itu tidak pernah terlihat lagi.\n\n".format(buildLoss))
            self.buildMaterials -= buildLoss
        elif wildCard == 3:
            foodGain = int(0.3*self.food)+2
            print("Beberapa pelancong menemukan gudang yang ditinggalkan dengan {:,} makanan di dalamnya.\n\n".format(foodGain))
            self.food += foodGain
        elif wildCard == 4:
            self.popGrowth = 0
            self.population -= 50
            self.birth = False
            self.birthRes = 10
            print("Sebuah meteor menghantam daratan, menyebabkan kematian 50 orang. Radiasi juga menyebabkan tingkat kelahiran menjadi 0 selama 10 hari.\n\n")
        elif wildCard == 5:
            pointsNeeded = self.levelUp - self.points
            self.points += pointsNeeded
            print("Anda menemukan gubuk penyihir dan dia dengan murah hati memberi Anda poin yang cukup untuk naik level!\n\n")
        elif wildCard == 6:
            buildGain = int(0.4*self.buildMaterials)+1
            self.buildMaterials += buildGain
            print("Anda menemukan sebuah bangunan dalam kondisi yang cukup baik, dan merobohkannya untuk menggunakan kembali {:,} bahan bangunan.\n\n".format(buildGain))
        elif wildCard == 7:
            foodLoss = int(0.3*self.food) - 1
            self.food -= foodLoss
            self.foodPro = int(0.5*self.foodPro)
            self.foodRes = 3
            self.foodDaysUntil = 0
            self.foodProCan = False
            print("Karena serangan angin, Anda kehilangan {:,} makanan dan produksi makanan Anda berkurang setengahnya selama 3 hari.\n\n".format(foodLoss))
        elif wildCard == 8:
            sp = random.randint(1,5)
            if sp == 1:
                self.addSpell("Sihir Kemakmuran")
                print("Anda mendapatkan Sihir Kemakmuran! Sihir ini akan menaikkan level Anda 1 level dalam produksi makanan.\n\n")
            elif self.sp == 2:
                self.addSpell("Sihir Kesuburan")
                print("Anda mendapatkan Sihir Kesuburan! Sihir ini akan memberikan Anda 100 populasi.\n\n")
            elif sp == 3:
                self.addSpell("Sihir Kekayaan")
                print("Anda mendapatkan Sihir Kekayaan! Sihir ini akan menaikkan level Anda 1 level dalam produksi uang.\n\n")
            elif sp == 4:
                self.addSpell("Sihir Kerja")
                print("Anda mendapatkan Sihir Kerja! Sihir ini akan menaikkan level Anda 1 level dalam produksi bahan bangunan.\n\n")
            elif sp == 5:
                if self.level < 5:
                    self.addSpell("Sihir Pedang")
                    print("Anda mendapatkan Sihir Pedang! Sihir ini akan memberikan anda 1.1 kali poin perang anda dalam pertempuran.\n\n")            
                elif self.level<10:
                    self.addSpell("Sihir Perang")
                    print("Anda mendapatkan Sihir Perang! Sihir ini akan memberikan Anda 1.5 kali poin perang Anda dalam pertempuran.\n\n")
                elif self.level<15:
                    self.addSpell("Sihir Serangan")
                    print("Anda mendapatkan Sihir Serangan! Sihir ini akan memberikan Anda 1.7 kali poin perang Anda dalam pertempuran.\n\n")
                elif self.level<20:
                    self.addSpell("Sihir Pertahanan")
                    print("Kamu mendapatkan Sihir Pertahanan! Sihir ini akan memberikan Anda 2 kali poin perang Anda dalam pertempuran.\n\n")
                elif self.level<25:
                    self.addSpell("Sihir Kehancuran")
                    print("Anda mendapatkan Sihir Kehancuran! Sihir ini akan memberikan Anda 2.5 kali poin perang Anda dalam pertempuran.\n\n")
                elif self.level<30:
                    self.addSpell("Sihir Kebusukan")
                    print("Anda mendapatkan Sihir Kebusukan! Sihir ini akan memberikan Anda 2.7 kali poin perang Anda dalam pertempuran.\n\n")
                else:
                    self.addSpell("Sihir Kematian")
                    print("Kamu mendapatkan Sihir Kematian! Sihir ini akan memberikan Anda 3 kali poin perang Anda dalam pertempuran.\n\n")
        else:
            self.points -= self.points+1
            print("Seorang penyihir jahat menyebabkan poin Anda turun di bawah 0 jadi sekarang Anda turun level.")
        
        session.commit()


    def useSpell(self):
        print("Berikut adalah Sihir yang Anda miliki:")
        
        mySpellName = [ spell.name for spell in self.getAllSpells() ]
        for spell in list(set(mySpellName)):
            print("- {}".format(spell))
        
        print("A: Sihir Kemakmuran")
        print("B: Sihir Kesuburan")
        print("C: Sihir Kekayaan")
        print("D: Sihir Kerja")
        print("E: Sihir Pedang")

        if self.level < 10:
            print("F: Sihir Perang")
        if self.level < 15:
            print("G: Sihir Serangan")
        if self.level < 20:
            print("H: Sihir Pertahanan")
        if self.level < 25:
            print("I: Sihir Penghancuran")
        if self.level < 30:
            print("J: Sihir Kebusukan")
        if self.level >= 30:
            print("K: Sihir Kematian")
        
        spe = str(input("Pilih salah satu spell : "))
        spe = spe.lower()
        
        if spe == "a":
            if "Sihir Kemakmuran" in mySpellName:
                playsound('sounds/godong.wav')
                print("Anda tiba-tiba mendengar suara tanaman yang tumbuh...\n\n")
                self.foodProLevel += 1
                self.foodPro += (100*self.foodProLevel)
                self.removeSpell("Sihir Kemakmuran")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "b":
            if "Sihir Kesuburan" in mySpellName:
                playsound('sounds/babywhine1-6318.wav')
                print("Anda tiba-tiba mendengar suara tangisan bayi...\n\n")
                self.population += 100
                self.removeSpell("Sihir Kesuburan")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "c":
            if "Sihir Kekayaan" in mySpellName:
                playsound('sounds/cha-ching-7053_1.wav')
                print("Anda tiba-tiba mendengar suara koin bergemerincing...\n\n")
                self.moneyProLevel += 1
                self.moneyProLevel += int((1.5*self.moneyProLevel))
                self.removeSpell("Sihir Kekayaan")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "d":
            if "Sihir Kerja" in mySpellName:
                playsound('sounds/palu.wav')
                print("Anda tiba-tiba mendengar suara palu berdenting...\n\n")
                self.buildProLevel += 1
                self.buildMaterialsPro += int((1.5*self.buildProLevel))
                self.removeSpell("Sihir Kerja")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "e":
            if "Sihir Pedang" in mySpellName:
                playsound('sounds/swingg.wav')
                print("Anda tiba-tiba mendengar suara pedang yang berdesir...\n\n")
                self.sword = 1.1
                self.removeSpell("Sihir Pedang")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "f":
            if "Sihir Perang" in mySpellName:
                playsound('sounds/auuu.wav')
                print("Anda tiba-tiba mendengar suara teriakan pertempuran...\n\n")
                self.warMult = 1.5
                self.removeSpell("Sihir Perang")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "g":
            if "Sihir Serangan" in mySpellName:
                playsound('sounds/auuu.wav')
                print("Anda tiba-tiba mendengar suara pasukan yang bergegas ke medan perang...\n\n")
                self.attack = 1.7
                self.removeSpell("Sihir Serangan")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "h":
            if "Sihir Pertahanan" in mySpellName:
                playsound('sounds/sword-battle-jingle-loop-96983.wav')
                print("Anda tiba-tiba mendengar suara pedang mengenai perisai...\n\n")
                self.defense = 2
                self.removeSpell("Sihir Pertahanan")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "i":
            if "Sihir Kehancuran" in mySpellName:
                playsound('sounds/rock-destroy-6409.wav')
                print("Anda tiba-tiba mendengar suara bangunan runtuh...\n\n")
                self.destruction = 2.5
                self.removeSpell("Sihir Kehancuran")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "j":
            if "Sihir Kebusukan" in mySpellName:
                playsound('sounds/wither.wav')
                print("Anda tiba-tiba melihat banyak kehiduan layu...\n\n")
                self.waste = 2.7
                self.removeSpell("Sihir Kebusukan")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50
        elif spe == "k":
            if "Sihir Kematian" in mySpellName:
                playsound('sounds/demonic-woman-scream-6333.wav')
                print("Anda tiba-tiba mendengar suara jeritan...\n\n")
                self.death = 3
                self.removeSpell("Sihir Kematian")
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                self.points -= self.level*50


    def changeLaw(self):
        print("Hukum apa yang ingin Anda ubah?")
        print("A: Hukum kelahiran")
        print("B: Hukum kerja")
        d = input()
        d = d.lower()
        if d == "a":
            print("Bagian apa yang ingin Anda ubah?")
            print("A: Ubah hukum kelahiran menjadi Terbatas (1/2x reguler)")
            print("B: Ubah hukum kelahiran menjadi Reguler (default)")
            print("C: Ubah hukum kelahiran menjadi Berlimpah (2x reguler)")
            d1 = input()
            d1 = d1.lower()
            if d1 == "a":
                self.birthMult = 0.5
            elif d1 == "c":
                self.birthMult = 2
            else:
                self.birthMult = 1
            
            print("Berhasil diubah!")
        else:
            print("Bagian apa yang ingin Anda ubah?")
            print("A: Ubah hukum kerja menjadi Lambat (orang mengkonsumsi x1/2 makanan dari biasanya, tetapi produksi uang dan bahan bangunan x1/2)")
            print("B: Ubah hukum kerja menjadi Reguler (default)")
            print("C: Ubah hukum kerja menjadi Efisien (produksi uang dan bahan bangunan x2, tetapi orang mengkonsumsi makanan x2 lebih banyak dari biasanya)")
            d1 = str(input())
            d1 = d1.lower()
            if d1 == "a":
                self.consumpMult = 0.5
                self.prodMult = 0.5
            elif d1 == "c":
                self.consumpMult = 2
                self.prodMult = 2
            else:
                self.consumpMult = 1
                self.prodMult = 1

            print("Berhasil diubah!")  


    def build(self):
        buildingList = [
            "Monolit Batu",
            "Orang-orangan Sawah",
            "Patung Bayi",
            "Patung Pembangun",
            "Altar Pengorbanan",
            "Kedutaan",
            "Bazaar",
            "Kuil",
            "Menara Bisnis",
            "Menara Kas",
            "Monumen Kehidupan",
        ]

        

        print("Bangunan yang bisa Anda bangun:")
        print("A: Batu Monolit (1 lahan, 60 bahan bangunan). Efek:\n   - +$5/hari\n   ("+builts[0]+")")
        print("B: Orang-orangan sawah (1 lahan, 60 bahan bangunan). Efek:\n   - +100 makanan/hari\n   ("+builts[1]+")")
        print("C: Patung Bayi (1 lahan, 120 bahan bangunan). Efek:\n   - +2 populasi/hari\n   ("+builts[2]+")")
        print("D: Patung Pembangun (1 lahan, 200 bahan bangunan). Efek:\n   - +20 bahan bangunan/hari\n   ("+builts[3]+")")
        print("E: Altar Pengorbanan (2 lahan, 350 bahan bangunan, 20 populasi). Efek:\n   - +2 kematian/hari\n   - +1000 makanan/hari\n   ("+builts[4]+")")
        print("F: Kedutaan (4 lahan, 500 bahan bangunan, $300) (mungkin tidak boleh dibangun jika skor hubungan Anda 5). Efek:\n   - +2 hubungan dengan "+name+" (maksimum)\n   ("+builts[5]+")")
        print("G: Bazaar (8 lahan, 700 bahan bangunan, $500). Efek:\n   - +$70/hari\n   - +75 bahan bangunan/hari\n   ("+builts[6]+")")
        print("H: Kuil (16 lahan, 1000 bahan bangunan, $1000). Efek:\n   - +50 populasi/hari\n   - +$100/hari\n   - +100 bahan bangunan/hari\n   ("+builts[7]+")")
        print("I: Menara Bisnis (32 lahan, 3000 bahan bangunan). Efek:\n   - +500 bahan bangunan/hari\n   ("+builts[8]+")")
        print("J: Menara Tunai (32 lahan, $3000). Efek:\n   - +$500/hari\n   ("+builts[9]+")")
        print("K: Monumen Kehidupan (64 lahan, 5000 bahan bangunan, $5000). Efek:\n   - Orang tidak lagi mati (kecuali orang yang mati sebagai korban)\n   ("+builts[10]+")")
        print("Kunci lainnya: batal")
        
        bdec = str(input())
        bdec = bdec.lower()
        if bdec=="a":
            if builts[0] == "Belum dibangun":
                if land >= 1:
                    if buildmaterials >= 60:
                        playsound('sounds/C:\tmp\wrryyy\palu.wav')
                        land -= 1
                        buildmaterials -= 60
                        moneypro += 5
                        builts[0] = "Dibangun"
                        print("Berhasil membangun Monolit Batu!\n\n")
                        buildingsL.append("Monolit Batu")
                        points += level*110
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "b":
            if builts[1] == "Belum dibangun":
                if land >= 1:
                    if buildmaterials >= 60:
                        playsound('sounds/palu.wav')
                        land -= 1
                        buildmaterials = buildmaterials-60
                        foodpro += 100
                        builts[1]="Dibangun"
                        print("Berhasil membangun Orang-orangan Sawah!\n\n")
                        buildingsL.append("Orang-orangan Sawah")
                        points += level*110
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        points -=level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "c":
            if builts[2] == "Belum dibangun":
                if land >= 1:
                    if buildmaterials >= 120:
                        playsound('sounds/palu.wav')
                        land -= 1
                        buildmaterials -= 120
                        popadd += 2
                        builts[2] = "Dibangun"
                        print("Berhasil membuat Patung Bayi!\n\n")
                        buildingsL.append("Patung Bayi")
                        points += level*130
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "d":
            if builts[3] == "Belum dibangun":
                if land >= 1:
                    if buildmaterials >= 200:
                        playsound('sounds/palu.wav')
                        land -= 1
                        buildmaterials -= 200
                        buildmaterialspro += 20
                        builts[3] = "Dibangun"
                        print("Berhasil membangun Patung Pembangun!\n\n")
                        buildingsL.append("Patung Pembangun")
                        points += level*150
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "e":
            if builts[4] == "Belum dibangun":
                if land >= 2:
                    if buildmaterials >= 350 and pop>=20:
                        playsound('sounds/palu.wav')
                        land -= 2
                        buildmaterials -= 350
                        pop -= 20
                        foodpro += 1000
                        deathadd += 2
                        builts[4] = "Dibangun"
                        print("Berhasil membangun Altar Pengorbanan, mengorbankan 20 orang tak berdosa dalam prosesnya!\n\n")
                        buildingsL.append("Altar Pengorbanan")
                        points += level*160
                    else:
                        print("Tidak cukup bahan bangunan/populasi!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "f":
            if builts[5] == "Belum dibangun":
                if land >= 4:
                    if buildmaterials >= 500 and money >= 300:
                        playsound('sounds/palu.wav')
                        land -= 4
                        buildmaterials -= 500
                        money -= 300
                        if relationship<=3:
                            relationship += 2
                        elif relationship==4:
                            relationship += 1
                        
                        builts[5]="Dibangun"
                        print("Berhasil membangun Kedutaan!\n\n")
                        buildingsL.append("Kedutaan")
                        points += level*180
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "g":
            if builts[6] == "Belum dibangun":
                if land >= 8:
                    if buildmaterials >= 700 and money >= 500:
                        playsound('sounds/palu.wav')
                        land -= 8
                        buildmaterials -= 700
                        money -= 500
                        moneypro += 70
                        buildmaterialspro += 75
                        builts[6] = "Dibangun"
                        print("Berhasil membangun Bazaar!\n\n")
                        buildingsL.append("Bazaar")
                        points += level*190
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "h":
            if builts[7] == "Belum dibangun":
                if land >= 16:
                    if buildmaterials >= 1000 and money >= 1000:
                        playsound('sounds/palu.wav')
                        land -= 16
                        buildmaterials -= 1000
                        money -= 1000
                        moneypro += 100
                        buildmaterialspro += 100
                        popadd += 50
                        builts[7] = "Dibangun"
                        print("Berhasil membangun Kuil!\n\n")
                        buildingsL.append("Kuil")
                        points += level*200
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "i":
            if builts[8] == "Belum dibangun":
                if land >= 32:
                    if buildmaterials >= 3000:
                        playsound('sounds/palu.wav')
                        land -= 32
                        buildmaterials -= 3000
                        buildmaterialspro += 500
                        builts[8] = "Dibangun"
                        print("Berhasil membangun Menara Bisnis!\n\n")
                        buildingsL.append("Menara Bisnis")
                        points += level*230
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "j":
            if builts[9] == "Belum dibangun":
                if land >= 32:
                    if money >= 3000:
                        playsound('sounds/palu.wav')
                        land -= 32
                        money -=3000
                        moneypro += 500
                        builts[9] = "Dibangun"
                        print("Berhasil membangun Menara Kas!\n\n")
                        buildingsL.append("Menara Kas")
                        points += level*230
                    else:
                        print("Tidak cukup uang!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        elif bdec == "k":
            if builts[10] == "Belum dibangun":
                if land >= 64:
                    if buildmaterials >= 5000 and money >= 5000:
                        playsound('sounds/palu.wav')
                        land -= 64
                        buildmaterials -=5000
                        money -= 5000
                        deathcan = False
                        builts[10] = "Dibangun"
                        print("Berhasil membangun Monumen Kehidupan! Orang tidak lagi mati, kecuali pengorbanan.\n\n")
                        buildingsL.append("Monumen Kehidupan")
                        points += level*260
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        points -= level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    points -= level*50
            else:
                print("Anda sudah membangun gedung ini!\n\n")
        else:
            print("\n")


    def trainSoldier(self):
        if self.level >= 5:
            if self.soldierPrice > self.money:                
                print("Tidak cukup uang!\n\n")
                self.points -= self.level*50
            else:
                playsound('sounds/clanks-89017.wav')
                self.money -= self.soldierPrice
                self.soldiers += 1
                self.soldierPrice += (15*self.soldiers)
                print("Berhasil diBuat!\n\n")
                self.points += self.level*100
        else:
            print()
            print()


    def createMortar(self):        
        if self.level >= 10:
            if self.mortarPrice > self.money:
                print("Tidak cukup uang!\n\n")
                self.points -= self.level*50
            else:
                playsound('sounds/clanks-89017.wav')
                self.money -= self.mortarPrice
                self.mortars += 1
                self.mortarPrice += (15*self.mortars)
                print("Berhasil diBuat!\n\n")
                self.points += self.level*150
        else:
            print()
            print()



Base.metadata.create_all(engine)

# Harus dijalankan satu kali saja
# session.add_all([
#     Spell(name="Sihir Kemakmuran"),
#     Spell(name="Sihir Kesuburan"),
#     Spell(name="Sihir Kekayaan"),
#     Spell(name="Sihir Kerja"),
#     Spell(name="Sihir Pedang"),
#     Spell(name="Sihir Perang"),
#     Spell(name="Sihir Serangan"),
#     Spell(name="Sihir Pertahanan"),
#     Spell(name="Sihir Kehancuran"),
#     Spell(name="Sihir Kebusukan"),
#     Spell(name="Sihir Kematian"),
#     Building(name="Monolit Batu"),
#     Building(name="Orang-orangan Sawah"),
#     Building(name="Patung Bayi"),
#     Building(name="Patung Pembangun"),
#     Building(name="Altar Pengorbanan"),
#     Building(name="Kedutaan"),
#     Building(name="Bazaar"),
#     Building(name="Kuil"),
#     Building(name="Menara Bisnis"),
#     Building(name="Menara Kas"),
#     Building(name="Monumen Kehidupan"),
# ])

session.commit()
