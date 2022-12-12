from sqlalchemy import Column, Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///game.db", echo=True, future=True)

Base = declarative_base()

class Player(Base):
    __tablename__ = "player_account"

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(30))
    is_online = Column(Boolean)

    kingdom = relationship("Kingdom", back_populates="ruler", uselist=False)

association_table = Table(
    "association_table",
    Base.metadata,
    Column("kingdom_id", ForeignKey("kingdom.id"), primary_key=True),
    Column("spell_id", ForeignKey("spell_table.id"), primary_key=True),
)

class Spell(Base):
    __tablename__ = "spell_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    kingdoms = relationship(
        "Kingdom", secondary=association_table, back_populates="spells"
    )
    

class Kingdom(Base):
    __tablename__ = "kingdom"
    
    id = Column(Integer, primary_key=True)
    # player_id = Column(Integer, ForeignKey("player_account.id"))
    
    ruler = relationship("Player", back_populates="kingdom")
    
    age = Column(String(50), default="Zaman Batu")
    name = Column(String(30))
    diffMult = Column(Float, default=1)
    kingdom_relationship = Column(Integer, default=5)

    birth = Column(Boolean, default=True)
    death = Column(Integer, default=1)

    daysUntil = Column(Integer, default=0)
    birthRes = Column(Integer, default=0)

    soldiers = Column(Integer, default=0)
    soldierPrice= Column(Integer, default=100)
    
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    levelUp = Column(Integer, default=200)

    population = Column(Integer, default=300)
    popGrowth = Column(Integer, default=5)
    popDeath = Column(Integer, default=1)
    
    buildMaterials = Column(Integer, default=50)
    buildMaterialsPro = Column(Integer, default=1)
    buildProUpgradePrice = Column(Integer, default=10)
    buildProLevel = Column(Integer, default=1)

    land = Column(Integer, default=1)

    money = Column(Integer, default=50)    
    moneyPro = Column(Integer, default=1)
    moneyProLevel = Column(Integer, default=1)
    moneyProUpgradePrice = Column(Integer, default=10)
    
    defenseLevel = Column(Integer, default=1)
    defenseUpgradePrice = Column(Integer, default=10)
    defenseUpgradeBuildCost = Column(Integer, default=10)

    mortars = Column(Integer, default=0)
    mortarprice = Column(Integer, default=500)

    missiles = Column(Integer, default=0)
    missileprice = Column(Integer, default=2000)

    nukes = Column(Integer, default=0)
    nukeprice = Column(Integer, default=700)

    hbombs = Column(Integer, default=0)
    hbombPrice = Column(Integer, default=10000)
    
    bhbombs=Column(Integer, default=0)
    bhbombPrice=Column(Integer, default=20000)

    food = Column(Integer, default=300)
    foodProCan = Column(Boolean, default=True)
    foodPro = Column(Integer, default=300)
    foodDaysUntil = Column(Integer, default=0)
    foodres = Column(Integer, default=0)
    foodProUpgradePrice = Column(Integer, default=50)
    foodProLevel = Column(Integer, default=1)

    spells = relationship(
        "Spell", secondary=association_table, back_populates="kingdoms"
    )

Base.metadata.create_all(engine)