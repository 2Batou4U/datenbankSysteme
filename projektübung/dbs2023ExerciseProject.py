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
        pass

    # delete all project related tables
    def deleteAllProjectTables(self):
        cursor = self.connection.cursor()

        print("Lösche alle Tabellen...")
        for command in self.commands['delete']:
            cursor.execute(command)

        self.connection.commit()
        pass

    # yes handling IDs manually is not optimal, however for our little project and for testing this should be
    # manageable! Implement all create and delete methods for each entity
    def createEigenschaft(self, eigenschaftenID: int, name: str):
        pass

    def createItem(self, itemID: int, name: str, geldwert: int, besitzerID: int):
        pass

    def createEigenschaftenBesitzen(self, itemID: int, eigenschaftenID: int):
        pass

    def createShop(self, besitzerID: int, name: str, geld: int, adresse: str, ladenBesitzer: str):
        pass

    def createDungeon(self, besitzerID: int, name: str, geld: int, adresse: str, schwierigkeitsgrad: int):
        pass

    def createTeam(self, besitzerID: int, avatarName: str, geld: int, stärke: int, magie: int, geschwindigkeit: int,
                   rang: int, waffenPref: str, geburtsdatum: str, geburtsort: str, istIn: int, affinität: int,
                   haustierID: int, haustierName: str, kampfkraft: int, rasse: str, niedichkeitsfaktor: float):
        pass

    def createDuellieren(self, avatar1: int, avatar2: int):
        pass

    def deleteEigenschaft(self, id: int):
        pass

    def deleteItem(self, id: int):
        pass

    def deleteEigenschaftenBesitzen(self, itemId: int, eigenschaftenID: int):
        pass

    def deleteShop(self, id: int):
        pass

    def deleteDungeon(self, id: int):
        pass

    def deleteTeam(self, besitzerID: int, haustierID: int):
        pass

    def deleteDuellieren(self, besitzerID1: int, besitzerID2: int):
        pass

    # Befüllt die Tabellen mit den Instanzen ihrer Wahl um die SQL-Abfragen zu testen
    def createWorld(self):
        pass

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
