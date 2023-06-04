from dbs2023ExerciseProject import DatabaseProject

dbs_test = DatabaseProject()

dbs_test.connectToMariaDB(user="adrian", pw="pomi2013S", host="152.89.239.24", port=3306, database="fantasy_welt")

#dbs_test.createWorld()

dbs_test.doExerciseRA1()

