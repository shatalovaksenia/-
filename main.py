import tkinter as tk
import os
import shlex
import sys
import argparse


class TerminalEmulator:
    def __init__(self, root, vfs_path=None, startup_script=None):
        self.root = root
        self.vfs_path = vfs_path
        self.startup_script = startup_script
        self.setup_window()
        self.create_widgets()
        self.current_dir = os.getcwd()

        # Отладочный вывод параметров
        self.print_text("=== Параметры эмулятора ===", 'yellow')
        self.print_text(f"VFS путь: {vfs_path}", 'yellow')
        self.print_text(f"Стартовый скрипт: {startup_script}", 'yellow')
        self.print_text("===========================", 'yellow')

        # Выполнение стартового скрипта, если указан
        if self.startup_script:
            self.execute_startup_script()

    def setup_window(self):
        username = os.getlogin() or 'user'
        hostname = os.getenv('COMPUTERNAME') or 'localhost'
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("700x500")



    def create_widgets(self):
        self.output = tk.Text(self.root, bg='black', fg='white', font=('Courier', 11))
        self.output.pack(fill='both', expand=True, padx=5, pady=5)
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill='x', padx=5, pady=5)
        username = os.getenv('USER') or 'user'
        self.prompt = f"{username}$ "
        tk.Label(input_frame, text=self.prompt, fg='green', bg='black').pack(side='left')
        self.entry = tk.Entry(input_frame, bg='black', fg='white', insertbackground='white')
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind('<Return>', self.run_command)
        self.entry.focus()

    def print_text(self, text, color='white'):
        tag_name = f"color_{color}"
        self.output.tag_configure(tag_name, foreground=color)
        self.output.insert('end', text + '\n', tag_name)
        self.output.see('end')

    def execute_startup_script(self):
        """Выполнение стартового скрипта"""
        if not os.path.exists(self.startup_script):
            self.print_text(f"ОШИБКА: Стартовый скрипт '{self.startup_script}' не найден!", 'red')
            return

        self.print_text(f"=== Выполнение стартового скрипта: {self.startup_script} ===", 'cyan')

        try:
            with open(self.startup_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                line = line.strip()

                # Пропуск пустых строк и комментариев
                if not line or line.startswith('#'):
                    continue

                # Отображение команды как будто её ввел пользователь
                self.print_text(self.prompt + line, 'cyan')

                # Выполнение команды
                try:
                    parts = shlex.split(line)
                    if not parts:
                        continue

                    cmd = parts[0]
                    args = parts[1:] if len(parts) > 1 else []

                    if cmd == 'exit':
                        self.print_text("Завершение работы по скрипту...", 'yellow')
                        return

                    elif cmd == 'ls':
                        self.print_text(f"команда: ls")
                        self.print_text(f"аргументы: {args}")

                    elif cmd == 'cd':
                        self.print_text(f"команда: cd")
                        self.print_text(f"аргументы: {args}")

                        if len(args) > 1:
                            self.print_text("ошибка: слишком много аргументов", 'red')
                        elif args:
                            self.print_text(f"переход в: {args[0]}", 'green')
                        else:
                            self.print_text("переход в домашнюю директорию", 'green')

                    else:
                        self.print_text(f"ошибка: команда '{cmd}' не найдена", 'red')

                except Exception as e:
                    self.print_text(f"ОШИБКА в строке {line_num}: {e}", 'red')

        except Exception as e:
            self.print_text(f"ОШИБКА чтения скрипта: {e}", 'red')

        self.print_text(f"=== Завершение выполнения стартового скрипта ===", 'cyan')

    def run_command(self, event):
        command = self.entry.get().strip()
        self.entry.delete(0, 'end')
        self.print_text(self.prompt + command)


        try:
            parts = shlex.split(command)
            if not parts:
                return

            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            if cmd == 'exit':
                self.root.quit()

            elif cmd == 'ls':
                self.print_text(f"команда: ls")
                self.print_text(f"аргументы: {args}")

            elif cmd == 'cd':
                self.print_text(f"команда: cd")
                self.print_text(f"аргументы: {args}")

                if len(args) > 1:
                    self.print_text("ошибка: слишком много аргументов", 'red')
                elif args:
                    self.print_text(f"переход в: {args[0]}", 'green')
                else:
                    self.print_text("переход в домашнюю директорию", 'green')

            else:
                self.print_text(f"ошибка: команда '{cmd}' не найдена", 'red')

        except Exception as e:
            self.print_text(f"ошибка разбора команды: {e}", 'red')






parser = argparse.ArgumentParser()
parser.add_argument("--vfs_path", "-p", help="Путь к физическому расположению VFS")
parser.add_argument("--name", "-m", help="Путь к физическому расположению VFS")
parser.add_argument("--script", "-s", help="Путь к стартовому скрипту")
args = parser.parse_args()

print("=== Параметры запуска ===")
print(f"VFS путь: {args.vfs_path}")
print(f"Скрипт: {args.script}")
print("========================")

root = tk.Tk()
app = TerminalEmulator(root, vfs_path=args.vfs_path, startup_script=args.script)
root.mainloop()