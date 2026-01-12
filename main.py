# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logics import *

FILENAME = "vacancies.txt"

def display_menu():
    print("\n" + "="*50)
    print("КАДРОВОЕ АГЕНТСТВО")
    print("="*50)
    print("1. Полный список (сортировка: образование ↑, должность ↑)")
    print("2. С испытательным сроком ≥ 2 мес (сортировка: испытат. срок ↓, стаж ↓, макс. возраст ↑)")
    print("3. С окладом в диапазоне N1–N2 (сортировка: соцпакет ↑, испытат. срок ↓)")
    print("4. Выход")
    print("="*50)

def get_int_input(prompt):
    """Безопасный ввод целого числа."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")

def main():
    # Загружаем вакансии из файла
    vacancies = read_vacancies(FILENAME)
    if not vacancies:
        print("Не удалось загрузить вакансии. Проверьте файл vacancies.txt.")
        return

    while True:
        display_menu()
        choice = input("Выберите пункт меню (1-4): ").strip()

        if choice == "1":
            sorted_vac = sort_by_education_position(vacancies)
            print_vacancies(sorted_vac, "Полный список вакансий")

        elif choice == "2":
            filtered = filter_by_probation(vacancies, 2)
            sorted_vac = sort_by_probation_experience_max_age(filtered)
            print_vacancies(sorted_vac, "Вакансии с испытательным сроком ≥ 2 месяцев")

        elif choice == "3":
            n1 = get_int_input("Введите минимальный оклад N1: ")
            n2 = get_int_input("Введите максимальный оклад N2: ")
            if n1 > n2:
                print("Ошибка: N1 не может быть больше N2.")
                continue
            filtered = filter_by_salary_range(vacancies, n1, n2)
            sorted_vac = sort_by_social_package_probation(filtered)
            print_vacancies(sorted_vac, f"Вакансии с окладом от {n1} до {n2} руб.")

        elif choice == "4":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")

        input("\nНажмите Enter для возврата в меню...")

if __name__ == "__main__":
    main()