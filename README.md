# TLS Experiment

Батарея когнитивных задач на PsychoPy: тест Корси (пространственная память) и
math/operation-span задача (рабочая память). Запускаются последовательно через
`main.py`, порядок задач чередуется по чётности номера участника.

## Структура

```
main.py                  # точка входа: запускает обе задачи через PsychoPy Session
corsi/                    # тест Корси (PsychoPy Builder: .psyexp + сгенерированный .py)
  3rdtask.psyexp
  3rdtask.py
  corsi_conditions.py     # генерация условий
  corsi_conditions.csv
math_task/                # math/operation-span задача
  math_task.psyexp
  math_task.py
  make_conditions.py      # генерация условий (уравнения, 40 проб)
  conditions.csv
data/                      # результаты запусков через main.py (в git не попадает)
```

## Требования

- Python 3.10
- [PsychoPy](https://www.psychopy.org/) 2026.1.3

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

Откроется диалог с полями `participant` и `session`, затем по очереди запустятся
обе задачи. Результаты (csv/log/psydat) сохраняются в `data/` и не отслеживаются
git'ом — там могут быть персональные данные участников.

## Генерация условий

- `math_task/make_conditions.py` — генерирует `math_task/conditions.csv`
- `corsi/corsi_conditions.py` — генерирует `corsi/corsi_conditions.csv`
