#!/usr/bin/env python3
"""
Демонстрация визуализации для трех различных пакетов
"""
import subprocess
import os
import time


def create_config(package_name, output_file, ascii_tree=True):
    """Создание конфигурационного файла для пакета"""
    config_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
    <packageName>{package_name}</packageName>
    <repositoryUrl>https://dl-cdn.alpinelinux.org/alpine/v3.18/main</repositoryUrl>
    <testRepositoryMode>false</testRepositoryMode>
    <outputImage>{output_file}</outputImage>
    <asciiTreeMode>{str(ascii_tree).lower()}</asciiTreeMode>
    <graphFormat>svg</graphFormat>
</config>'''

    with open('config.xml', 'w') as f:
        f.write(config_content)


def run_analysis():
    """Запуск анализа с текущей конфигурацией"""
    result = subprocess.run(['python3', 'apk_analyzer.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode


def main():
    """Демонстрация для трех пакетов"""
    packages = [
        ("nginx", "nginx_dependencies.svg"),
        ("python3", "python3_dependencies.svg"),
        ("postgresql", "postgresql_dependencies.svg")
    ]

    print("ДЕМОНСТРАЦИЯ ВИЗУАЛИЗАЦИИ ЗАВИСИМОСТЕЙ")
    print("=" * 60)

    for package_name, output_file in packages:
        print(f"\n\nАнализ пакета: {package_name}")
        print("-" * 40)

        # Создаем конфигурацию
        create_config(package_name, output_file, ascii_tree=True)

        # Запускаем анализ
        if run_analysis() == 0:
            print(f"✓ Граф для {package_name} сохранен как {output_file}")

            # Проверяем создание файла
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ Файл графа создан, размер: {file_size} байт")
            else:
                print(f"✗ Файл графа не создан")
        else:
            print(f"✗ Ошибка анализа для {package_name}")

        # Пауза между пакетами
        time.sleep(1)

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("Созданы файлы графов:")
    for _, output_file in packages:
        if os.path.exists(output_file):
            print(f"  - {output_file}")


if __name__ == "__main__":
    main()