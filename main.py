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


engine = create_engine("mysql+pymysql://root:@localhost/clash_of_clans", echo=True)

session = Session(engine)

builts = [ "Belum dibangun" for _ in range(11) ]

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
        player = result.fetchone()[0]
        
        if player == None:
            print("\n\nUsername atau password salah!!!\n\n")
        else:
            print("\n\nAnda berhasil login")
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
        is_online=True
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
        kingdom.exploreLand()

    elif dailydecision == "i":
        kingdom.randomEvent()

    elif dailydecision == "j":
        kingdom.useSpell()

    elif dailydecision == "k":
        kingdom.changeLaw()

    elif dailydecision == "l":
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

    elif dailydecision == "m":
        if level >= 5:
            if soldierprice > money:                
                print("Tidak cukup uang!\n\n")
                points -= level*50
            else:
                playsound('sounds/clanks-89017.wav')
                money -= soldierprice
                soldiers +=1
                soldierprice += (15*soldiers)
                print("Berhasil diBuat!\n\n")
                points += level*100
        else:
            print()
            print()

    elif dailydecision == "n":
        if level >= 10:
            if mortarprice > money:
                print("Tidak cukup uang!\n\n")
                points -= level*50
            else:
                playsound('sounds/clanks-89017.wav')
                money -=mortarprice
                mortars += 1
                mortarprice += (15*mortars)
                print("Berhasil diBuat!\n\n")
                points += level*150
        else:
            print()
            print()

    elif dailydecision == "o":
        if level >= 15:
            if missileprice > money:
                print("Tidak cukup uang!\n\n")
                points -= level*50
            else:
                playsound('sounds/clanks-89017.wav')
                money -= missileprice
                missiles += 1
                missileprice += (15*missiles)
                print("Berhasil diBuat!\n\n")
                points += level*150
        else:
            print()
            print()

    elif dailydecision == "p":
        if level >= 20:
            if nukeprice > money:
                print("Tidak cukup uang!\n\n")
                points -= level*50
            else:
                playsound('sounds/clanks-89017.wav')
                money -= nukeprice
                nukes += 1
                nukeprice += (15*nukes)
                print("Berhasil diBuat!\n\n")
                points += level*150
        else:
            print()
            print()

    elif dailydecision == "q":
        if level >= 25:
            if hbombprice > money:
                print("Tidak cukup uang!\n\n")
                points -= level*50
            else:
                playsound('sounds/clanks-89017.wav')
                money -= hbombprice
                hbombs += 1
                hbombprice += (15*hbombs)
                print("Berhasil diBuat!\n\n")
                points += level*150
        else:
            print()
            print()

    elif dailydecision == "r":
        if level >= 30:
            if bhbombprice > money:
                print("Tidak cukup uang!\n\n")
                points -= level*50
            else:
                playsound('sounds/clanks-89017.wav')
                money -= bhbombprice
                bhbombs += 1
                bhbombprice += (15*bhbombs)
                print("Berhasil diBuat!\n\n")
                points += level*150
        else:
            print()
            print()
    
]    elif dailydecision == "x":
        break
    else:
        print()
        print()
    
    time.sleep(1)
    kingdom.day += 1

    if pop<=0:
        print("Populasi Anda menjadi nol. Kerajaan Anda...")
        time.sleep(1)
        print("\n hancur.")
        time.sleep(0.5)
        print("Anda kalah.")
        time.sleep(2)
        kingdom.endGame = True
