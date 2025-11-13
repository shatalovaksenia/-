#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей пакетов
"""

import xml.etree.ElementTree as ET
import os
import sys
import argparse
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class RepositoryMode(Enum):
    REMOTE = "remote"
    TEST = "test"


@dataclass
class Config:
    package_name: str
    repository_url: str
    test_repository_mode: bool
    test_repository_path: str
    output_filename: str
    ascii_tree_mode: bool


class DependencyNode:
    def __init__(self, name: str, version: str = "latest"):
        self.name = name
        self.version = version
        self.dependencies: List['DependencyNode'] = []

    def add_dependency(self, dependency: 'DependencyNode'):
        self.dependencies.append(dependency)

    def __str__(self):
        return f"{self.name}@{self.version}"

    def __eq__(self, other):
        return isinstance(other, DependencyNode) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class ConfigError(Exception):
    """Исключение для ошибок конфигурации"""
    pass


class RepositoryError(Exception):
    """Исключение для ошибок репозитория"""
    pass


class DependencyResolver:
    """Класс для разрешения зависимостей пакетов"""

    def __init__(self, config: Config):
        self.config = config
        # Тестовые данные для демонстрации
        self.test_packages = {
            "example-package": ["dep-a", "dep-b"],
            "dep-a": ["dep-c", "dep-d"],
            "dep-b": ["dep-c"],
            "dep-c": ["dep-e"],
            "dep-d": [],
            "dep-e": []
        }

    def resolve_dependencies(self, package_name: str) -> DependencyNode:
        """Разрешает зависимости для указанного пакета"""
        if not package_name:
            raise RepositoryError("Имя пакета не может быть пустым")

        if self.config.test_repository_mode:
            return self._resolve_from_test_repo(package_name)
        else:
            return self._resolve_from_remote(package_name)

    def _resolve_from_test_repo(self, package_name: str) -> DependencyNode:
        """Разрешает зависимости из тестового репозитория"""
        if not self.config.test_repository_path:
            raise RepositoryError("Путь к тестовому репозиторию не указан")

        # В реальной реализации здесь был бы парсинг тестового репозитория
        # Для демонстрации используем заранее подготовленные данные

        if package_name not in self.test_packages:
            raise RepositoryError(f"Пакет '{package_name}' не найден в тестовом репозитории")

        return self._build_dependency_tree(package_name, set())

    def _build_dependency_tree(self, package_name: str, visited: Set[str]) -> DependencyNode:
        """Рекурсивно строит дерево зависимостей"""
        if package_name in visited:
            return DependencyNode(package_name + " (цикл)")

        visited.add(package_name)
        node = DependencyNode(package_name)

        for dep in self.test_packages.get(package_name, []):
            dependency_node = self._build_dependency_tree(dep, visited.copy())
            node.add_dependency(dependency_node)

        return node

    def _resolve_from_remote(self, package_name: str) -> DependencyNode:
        """Разрешает зависимости из удаленного репозитория"""
        if not self.config.repository_url:
            raise RepositoryError("URL репозитория не указан")

        # В реальной реализации здесь был бы HTTP-запрос к репозиторию
        # Для демонстрации используем те же данные
        return self._resolve_from_test_repo(package_name)


class GraphVisualizer:
    """Класс для визуализации графа зависимостей"""

    def __init__(self, config: Config):
        self.config = config

    def generate_ascii_tree(self, root: DependencyNode) -> str:
        """Генерирует ASCII-представление дерева зависимостей"""
        return self._build_ascii_tree(root, "", True, [])

    def _build_ascii_tree(self, node: DependencyNode, prefix: str, is_last: bool, visited: List[str]) -> str:
        """Рекурсивно строит ASCII-дерево"""
        if node.name in visited:
            return f"{prefix}{'└── ' if is_last else '├── '}{node.name} (уже посещен)\n"

        visited.append(node.name)

        result = f"{prefix}{'└── ' if is_last else '├── '}{node}\n"

        if node.dependencies:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, dep in enumerate(node.dependencies):
                is_last_dep = i == len(node.dependencies) - 1
                result += self._build_ascii_tree(dep, new_prefix, is_last_dep, visited.copy())

        return result

    def generate_graph_image(self, root: DependencyNode) -> None:
        """Генерирует изображение графа (заглушка для демонстрации)"""
        # В реальной реализации здесь использовалась бы библиотека типа graphviz
        print(f"Генерируется изображение графа в файл: {self.config.output_filename}")
        print("(В реальной реализации здесь было бы создание PNG/PDF файла)")

        # Создаем пустой файл для демонстрации
        try:
            with open(self.config.output_filename, 'w') as f:
                f.write("# Dependency Graph Visualization\n")
                f.write(f"# Package: {root.name}\n")
            print(f"Файл {self.config.output_filename} создан успешно")
        except IOError as e:
            raise RepositoryError(f"Ошибка при создании файла {self.config.output_filename}: {e}")


class ConfigParser:
    """Класс для парсинга конфигурационного файла"""

    @staticmethod
    def parse_config(file_path: str) -> Config:
        """Парсит XML конфигурационный файл"""
        try:
            if not os.path.exists(file_path):
                raise ConfigError(f"Конфигурационный файл не найден: {file_path}")

            tree = ET.parse(file_path)
            root = tree.getroot()

            # Извлекаем значения с проверкой на существование
            package_name = ConfigParser._get_element_text(root, 'packageName')
            repository_url = ConfigParser._get_element_text(root, 'repositoryUrl')
            test_repository_mode = ConfigParser._parse_boolean(
                ConfigParser._get_element_text(root, 'testRepositoryMode'))
            test_repository_path = ConfigParser._get_element_text(root, 'testRepositoryPath')
            output_filename = ConfigParser._get_element_text(root, 'outputFileName')
            ascii_tree_mode = ConfigParser._parse_boolean(ConfigParser._get_element_text(root, 'asciiTreeMode'))

            # Валидация обязательных полей
            if not package_name:
                raise ConfigError("Имя пакета не может быть пустым")

            if not output_filename:
                raise ConfigError("Имя выходного файла не может быть пустым")

            return Config(
                package_name=package_name,
                repository_url=repository_url,
                test_repository_mode=test_repository_mode,
                test_repository_path=test_repository_path,
                output_filename=output_filename,
                ascii_tree_mode=ascii_tree_mode
            )

        except ET.ParseError as e:
            raise ConfigError(f"Ошибка парсинга XML: {e}")
        except Exception as e:
            raise ConfigError(f"Ошибка чтения конфигурации: {e}")

    @staticmethod
    def _get_element_text(root, tag: str) -> str:
        """Извлекает текст элемента или возвращает пустую строку"""
        element = root.find(tag)
        return element.text if element is not None else ""

    @staticmethod
    def _parse_boolean(value: str) -> bool:
        """Парсит строковое значение в boolean"""
        if not value:
            return False
        return value.lower() in ('true', '1', 'yes', 'y')


class DependencyVisualizer:
    """Основной класс приложения"""

    def __init__(self, config: Config):
        self.config = config
        self.dependency_resolver = DependencyResolver(config)
        self.graph_visualizer = GraphVisualizer(config)

    def run(self) -> None:
        """Запускает процесс визуализации зависимостей"""
        try:
            # Выводим параметры конфигурации
            self._print_config()

            # Разрешаем зависимости
            print(f"\nРазрешение зависимостей для пакета: {self.config.package_name}")
            root_node = self.dependency_resolver.resolve_dependencies(self.config.package_name)

            # Выводим ASCII-дерево если включен режим
            if self.config.ascii_tree_mode:
                print("\nДерево зависимостей (ASCII):")
                ascii_tree = self.graph_visualizer.generate_ascii_tree(root_node)
                print(ascii_tree)

            # Генерируем изображение графа
            print("\nГенерация изображения графа...")
            self.graph_visualizer.generate_graph_image(root_node)

            print("\nВизуализация завершена успешно!")

        except (RepositoryError, ConfigError) as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Неожиданная ошибка: {e}", file=sys.stderr)
            sys.exit(1)

    def _print_config(self) -> None:
        """Выводит параметры конфигурации в формате ключ-значение"""
        print("Параметры конфигурации:")
        print(f"  packageName: {self.config.package_name}")
        print(f"  repositoryUrl: {self.config.repository_url}")
        print(f"  testRepositoryMode: {self.config.test_repository_mode}")
        print(f"  testRepositoryPath: {self.config.test_repository_path}")
        print(f"  outputFileName: {self.config.output_filename}")
        print(f"  asciiTreeMode: {self.config.ascii_tree_mode}")


def main():
    """Точка входа в приложение"""
    parser = argparse.ArgumentParser(description='Инструмент визуализации графа зависимостей пакетов')
    parser.add_argument('--config', '-c', default='config.xml',
                        help='Путь к конфигурационному файлу (по умолчанию: config.xml)')

    args = parser.parse_args()

    try:
        # Парсим конфигурацию
        config = ConfigParser.parse_config(args.config)

        # Запускаем визуализатор
        visualizer = DependencyVisualizer(config)
        visualizer.run()

    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
        sys.exit(1)


if __name__ == "__main__":
    main()