
import json
import csv
from pathlib import Path

QUESTIONS_FILE = Path(__file__).with_name('questions.json')
SCORES_FILE = Path(__file__).with_name('scores.csv')


def read_questions():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_scores():
    scores = []

    if SCORES_FILE.exists():
        with open(SCORES_FILE, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=';')

            for row in reader:
                if len(row) != 3:
                    continue

                try:
                    points = int(row[1])
                    total = int(row[2])
                except ValueError:
                    continue

                scores.append((row[0], points, total))

    return scores


def save_score(name, points, total):
    with open(SCORES_FILE, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([name, points, total])


questions = read_questions()

points = 0
total = len(questions)

print('Tere tulemast viktoriini!')
print(f'Küsimusi on kokku {total}.')

for i, question in enumerate(questions, start=1):

    print()
    print(f'Küsimus {i}/{total}')
    print(question['question'])

    for number, answer in enumerate(question['answers'], start=1):
        print(f'{number}. {answer}')

    while True:
        try:
            answer = int(input('Sisesta oma valik (1, 2 või 3): '))

            if answer in [1, 2, 3]:
                break
            else:
                print('Palun vali 1, 2 või 3.')

        except ValueError:
            print('Palun sisesta number!')

    if answer == question['correct']:
        points += 1
        print('Õige vastus!')
    else:
        print('Vale vastus!')

print()
print('Mäng läbi!')
print(f'Sinu punktisumma on: {points}/{total}')

name = input('Sisesta oma nimi: ')

save_score(name, points, total)

print('Tulemus salvestatud!')

scores = read_scores()

print()
print(f'Varem mängitud mänge: {len(scores)}')

scores.sort(
    key=lambda item: (
        item[1] / item[2] if item[2] > 0 else 0,
        item[1]
    ),
    reverse=True
)

print()
print('Viis parimat tulemust:')

for i, (name, points, total) in enumerate(scores[:5], start=1):
    print(f'{i}. {name} - {points}/{total}')
    