# logics.py
import os

# Структура записи о вакансии (список полей)
FIELDS = [
    "должность", "необходимый стаж работы", "пол", "образование",
    "минимальный возраст", "максимальный возраст", "знание иностранных языков",
    "минимальный оклад", "наличие соцпакета", "испытательный срок"
]

def read_vacancies(filename):
    """
    Чтение вакансий из текстового файла.
    Возвращает список списков (каждый подсписок — запись).
    """
    vacancies = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(';')
                if len(parts) != len(FIELDS):
                    print(f"Пропущена строка из-за неверного формата: {line}")
                    continue
                # Преобразуем числовые поля в числа
                parts[1] = int(parts[1])   # стаж
                parts[4] = int(parts[4])   # мин возраст
                parts[5] = int(parts[5])   # макс возраст
                parts[7] = int(parts[7])   # оклад
                parts[9] = int(parts[9])   # испытательный срок
                vacancies.append(parts)
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    return vacancies

def write_vacancies(filename, vacancies):
    """
    Запись вакансий в текстовый файл.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for v in vacancies:
                line = ';'.join(map(str, v))
                file.write(line + '\n')
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

def quick_sort(arr, key_func, reverse=False):
    """
    Реализация сортировки Хоара (быстрой сортировки).
    key_func — функция, возвращающая ключ для сравнения.
    reverse — обратный порядок.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    pivot_key = key_func(pivot)
    left = []
    middle = []
    right = []
    for x in arr:
        x_key = key_func(x)
        if reverse:
            if x_key > pivot_key:
                left.append(x)
            elif x_key < pivot_key:
                right.append(x)
            else:
                middle.append(x)
        else:
            if x_key < pivot_key:
                left.append(x)
            elif x_key > pivot_key:
                right.append(x)
            else:
                middle.append(x)
    return quick_sort(left, key_func, reverse) + middle + quick_sort(right, key_func, reverse)

# ----------------------------------------------------------------
# 1. Сортировка по образованию (возрастание) + должность (возрастание)
def sort_by_education_position(vacancies):
    def key_func(v):
        # v[3] - образование, v[0] - должность
        return (v[3], v[0])
    return quick_sort(vacancies, key_func, reverse=False)

# ----------------------------------------------------------------
# 2. Сортировка для вакансий с испытательным сроком >= 2 месяцев
def filter_by_probation(vacancies, min_months=2):
    return [v for v in vacancies if v[9] >= min_months]

def sort_by_probation_experience_max_age(vacancies):
    def key_func(v):
        # v[9] - испытательный срок (по убыванию)
        # v[1] - стаж (по убыванию)
        # v[5] - максимальный возраст (по возрастанию)
        return (-v[9], -v[1], v[5])
    return quick_sort(vacancies, key_func, reverse=False)

# ----------------------------------------------------------------
# 3. Сортировка для вакансий с окладом в диапазоне [N1, N2]
def filter_by_salary_range(vacancies, n1, n2):
    return [v for v in vacancies if n1 <= v[7] <= n2]

def sort_by_social_package_probation(vacancies):
    def key_func(v):
        # v[8] - наличие соцпакета (есть/нет) -> преобразуем в число (1 есть, 0 нет)
        # v[9] - испытательный срок (по убыванию)
        social_score = 1 if v[8].lower() == 'есть' else 0
        return (social_score, -v[9])
    return quick_sort(vacancies, key_func, reverse=False)

# ----------------------------------------------------------------
# Форматированный вывод вакансий
def print_vacancies(vacancies, title=""):
    if title:
        print(f"\n--- {title} ---")
    if not vacancies:
        print("Нет вакансий, соответствующих условиям.")
        return
    # Заголовок
    header = " | ".join(FIELDS)
    print(header)
    print("-" * len(header))
    for v in vacancies:
        print(" | ".join(map(str, v)))
    print(f"\nВсего: {len(vacancies)} записей.")