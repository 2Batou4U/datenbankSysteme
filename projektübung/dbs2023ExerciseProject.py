import json
import mariadb
from mariadb.constants import CLIENT


# NOTE: Don't change the interfaces.
class DatabaseProject:
    """
    DatabaseProject enthält alle wichtigen Methoden, um die von uns erstellte Fantasy-Welt zu testen.
    """

    def __init__(self):
        self.connection: mariadb.Connection | None = None

        with open('queries.json') as query_json:
            self.queries = json.load(query_json)

    def connectToMariaDB(self, user: str, pw: str, host: str, database: str, port: int = 3306):
        """
        Connects to specified database and saves connection in 'connection' class variable.

        :param user: Username for the Database specified.
        :param pw: Password of the user for the Database specified.
        :param host: IP address of the Database specified.
        :param database: Name of the Database specified.
        :param port: Port of the Database specified. Default value is '3306'
        :return: Error if anything goes wrong; Else returns nothing.
        """
        try:
            self.connection = mariadb.connect(
                user=user,
                password=pw,
                host=host,
                port=port,
                database=database,
                client_flag=CLIENT.MULTI_STATEMENTS,
            )

        except mariadb.DatabaseError as d_err:
            return d_err

    def disconnect(self):
        """
        Disconnects from the database saved in 'connection'.

        :return: Error if anything goes wrong; Else returns nothing.
        """
        try:
            self.connection.close()
        except mariadb.DatabaseError as d_err:
            return d_err

    def createProjectDBTables(self):
        """
        Creates all the tables needed for testing inside our project.

        :return: Error if anything goes wrong; Else returns nothing.
        """
        cursor = self.connection.cursor()
        try:
            for query in self.queries:
                print(f"Erstelle Tabelle '{query}'...")
                cursor.execute(self.queries[query])

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

        finally:
            self.connection.commit()

    # delete all project related tables
    def deleteAllProjectTables(self):
        """
        Code for cleaning up the database shamelessly stolen from StackOverflow. :)

        :return: Error if anything goes wrong; Else returns nothing.
        """
        cursor = self.connection.cursor()
        try:
            print(f"Lösche alle Tabellen...")

            cursor.execute(f"""
            SET FOREIGN_KEY_CHECKS=0;
            SET @tables = NULL;
            SELECT GROUP_CONCAT('`', table_schema, '`.`', table_name,'`') INTO @tables FROM information_schema.tables 
            WHERE table_schema = 'fantasy_welt';
            SET @tables = CONCAT('DROP TABLE ', @tables);
            PREPARE stmt1 FROM @tables;
            EXECUTE stmt1;
            DEALLOCATE PREPARE stmt1;
            SET FOREIGN_KEY_CHECKS=1;
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    # yes handling IDs manually is not optimal, however for our little project and for testing this should be
    # manageable! Implement all create and delete methods for each entity
    def createEigenschaft(self, eigenschaftenID: int, name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into eigenschaften (eigenschaften_id, beschreibung) 
            values ({eigenschaftenID}, '{name}');
            """)
        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def createItem(self, itemID: int, name: str, geldwert: int, besitzerID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into item (item_id, name, geldwert, besitzer) 
            values ({itemID}, '{name}', {geldwert}, {besitzerID});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def createEigenschaftenBesitzen(self, itemID: int, eigenschaftenID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into eigenschaftenbesitzen (eigenschaften_id, item_id) 
            values ({eigenschaftenID}, {itemID});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def createShop(self, besitzerID: int, name: str, geld: int, adresse: str, ladenBesitzer: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into besitzer (besitzer_id, name, geld) 
            values ({besitzerID}, '{name}', {geld});
            
            insert into ort (besitzer_id, adresse) 
            values ({besitzerID}, '{adresse}');
            
            insert into shop (besitzer_id, ladenbesitzer) 
            values ({besitzerID}, '{ladenBesitzer}');
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def createDungeon(self, besitzerID: int, name: str, geld: int, adresse: str, schwierigkeitsgrad: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into besitzer (besitzer_id, name, geld) 
            values ({besitzerID}, '{name}', {geld});

            insert into ort (besitzer_id, adresse) 
            values ({besitzerID}, '{adresse}');

            insert into dungeon (besitzer_id, schwierigkeitsgrad) 
            values ({besitzerID}, {schwierigkeitsgrad});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def createTeam(self, besitzerID: int, avatarName: str, geld: int, staerke: int, magie: int, geschwindigkeit: int,
                   rang: int, waffenPref: str, geburtsdatum: str, geburtsort: str, istIn: int, affinitaet: int,
                   haustierID: int, haustierName: str, kampfkraft: int, rasse: str, niedlichkeitsfaktor: float):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into besitzer (besitzer_id, name, geld) 
            values ({besitzerID}, '{avatarName}', {geld});

            insert into avatar (besitzer_id, staerke, magie, geschwindigkeit, rang, waffenpref, geburtsdatum, 
            geburtsort, istin) 
            values ({besitzerID}, {staerke}, {magie}, {geschwindigkeit}, {rang}, '{waffenPref}', DATE '{geburtsdatum}', 
            '{geburtsort}', {istIn});

            insert into haustier (haustier_id, name, kampfkraft, rasse, niedlichkeitsfaktor) 
            values ({haustierID}, '{haustierName}', {kampfkraft}, '{rasse}', {niedlichkeitsfaktor});

            insert into team (besitzer_id, haustier_id, affinitaet) 
            values ({besitzerID}, {haustierID}, {affinitaet});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def createDuellieren(self, avatar1: int, avatar2: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            insert into duellieren (AID1, AID2) 
            values ({avatar1}, {avatar2});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteEigenschaft(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from eigenschaften 
            where (eigenschaften_id = {id});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteItem(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from item 
            where (item_id = {id});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteEigenschaftenBesitzen(self, itemId: int, eigenschaftenID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from eigenschaftenbesitzen 
            where (eigenschaften_id= {eigenschaftenID}) 
            and (item_id = {itemId});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteShop(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from besitzer 
            where exists
            (select * from shop 
            where (shop.besitzer_id = besitzer.besitzer_id) 
            and (besitzer_id = {id}));
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteDungeon(self, id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from besitzer 
            where exists
            (select * from dungeon 
            where (dungeon.besitzer_id = besitzer.besitzer_id) 
            and (besitzer_id = {id});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteTeam(self, besitzerID: int, haustierID: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from haustier 
            where (haustier_id = {haustierID});
            
            delete from besitzer 
            where (besitzer_id = {besitzerID});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def deleteDuellieren(self, besitzerID1: int, besitzerID2: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"""
            delete from duellieren 
            where (aid1 = {besitzerID1} and aid2 = {besitzerID2}) 
            or (aid1 = {besitzerID2} and aid2 = {besitzerID1});
            """)

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    """
    Die Test-Müllhalde für unsere Datenbank.
    """

    def createWorld(self):

        self.deleteAllProjectTables()
        self.createProjectDBTables()

        self.createEigenschaft(eigenschaftenID=1001, name="Brennen")
        self.createEigenschaft(eigenschaftenID=1002, name="Fruchtig")

        self.createShop(besitzerID=2001, name="Edeka", geld=99999, adresse="Area 51", ladenBesitzer="Udo Lindenberg")

        self.createDungeon(besitzerID=6001, name="Datenbanksysteme", geld=1000, adresse="Universität", schwierigkeitsgrad=5)
        self.createDungeon(besitzerID=6002, name="Arbeitswelt", geld=500, adresse="McDonalds", schwierigkeitsgrad=9)

        self.createTeam(besitzerID=4001, avatarName="Eivor", geld=5000, staerke=740, magie=500, geschwindigkeit=320,
                        rang=50, waffenPref="Assassinen-Klinge", geburtsdatum="0900-12-23", geburtsort="Norwegen",
                        istIn=6002, affinitaet=100, haustierID=5001, haustierName="Sýnin", kampfkraft=1, rasse="Rabe",
                        niedlichkeitsfaktor=0.8)

        self.createTeam(besitzerID=4002, avatarName="Geralt", geld=80, staerke=600, magie=400, geschwindigkeit=500,
                        rang=25, waffenPref="Silberschwert", geburtsdatum="1168-01-18", geburtsort="Rivia",
                        istIn=6002, affinitaet=100, haustierID=5002, haustierName="Einhorn", kampfkraft=0, rasse="Einhorn",
                        niedlichkeitsfaktor=1.0)

        self.createTeam(besitzerID=4003, avatarName="V", geld=25000, staerke=999, magie=0, geschwindigkeit=999, rang=50,
                        waffenPref="Monowire", geburtsdatum="2049-06-10", geburtsort="Night City", istIn=2001,
                        affinitaet=20, haustierID=5003, haustierName="Johnny", kampfkraft=9999, rasse="Mensch",
                        niedlichkeitsfaktor=0.1)

        self.createTeam(besitzerID=4004, avatarName="Atzmüller", geld=99999, staerke=300, magie=0, geschwindigkeit=250,
                        rang=99, waffenPref="Notenvergabe", geburtsdatum="1970-01-01", geburtsort="Erde", istIn=2001,
                        affinitaet=500, haustierID=5004, haustierName="Student", kampfkraft=1, rasse="Geringverdiener",
                        niedlichkeitsfaktor=1.0)

        self.createTeam(besitzerID=4005, avatarName="Prüfungsamt", geld=999, staerke=999, magie=999, geschwindigkeit=999,
                        rang=99, waffenPref="Fehlversuch", geburtsdatum="0001-01-01", geburtsort="Jenseits", istIn=6001,
                        affinitaet=1, haustierID=5005, haustierName="Beamter", kampfkraft=0, rasse="Arbeitsdrohne",
                        niedlichkeitsfaktor=0.0)

        self.createDuellieren(avatar1=4001, avatar2=4002)
        self.createDuellieren(avatar1=4003, avatar2=4004)
        self.createDuellieren(avatar1=4002, avatar2=4003)
        self.createDuellieren(avatar1=4005, avatar2=4004)
        self.createDuellieren(avatar1=4002, avatar2=4005)
        self.createDuellieren(avatar1=4004, avatar2=4005)

        self.createItem(itemID=3001, name="Mojito", geldwert=1500, besitzerID=2001)
        self.createItem(itemID=3002, name="Tequila", geldwert=800, besitzerID=2001)
        self.createItem(itemID=3003, name="Vodka-O", geldwert=400, besitzerID=2001)

        self.createItem(itemID=3004, name="Old Fashioned", geldwert=2000, besitzerID=4003)

        self.createItem(itemID=3005, name="Datenbanksysteme-Schein", geldwert=500, besitzerID=4001)
        self.createItem(itemID=3009, name="Datenbanksysteme-Schein", geldwert=500, besitzerID=4004)

        self.createItem(itemID=3006, name="Fehlversuch", geldwert=0, besitzerID=4002)
        self.createItem(itemID=3007, name="Fehlversuch", geldwert=0, besitzerID=4002)
        self.createItem(itemID=3008, name="Fehlversuch", geldwert=0, besitzerID=4002)

        self.createEigenschaftenBesitzen(eigenschaftenID=1001, itemID=3002)
        self.createEigenschaftenBesitzen(eigenschaftenID=1002, itemID=3001)

        self.connection.commit()

    def doExerciseRA1(self) -> list[tuple]:
        """
        Geben Sie alle existierenden Rassen von Haustieren aus.
        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select distinct rasse from haustier
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseRA2(self) -> list[tuple]:
        """
        Geben Sie die AvatarIDs aller Spieler aus, die sich im Dungeon 'Datenbanksysteme'
        befinden.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select a.besitzer_id from avatar a 
            left join ort o on a.istin=o.besitzer_id 
            left join besitzer b on o.besitzer_id = b.besitzer_id 
            where b.name = 'Datenbanksysteme'
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseRA3(self) -> list[tuple]:
        """
        Geben Sie alle paare von AvatarIDs aus, die sich noch nicht duelliert haben.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select a1.besitzer_id as aid1, a2.besitzer_id as aid2 from avatar a1 
            cross join avatar a2 
            where a1.besitzer_id != a2.besitzer_id 
            except (select aid1, aid2 from duellieren)
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseTK1(self) -> list[tuple]:
        """
        Geben Sie den Item-Namen, den Avatar-Namen, sowie den Shop-Namen aus, bei
        Vorkomnissen in denen der Avatar, sowie der Shop zwar ein gleichnamiges Item
        besitzen, dieser im Shop jedoch mehr wert ist als beim Spieler.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select b1.name as avatar, b2.name as shop, s_item as item from 
            (select a.besitzer_id a_name, i1.name as a_item, i1.geldwert as a_geldwert, s.besitzer_id as s_name, 
                    i2.name as s_item, i2.geldwert as s_geldwert from 
            (item i1 left join avatar a on i1.besitzer = a.besitzer_id), 
            (item i2 left join shop s on i2.besitzer = s.besitzer_id) 
            where a.besitzer_id is not null) as output 
            join besitzer b1 on a_name=b1.besitzer_id 
            join besitzer b2 on s_name=b2.besitzer_id 
            where a_item=s_item 
            and s_geldwert>a_geldwert;
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseTK2(self) -> list[tuple]:
        """
        Geben Sie alle Eigenschaften aus, bei denen jedes Item mit jener Eigenschaft einen Geldwert > 1000 hat.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select distinct eb.eigenschaften_id from eigenschaftenbesitzen eb
            right join item on item.item_id = eb.item_id 
            where item.geldwert > 1000
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseTK3(self) -> list[tuple]:
        """
        Geben Sie die Dungeons aus, in denen keiner der Spieler das Item 'Datenbanksysteme-Schein' besitzt, es jedoch
        im Dungeon enthalten ist.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select d.besitzer_id from dungeon d 
            where d.besitzer_id not in 
            (select distinct d.besitzer_id from dungeon d 
            inner join avatar a on d.besitzer_id = a.istin 
            left outer join item i1 on a.besitzer_id = i1.besitzer 
            left outer join item i2 on d.besitzer_id = i2.besitzer 
            where i1.name = 'Datenbanksysteme-Schein' 
            and i2.name = 'Datenbanksysteme-Schein')
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseDK1(self) -> list[tuple]:
        """
        Geben Sie die AvatarID der Spieler aus, die zu ihren Haus-
        tieren eine Affinität >= 80% besitzen.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select besitzer_id from team 
            where affinitaet >0.8
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseDK2(self) -> list[tuple]:
        """
        Geben Sie die AvatarID der Spieler aus, die sich zwar mit dem Avatar 'Atzmüller'
        duelliert haben, jedoch nicht das Item 'Datenbanksysteme-Schein' besitzen.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select d.aid1 from duellieren d 
            left join besitzer b on d.aid2 = b.besitzer_id 
            where d.aid1 not in 
            (select besitzer from item i 
            where i.name = 'Datenbanksysteme-Schein') 
            and b.name = 'Atzmüller'
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseDK3(self) -> list[tuple]:
        """
        Geben Sie die Namen aller Haustiere aus, bei denen die Kampfstärke > 9000 und
        der Niedlichkeitsfaktor >= 80% ist. Nutzen Sie dabei keine Exists-Quantifizierung.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select h.name from team t 
            natural join haustier h 
            where h.kampfkraft > 9000 
            and h.niedlichkeitsfaktor >= 0.8
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL1(self) -> list[tuple]:
        """
        Geben Sie die Waffe wieder, welche gerade am häufigsten bevorzugt ist.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select a.waffenpref, COUNT(a.waffenpref) as anzahl from avatar a 
            group by a.waffenpref 
            order by anzahl desc 
            limit 1
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL2(self) -> list[tuple]:
        """
        Geben Sie die durchschnittliche Niedlichkeit aller Haustiere aus, von den Avataren, die gerade weniger als
        500 Geld besitzen und sich gleichzeitig in einem Dungeon befinden, welcher ein Item beinhaltet,
        den kein Laden besitzt.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select AVG(h.niedlichkeitsfaktor) as niedlichkeit from haustier h 
            natural join team t 
            natural join avatar a 
            join besitzer b on a.besitzer_id = b.besitzer_id 
            where b.geld < 500 
            and a.istin in 
            (select d.besitzer_id from dungeon d 
            join item i on d.besitzer_id = i.besitzer 
            where i.name not in
            (select i.name from shop s 
            join item i on s.besitzer_id = i.besitzer ))
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL3(self) -> list[tuple]:
        """
        Geben Sie aus, wie viele Avatare das Item 'Datenbanksysteme-Schein' besitzen, geteilt durch die Anzahl aller
        'Datenbanksysteme-Schein'-Items, die existieren.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select 
            (select count(*) as spieler_anz from avatar a 
            join item i on i.besitzer = a.besitzer_id 
            where i.name = 'Datenbanksysteme-Schein') 
            /
            (select count(*) as item_anz from item i 
            where i.name = 'Datenbanksysteme-Schein');
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL4(self) -> list[tuple]:
        """
        Geben Sie jeden Avatar, der nach dem 1.1.200 geboren worden ist. Sortieren Sie diese Daten nach Geburtsdatum.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            select * from avatar a 
            where geburtsdatum > date('2000-1-1') 
            order by geburtsdatum desc;
            """)

            return cursor.fetchall()

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL5(self) -> list[tuple]:
        """
        Finden Sie jeden Avatar, der sich in einem Laden befindet und weniger als 100 Geld hat. Ändern Sie seinen
        Standort auf den Dungeon 'Arbeitswelt'

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            update avatar a
            join besitzer b on a.besitzer_id = b.besitzer_id
            join shop s on a.istin = s.besitzer_id
            set a.istin = (select besitzer_id from besitzer where name = 'Arbeitswelt' limit 1)
            where b.geld <= 100;
            """)

            return [('Status', 'Update ausgeführt.')]

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL6(self) -> list[tuple]:
        """
        Löschen Sie alle Avatare, die sich mit dem Avatar 'Prüfungsamt' duelliert haben und drei Items mit dem Namen
        'Fehlversuch' besitzen.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            delete from avatar 
            where besitzer_id = (select b1.besitzer_id from avatar a
            join besitzer b1 on a.besitzer_id = b1.besitzer_id
            join duellieren d on a.besitzer_id = d.aid1
            join besitzer b2 on d.aid2 = b2.besitzer_id
            where b2.name = 'Prüfungsamt'
            and (select count(*) from item
            where name = 'Fehlversuch'
            and besitzer = b1.besitzer_id) >= 3);
            """)

            return [('Status', 'Löschen ausgeführt.')]

        except mariadb.IntegrityError as i_err:
            print(f"█ Etwas ist schief gelaufen: {i_err}")

    def doExerciseSQL7(self) -> list[tuple]:
        """
        Erstellen Sie eine Sicht für einen Dieb, die diesem nur erlaubt den aufsummierten, durchschnittlichen Geldbesitz
        (Geld + Item-Wert) eines Besitzers anzusehen, jedoch nicht die genauen Items. Die Summe soll in 5000er-Schritten
        sein.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        pass

    def doExerciseSQL8(self) -> list[tuple]:
        """
        Erstellen Sie einen Trigger, welcher einen Avatar zum Dungeon 'Arbeitswelt' verschiebt, wenn dieser sich im
        Dungeon 'Datenbanksysteme' befindet und das Item 'Datenbanksysteme-Schein' besitzt.

        :return: Liste aus Tupeln mit Ergebnissen.
        """
        pass
