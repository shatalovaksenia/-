#!/usr/bin/env python3
"""
Минимальный прототип инструмента визуализации графа зависимостей пакетов
Этап 1: Конфигурация и базовый функционал
"""

import xml.etree.ElementTree as ET
import sys
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class RepositoryMode(Enum):
    REMOTE = "remote"
    LOCAL = "local"


@dataclass
class Config:
    """Класс для хранения конфигурационных параметров"""
    package_name: str
    repository_url: str
    test_repository_mode: bool
    test_repository_path: str
    output_file_name: str
    ascii_tree_output: bool


class ConfigurationError(Exception):
    """Исключение для ошибок конфигурации"""
    pass


class DependencyManager:
    """Основной класс для управления зависимостями"""

    def __init__(self, config: Config):
        self.config = config
        self.dependencies = {}

    def load_config_from_xml(self, config_path: str) -> Config:
        """
        Загрузка конфигурации из XML файла
        """
        try:
            if not os.path.exists(config_path):
                raise ConfigurationError(f"Конфигурационный файл не найден: {config_path}")

            tree = ET.parse(config_path)
            root = tree.getroot()

            # Извлечение параметров с проверкой на существование
            package_name = self._get_element_text(root, 'packageName')
            repository_url = self._get_element_text(root, 'repositoryUrl')

            test_repository_mode_str = self._get_element_text(root, 'testRepositoryMode')
            test_repository_mode = self._parse_boolean(test_repository_mode_str, 'testRepositoryMode')

            test_repository_path = self._get_element_text(root, 'testRepositoryPath')
            output_file_name = self._get_element_text(root, 'outputFileName')

            ascii_tree_output_str = self._get_element_text(root, 'asciiTreeOutput')
            ascii_tree_output = self._parse_boolean(ascii_tree_output_str, 'asciiTreeOutput')

            # Валидация обязательных параметров
            if not package_name:
                raise ConfigurationError("Имя пакета не может быть пустым")

            if not repository_url and not test_repository_mode:
                raise ConfigurationError("Должен быть указан URL репозитория или включен тестовый режим")

            if test_repository_mode and not test_repository_path:
                raise ConfigurationError("В тестовом режиме должен быть указан путь к репозиторию")

            if not output_file_name:
                raise ConfigurationError("Имя выходного файла не может быть пустым")

            return Config(
                package_name=package_name,
                repository_url=repository_url,
                test_repository_mode=test_repository_mode,
                test_repository_path=test_repository_path,
                output_file_name=output_file_name,
                ascii_tree_output=ascii_tree_output
            )

        except ET.ParseError as e:
            raise ConfigurationError(f"Ошибка парсинга XML: {e}")
        except Exception as e:
            raise ConfigurationError(f"Ошибка загрузки конфигурации: {e}")

    def _get_element_text(self, root, element_name: str) -> str:
        """Получение текста элемента с обработкой ошибок"""
        element = root.find(element_name)
        if element is None:
            raise ConfigurationError(f"Отсутствует обязательный параметр: {element_name}")
        return element.text or ""

    def _parse_boolean(self, value: str, param_name: str) -> bool:
        """Парсинг булевых значений"""
        if value.lower() in ('true', '1', 'yes'):
            return True
        elif value.lower() in ('false', '0', 'no'):
            return False
        else:
            raise ConfigurationError(f"Некорректное значение для {param_name}: {value}. Ожидается 'true' или 'false'")

    def display_configuration(self):
        """Вывод конфигурации в формате ключ-значение"""
        print("=== Конфигурация приложения ===")
        print(f"Имя анализируемого пакета: {self.config.package_name}")
        print(f"URL-адрес репозитория: {self.config.repository_url}")
        print(f"Режим работы с тестовым репозиторием: {self.config.test_repository_mode}")
        print(f"Путь к тестовому репозиторию: {self.config.test_repository_path}")
        print(f"Имя сгенерированного файла: {self.config.output_file_name}")
        print(f"Режим вывода в формате ASCII-дерева: {self.config.ascii_tree_output}")
        print("=" * 40)

    def validate_repository_access(self):
        """Валидация доступа к репозиторию"""
        if self.config.test_repository_mode:
            if not os.path.exists(self.config.test_repository_path):
                raise ConfigurationError(f"Тестовый репозиторий не найден: {self.config.test_repository_path}")
            print(f"✓ Тестовый репозиторий доступен: {self.config.test_repository_path}")
        else:
            # Здесь может быть проверка доступности URL
            print(f"✓ Используется удаленный репозиторий: {self.config.repository_url}")

    def validate_output_file(self):
        """Валидация выходного файла"""
        output_dir = os.path.dirname(self.config.output_file_name) or '.'
        if not os.path.exists(output_dir):
            raise ConfigurationError(f"Директория для выходного файла не существует: {output_dir}")

        # Проверка расширения файла
        valid_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.pdf']
        file_ext = os.path.splitext(self.config.output_file_name)[1].lower()
        if file_ext not in valid_extensions:
            print(f"⚠ Предупреждение: нестандартное расширение файла: {file_ext}")

        print(f"✓ Выходной файл будет сохранен как: {self.config.output_file_name}")

    def generate_sample_dependencies(self):
        """Генерация примерных зависимостей для демонстрации"""
        # В реальной реализации здесь будет логика получения зависимостей
        self.dependencies = {
            self.config.package_name: {
                'dependencies': ['dep1', 'dep2', 'dep3'],
                'version': '1.0.0'
            },
            'dep1': {
                'dependencies': ['subdep1', 'subdep2'],
                'version': '2.1.0'
            },
            'dep2': {
                'dependencies': [],
                'version': '1.5.0'
            },
            'dep3': {
                'dependencies': ['dep2'],
                'version': '3.0.0'
            },
            'subdep1': {
                'dependencies': [],
                'version': '0.1.0'
            },
            'subdep2': {
                'dependencies': [],
                'version': '1.2.3'
            }
        }

    def display_ascii_tree(self):
        """Отображение зависимостей в формате ASCII-дерева"""
        if not self.dependencies:
            print("Нет данных о зависимостях для отображения")
            return

        print("\n=== Дерево зависимостей (ASCII) ===")

        def build_tree(package, level=0, visited=None):
            if visited is None:
                visited = set()

            if package in visited:
                return f"{'  ' * level}└── {package} [циклическая зависимость]\n"

            visited.add(package)

            if package not in self.dependencies:
                return f"{'  ' * level}└── {package} (не найден)\n"

            package_info = self.dependencies[package]
            tree_str = f"{'  ' * level}└── {package} v{package_info['version']}\n"

            deps = package_info['dependencies']
            for i, dep in enumerate(deps):
                is_last = i == len(deps) - 1
                prefix = '  ' * (level + 1) + ('└── ' if is_last else '├── ')
                tree_str += prefix + build_tree(dep, level + 2, visited.copy()).lstrip()

            return tree_str

        print(build_tree(self.config.package_name))

    def run(self):
        """Основной метод запуска приложения"""
        try:
            # Демонстрация работы
            self.display_configuration()

            # Валидация параметров
            self.validate_repository_access()
            self.validate_output_file()

            # Генерация примерных данных
            self.generate_sample_dependencies()

            # Отображение ASCII-дерева если включено
            if self.config.ascii_tree_output:
                self.display_ascii_tree()
            else:
                print("\nРежим ASCII-дерева отключен в конфигурации")

            print(f"\n✓ Приложение успешно завершило работу")
            print(f"✓ Граф зависимостей будет сохранен в: {self.config.output_file_name}")

        except ConfigurationError as e:
            print(f"❌ Ошибка конфигурации: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            sys.exit(1)


def main():
    """Точка входа в приложение"""
    if len(sys.argv) != 2:
        print("Использование: python main.py <config_file.xml>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # Создание менеджера зависимостей
        manager = DependencyManager(Config("", "", False, "", "", False))

        # Загрузка конфигурации
        config = manager.load_config_from_xml(config_file)
        manager.config = config

        # Запуск приложения
        manager.run()

    except ConfigurationError as e:
        print(f"❌ Ошибка загрузки конфигурации: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()