import time
import sys
import random

from pygame import mixer 
from playsound import playsound
from sqlalchemy import select
from sqlalchemy.orm import Session


from models import *

mixer.init()
mixer.music.load('sounds/Main.mp3')
mixer.music.play()

print("Selamat datang di Kingdoms")
print("1. Login")
print("2. Register")
print("3. Exit")

pilih = int(input("\nPilih salah satu : "))

if pilih == 1:
    while True:
        username = input("Masukkan username : ")
        password = input("Masukkan password : ")
        
        query = select(Player).where(
            (Player.username==username) &
            (Player.password==password)
        )
        result = session.execute(query)
        player = result.fetchone()
        
        if player == None:
            print("\n\nUsername atau password salah!!!\n\n")
        else:
            print("\n\nAnda berhasil login")
            player = player[0]
            break
    
    kingdom = player.kingdom
    if kingdom.endGame:
        print("Kerajaan anda  telah  berakhir")
        sys.exit()
        
elif pilih == 2:
    username = input("Masukkan username : ")
    password = input("Masukkan password : ")

    player = Player(
        username=username,
        password=password,
        is_online=1
    )

    session.add(player)
    session.commit()

    print("\n\nSelamat datang di Kingdoms, sebuah permainan kerajaan di mana Anda meningkatkan, menaikkan level, dan mencoba mengalahkan musuh-musuh Anda.\n")
    time.sleep(1)

    # Cek apakah baru memulai game atau tidak
    # Jika baru maka tampilkan pilihan kesulitan
    print("Silakan pilih tingkat kesulitan lawan:")
    print("1: Super Mudah")
    print("2: Mudah")
    print("3: Normal")
    print("4: Susah")
    print("5: Sangat Susah")

    d = int(input())

    if d == 1:
        diffmult = 2
    elif d == 2:
        diffmult = 1.5
    elif d == 4:
        diffmult = 0.7
    elif d == 5:
        diffmult = 0.5
    else:
        diffmult = 1

    kingdom_name = input("Apa nama kerajaan Anda?: ")
    player.kingdom = Kingdom(name=kingdom_name, diffMult=diffmult)

    kingdom = player.kingdom
    session.add(kingdom)
    session.commit()

else:
    sys.exit()



print()
print("Selamat datang {}, penguasa {}.\n".format(kingdom.ruler, kingdom.name))
print(f"Anda mulai dengan {kingdom.population} orang di kerajaan Anda. Anda mulai dengan {kingdom.buildMaterials} bahan bangunan, {kingdom.money}$, {kingdom.food} makanan, dan memiliki {kingdom.land} lahan. Rakyat Anda menghasilkan {kingdom.foodPro} makanan/hari, {kingdom.buildMaterialsPro} bahan bangunan per hari, dan {kingdom.moneyPro}$ per hari.\n\n")

time.sleep(1)

while not kingdom.endGame:
    if kingdom.points >= kingdom.levelUp:
        kingdom.level += 1
        kingdom.points = 0
        kingdom.levelUp = int(kingdom.levelUp*1.5)
        print("\n\n\n\n-----------\n|NAIK LEVEL!|\n-----------\n\n\n\n")
        time.sleep(1)
        if kingdom.level == 5:
            playsound('sounds/tada-fanfare-a-6313.wav')
            print("Anda telah memasuki Zaman Tembaga!\nAnda mendapatkan unit baru: Prajurit!\n\n\n")
            kingdom.age = "Zaman Tembaga"
        elif kingdom.level == 10:
            playsound('sounds/tada-fanfare-a-6313.wav')
            print("Anda telah memasuki Zaman Perunggu!\nAnda mendapatkan unit baru: Mortir!\n\n\n")
            kingdom.age = "Zaman Perunggu"
        elif kingdom.level == 15:
            playsound('sounds/tada-fanfare-a-6313.wav')
            print("Anda telah memasuki Zaman Besi!\nAnda mendapatkan unit baru: Rudal!\n\n\n")
            kingdom.age = "Zaman Besi"
        elif kingdom.level == 20:
            playsound('sounds/tada-fanfare-a-6313.wav')
            print("Anda telah memasuki Abad Pertengahan!\nAnda mendapatkan unit baru: Nuklir!\n\n\n")
            kingdom.age = "Abad Pertengahan"
        elif kingdom.level == 25:
            playsound('sounds/tada-fanfare-a-6313.wav')
            print("Anda telah memasuki Zaman Modern!\nAnda mendapatkan unit baru: Bom H!\n\n\n")
            kingdom.age = "Zaman Modern"
        elif kingdom.level == 30:
            playsound('sounds/tada-fanfare-a-6313.wav')
            print("Anda telah memasuki Zaman Masa Depan!\nAnda mendapatkan unit baru: Bom Lubang Hitam!\n\n\n")
            kingdom.age = "Zaman Masa Depan"

            kingdom.addSpell("Sihir Kemakmuran")
            kingdom.addSpell("Sihir Kesuburan")
            kingdom.addSpell("Sihir Kekayaan")
            kingdom.addSpell("Sihir Kerja")
            kingdom.addSpell("Sihir Pedang")
            kingdom.addSpell("Sihir Perang")
            kingdom.addSpell("Sihir Serangan")
            kingdom.addSpell("Sihir Pertahanan")
            kingdom.addSpell("Sihir Kehancuran")
            kingdom.addSpell("Sihir Kebusukan")
            kingdom.addSpell("Sihir Kematian")
            kingdom.addSpell("Sihir Kemakmuran")
            kingdom.addSpell("Sihir Kesuburan")
            kingdom.addSpell("Sihir Kekayaan")
            kingdom.addSpell("Sihir Kerja")
            kingdom.addSpell("Sihir Pedang")
            kingdom.addSpell("Sihir Perang")
            kingdom.addSpell("Sihir Serangan")
            kingdom.addSpell("Sihir Pertahanan")
            kingdom.addSpell("Sihir Kehancuran")
            kingdom.addSpell("Sihir Kebusukan")
            kingdom.addSpell("Sihir Kematian")

        time.sleep(1)
    
    elif kingdom.points < 0:
        if kingdom.level > 1:
            kingdom.points = 0
            kingdom.level -= 1
            kingdom.levelUp = int(kingdom.levelUp/2)
            print("\n\n\n\n-------------\n|TURUN LEVEL!|\n-------------\n\n\n\n")
        else:
            kingdom.points = 0
            print("\n\n\n\n--------------------------------------\n|Poin Anda berada di bawah 0. Hati-hati!|\n--------------------------------------\n\n\n\n")
        
        time.sleep(2)
    
    kingdom.prodMaterials()
    kingdom.makeMoney()
    kingdom.birthPopulation()
    kingdom.deathPopulation()
    kingdom.prodFood()
    kingdom.consumeFood()    

    session.commit()

    print(kingdom)
    print()
    
    kingdom.showDecision()

    dailydecision = str(input())
    dailydecision = dailydecision.lower()
    
    if dailydecision == "a":
        kingdom.upgradeBuild()

    elif dailydecision == "b":
        kingdom.upgradeMoneyProd()
        
    elif dailydecision == "c":
        kingdom.upgradeDefense()

    elif dailydecision == "d":
        kingdom.upgradeFoodProd()

    elif dailydecision == "e":
        # if tradewith == 1:
        trade = str(input("Apa yang ingin Anda tukar ('b' untuk bahan bangunan, dan 'u' untuk uang): "))
        trade = trade.lower()
        if trade == "b":
            print("Pedagang akan menukarkan bahan bangunan dengan harga masing-masing $1.")
            tradenum = int(input("Berapa banyak yang ingin Anda perdagangkan?: "))

            kingdom.tradeBuilding(tradenum)

        elif trade == "u":
            print("Pedagang akan menukar masing-masing $1 untuk bahan bangunan.")
            tradenum=int(input("Berapa banyak yang ingin Anda perdagangkan?: "))

            kingdom.tradeMoney(tradenum)

    elif dailydecision == "f":
        kingdom.war()

    elif dailydecision == "g":
        kingdom.showAttackLog()

    elif dailydecision == "h":
        kingdom.showAttackedLog()

    elif dailydecision == "i":
        kingdom.exploreLand()

    elif dailydecision == "j":
        kingdom.randomEvent()

    elif dailydecision == "k":
        kingdom.useSpell()

    elif dailydecision == "l":
        kingdom.changeLaw()
        
    elif dailydecision == "m":
        kingdom.build()

    elif dailydecision == "n":
        kingdom.trainSoldier()

    elif dailydecision == "o":
        kingdom.createMortar()

    elif dailydecision == "p":
        kingdom.createMissile()

    elif dailydecision == "q":
        kingdom.createNuke()

    elif dailydecision == "r":
        kingdom.createHBomb()
    
    elif dailydecision == "s":
        kingdom.createBHBomb()

    elif dailydecision == "x":
        player.is_online = 0
        session.commit()
        break
    else:
        print()
        print()
    
    time.sleep(1)
    kingdom.day += 1
    session.commit()

    if kingdom.population <=0:
        print("Populasi Anda menjadi nol. Kerajaan Anda...")
        time.sleep(1)
        print("\n hancur.")
        time.sleep(0.5)
        print("Anda kalah.")
        time.sleep(2)
        kingdom.endGame = True
        
        session.commit()