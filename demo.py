#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования различных сценариев
"""

import os
import subprocess
import sys


def run_demo():
    """Запускает демонстрацию различных сценариев"""

    print("=== Демонстрация инструмента визуализации зависимостей ===\n")

    # Сценарий 1: Нормальная работа
    print("1. Нормальная работа:")
    subprocess.run([sys.executable, "dependency_visualizer.py", "--config", "config.xml"])

    print("\n" + "=" * 50 + "\n")

    # Сценарий 2: Файл конфигурации не существует
    print("2. Ошибка: файл конфигурации не существует:")
    subprocess.run([sys.executable, "dependency_visualizer.py", "--config", "nonexistent.xml"])

    print("\n" + "=" * 50 + "\n")

    # Сценарий 3: Неверный XML
    print("3. Ошибка: неверный формат XML:")
    with open("bad_config.xml", "w") as f:
        f.write("<?xml version=\"1.0\"?><config><packageName>test</packageName><unclosed_tag>")

    subprocess.run([sys.executable, "dependency_visualizer.py", "--config", "bad_config.xml"])

    # Очистка
    if os.path.exists("bad_config.xml"):
        os.remove("bad_config.xml")


if __name__ == "__main__":
    run_demo()