from dbs2023ExerciseProject import DatabaseProject

dbs_test = DatabaseProject()

dbs_test.connectToMariaDB(user="adrian", pw="pomi2013S", host="152.89.239.24", port=3306, database="fantasy_welt")

dbs_test.createWorld()

# Test zu RA1
ra1: list[tuple] = dbs_test.doExerciseRA1()
for data in ra1:
    print(f"""'{data[0]}' ist eine Haustierrasse.""")

# Test zu RA2
ra2: list[tuple] = dbs_test.doExerciseRA2()
for data in ra2:
    print(f"""Avatar {data[0]} befindet sich in Dungeon: 'Datenbanksysteme'.""")

# Test zu RA3
ra3: list[tuple] = dbs_test.doExerciseRA3()
for data in ra3:
    print(f"""Avatar {data[0]} hat Avatar {data[1]} noch nicht duelliert.""")

# Test zu TK1
tk1: list[tuple] = dbs_test.doExerciseTK1()
for data in tk1:
    print(f"""Das Item {data[2]} ist bei dem Avatar {data[0]} mehr Wert als im Shop {data[1]}.""")

# Test zu TK2
tk2: list[tuple] = dbs_test.doExerciseTK2()
for data in tk2:
    print(f"""Alle Items mit Eigenschaft {data[0]} sind wertvoll (>1000 Geld).""")

# Test zu TK3
tk3: list[tuple] = dbs_test.doExerciseTK3()
for data in tk3:
    print(f"""Der Dungeon {data[0]} hat das Item 'Datenbanksysteme-Schein', aber die Avatare vor Ort nicht.""")

# Test zu DK1
dk1: list[tuple] = dbs_test.doExerciseDK1()
for data in dk1:
    print(f"""Avatar {data[0]} hat zu seinem Haustier eine Affinität größer als 80%.""")

# Test zu DK2
dk2: list[tuple] = dbs_test.doExerciseDK2()
for data in dk2:
    print(f"""Avatar {data[0]} hat sich mit Atzmüller duelliert, ohne einen Datenbanksysteme-Schein zu besitzen.""")

# Test zu DK3
dk3: list[tuple] = dbs_test.doExerciseDK3()
for data in dk3:
    print(f"""Haustier {data[0]} hat eine Kampfkraft > 9000 und einen Niedlichkeitsfaktor >= 0.8.""")

# Test zu SQL1
sql1: list[tuple] = dbs_test.doExerciseSQL1()
for data in sql1:
    print(f"""Die bevorzugte Waffe der Spieler ist '{data[0]}'. {data[1]} Spieler bevorzugen diese Waffe.""")

# Test zu SQL2
sql2: list[tuple] = dbs_test.doExerciseSQL2()
for data in sql2:
    print(f"""Ich schreibe die Bedingungen nicht ab. Das Ergebnis ist '{data[0]}'.""")
