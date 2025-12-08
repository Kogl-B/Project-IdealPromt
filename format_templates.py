#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для форматирования шаблонов Word
1. Устанавливает размер шрифта 9.5 pt для всего текста, кроме заголовков
2. Удаляет отступы колонтитулов
"""

from docx import Document
from docx.shared import Pt

def format_document(filepath, output_filepath):
    """Форматирование документа"""
    doc = Document(filepath)
    
    print(f"\n=== Обработка: {filepath} ===")
    
    # 1. Форматирование шрифтов в параграфах
    print("\n1. Изменение размеров шрифтов...")
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        
        # Заголовки остаются 11 pt
        if 'УВЕДОМЛЕНИЕ О ЯВКЕ' in text or 'ПРИГЛАШЕНИЕ' in text:
            print(f"   [{i}] Заголовок (11 pt): {text[:50]}...")
            for run in para.runs:
                run.font.size = Pt(11)
        else:
            # Весь остальной текст - 9.5 pt
            for run in para.runs:
                run.font.size = Pt(9.5)
    
    # 2. Форматирование таблиц
    print("\n2. Форматирование таблиц...")
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.font.size = Pt(9.5)
    
    # 3. Удаление отступов колонтитулов и границ
    # 3. Удаление колонтитулов и их отступов
    print("\n3. Удаление колонтитулов и отступов...")
    for i, section in enumerate(doc.sections):
        print(f"   Секция {i}:")
        print(f"     До: top_margin={section.top_margin.cm:.2f}см, bottom_margin={section.bottom_margin.cm:.2f}см")
        
        # Полностью удаляем все отступы - колонтитулы не нужны
        section.header_distance = Pt(0)
        section.footer_distance = Pt(0)
        section.top_margin = Pt(0)
        section.bottom_margin = Pt(0)
        
        # Очищаем содержимое колонтитулов
        for header in [section.header, section.first_page_header, section.even_page_header]:
            if header:
                for para in header.paragraphs:
                    para.clear()
        
        for footer in [section.footer, section.first_page_footer, section.even_page_footer]:
            if footer:
                for para in footer.paragraphs:
                    para.clear()
        
        print(f"     После: top_margin={section.top_margin.cm:.2f}см, bottom_margin={section.bottom_margin.cm:.2f}см")
        print(f"            header_distance={section.header_distance.cm:.2f}см, footer_distance={section.footer_distance.cm:.2f}см")
        print(f"            Колонтитулы очищены")
    
    # Сохранение
    doc.save(output_filepath)
    print(f"\n✓ Сохранено: {output_filepath}")


def main():
    # Обработка первого шаблона
    format_document(
        'Письма  УВЕДОМЛЕНИЕ, ПРИГЛАШЕНИЕ.docx',
        'Письма  УВЕДОМЛЕНИЕ, ПРИГЛАШЕНИЕ.docx'
    )
    
    # Обработка второго шаблона
    format_document(
        'Письма НЕ ЗАНЯТЫЕ.docx',
        'Письма НЕ ЗАНЯТЫЕ.docx'
    )
    
    print("\n" + "=" * 50)
    print("Форматирование завершено!")
    print("=" * 50)


if __name__ == '__main__':
    main()
