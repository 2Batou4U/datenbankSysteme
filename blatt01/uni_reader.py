import pandas as pd


def analyze_student_results(file):
    # Einlesen der CSV-Datei
    df = pd.read_csv(filepath_or_buffer=file, sep=";")

    # Anzahl der Teilnehmenden
    num_students = df.shape[0]
    print(f'Anzahl der Teilnehmenden: {num_students}')

    # Beste Noten für jede:n Schüler:in
    df['best_grade'] = df[['G1', 'G2', 'G3']].max(axis=1)
    print("\nBeste Noten für jede:n Schüler:in:")
    print(df[['best_grade']])

    # Durchschnittsnoten für die Prüfungszeitpunkte G1, G2 und G3
    avg_grades = df[['G1', 'G2', 'G3']].mean()
    print("\nDurchschnittsnoten für die Prüfungszeitpunkte G1, G2 und G3:")
    print(avg_grades)

    df.to_csv("csv/student-mat-out.csv")


analyze_student_results("csv/student-mat.csv")
