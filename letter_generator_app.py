#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор писем - Приложение с графическим интерфейсом
Заменяет данные в шаблонах Word на основе таблицы Excel

Created by Kogl
Email: korobach2222@mail.ru
"""

import os
import re
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from docx import Document
import openpyxl
from threading import Thread


class LetterGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор писем")
        self.root.geometry("700x580")
        self.root.resizable(True, True)
        
        # Путь к файлу конфигурации
        self.config_file = os.path.join(os.path.expanduser("~"), ".letter_generator_config.json")
        
        # Переменные для путей к файлам
        self.template1_path = tk.StringVar()
        self.template2_path = tk.StringVar()
        self.excel_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.join(os.getcwd(), "Готовые письма"))
        self.test_mode = tk.BooleanVar(value=False)
        self.merge_mode = tk.StringVar(value="separate")  # "separate" или "single"
        
        # Загрузка сохраненных путей
        self.load_config()
        
        # Шаблонные значения для замены
        # На первой странице: "Чуль С.В., 30.06.1981 года рождения" и адрес
        # На второй странице: "Чуль С.В., 30.06.1981 рождения" (без слова "года")
        self.TEMPLATE_NAME = 'Чуль С.В.'
        self.TEMPLATE_DATE_FULL = '30.06.1981 года рождения'  # Первая страница
        self.TEMPLATE_DATE_SHORT = '30.06.1981 рождения'      # Вторая страница (приглашение)
        self.TEMPLATE_DATE = '30.06.1981'  # Общий вариант даты
        # Адрес с неразрывным пробелом (\xa0) после "г." - для первого шаблона
        self.TEMPLATE_ADDRESS = 'г.\xa0Минск,                             ул. Берестянская, 11-269'
        # Упрощенный вариант адреса - для второго шаблона
        self.TEMPLATE_ADDRESS_SHORT = 'ул. Берестянская, 11-269'
        
        self.create_widgets()
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # === Секция выбора файлов ===
        files_frame = ttk.LabelFrame(main_frame, text="Выбор файлов", padding="10")
        files_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Шаблон 1 (Уведомление + Приглашение)
        ttk.Label(files_frame, text="Шаблон 1 (Уведомление, Приглашение):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(files_frame, textvariable=self.template1_path, width=50).grid(row=1, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(files_frame, text="Обзор...", command=lambda: self.browse_file(self.template1_path, "Word файлы", "*.docx")).grid(row=1, column=1)
        
        # Шаблон 2 (Не занятые)
        ttk.Label(files_frame, text="Шаблон 2 (Не занятые):").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(files_frame, textvariable=self.template2_path, width=50).grid(row=3, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(files_frame, text="Обзор...", command=lambda: self.browse_file(self.template2_path, "Word файлы", "*.docx")).grid(row=3, column=1)
        
        # Excel файл
        ttk.Label(files_frame, text="База данных (Excel):").grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(files_frame, textvariable=self.excel_path, width=50).grid(row=5, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(files_frame, text="Обзор...", command=lambda: self.browse_file(self.excel_path, "Excel файлы", "*.xlsx")).grid(row=5, column=1)
        
        # Папка для результатов
        ttk.Label(files_frame, text="Папка для результатов:").grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(files_frame, textvariable=self.output_dir, width=50).grid(row=7, column=0, sticky=tk.EW, padx=(0, 5))
        ttk.Button(files_frame, text="Обзор...", command=self.browse_output_dir).grid(row=7, column=1)
        
        files_frame.columnconfigure(0, weight=1)
        
        # === Секция настроек ===
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(settings_frame, text="Тест (обработать только первую строку)", 
                        variable=self.test_mode).pack(anchor=tk.W, pady=(0, 10))
        
        # Режим создания документов
        ttk.Label(settings_frame, text="Режим создания документов:").pack(anchor=tk.W)
        ttk.Radiobutton(settings_frame, text="Отдельные файлы для каждого человека",
                        variable=self.merge_mode, value="separate").pack(anchor=tk.W, padx=(20, 0))
        ttk.Radiobutton(settings_frame, text="Всё в одном файле Word",
                        variable=self.merge_mode, value="single").pack(anchor=tk.W, padx=(20, 0))
        
        # === Кнопка запуска ===
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="▶ СТАРТ", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.progress = ttk.Progressbar(button_frame, mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # === Лог вывода ===
        log_frame = ttk.LabelFrame(main_frame, text="Лог выполнения", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # === Контакты автора ===
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(5, 0))
        
        author_label = ttk.Label(footer_frame, text="Created by Kogl | korobach2222@mail.ru", 
                                 foreground="gray", font=('TkDefaultFont', 8))
        author_label.pack(side=tk.RIGHT)
        
    def load_config(self):
        """Загрузка сохраненных путей из конфигурационного файла"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.template1_path.set(config.get('template1_path', ''))
                    self.template2_path.set(config.get('template2_path', ''))
                    self.excel_path.set(config.get('excel_path', ''))
                    self.output_dir.set(config.get('output_dir', os.path.join(os.getcwd(), "Готовые письма")))
                    self.test_mode.set(config.get('test_mode', False))
                    self.merge_mode.set(config.get('merge_mode', 'separate'))
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
    
    def save_config(self):
        """Сохранение путей в конфигурационный файл"""
        try:
            config = {
                'template1_path': self.template1_path.get(),
                'template2_path': self.template2_path.get(),
                'excel_path': self.excel_path.get(),
                'output_dir': self.output_dir.get(),
                'test_mode': self.test_mode.get(),
                'merge_mode': self.merge_mode.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
        
    def browse_file(self, var, filetypes_name, filetypes_ext):
        """Открыть диалог выбора файла"""
        filename = filedialog.askopenfilename(
            filetypes=[(filetypes_name, filetypes_ext), ("Все файлы", "*.*")]
        )
        if filename:
            var.set(filename)
            self.save_config()  # Автосохранение после выбора файла
    
    def browse_output_dir(self):
        """Открыть диалог выбора папки"""
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir.set(dirname)
            self.save_config()  # Автосохранение после выбора папки
    
    def log(self, message):
        """Добавить сообщение в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def full_name_to_initials(self, full_name):
        """Преобразование полного имени в формат 'Фамилия И.О.'"""
        if not full_name:
            return ''
        # Очистка от null значений
        full_name = full_name.replace(' null', '').replace('null ', '').replace('null', '')
        parts = full_name.strip().split()
        if len(parts) == 0:
            return ''
        surname = parts[0].capitalize()
        if len(parts) == 1:
            return surname
        elif len(parts) == 2:
            return f"{surname} {parts[1][0].upper()}."
        else:
            return f"{surname} {parts[1][0].upper()}.{parts[2][0].upper()}."
    
    def format_date(self, date_value):
        """Форматирование даты в формат ДД.ММ.ГГГГ"""
        if not date_value:
            return ''
        if hasattr(date_value, 'strftime'):
            return date_value.strftime('%d.%m.%Y')
        date_str = str(date_value)
        if ' ' in date_str:
            date_str = date_str.split(' ')[0]
        if '-' in date_str:
            parts = date_str.split('-')
            if len(parts) == 3:
                return f"{parts[2]}.{parts[1]}.{parts[0]}"
        return date_str
    
    def read_excel_data(self, filepath):
        """Чтение данных из Excel файла"""
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        data = []
        
        for row in range(2, ws.max_row + 1):  # Начинаем со 2-й строки (пропускаем заголовок)
            name = ws.cell(row=row, column=1).value  # A - ФИО
            date = ws.cell(row=row, column=2).value  # B - Дата рождения
            address = ws.cell(row=row, column=3).value  # C - Адрес
            
            if not name:
                continue
            
            full_name = str(name).strip()
            full_name_clean = full_name.replace(' null', '').replace('null ', '').replace('null', '').strip()
            
            data.append({
                'name_full': full_name_clean,
                'name_initials': self.full_name_to_initials(full_name),
                'date': self.format_date(date),
                'address': str(address).strip() if address else ''
            })
        
        return data
    
    def replace_text_in_runs(self, paragraph, old_text, new_text):
        """Замена текста в параграфе с сохранением форматирования"""
        replaced = False
        
        # Попытка заменить текст в отдельных runs
        for run in paragraph.runs:
            if old_text in run.text:
                run.text = run.text.replace(old_text, new_text)
                replaced = True
        
        if replaced:
            return True
        
        # Если текст разбит между runs, объединяем и заменяем
        if old_text in paragraph.text:
            full_text = paragraph.text
            new_full_text = full_text.replace(old_text, new_text)
            if paragraph.runs:
                paragraph.runs[0].text = new_full_text
                for run in paragraph.runs[1:]:
                    run.text = ''
                return True
        
        return False
    
    def replace_in_document(self, doc, replacements):
        """Замена текста во всём документе"""
        replaced_count = {key: 0 for key in replacements.keys()}
        
        # Замена в параграфах
        for paragraph in doc.paragraphs:
            for old_text, new_text in replacements.items():
                if old_text and old_text in paragraph.text:
                    if self.replace_text_in_runs(paragraph, old_text, new_text):
                        replaced_count[old_text] += 1
        
        # Замена в таблицах
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for old_text, new_text in replacements.items():
                            if old_text and old_text in paragraph.text:
                                if self.replace_text_in_runs(paragraph, old_text, new_text):
                                    replaced_count[old_text] += 1
        
        # Замена в колонтитулах
        for section in doc.sections:
            for header in [section.header, section.first_page_header, section.even_page_header]:
                if header:
                    for paragraph in header.paragraphs:
                        for old_text, new_text in replacements.items():
                            if old_text and old_text in paragraph.text:
                                if self.replace_text_in_runs(paragraph, old_text, new_text):
                                    replaced_count[old_text] += 1
            
            for footer in [section.footer, section.first_page_footer, section.even_page_footer]:
                if footer:
                    for paragraph in footer.paragraphs:
                        for old_text, new_text in replacements.items():
                            if old_text and old_text in paragraph.text:
                                if self.replace_text_in_runs(paragraph, old_text, new_text):
                                    replaced_count[old_text] += 1
        
        return replaced_count
    
    def generate_letter(self, template_path, output_path, data, is_template1=True):
        """Генерация письма из шаблона"""
        doc = Document(template_path)
        
        # Очищаем колонтитулы и отступы
        self.clear_headers_footers(doc)
        
        if is_template1:
            # Для первого шаблона (2 страницы - уведомление и приглашение)
            # Заменяем: Имя, Дату (два варианта), Адрес
            
            # Формируем дату в нужных форматах
            date_full = f"{data['date']} года рождения" if data['date'] else ''
            date_short = f"{data['date']} рождения" if data['date'] else ''
            
            replacements = {
                self.TEMPLATE_NAME: data['name_initials'],
                self.TEMPLATE_DATE_FULL: date_full,    # "30.06.1981 года рождения" -> "ДД.ММ.ГГГГ года рождения"
                self.TEMPLATE_DATE_SHORT: date_short,  # "30.06.1981 рождения" -> "ДД.ММ.ГГГГ рождения"
                self.TEMPLATE_DATE: data['date'],      # Просто дата на всякий случай
                self.TEMPLATE_ADDRESS: data['address'],
            }
        else:
            # Для второго шаблона (1 страница)
            replacements = {
                self.TEMPLATE_NAME: data['name_initials'],
                self.TEMPLATE_ADDRESS_SHORT: data['address'],  # Короткий формат адреса
            }
        
        replaced = self.replace_in_document(doc, replacements)
        doc.save(output_path)
        
        return replaced
    
    def start_processing(self):
        """Запуск обработки в отдельном потоке"""
        # Проверка заполнения полей
        if not self.template1_path.get():
            messagebox.showerror("Ошибка", "Выберите первый шаблон (Уведомление, Приглашение)")
            return
        if not self.template2_path.get():
            messagebox.showerror("Ошибка", "Выберите второй шаблон (Не занятые)")
            return
        if not self.excel_path.get():
            messagebox.showerror("Ошибка", "Выберите файл Excel с данными")
            return
        
        # Проверка существования файлов
        for path, name in [(self.template1_path.get(), "Шаблон 1"),
                           (self.template2_path.get(), "Шаблон 2"),
                           (self.excel_path.get(), "Excel файл")]:
            if not os.path.exists(path):
                messagebox.showerror("Ошибка", f"Файл не найден: {path}")
                return
        
        # Сохраняем конфигурацию перед запуском
        self.save_config()
        
        # Блокируем кнопку и запускаем обработку
        self.start_button.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        
        thread = Thread(target=self.process_files)
        thread.start()
    
    def merge_documents(self, doc1, doc2):
        """Объединение двух документов: добавление содержимого doc2 в конец doc1"""
        import tempfile
        
        # Сохраняем doc2 во временный файл
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            temp_path = tmp.name
            doc2.save(temp_path)
        
        # Загружаем временный файл заново
        temp_doc = Document(temp_path)
        
        # Добавляем разрыв страницы перед добавлением нового содержимого
        doc1.add_page_break()
        
        # Копируем все элементы из временного документа
        for element in temp_doc.element.body:
            doc1.element.body.append(element)
        
        # Удаляем временный файл
        try:
            os.unlink(temp_path)
        except:
            pass
        
        return doc1
    
    def clear_headers_footers(self, doc):
        """Полная очистка колонтитулов и установка отступов в 0"""
        from docx.shared import Cm
        
        for section in doc.sections:
            # Устанавливаем все отступы колонтитулов в 0
            section.top_margin = Cm(0)
            section.bottom_margin = Cm(0)
            section.header_distance = Cm(0)
            section.footer_distance = Cm(0)
            
            # Очищаем содержимое всех колонтитулов
            for header in [section.header, section.first_page_header, section.even_page_header]:
                for paragraph in header.paragraphs:
                    paragraph.clear()
            
            for footer in [section.footer, section.first_page_footer, section.even_page_footer]:
                for paragraph in footer.paragraphs:
                    paragraph.clear()
    
    def process_files(self):
        """Основная логика обработки файлов"""
        try:
            self.log("=" * 50)
            self.log("Генератор писем - запуск обработки")
            self.log("=" * 50)
            
            # Создание папки для результатов
            output_dir = self.output_dir.get()
            os.makedirs(output_dir, exist_ok=True)
            self.log(f"Папка для результатов: {output_dir}")
            
            # Чтение данных из Excel
            self.log("\nЧтение данных из Excel...")
            data_list = self.read_excel_data(self.excel_path.get())
            self.log(f"Найдено записей: {len(data_list)}")
            
            if not data_list:
                self.log("ОШИБКА: Нет данных для обработки!")
                return
            
            # Тестовый режим
            if self.test_mode.get():
                self.log("\n*** ТЕСТОВЫЙ РЕЖИМ - обрабатывается только 1 запись ***")
                data_list = data_list[:1]
            else:
                self.log(f"\n*** ПОЛНЫЙ РЕЖИМ - будут обработаны все {len(data_list)} записей ***")
            
            # Показать режим создания документов
            if self.merge_mode.get() == "single":
                self.log("*** РЕЖИМ: Все документы в одном файле ***")
            else:
                self.log("*** РЕЖИМ: Отдельные файлы для каждого человека ***")
            
            # Показать пример данных
            self.log("\nПример данных для обработки:")
            for i, d in enumerate(data_list[:3], 1):
                self.log(f"  {i}. {d['name_initials']}, {d['date']}, {d['address'][:40]}...")
            
            # Настройка прогресс-бара
            total = len(data_list)
            self.progress['maximum'] = total
            self.progress['value'] = 0
            
            # Обработка каждой записи
            self.log("\n--- Генерация писем ---")
            created_count = 0
            
            # Режим: все в одном файле
            if self.merge_mode.get() == "single":
                import tempfile
                temp_files1 = []  # Временные файлы для Уведомлений
                temp_files2 = []  # Временные файлы для Не занятых
                
                for i, data in enumerate(data_list, 1):
                    self.log(f"\n[{i}/{total}] Обработка: {data['name_initials']}")
                    
                    # Генерация временного первого письма
                    temp_doc1 = Document(self.template1_path.get())
                    self.clear_headers_footers(temp_doc1)
                    date_full = f"{data['date']} года рождения" if data['date'] else ''
                    date_short = f"{data['date']} рождения" if data['date'] else ''
                    replacements1 = {
                        self.TEMPLATE_NAME: data['name_initials'],
                        self.TEMPLATE_DATE_FULL: date_full,
                        self.TEMPLATE_DATE_SHORT: date_short,
                        self.TEMPLATE_DATE: data['date'],
                        self.TEMPLATE_ADDRESS: data['address'],
                    }
                    self.replace_in_document(temp_doc1, replacements1)
                    
                    # Сохраняем во временный файл
                    tmp1 = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
                    temp_doc1.save(tmp1.name)
                    temp_files1.append(tmp1.name)
                    tmp1.close()
                    
                    self.log(f"  ✓ Подготовлено: Уведомление для {data['name_initials']}")
                    
                    # Генерация временного второго письма
                    temp_doc2 = Document(self.template2_path.get())
                    self.clear_headers_footers(temp_doc2)
                    replacements2 = {
                        self.TEMPLATE_NAME: data['name_initials'],
                        self.TEMPLATE_ADDRESS_SHORT: data['address'],
                    }
                    self.replace_in_document(temp_doc2, replacements2)
                    
                    # Сохраняем во временный файл
                    tmp2 = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
                    temp_doc2.save(tmp2.name)
                    temp_files2.append(tmp2.name)
                    tmp2.close()
                    
                    self.log(f"  ✓ Подготовлено: Не занятые для {data['name_initials']}")
                    
                    # Обновление прогресса
                    self.progress['value'] = i
                    self.root.update_idletasks()
                
                # Объединяем все временные файлы в один документ
                self.log("\n--- Объединение документов ---")
                
                if temp_files1:
                    merged_doc1 = Document(temp_files1[0])
                    for temp_file in temp_files1[1:]:
                        temp_doc = Document(temp_file)
                        merged_doc1.add_page_break()
                        # Копируем параграфы
                        for para in temp_doc.paragraphs:
                            new_para = merged_doc1.add_paragraph()
                            new_para.alignment = para.alignment
                            new_para.paragraph_format.left_indent = para.paragraph_format.left_indent
                            new_para.paragraph_format.right_indent = para.paragraph_format.right_indent
                            new_para.paragraph_format.first_line_indent = para.paragraph_format.first_line_indent
                            new_para.paragraph_format.space_before = para.paragraph_format.space_before
                            new_para.paragraph_format.space_after = para.paragraph_format.space_after
                            for run in para.runs:
                                new_run = new_para.add_run(run.text)
                                new_run.bold = run.bold
                                new_run.italic = run.italic
                                new_run.underline = run.underline
                                if run.font.size:
                                    new_run.font.size = run.font.size
                                if run.font.name:
                                    new_run.font.name = run.font.name
                        # Копируем таблицы
                        for table in temp_doc.tables:
                            new_table = merged_doc1.add_table(rows=len(table.rows), cols=len(table.columns))
                            for i_row, row in enumerate(table.rows):
                                for i_col, cell in enumerate(row.cells):
                                    new_table.rows[i_row].cells[i_col].text = cell.text
                    
                    self.clear_headers_footers(merged_doc1)
                    output1 = os.path.join(output_dir, "Уведомления_все.docx")
                    merged_doc1.save(output1)
                    self.log(f"✓ Сохранен объединенный файл: Уведомления_все.docx")
                    created_count += 1
                    
                    # Удаляем временные файлы
                    for temp_file in temp_files1:
                        try:
                            os.unlink(temp_file)
                        except:
                            pass
                
                if temp_files2:
                    merged_doc2 = Document(temp_files2[0])
                    for temp_file in temp_files2[1:]:
                        temp_doc = Document(temp_file)
                        merged_doc2.add_page_break()
                        # Копируем параграфы
                        for para in temp_doc.paragraphs:
                            new_para = merged_doc2.add_paragraph()
                            new_para.alignment = para.alignment
                            new_para.paragraph_format.left_indent = para.paragraph_format.left_indent
                            new_para.paragraph_format.right_indent = para.paragraph_format.right_indent
                            new_para.paragraph_format.first_line_indent = para.paragraph_format.first_line_indent
                            new_para.paragraph_format.space_before = para.paragraph_format.space_before
                            new_para.paragraph_format.space_after = para.paragraph_format.space_after
                            for run in para.runs:
                                new_run = new_para.add_run(run.text)
                                new_run.bold = run.bold
                                new_run.italic = run.italic
                                new_run.underline = run.underline
                                if run.font.size:
                                    new_run.font.size = run.font.size
                                if run.font.name:
                                    new_run.font.name = run.font.name
                        # Копируем таблицы
                        for table in temp_doc.tables:
                            new_table = merged_doc2.add_table(rows=len(table.rows), cols=len(table.columns))
                            for i_row, row in enumerate(table.rows):
                                for i_col, cell in enumerate(row.cells):
                                    new_table.rows[i_row].cells[i_col].text = cell.text
                    
                    self.clear_headers_footers(merged_doc2)
                    output2 = os.path.join(output_dir, "Не_занятые_все.docx")
                    merged_doc2.save(output2)
                    self.log(f"✓ Сохранен объединенный файл: Не_занятые_все.docx")
                    created_count += 1
                    
                    # Удаляем временные файлы
                    for temp_file in temp_files2:
                        try:
                            os.unlink(temp_file)
                        except:
                            pass
            
            # Режим: отдельные файлы
            else:
                for i, data in enumerate(data_list, 1):
                    self.log(f"\n[{i}/{total}] Обработка: {data['name_initials']}")
                    
                    # Безопасное имя файла
                    safe_name = re.sub(r'[<>:"/\\|?*]', '_', data['name_initials'])
                    
                    # Генерация первого письма (Уведомление + Приглашение)
                    output1 = os.path.join(output_dir, f"Уведомление_{safe_name}.docx")
                    replaced1 = self.generate_letter(self.template1_path.get(), output1, data, is_template1=True)
                    self.log(f"  ✓ Создано: Уведомление_{safe_name}.docx")
                    name_count = replaced1.get(self.TEMPLATE_NAME, 0)
                    date_count = replaced1.get(self.TEMPLATE_DATE_FULL, 0) + replaced1.get(self.TEMPLATE_DATE_SHORT, 0)
                    addr_count = replaced1.get(self.TEMPLATE_ADDRESS, 0)
                    self.log(f"    Замены: Имя={name_count}, Дата={date_count}, Адрес={addr_count}")
                    created_count += 1
                    
                    # Генерация второго письма (Не занятые)
                    output2 = os.path.join(output_dir, f"Не_занятые_{safe_name}.docx")
                    replaced2 = self.generate_letter(self.template2_path.get(), output2, data, is_template1=False)
                    self.log(f"  ✓ Создано: Не_занятые_{safe_name}.docx")
                    created_count += 1
                    
                    # Обновление прогресса
                    self.progress['value'] = i
                    self.root.update_idletasks()
            
            self.log("\n" + "=" * 50)
            self.log(f"ГОТОВО! Создано файлов: {created_count}")
            self.log(f"Результаты в папке: {output_dir}")
            self.log("=" * 50)
            
            messagebox.showinfo("Успех", f"Обработка завершена!\nСоздано файлов: {created_count}")
            
        except Exception as e:
            self.log(f"\nОШИБКА: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
        
        finally:
            self.start_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = LetterGeneratorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
