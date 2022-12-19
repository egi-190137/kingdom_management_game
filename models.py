import time
from playsound import playsound
import random

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import select

from sqlalchemy.orm import Session


engine = create_engine("mysql+pymysql://root:@localhost/clash_of_clans", echo=False)

Base = declarative_base()

session = Session(engine)

class Player(Base):
    __tablename__ = "player_account"

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(30))
    is_online = Column(Boolean)

    kingdom = relationship("Kingdom", back_populates="ruler", uselist=False)

    def __str__(self):
        return self.username


class KingdomSpellRelation(Base):
    __tablename__ = "spell_kingdom_relation"

    id = Column(Integer, primary_key=True)

    kingdom_id = Column(Integer, ForeignKey("kingdom.id"))
    spell_id = Column(Integer, ForeignKey("spell.id"))

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

    id = Column(Integer, primary_key=True)
    
    kingdom_id = Column(Integer, ForeignKey("kingdom.id"))
    building_id = Column(Integer, ForeignKey("building.id"))

    kingdom = relationship("Kingdom", back_populates="building_relations")
    building = relationship("Building", back_populates="kingdoms_relation")


class Building(Base):
    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    kingdoms_relation = relationship("KingdomBuildingRelation", back_populates="building")

    def __str__(self):
        return self.name


class WarLog(Base):
    __tablename__ = "war_log"

    id = Column(Integer, primary_key=True)
    
    id_penyerang = Column(Integer, ForeignKey("kingdom.id"))
    id_musuh = Column(Integer, ForeignKey("kingdom.id"))

    warPoints = Column(Integer, default=0)
    moneyAdd = Column(Integer, default=0)
    enemyWarPoints = Column(Integer, default=0) 
    buildAdd = Column(Integer, default=0)
    landAdd = Column(Integer, default=0)
    foodAdd = Column(Integer, default=0)
    popDeath = Column(Integer, default=0)
    enemyPopDeath = Column(Integer, default=0)
    pointsAdd = Column(Integer, default=0)

    def getNamaPenyerang(self):
        query = select(Kingdom.name).where(Kingdom.id == self.id_penyerang)
        result = session.execute(query)
        kingdom = result.fetchone()[0]
        return kingdom
    
    def getNamaMusuh(self):
        query = select(Kingdom.name).where(Kingdom.id == self.id_musuh)
        result = session.execute(query)
        kingdom = result.fetchone()[0]
        return kingdom
    
    def menangKalah(self, status):
        if self.warPoints == self.enemyWarPoints:
            return "PERTANDINGAN SERI"
        elif self.warPoints > self.enemyWarPoints:
            return "ANDA MENANG" if status == "menyerang" else "ANDA KALAH"
        else:
            return "ANDA MENANG" if status == "diserang" else "ANDA KALAH"



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

    money = Column(Integer, default=100)    
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
        spell_list = "\n".join([f"- {spell}" for spell in self.getAllSpells()])
        building_list = "\n".join([f"- {building}" for building in self.getAllBuildings()])
        
        kingdom_info = f"""\nHari {self.day:,} : 
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
"""
        if spell_list != "":
            kingdom_info += f"""Sihir: 
{spell_list}
"""
        if building_list != "":
            kingdom_info += f"""Bangunan: 
{building_list}
"""
        return kingdom_info


    def addSpell(self, spellName):
        spell = session.execute(
            select(Spell).where(Spell.name == spellName)
            ).fetchone()[0]
        
        relation = KingdomSpellRelation(spell=spell)

        self.spell_rellations.append(relation) 

        session.commit()


    def removeSpell(self, spellName):
        relation = session.execute(
            select(KingdomSpellRelation, Spell)
            .join(KingdomSpellRelation.spell)
            .where(
            (Spell.name==spellName) & 
            (KingdomSpellRelation.kingdom==self))
        ).fetchone()[0]

        self.spell_rellations.remove(relation)
        session.delete(relation)

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
        print("Apa yang ingin Anda lakukan, {}?".format(self.ruler.username))
        print("A: Tingkatkan produksi bahan bangunan seharga ${:,} (level saat ini: {:,})".format(self.buildProUpgradePrice, self.buildProLevel))
        print("B: Tingkatkan produksi uang seharga {:,} bahan bangunan (level saat ini: {:,})".format(self.moneyProUpgradePrice, self.moneyProLevel))
        print("C: Tingkatkan pertahanan seharga ${:,} dan {:,} bahan bangunan dan {:,} lahan (level saat ini: {:,})".format(self.defenseUpgradePrice, self.defenseUpgradeBuildCost, self.defenseUpgradeLandCost, self.defenseLevel))
        print("D: Tingkatkan produksi makanan seharga ${:,} (level saat ini: {:,}".format(self.foodProUpgradePrice, self.foodProLevel))
        print("E: Coba berdagang")
        print("F: Nyatakan perang")
        print("G: Log serangan")
        print("H: Log diserang")
        print("I: Jelajahi lahan baru seharga ${:,}".format(self.explorePrice))
        print("J: Kejadian Random")
        print("K: Mengeluarkan Sihir")
        print("L: Mengatur hukum lahan")
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
        
        print("Y/kunci lainnya: Hari berikutnya")
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
            starved = int((consumption-self.food)/self.consumpMult)
            self.population -= starved
            self.food = 0
            print("Anda tidak memiliki cukup makanan, jadi {} orang meninggal karena kelaparan.".format(starved))
            time.sleep(1)
        else:
            self.food = int(self.food-consumption)
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
    

    def showAttackLog(self, num=5):
        query = select(WarLog).where(WarLog.id_penyerang == self.id).order_by(WarLog.id.desc()).limit(num)
        result = session.scalars(query)
        logs = [ data for data in result ]
        
        print("=====LOG MENYERANG=====")
        print()

        if logs == []:
            print("\nAnda belum melakukan serangan\n")

        for log in logs:
            menangKalah = log.menangKalah(status="menyerang")
            logText = f"""Kerajaan musuh : {log.getNamaMusuh()}
Hasil pertandingan :
===={menangKalah}====
"""
            if menangKalah == "PERTANDINGAN SERI":
                logText += "Kalian seri. Tidak ada di antara kalian yang kehilangan apapun."
            else:
                if menangKalah == "ANDA MENANG":
                    logText += "Kerajaan anda mendapatkan : "
                else:
                    logText += "Kerajaan anda kehilangan : "
                
                logText += f"""
- ${abs(log.moneyAdd):,}
- {abs(log.buildAdd):,} bahan bangunan
- {abs(log.landAdd):,} lahan
- {abs(log.foodAdd):,} makanan
- {abs(log.pointsAdd):,} points
Anda telah kehilangan {log.popDeath:,} orang-orang dalam perang.\n\n
"""
                if menangKalah == "ANDA MENANG":
                    logText += "Kerajaan musuh kehilangan : "
                else:
                    logText += "Kerajaan musuh mendapatkan : "

                logText += f"""
- ${abs(log.moneyAdd):,}
- {abs(log.buildAdd):,} bahan bangunan
- {abs(log.landAdd):,} lahan
- {abs(log.foodAdd):,} makanan
- {abs(log.pointsAdd):,} points
Musuh anda telah kehilangan {log.enemyPopDeath:,} orang-orang dalam perang.\n\n"""
            print(logText)
            print()
            print()


    def showAttackedLog(self, num=5):
        query = select(WarLog).where(WarLog.id_musuh == self.id).order_by(WarLog.id_penyerang.desc()).limit(num)
        result = session.scalars(query)
        logs = [ data for data in result ]

        print("=====LOG DISERANG=====")
        if logs == []:
            print("\nAnda belum melakukan serangan\n")

        for log in logs:
            menangKalah = log.menangKalah(status="diserang")
            logText = f"""Kerajaan musuh : {log.getNamaPenyerang()}
Hasil pertandingan :
===={menangKalah}====
"""
            if menangKalah == "PERTANDINGAN SERI":
                logText += "Kalian seri. Tidak ada di antara kalian yang kehilangan apapun."
            else:
                if menangKalah == "ANDA MENANG":
                    logText += "Kerajaan anda mendapatkan : "
                else:
                    logText += "Kerajaan anda kehilangan : "
                
                logText += f"""
- ${abs(log.moneyAdd):,}
- {abs(log.buildAdd):,} bahan bangunan
- {abs(log.landAdd):,} lahan
- {abs(log.foodAdd):,} makanan
- {abs(log.pointsAdd):,} points
Anda telah kehilangan {log.enemyPopDeath:,} orang-orang dalam perang.\n\n
"""

                if menangKalah == "ANDA MENANG":
                    logText += "Kerajaan musuh kehilangan : "
                else:
                    logText += "Kerajaan musuh mendapatkan : "

                logText += f"""
- ${abs(log.moneyAdd):,}
- {abs(log.buildAdd):,} bahan bangunan
- {abs(log.landAdd):,} lahan
- {abs(log.foodAdd):,} makanan
- {abs(log.pointsAdd):,} points
Musuh anda telah kehilangan {log.popDeath:,} orang-orang dalam perang.\n\n
"""
            print(logText)
            print()
            print()


    def war(self):
        # Cari musuh secara random
        query = select(Kingdom, Player).join(Kingdom.ruler).where(
            (Kingdom.id != self.id) & (Player.is_online == 0))
        
        result = session.scalars(query)
        enemies = [ data for data in result ]

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
        
        if warPoints == enemyWarPoints:
            print("Kalian seri. Tidak ada di antara kalian yang kehilangan apapun.")
            time.sleep(1)

            log = WarLog(id_penyerang=self.id, id_musuh=enemy.id)
            
            session.add(log)

        else:
            winBy = warPoints - enemyWarPoints
            if winBy > 0: # jika menang
                playsound('sounds/success-fanfare-trumpets-6185.wav')
                print("\n\nKamu menang! Kamu menjarah kota mereka dan mendapatkan banyak item:")
                buildAdd    = int(0.5*winBy)+11
                landAdd     = int(0.5*winBy)
                foodAdd     = int(0.5*winBy)+50
                popDeath    = int(0.1*self.population)
                enemyPopDeath = int(0.5*enemy.population)
                pointsAdd = self.level*100

            else:
                playsound('sounds/piano-crash-sound-37898.wav')
                print("\n\nKamu kalah. Mereka menjarah kotamu dan mendapatkan banyak item:")
                buildAdd = int(0.5*winBy)
                landAdd = int(0.5*self.land)
                foodAdd = int(0.5*winBy)
                popDeath = int(0.5*self.population)
                enemyPopDeath = int(0.1*enemy.population)
                pointsAdd = (self.level*100)


            moneyAdd    = int(0.5*winBy)
            
            self.money += moneyAdd
            if self.money < 0:
                moneyAdd -= self.money
                self.money = 0
            
            enemy.money -= moneyAdd
            if enemy.money < 0:
                moneyAdd += enemy.money
                enemy.money = 0
            
            self.buildMaterials += buildAdd
            if self.buildMaterials < 0:
                buildAdd -= self.buildMaterials
                self.buildMaterials = 0

            enemy.buildMaterials -= buildAdd
            if enemy.buildMaterials < 0:
                buildAdd += enemy.buildMaterials
                enemy.buildMaterials = 0

            self.land += landAdd
            enemy.land -= landAdd
            
            self.food += foodAdd
            if self.food < 0:
                foodAdd -= self.food
                self.food = 0

            enemy.food -= foodAdd
            if enemy.food < 0:
                foodAdd += enemy.food
                enemy.food = 0

            self.population -= popDeath
            enemy.population -= enemyPopDeath

            self.points += pointsAdd
            if self.points < 0:
                self.level -= 1
                self.points = 0

            enemy.points -= pointsAdd
            if enemy.points < 0:
                enemy.level -= 1
                enemy.points = 0

            print("- ${:,}".format(abs(moneyAdd)))
            print("- {:,} bahan bangunan".format(abs(buildAdd)))
            print("- {:,} lahan".format(abs(landAdd)))
            print("- {:,} makanan\n".format(abs(foodAdd)))
            print("- {:,} points\n".format(abs(pointsAdd)))
            print("Anda telah kehilangan {:,} orang-orang dalam perang.\n\n".format(popDeath))
            time.sleep(2)

            log = WarLog(
                id_penyerang=self.id, 
                id_musuh=enemy.id,
                warPoints=warPoints,
                enemyWarPoints=enemyWarPoints,
                moneyAdd=moneyAdd,
                buildAdd=buildAdd,   
                landAdd=landAdd,
                foodAdd=foodAdd,
                popDeath=popDeath,
                enemyPopDeath=enemyPopDeath,
                pointsAdd=pointsAdd
            )

            session.add(log)
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
        session.commit()

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
        session.commit()


    def build(self):
        buildingList = [
            "Monolit Batu",
            "Orang-orangan Sawah",
            "Patung Bayi",
            "Patung Pembangun",
            "Altar Pengorbanan",
            "Bazaar",
            "Kuil",
            "Menara Bisnis",
            "Menara Kas",
            "Monumen Kehidupan",
        ]

        buildingInfo = [ ("Sudah dibangun" if self.checkBuildingExist(build) else "Belum dibangun") for build in buildingList ]

        print("Bangunan yang bisa Anda bangun:")
        print("A: Batu Monolit (1 lahan, 60 bahan bangunan). Efek:\n   - +$5/hari\n   ("+buildingInfo[0]+")")
        print("B: Orang-orangan sawah (1 lahan, 60 bahan bangunan). Efek:\n   - +100 makanan/hari\n   ("+buildingInfo[1]+")")
        print("C: Patung Bayi (1 lahan, 120 bahan bangunan). Efek:\n   - +2 populasi/hari\n   ("+buildingInfo[2]+")")
        print("D: Patung Pembangun (1 lahan, 200 bahan bangunan). Efek:\n   - +20 bahan bangunan/hari\n   ("+buildingInfo[3]+")")
        print("E: Altar Pengorbanan (2 lahan, 350 bahan bangunan, 20 populasi). Efek:\n   - +2 kematian/hari\n   - +1000 makanan/hari\n   ("+buildingInfo[4]+")")
        print("F: Bazaar (8 lahan, 700 bahan bangunan, $500). Efek:\n   - +$70/hari\n   - +75 bahan bangunan/hari\n   ("+buildingInfo[5]+")")
        print("G: Kuil (16 lahan, 1000 bahan bangunan, $1000). Efek:\n   - +50 populasi/hari\n   - +$100/hari\n   - +100 bahan bangunan/hari\n   ("+buildingInfo[6]+")")
        print("H: Menara Bisnis (32 lahan, 3000 bahan bangunan). Efek:\n   - +500 bahan bangunan/hari\n   ("+buildingInfo[7]+")")
        print("I: Menara Tunai (32 lahan, $3000). Efek:\n   - +$500/hari\n   ("+buildingInfo[8]+")")
        print("J: Monumen Kehidupan (64 lahan, 5000 bahan bangunan, $5000). Efek:\n   - Orang tidak lagi mati (kecuali orang yang mati sebagai korban)\n   ("+buildingInfo[9]+")")
        print("Kunci lainnya: batal")
        
        bdec = input()
        bdec = bdec.lower()

        if bdec not in "abcdefghij":
            return None

        idx = "abcdefghij".index(bdec)
        if buildingInfo[idx] == "Sudah dibangun":
            print("Anda sudah membangun gedung ini!\n\n")
        else:
            if idx == 0:
                if self.land >= 1:
                    if self.buildMaterials >= 60:
                        playsound('sounds/palu.wav')
                        self.land -= 1
                        self.buildMaterials -= 60
                        self.moneyPro += 5
                        print("Berhasil membangun Monolit Batu!\n\n")
                        self.addBuilding("Monolit Batu")
                        self.points += self.level*110
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 1:
                if self.land >= 1:
                    if self.buildMaterials >= 60:
                        playsound('sounds/palu.wav')
                        self.land -= 1
                        self.buildMaterials -= 60
                        self.foodPro += 100
                        print("Berhasil membangun Orang-orangan Sawah!\n\n")
                        self.addBuilding("Orang-orangan Sawah")
                        self.points += self.level*110
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 2:
                if self.land >= 1:
                    if self.buildMaterials >= 120:
                        playsound('sounds/palu.wav')
                        self.land -= 1
                        self.buildMaterials -= 120
                        self.popAdd += 2
                        print("Berhasil membuat Patung Bayi!\n\n")
                        self.addBuilding("Patung Bayi")
                        self.points += self.level*130
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 3:
                if self.land >= 1:
                    if self.buildMaterials >= 200:
                        playsound('sounds/palu.wav')
                        self.land -= 1
                        self.buildMaterials -= 200
                        self.buildMaterialsPro += 20
                        print("Berhasil membangun Patung Pembangun!\n\n")
                        self.addBuilding("Patung Pembangun")
                        self.points += self.level*150
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 4:
                if self.land >= 2:
                    if self.buildMaterials >= 350 and self.population >= 20:
                        playsound('sounds/palu.wav')
                        self.land -= 2
                        self.buildMaterials -= 350
                        self.population -= 20
                        self.foodPro += 1000
                        self.deathAdd += 2
                        print("Berhasil membangun Altar Pengorbanan, mengorbankan 20 orang tak berdosa dalam prosesnya!\n\n")
                        self.addBuilding("Altar Pengorbanan")
                        self.points += self.level*160
                    else:
                        print("Tidak cukup bahan bangunan/populasi!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 5:            
                if self.land >= 8:
                    if self.buildMaterials >= 700 and self.money >= 500:
                        playsound('sounds/palu.wav')
                        self.land -= 8
                        self.buildMaterials -= 700
                        self.money -= 500
                        self.moneyPro += 70
                        self.buildMaterialsPro += 75
                        print("Berhasil membangun Bazaar!\n\n")
                        self.addBuilding("Bazaar")
                        self.points += self.level*190
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 6:
                if self.land >= 16:
                    if self.buildMaterials >= 1000 and self.money >= 1000:
                        playsound('sounds/palu.wav')
                        self.land -= 16
                        self.buildMaterials -= 1000
                        self.money -= 1000
                        self.moneyPro += 100
                        self.buildMaterialsPro += 100
                        self.popAdd += 50
                        print("Berhasil membangun Kuil!\n\n")
                        self.addBuilding("Kuil")
                        self.points += self.level*200
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 7:
                if self.land >= 32:
                    if self.buildMaterials >= 3000:
                        playsound('sounds/palu.wav')
                        self.land -= 32
                        self.buildMaterials -= 3000
                        self.buildMaterialsPro += 500
                        print("Berhasil membangun Menara Bisnis!\n\n")
                        self.addBuilding("Menara Bisnis")
                        self.points += self.level*230
                    else:
                        print("Bahan bangunan tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 8:
                if self.land >= 32:
                    if self.money >= 3000:
                        playsound('sounds/palu.wav')
                        self.land -= 32
                        self.money -=3000
                        self.moneyPro += 500
                        print("Berhasil membangun Menara Kas!\n\n")
                        self.addBuilding("Menara Kas")
                        self.points += self.level*230
                    else:
                        print("Tidak cukup uang!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            elif idx == 9:
                if self.land >= 64:
                    if self.buildMaterials >= 5000 and self.money >= 5000:
                        playsound('sounds/palu.wav')
                        self.land -= 64
                        self.buildMaterials -=5000
                        self.money -= 5000
                        self.deathCan = False
                        print("Berhasil membangun Monumen Kehidupan! Orang tidak lagi mati, kecuali pengorbanan.\n\n")
                        self.addBuilding("Monumen Kehidupan")
                        self.points += self.level*260
                    else:
                        print("Bahan bangunan/uang tidak cukup!\n\n")
                        self.points -= self.level*50
                else:
                    print("Tidak cukup lahan!\n\n")
                    self.points -= self.level*50
            else:
                print("\n")
        session.commit()


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
        session.commit()


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
        session.commit()


    def createMissile(self):
        if self.level >= 15:
            if self.missilePrice > self.money:
                print("Tidak cukup uang!\n\n")
                self.points -= self.level*50
            else:
                playsound('sounds/clanks-89017.wav')
                self.money -= self.missilePrice
                self.missiles += 1
                self.missilePrice += (15*self.missiles)
                print("Berhasil diBuat!\n\n")
                self.points += self.level*150
        else:
            print()
            print()
        session.commit()


    def createNuke(self):
        if self.level >= 20:
            if self.nukePrice > self.money:
                print("Tidak cukup uang!\n\n")
                self.points -= self.level*50
            else:
                playsound('sounds/clanks-89017.wav')
                self.money -= self.nukePrice
                self.nukes += 1
                self.nukePrice += (15*self.nukes)
                print("Berhasil diBuat!\n\n")
                self.points += self.level*150
        else:
            print()
            print()
        session.commit()


    def createHBomb(self):
        if self.level >= 25:
            if self.hbombPrice > self.money:
                print("Tidak cukup uang!\n\n")
                self.points -= self.level*50
            else:
                playsound('sounds/clanks-89017.wav')
                self.money -= self.hbombPrice
                self.hbombs += 1
                self.hbombPrice += (15*self.hbombs)
                print("Berhasil diBuat!\n\n")
                self.points += self.level*150
        else:
            print()
            print()
        session.commit()
    

    def createBHBomb(self):
        if self.level >= 30:
            if self.bhbombPrice > self.money:
                print("Tidak cukup uang!\n\n")
                self.points -= self.level*50
            else:
                playsound('sounds/clanks-89017.wav')
                self.money -= self.bhbombPrice
                self.bhbombs += 1
                self.bhbombPrice += (15*self.bhbombs)
                print("Berhasil diBuat!\n\n")
                self.points += self.level*150
        else:
            print()
            print()
        session.commit()



Base.metadata.create_all(engine)

# Cek apakah tabel spell
query = select(Spell)
result = session.scalars(query)
spells = [ data for data in result ]

if spells == []:
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
        Spell(name="Sihir Kematian")
    ])

# Cek apakah tabel building masih kosong
query = select(Building)
result = session.scalars(query)
buildings = [ data for data in result ]

if buildings == []:
    session.add_all([
        Building(name="Monolit Batu"),
        Building(name="Orang-orangan Sawah"),
        Building(name="Patung Bayi"),
        Building(name="Patung Pembangun"),
        Building(name="Altar Pengorbanan"),
        Building(name="Bazaar"),
        Building(name="Kuil"),
        Building(name="Menara Bisnis"),
        Building(name="Menara Kas"),
        Building(name="Monumen Kehidupan"),
    ])

session.commit()
