from dbs2023ExerciseProject import DatabaseProject

dbs_test = DatabaseProject()

dbs_test.connectToMariaDB(user="adrian", pw="pomi2013S", host="152.89.239.24", port=3306, database="fantasy_welt")
dbs_test.deleteAllProjectTables()
dbs_test.createProjectDBTables()

dbs_test.createEigenschaft(1, "Brennen")
dbs_test.createShop(besitzerID=2, name="Orgienladen", geld=99999, adresse="G35", ladenBesitzer="Atzmueller")
dbs_test.createItem(1, "Mojito", 12, 2)
dbs_test.createDungeon(besitzerID=3, name="Adrians Einöde", geld=9, adresse="Dunkelwald", schwierigkeitsgrad=3)
dbs_test.createTeam(61, "Helmut", 6, 10, 5000, 1, 50, "Flasche", "2000-05-12", "Erde", 2, 20, 1, "Hugo", 9001, "Dackel", 1.0)
dbs_test.createTeam(60, "Helga", 6, 10, 5000, 1, 50, "Flasche", "2000-05-12", "Erde", 2, 20, 2, "Huga", 9001, "Dackel", 1.0)
dbs_test.createDuellieren(60, 61)
