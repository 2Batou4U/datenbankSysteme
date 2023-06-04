from dbs2023ExerciseProject import DatabaseProject

dbs_test = DatabaseProject()

dbs_test.connectToMariaDB(user="adrian", pw="pomi2013S", host="152.89.239.24", port=3306, database="fantasy_welt")

dbs_test.createWorld()
# dbs_test.doExerciseRA1()
# dbs_test.doExerciseRA2()
# dbs_test.doExerciseRA3()
dbs_test.doExerciseTK1()
