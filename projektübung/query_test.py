from dbs2023ExerciseProject import DatabaseProject, DBSException
import logging


def start_test(clean_slate: bool, modify_data: bool):
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    dbs_test = DatabaseProject()

    try:
        dbs_test.connectToMariaDB(user="adrian", pw="pomi2013S", host="152.89.239.24", port=3306, database="fantasy_welt")

        if clean_slate:
            dbs_test.deleteAllProjectTables()
            dbs_test.createProjectDBTables()

            # Test zu SQL8 schon hier, wegen der Deklaration des Triggers
            sql8: list[tuple] = dbs_test.doExerciseSQL8()
            for data in sql8:
                logging.info(f"""{data[0]}: {data[1]}""")

            # Erstellt alle Datentupel zum Testen
            dbs_test.createWorld()

        # Test zu RA1
        ra1: list[tuple] = dbs_test.doExerciseRA1()
        for data in ra1:
            logging.info(f"""'{data[0]}' ist eine Haustierrasse.""")

        # Test zu RA2
        ra2: list[tuple] = dbs_test.doExerciseRA2()
        for data in ra2:
            logging.info(f"""Avatar {data[0]} befindet sich in Dungeon: 'Datenbanksysteme'.""")

        # Test zu RA3
        ra3: list[tuple] = dbs_test.doExerciseRA3()
        for data in ra3:
            logging.info(f"""Avatar {data[0]} hat Avatar {data[1]} noch nicht duelliert.""")

        # Test zu TK1
        tk1: list[tuple] = dbs_test.doExerciseTK1()
        for data in tk1:
            logging.info(f"""Das Item {data[2]} ist bei dem Avatar {data[0]} mehr Wert als im Shop {data[1]}.""")

        # Test zu TK2
        tk2: list[tuple] = dbs_test.doExerciseTK2()
        for data in tk2:
            logging.info(f"""Alle Items mit Eigenschaft {data[0]} sind wertvoll (>1000 Geld).""")

        # Test zu TK3
        tk3: list[tuple] = dbs_test.doExerciseTK3()
        for data in tk3:
            logging.info(
                f"""Der Dungeon {data[0]} hat das Item 'Datenbanksysteme-Schein', aber die Avatare vor Ort nicht.""")

        # Test zu DK1
        dk1: list[tuple] = dbs_test.doExerciseDK1()
        for data in dk1:
            logging.info(f"""Avatar {data[0]} hat zu seinem Haustier eine Affinität größer als 80%.""")

        # Test zu DK2
        dk2: list[tuple] = dbs_test.doExerciseDK2()
        for data in dk2:
            logging.info(
                f"""Avatar {data[0]} hat sich mit Atzmüller duelliert, ohne einen Datenbanksysteme-Schein zu besitzen.""")

        # Test zu DK3
        dk3: list[tuple] = dbs_test.doExerciseDK3()
        for data in dk3:
            logging.info(f"""Haustier {data[0]} hat eine Kampfkraft > 9000 und einen Niedlichkeitsfaktor >= 0.8.""")

        # Test zu SQL1
        sql1: list[tuple] = dbs_test.doExerciseSQL1()
        for data in sql1:
            logging.info(f"""Die bevorzugte Waffe der Spieler ist '{data[0]}'. {data[1]} Spieler bevorzugen diese Waffe.""")

        # Test zu SQL2
        sql2: list[tuple] = dbs_test.doExerciseSQL2()
        for data in sql2:
            logging.info(f"""Ich schreibe die Bedingungen nicht ab. Das Ergebnis ist '{data[0]}'.""")

        # Test zu SQL3
        sql3: list[tuple] = dbs_test.doExerciseSQL3()
        for data in sql3:
            logging.info(f"""{int(data[0] * 100)}% der Items 'Datenbanksysteme-Schein' werden von Spielern besessen.""")

        # Test zu SQL4
        sql4: list[tuple] = dbs_test.doExerciseSQL4()
        for data in sql4:
            logging.info(f"""Avatar {data[0]} wurde am {data[6]} geboren.""")

        # Test zu SQL4
        sql4: list[tuple] = dbs_test.doExerciseSQL4()
        for data in sql4:
            logging.info(f"""Avatar {data[0]} wurde am {data[6]} geboren.""")

        if modify_data:
            # Test zu SQL5
            sql5: list[tuple] = dbs_test.doExerciseSQL5()
            for data in sql5:
                logging.info(f"""{data[0]}: {data[1]}""")


            # Test zu SQL6
            sql6: list[tuple] = dbs_test.doExerciseSQL6()
            for data in sql6:
                logging.info(f"""{data[0]}: {data[1]}""")

            # Test zu SQL7
            sql7: list[tuple] = dbs_test.doExerciseSQL7()
            for data in sql7:
                logging.info(f"""{data[0]}: {data[1]}""")

    except DBSException as dbs_err:
        logging.error(dbs_err)


start_test(clean_slate=True, modify_data=True)
