import time
import sys
import random

from pygame import mixer 
from playsound import playsound

from sqlalchemy import select
from sqlalchemy.orm import Session


# from functions import *
from models import *

mixer.init()
mixer.music.load('sounds/Main.mp3')
mixer.music.play()


# engine = create_engine("sqlite:///game.db", echo=True, future=True)
engine = create_engine("mysql+pymysql://root:@localhost/clash_of_clans", echo=True)

session = Session(engine)

# age="Zaman Batu"
relationship=5
# endgame=False
# soldiers=0
# soldierprice=100
# points=0
# level=166
# levelup=200
popgrowth=5
enemypopgrowth=5
# popdeath=1
enemypopdeath=2
# deathcan=True
# land=1
# buildmaterials=5000000
# buildmaterialspro=1
# money=500000000
# day=1
# pop=300
# buildproupgradeprice=10
# buildprolevel=1
# moneypro=1
# moneyprolevel=1
# moneyproupgradeprice=10
# defenselevel=1
# defenseupgradeprice=10
# defenseupgradebuildcost=10
enemypop=300
enemydefenselevel=1
# exploreprice=10
defenseupgradelandcost=1
enemysoldiers=0
# mortars=0
# mortarprice=500
enemymortars=0
# missiles=0
# missileprice=2000
enemymissiles=0
# nukes=0
# nukeprice=7000
enemynukes=0
# hbombs=0
# hbombprice=10000
enemyhbombs=0
# bhbombs=0
# bhbombprice=20000
enemybhbombs=0
# food=300
# foodpro=300
# foodproupgradeprice=50
# foodprolevel=1
# daysuntil=0
# birth=True
# birthres=0
# foodres=0
# foodprocan=True
spells=[]
sword=1
# war2=1 => warMult
attack=1
defense=1
destruction=1
waste=1
death=1
# consumpmult=1
# prodmult=1
# birthmult=1
# diffmult=1
buildingsL=[]
popadd=0
# deathadd=0

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
        player = result.fetchone()
        
        if player == None:
            print("\n\nUsername atau password salah!!!\n\n")
        else:
            print("\n\nAnda berhasil login")
            break
        
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

else:
    sys.exit()


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
player.kingdom = Kingdom(name=kingdom_name, diffmult=diffmult)

kingdom = player.kingdom

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

            kingdom.spells.append("Sihir Kemakmuran")
            kingdom.spells.append("Sihir Kesuburan")
            kingdom.spells.append("Sihir Kekayaan")
            kingdom.spells.append("Sihir Kerja")
            kingdom.spells.append("Sihir Pedang")
            kingdom.spells.append("Sihir Perang")
            kingdom.spells.append("Sihir Serangan")
            kingdom.spells.append("Sihir Pertahanan")
            kingdom.spells.append("Sihir Kehancuran")
            kingdom.spells.append("Sihir Kebusukan")
            kingdom.spells.append("Sihir Kematian")
            kingdom.spells.append("Sihir Kemakmuran")
            kingdom.spells.append("Sihir Kesuburan")
            kingdom.spells.append("Sihir Kekayaan")
            kingdom.spells.append("Sihir Kerja")
            kingdom.spells.append("Sihir Pedang")
            kingdom.spells.append("Sihir Perang")
            kingdom.spells.append("Sihir Serangan")
            kingdom.spells.append("Sihir Pertahanan")
            kingdom.spells.append("Sihir Kehancuran")
            kingdom.spells.append("Sihir Kebusukan")
            kingdom.spells.append("Sihir Kematian")

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
    
    # enemypopgrowth  = int(enemypop/90)
    # enemypopdeath   = int(enemypop/150)
    kingdom.prodMaterials()
    kingdom.makeMoney()
    kingdom.birthPopulation()
    kingdom.deathPopulation()
    kingdom.prodFood()
    kingdom.consumeFood()    
    # enemypop += enemypopgrowth
    # enemypop -= enemypopdeath
    
    # <!------Masih perlu diganti-----!>
    # <!------AWAL-----!>
    r = [ int(x*diffmult) for x in (40, 40, 50, 70, 100, 150, 200) ]

    ranint = [ random.randint(1, x) for x in r ]

    if ranint[0] == 1:
        enemydefenselevel = enemydefenselevel+1
    
    if kingdom.level>=5:
        if ranint[1] == 1:
            enemysoldiers += 1
    if kingdom.level>=10:
        if ranint[2] == 1:
            enemymortars += 1
    if kingdom.level>=15:
        if ranint[3] == 1:
            enemymissiles += 1
    if kingdom.level>=20:
        if ranint[4] == 1:
            enemynukes += 1
    if kingdom.level>=25:
        if ranint[5] == 1:
            enemyhbombs += 1
    if kingdom.level>=30:
        if ranint[6] == 1:
            enemybhbombs += 1
    # <!------AKHIR------!>

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

        # else:
        #     print("Anda tidak memiliki perjanjian dengan {}!\n\n".format(name))
        #     points -= level*50

    elif dailydecision == "f":
        # if tradewith==1:
        #     print("Anda memiliki perjanjian dengan {}, jadi Anda tidak dapat menyerang mereka.".format(name))
        # else:
            
        # relationship -= 2
        # if relationship < 0:
        #     relationship = 0

        kingdom.war()

    elif dailydecision == "g":
        if exploreprice > money:
            print("Tidak cukup uang!\n\n")
            points -= level*50
        else:
            landgain = int((0.5*land)+1)
            money -= exploreprice
            land +=landgain
            exploreprice = int(1.8*exploreprice)
            exploregainNum = random.randint(1,9)
            if exploregainNum == 1:
                spells.append("Sihir Kemakmuran")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kemakmuran!\n\n".format(landgain))
            elif exploregainNum == 2:
                spells.append("Sihir Kesuburan")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kesuburan!\n\n".format(landgain))
            elif exploregainNum == 3:
                spells.append("Sihir Kekayaan")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kekayaan!\n\n".format(landgain))
            elif exploregainNum == 4:
                spells.append("Sihir Kerja")
                print("Anda pergi menjelajah dan menemukan {:,} lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kerja!\n\n".format(landgain))
            elif exploregainNum == 5:
                if level < 5:
                    spells.append("Sihir Pedang")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Pedang!\n\n")
                elif level < 10:
                    spells.append("Sihir Perang")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Perang!\n\n")
                elif level < 15:
                    spells.append("Sihir Serangan")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Serangan!\n\n")
                elif level < 20:
                    spells.append("Sihir Pertahanan")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Pertahanan!\n\n")
                elif level < 25:
                    spells.append("Sihir Kehancuran")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kehancuran!\n\n")
                elif level<30:
                    spells.append("Sihir Kebusukan")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kebusukan!\n\n")
                else:
                    spells.append("Sihir Kematian")
                    print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan. Anda juga menemukan buku Sihir yang mengajarkan Anda Sihir Kematian!\n\n")
            else:
                print("Anda pergi menjelajah dan menemukan "+str("{:,}".format(landgain))+" lahan.")
            points += level*50

    elif dailydecision == "i":
        wildcard = random.randint(1,10)
        
        if wildcard == 1:
            moneygain = int(0.7*money)+1
            print("Beberapa petani menemukan peti harta karun tersembunyi yang berisi {:,} di dalam lahan ketika sedang membajak ladang mereka.\n\n".format(moneygain))
            money += moneygain
        elif wildcard == 2:
            buildloss = int(0.3*buildmaterials)
            print("Seorang pekerja yang kikuk menjatuhkan {:,} bahan bangunan ke dalam lubang tak berujung yang tak berujung, di mana bahan bangunan itu tidak pernah terlihat lagi.\n\n".format(buildloss))
            buildmaterials -= buildloss
        elif wildcard == 3:
            foodgain = int(0.3*food)+2
            print("Beberapa pelancong menemukan gudang yang ditinggalkan dengan {:,} makanan di dalamnya.\n\n".format(foodgain))
            food += foodgain
        elif wildcard == 4:
            popgrowth = 0
            pop -= 50
            birth = False
            birthres = 10
            print("Sebuah meteor menghantam daratan, menyebabkan kematian 50 orang. Radiasi juga menyebabkan tingkat kelahiran menjadi 0 selama 10 hari.\n\n")
        elif wildcard == 5:
            pointsneeded = levelup - points
            points += pointsneeded
            print("Anda menemukan gubuk penyihir dan dia dengan murah hati memberi Anda poin yang cukup untuk naik level!\n\n")
        elif wildcard == 6:
            tradewith = 0
            print("Penasihat kerajaan Anda yang tidak kompeten secara tidak sengaja mengirimkan catatan yang kejam kepada {}. Hal ini membuat mereka marah, sehingga mereka menghentikan perjanjian Anda.\n\n".format(name))
        elif wildcard == 7:
            buildgain = int(0.4*buildmaterials)+1
            buildmaterials = buildmaterials+buildgain
            print("Anda menemukan sebuah bangunan dalam kondisi yang cukup baik, dan merobohkannya untuk menggunakan kembali {:,} bahan bangunan.\n\n".format(buildgain))
        elif wildcard == 8:
            foodloss = int((0.3*food)-1)
            food -= foodloss
            foodpro = int(0.5*foodpro)
            foodres = 3
            fooddaysuntil = 0
            foodprocan = False
            print("Karena serangan angin, Anda kehilangan {:,} makanan dan produksi makanan Anda berkurang setengahnya selama 3 hari.\n\n".format(foodloss))
        elif wildcard == 9:
            sp = random.randint(1,5)
            if sp == 1:
                spells.append("Sihir Kemakmuran")
                print("Anda mendapatkan Sihir Kemakmuran! Sihir ini akan menaikkan level Anda 1 level dalam produksi makanan.\n\n")
            elif sp == 2:
                spells.append("Sihir Kesuburan")
                print("Anda mendapatkan Sihir Kesuburan! Sihir ini akan memberikan Anda 100 populasi.\n\n")
            elif sp == 3:
                spells.append("Sihir Kekayaan")
                print("Anda mendapatkan Sihir Kekayaan! Sihir ini akan menaikkan level Anda 1 level dalam produksi uang.\n\n")
            elif sp == 4:
                spells.append("Sihir Kerja")
                print("Anda mendapatkan Sihir Kerja! Sihir ini akan menaikkan level Anda 1 level dalam produksi bahan bangunan.\n\n")
            elif sp == 5:
                if level < 5:
                    spells.append("Sihir Pedang")
                    print("Anda mendapatkan Sihir Pedang! Sihir ini akan memberikan anda 1.1 kali poin perang anda dalam pertempuran.\n\n")            
                elif level<10:
                    spells.append("Sihir Perang")
                    print("Anda mendapatkan Sihir Perang! Sihir ini akan memberikan Anda 1.5 kali poin perang Anda dalam pertempuran.\n\n")
                elif level<15:
                    spells.append("Sihir Serangan")
                    print("Anda mendapatkan Sihir Serangan! Sihir ini akan memberikan Anda 1.7 kali poin perang Anda dalam pertempuran.\n\n")
                elif level<20:
                    spells.append("Sihir Pertahanan")
                    print("Kamu mendapatkan Sihir Pertahanan! Sihir ini akan memberikan Anda 2 kali poin perang Anda dalam pertempuran.\n\n")
                elif level<25:
                    spells.append("Sihir Kehancuran")
                    print("Anda mendapatkan Sihir Kehancuran! Sihir ini akan memberikan Anda 2.5 kali poin perang Anda dalam pertempuran.\n\n")
                elif level<30:
                    spells.append("Sihir Kebusukan")
                    print("Anda mendapatkan Sihir Kebusukan! Sihir ini akan memberikan Anda 2.7 kali poin perang Anda dalam pertempuran.\n\n")
                else:
                    spells.append("Sihir Kematian")
                    print("Kamu mendapatkan Sihir Kematian! Sihir ini akan memberikan Anda 3 kali poin perang Anda dalam pertempuran.\n\n")
        else:
            points -= points+1
            print("Seorang penyihir jahat menyebabkan poin Anda turun di bawah 0 jadi sekarang Anda turun level.")

    elif dailydecision == "j":
        print("Berikut adalah Sihir yang Anda miliki:")
        
        for spell in list(set(spells)):
            print("- {}".format(spell))
        
        print("A: Sihir Kemakmuran")
        print("B: Sihir Kesuburan")
        print("C: Sihir Kekayaan")
        print("D: Sihir Kerja")
        print("E: Sihir Pedang")

        if level < 10:
            print("F: Sihir Perang")
        if level < 15:
            print("G: Sihir Serangan")
        if level < 20:
            print("H: Sihir Pertahanan")
        if level < 25:
            print("I: Sihir Penghancuran")
        if level < 30:
            print("J: Sihir Kebusukan")
        if level >= 30:
            print("K: Sihir Kematian")
        
        spe = str(input("Pilih salah satu spell : "))
        spe = spe.lower()
        
        if spe=="a":
            if "Sihir Kemakmuran" in spells:
                playsound('sounds/godong.wav')
                print("Anda tiba-tiba mendengar suara tanaman yang tumbuh...\n\n")
                foodprolevel += 1
                foodpro += (100*foodprolevel)
                thing = spells.index("Sihir Kemakmuran")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="b":
            if "Sihir Kesuburan" in spells:
                playsound('sounds/babywhine1-6318.wav')
                print("Anda tiba-tiba mendengar suara tangisan bayi...\n\n")
                pop += 100
                thing = spells.index("Sihir Kesuburan")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="c":
            if "Sihir Kekayaan" in spells:
                playsound('sounds/cha-ching-7053_1.wav')
                print("Anda tiba-tiba mendengar suara koin bergemerincing...\n\n")
                moneyprolevel += 1
                moneypro += int((1.5*moneyprolevel))
                thing = spells.index("Sihir Kekayaan")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="d":
            if "Sihir Kerja" in spells:
                playsound('sounds/palu.wav')
                print("Anda tiba-tiba mendengar suara palu berdenting...\n\n")
                buildprolevel += 1
                buildmaterialspro += int((1.5*buildprolevel))
                thing = spells.index("Sihir Kerja")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="e":
            if "Sihir Pedang" in spells:
                playsound('sounds/swingg.wav')
                print("Anda tiba-tiba mendengar suara pedang yang berdesir...\n\n")
                sword = 1.1
                thing = spells.index("Sihir Pedang")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -=level*50
        elif spe=="f":
            if "Sihir Perang" in spells:
                playsound('sounds/auuu.wav')
                print("Anda tiba-tiba mendengar suara teriakan pertempuran...\n\n")
                war2 = 1.5
                thing = spells.index("Sihir Perang")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="g":
            if "Sihir Serangan" in spells:
                playsound('sounds/auuu.wav')
                print("Anda tiba-tiba mendengar suara pasukan yang bergegas ke medan perang...\n\n")
                attack = 1.7
                thing = spells.index("Sihir Serangan")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="h":
            if "Sihir Pertahanan" in spells:
                playsound('sounds/sword-battle-jingle-loop-96983.wav')
                print("Anda tiba-tiba mendengar suara pedang mengenai perisai...\n\n")
                defense = 2
                thing=spells.index("Sihir Pertahanan")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="i":
            if "Sihir Kehancuran" in spells:
                playsound('sounds/rock-destroy-6409.wav')
                print("Anda tiba-tiba mendengar suara bangunan runtuh...\n\n")
                destruction = 2.5
                thing = spells.index("Sihir Kehancuran")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
        elif spe=="j":
            if "Sihir Kebusukan" in spells:
                playsound('sounds/wither.wav')
                print("Anda tiba-tiba melihat banyak kehiduan layu...\n\n")
                waste = 2.7
                thing = spells.index("Sihir Kebusukan")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -=level*50

        elif spe=="k":
            if "Sihir Kematian" in spells:
                playsound('sounds/demonic-woman-scream-6333.wav')
                print("Anda tiba-tiba mendengar suara jeritan...\n\n")
                death = 3
                thing = spells.index("Sihir Kematian")
                spells.pop(thing)
            else:
                print("Anda tidak memiliki Sihir ini!\n\n")
                points -= level*50
    
    elif dailydecision == "k":
        print("Hukum apa yang ingin Anda ubah?")
        print("A: Hukum kelahiran")
        print("B: Hukum kerja")
        d = str(input())
        d = d.lower()
        if d == "a":
            print("Bagian apa yang ingin Anda ubah?")
            print("A: Ubah hukum kelahiran menjadi Terbatas (1/2x reguler)")
            print("B: Ubah hukum kelahiran menjadi Reguler (default)")
            print("C: Ubah hukum kelahiran menjadi Berlimpah (2x reguler)")
            d1 = str(input())
            d1 = d1.lower()
            if d1=="a":
                birthmult = 0.5
            elif d1=="c":
                birthmult = 2
            else:
                birthmult = 1
            
            print("Berhasil diubah!")
        else:
            print("Bagian apa yang ingin Anda ubah?")
            print("A: Ubah hukum kerja menjadi Lambat (orang mengkonsumsi x1/2 makanan dari biasanya, tetapi produksi uang dan bahan bangunan x1/2)")
            print("B: Ubah hukum kerja menjadi Reguler (default)")
            print("C: Ubah hukum kerja menjadi Efisien (produksi uang dan bahan bangunan x2, tetapi orang mengkonsumsi makanan x2 lebih banyak dari biasanya)")
            d2 = str(input())
            d2 = d2.lower()
            if d2 == "a":
                consumpmult = 0.5
                prodmult = 0.5
            elif d2 == "c":
                consumpmult = 2
                prodmult = 2
            else:
                consumpmult = 1
                prodmult = 1

            print("Berhasil diubah!")
    
    elif dailydecision == "l":
        print("Apa yang ingin Anda lakukan?")
        print("1: Membatalkan perjanjian yang sudah ada")
        print("2: Mengusulkan perjanjian")
        t = int(input())
        
        if t == 1:
            if tradewith == 0:
                print("Tidak ada perjanjian untuk membatalkan!")
            else:
                tradewith = 0
                relationship -= 1
                print("Perjanjian dibatalkan!")
        else:
            if tradewith == 1:
                print("Anda sudah memiliki perjanjian!")
            else:                
                if relationship <= 2:
                    if relationship <= 0:
                        r = random.randint(1,5)
                    else:
                        r = random.randint(1,3)

                    if r == 1:
                        tradewith = 1
                        relationship=relationship+random.randint(1,2)
                        print("{} telah dengan hati-hati menerima proposal perjanjian Anda!\n\n".format(name))
                    else:
                        print("{} telah menolak proposal perjanjian Anda!\n\n".format(name))
                
                elif relationship == 3:
                    r = random.randint(1,3)
                    if r == 1:
                        print("{} telah menolak proposal perjanjian Anda!\n\n".format(name))
                    else:
                        tradewith = 1
                        relationship = 4
                        print("{} telah menerima proposal perjanjian Anda!\n\n".format(name))
                else:
                    tradewith = 1
                    relationship = 5
                    print("Perjanjian dibuat!\n\n")

    elif dailydecision == "m":
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

    elif dailydecision == "n":
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

    elif dailydecision == "o":
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

    elif dailydecision == "p":
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

    elif dailydecision == "q":
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

    elif dailydecision == "r":
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

    elif dailydecision == "s":
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
    
    elif dailydecision == "x":
        kingdom.endGame = True
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
