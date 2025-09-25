import tkinter as tk
import os
import shlex

class TerminalEmulator:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.current_dir = os.getcwd()
        
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
        self.output.insert('end', text + '\n')
        self.output.see('end')
        
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
if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalEmulator(root)
    root.mainloop()
