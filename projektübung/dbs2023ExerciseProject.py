import json

import mariadb
import sys
# hide password
import getpass


# Example use in for example jupyter notebook:
# from dbs2023ExerciseProject import DatabaseProject
# dbsp = DatabaseProject()
# dbsp.connectToMariaDB('root', getpass.getpass(), 'localhost', 3306, 'dbName')
# dbsp.createProjectDBTables()
# ...

# NOTE: Don't change the interfaces.
class DatabaseProject:

    # connect to mariaDB. Handle connection object with class variable self.connection
    # NOTE: Database should be 
    # created beforehand because the mariadb package does not support the CREATE DATABASE statement!
    def __init__(self):
        self.connection: mariadb.Connection | None = None

        with open('queries.json') as query_json:
            self.queries = json.load(query_json)

        with open('commands.json') as command_json:
            self.commands = json.load(command_json)

    def connectToMariaDB(self, user: str, pw, host: str, port: int, database: str):
        try:
            self.connection = mariadb.connect(
                user=user,
                password=pw,
                host=host,
                port=port,
                database=database
            )
        except mariadb.DatabaseError as derr:
            return derr

    # disconnect from mariaDB
    def disconnect(self):
        try:
            self.connection.close()
        except mariadb.DatabaseError as derr:
            return derr

    # create all tables for the project.
    def createProjectDBTables(self):
        cursor = self.connection.cursor()

        for query in self.queries:
            print(f"Erstelle Tabelle '{query}'...")
            cursor.execute(self.queries[query])

        self.connection.commit()

    # delete all project related tables
    def deleteAllProjectTables(self):
        cursor = self.connection.cursor()

        print("Lösche alle Tabellen...")
        for command in self.commands['delete']:
            cursor.execute(command)

        self.connection.commit()

    # yes handling IDs manually is not optimal, however for our little project and for testing this should be
    # manageable! Implement all create and delete methods for each entity
    def createEigenschaft(self, eigenschaftenID: int, name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['create_eigenschaft'].format(eigenschaftenID=eigenschaftenID, name=name))
        except mariadb.IntegrityError:
            print("Eintrag existiert bereits! :(")
        self.connection.commit()

    def createItem(self, itemID: int, name: str, geldwert: int, besitzerID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['create_item'].format(itemID=itemID, name=name, geldwert=geldwert, besitzerID=besitzerID))
        except mariadb.IntegrityError:
            print("Eintrag existiert bereits! :(")
        self.connection.commit()

    def createEigenschaftenBesitzen(self, itemID: int, eigenschaftenID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                self.commands['create_eigenschaftenBesitzen'].format(itemID=itemID, eigenschaftenID=eigenschaftenID))
        except mariadb.IntegrityError:
            print("Eintrag existiert bereits! :(")
        self.connection.commit()

    def createShop(self, besitzerID: int, name: str, geld: int, adresse: str, ladenBesitzer: str):
        cursor = self.connection.cursor()
        try:
           cursor.execute(self.commands['create_shop'][0].format(besitzerID=besitzerID, name=name, geld=geld))
           cursor.execute(self.commands['create_shop'][1].format(besitzerID=besitzerID, adresse=adresse))
           cursor.execute(self.commands['create_shop'][2].format(besitzerID=besitzerID, ladenBesitzer=ladenBesitzer))
        except mariadb.IntegrityError:
            print("Eintrag existiert bereits! :(")
        self.connection.commit()

    def createDungeon(self, besitzerID: int, name: str, geld: int, adresse: str, schwierigkeitsgrad: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['create_dungeon'][0].format(besitzerID=besitzerID, name=name, geld=geld))
            cursor.execute(self.commands['create_dungeon'][1].format(besitzerID=besitzerID, adresse=adresse))
            cursor.execute(self.commands['create_dungeon'][2].format(besitzerID=besitzerID, schwierigkeitsgrad=schwierigkeitsgrad))
        except mariadb.IntegrityError:
            print("Eintrag existiert bereits! :(")
        self.connection.commit()

    def createTeam(self, besitzerID: int, avatarName: str, geld: int, staerke: int, magie: int, geschwindigkeit: int,
                   rang: int, waffenPref: str, geburtsdatum: str, geburtsort: str, istIn: int, affinitaet: int,
                   haustierID: int, haustierName: str, kampfkraft: int, rasse: str, niedlichkeitsfaktor: float):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['create_team'][0].format(besitzerID=besitzerID, avatarName=avatarName, geld=geld))
            cursor.execute(self.commands['create_team'][1].format(besitzerID=besitzerID, staerke=staerke, magie=magie, geschwindigkeit=geschwindigkeit, rang=rang, waffenPref=waffenPref, geburtsdatum=geburtsdatum, geburtsort=geburtsort, istIn=istIn))
            cursor.execute(self.commands['create_team'][2].format(haustierID=haustierID, haustierName=haustierName, kampfkraft=kampfkraft, rasse=rasse, niedlichkeitsfaktor=niedlichkeitsfaktor))
            cursor.execute(self.commands['create_team'][3].format(besitzerID=besitzerID, haustierID=haustierID, affinitaet=affinitaet))
        except mariadb.IntegrityError:
            print("Eintrag existiert bereits! :(")
        self.connection.commit()

    def createDuellieren(self, avatar1: int, avatar2: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['create_duellieren'].format(avatar1=avatar1, avatar2=avatar2))
        except mariadb.IntegrityError as err:
            print(err)
        self.connection.commit()

    def deleteEigenschaft(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['delete_eigenschaft'].format(id=id))

        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()

    def deleteItem(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['delete_item'].format(id=id))

        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()

    def deleteEigenschaftenBesitzen(self, itemId: int, eigenschaftenID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['delete_eigenschaftenbesitzen'].format(itemID=itemId, eigenschaftenID=eigenschaftenID))

        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()

    def deleteShop(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(self.commands['delete_shop'].format(id=id))
        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()

    def deleteDungeon(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                self.commands['delete_dungeon'].format(id=id))

        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()
    def deleteTeam(self, besitzerID: int, haustierID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                self.commands['delete_team'].format(haustierID=haustierID))

        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()

    def deleteDuellieren(self, besitzerID1: int, besitzerID2: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                self.commands['delete_duellieren'].format(aid1=besitzerID1, aid2=besitzerID2))

        except mariadb.IntegrityError:
            print("Zu löschender Eintrag existiert nicht! :(")
        self.connection.commit()

    # Befüllt die Tabellen mit den Instanzen ihrer Wahl um die SQL-Abfragen zu testen
    def createWorld(self):

        self.createProjectDBTables()

        self.createEigenschaft(1, "Brennen")
        self.createShop(besitzerID=2, name="Orgienladen", geld=99999, adresse="G35", ladenBesitzer="Atzmueller")
        self.createItem(1, "Mojito", 12, 2)
        self.createDungeon(besitzerID=3, name="Adrians Einöde", geld=9, adresse="Dunkelwald", schwierigkeitsgrad=3)
        self.createTeam(61, "Helmut", 6, 10, 5000, 1, 50, "Flasche", "2000-05-12", "Erde", 2, 20, 1, "Hugo", 9001,
                            "Dackel", 1.0)
        self.createTeam(60, "Helga", 6, 10, 5000, 1, 50, "Flasche", "2000-05-12", "Erde", 2, 20, 2, "Huga", 9001,
                            "Dackel", 1.0)
        self.createDuellieren(60, 61)
        self.createEigenschaftenBesitzen(1, 1)

    # Geben Sie eine List aus, mit allen Rassen von existierenden Haustieren.
    def doExerciseRA1(self):
        pass

    # Geben Sie jede Avatar ID aus, welche sich im Dungeon mit dem Namen "Datenbanksysteme" befindet.
    def doExerciseRA2(self):
        pass

    # Gib jedes Avatar-ID-Paar aus, welches sich noch nicht duelliert hat.
    def doExerciseRA3(self):
        pass

    # Selektieren Sie ein Tripel, welches aus Item-Name, Avatar-Name und Shop-Name besteht, in welchem der Avatar und
    # der Shop beide ein gleichnamiges Item besitzen, der Geldwert im Shop des Items jedoch größer ist, als beim Item
    # des Avatars.
    def doExerciseTK1(self):
        pass

    # Selektieren Sie alle Eigenschaften, wo jedes Item mit dieser Eigenschaft einen Geldwert von größer 1000 hat. 
    def doExerciseTK2(self):
        pass

    # Selektieren Sie jeden Dungeon, in welchem jeder sich vor Ort befindenden Avatar nicht das Item 
    # ''Datenbanksysteme-Schein'' besitzt, es jedoch im Dungeon enthalten ist.
    def doExerciseTK3(self):
        pass

    # Geben Sie jede Avatar ID aus, welcher zu seinem Haustier-Partner eine Affinität größer 80% hat.
    def doExerciseDK1(self):
        pass

    # Geben Sie jede Avatar ID aus, der sich mit dem Avatar ''Atzmüller'' duelliert hat und nicht das Item 
    # ''Datenbanksysteme-Schein'' besitzt.
    def doExerciseDK2(self):
        pass

    # Geben Sie die Namen aller Haustiere aus, mit einer Kampfstärke größer 9000 und einem Niedlichkeitsfaktor von 
    # mindestens 80% an. Nutzen Sie dabei keine Exists Quantifizierung.
    def doExerciseDK3(self):
        pass

    # Geben Sie die Waffe wieder, welche gerade am häufigsten bevorzugt ist.
    def doExerciseSQL1(self):
        pass

    # Geben Sie die durchschnittliche Niedlichkeit aller Haustiere aus, von den Avataren, die gerade mit weniger als 
    # 500 Geld, die gleichzeitig in einem Dungeon sind, welcher ein Item beinhaltet, der in keinem Laden vorhanden ist.
    def doExerciseSQL2(self):
        pass

    # Geben Sie aus, wie viele Avatare das Item ''Datenbanksysteme-Schein'' besitzen, geteilt durch die Anzahl aller 
    # ''Datenbanksysteme-Schein''-Items die existieren.
    def doExerciseSQL3(self):
        pass

    # Geben Sie jeden Avatar aus, der nach 1.1.2000 geboren wurden. Absteigend sortiert nach Geburtsdatum.
    def doExerciseSQL4(self):
        pass

    # Ändern Sie den Ort von jedem Avatar, welcher sich in einem Laden befindet und weniger als 100 Geld hat zum 
    # Dungeon ''Arbeitswelt''.
    def doExerciseSQL5(self):
        pass

    # Löschen Sie alle Avatare, die sich mit dem Avatar ''Prüfungsamt'' duelliert haben und dreimal das Item 
    # ''Fehlversuch'' haben.
    def doExerciseSQL6(self):
        pass

    # Erstellen Sie eine Sicht für einen Dieb, die dem Dieb nur erlaubt den aufsummierten durchschnittlichen 
    # Geld-Besitzt (Besessenes Geld + Geldwert aller Items) in 500er-Schritten eines Besitzers zu sehen, jedoch nicht
    # die genauen Items.
    def doExerciseSQL7(self):
        pass

    # Erstellen Sie einen Trigger, welcher einen Avatar zum Dungeon ''Arbeitswelt'' verschiebt, wenn dieser sich im 
    # Dungeon ''Datenbanksysteme'' befindet und das Item ''Datenbanksysteme-Schein'' besitzt.
    def doExerciseSQL8(self):
        pass
