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


kingdom_spell_relation = Table(
    "spell_kingdom_relation",
    Base.metadata,
    Column("kingdom_id", ForeignKey("kingdom.id"), primary_key=True),
    Column("spell_id", ForeignKey("spell.id"), primary_key=True),
)


class Spell(Base):
    __tablename__ = "spell"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    kingdoms = relationship(
        "Kingdom", secondary=kingdom_spell_relation, back_populates="spells"
    )


kingdom_building_relation = Table(
    "building_kingdom_relation",
    Base.metadata,
    Column("kingdom_id", ForeignKey("kingdom.id"), primary_key=True),
    Column("building_id", ForeignKey("building.id"), primary_key=True),
)


class Building(Base):
    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    kingdoms = relationship(
        "Kingdom", secondary=kingdom_building_relation, back_populates="buildings"
    )


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

    spells = relationship(
        "Spell", secondary=kingdom_spell_relation, back_populates="kingdoms"
    )

    buildings = relationship(
        "Building", secondary=kingdom_building_relation, back_populates="kingdoms"
    )


    def __str__(self):
        spellsS     = "\n".join([f"- {spell}" for spell in self.spells])
        buildingsLS = "\n".join([f"- {building}" for building in self.buildings])
        
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
        print("L: Kelola hubungan perjanjian")
        print("M: Membangun sesuatu")
        
        if self.level>=5:
            print("N: Latih Prajurit seharga ${:,} (saat ini Anda memiliki {:,})".format(self.soldierPrice, self.soldiers))
        if self.level>=10:
            print("O: Buat Mortir seharga ${:,} (saat ini Anda memiliki {:,})".format(self.mortarPrice, self.mortars))
        if self.level>=15:
            print("P: Buat Rudal seharga ${:,} (saat ini Anda memiliki {:,})".format(self.missilePrice, self.missiles))
        if self.level>=20:
            print("Q: Buat Nuklir seharga ${:,} (saat ini Anda memiliki {:,})".format(self.nukePrice, self.nukes))
        if self.level>=25:
            print("R: Buat Bom H seharga ${:,} (saat ini Anda memiliki {:,})".format(self.hbombPrice, self.hbombs))
        if self.level>=30:
            print("S: Buat Bom Lubang Hitam seharga ${:,} (saat ini Anda memiliki {:,})".format(self.bhbombPrice, self.bhbombs))
        
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
            self.population         -= (0.1*pop)
            
            print("- ${:,}".format(moneyAdd))
            print("- {:,} bahan bangunan".format(buildAdd))
            print("- {:,} lahan baru".format(landAdd))
            print("- {:,} lebih banyak makanan\n".format(foodAdd))
            print("Namun, Anda telah kehilangan {:,} orang-orang dalam perang.\n\n".format(int(0.1*pop)))
            time.sleep(2)
        elif warPoints < enemyWarPoints:
            playsound('sounds/piano-crash-sound-37898.wav')
            loseBy = enemyWarPoints-warPoints
            print("\n\nKamu kalah. Mereka menjarah kotamu dan mendapatkan banyak item:")
            
            moneySubtract   = int(0.5*loseBy)
            buildSubtract   = int(0.5*loseBy)
            landSubtract    = int(0.5*land)
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


session.add_all([
    Spell(name="Sihir Kemakmuran"),
    Spell(name="Sihir Kesuburan"),
    Spell(name="Sihir Kekayaan"),
    Spell(name="Sihir Kerja"),
    Spell(name="Sihir Pedang"),
    Spell(name="Sihir Perang"),
    Spell(name="Sihir Serangan"),
    Spell(name="Sihir Pertahanan"),
    Spell(name="Sihir Kehancuran"),
    Spell(name="Sihir Kebusukan"),
    Spell(name="Sihir Kematian"),
    Building(name="Monolit Batu"),
    Building(name="Orang-orangan Sawah"),
    Building(name="Patung Bayi"),
    Building(name="Patung Pembangun"),
    Building(name="Altar Pengorbanan"),
    Building(name="Kedutaan"),
    Building(name="Bazaar"),
    Building(name="Kuil"),
    Building(name="Menara Bisnis"),
    Building(name="Menara Kas"),
    Building(name="Monumen Kehidupan"),
])

session.commit()

Base.metadata.create_all(engine)