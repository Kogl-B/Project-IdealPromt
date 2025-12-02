# Руководство по написанию промтов / Prompt Writing Guide

## 🎯 Основные принципы / Core Principles

### 1. Ясность и специфичность / Clarity and Specificity

**Плохо / Bad:**
```
Напиши код
Write code
```

**Хорошо / Good:**
```
Напиши функцию на Python, которая принимает список чисел и возвращает их среднее значение. Добавь обработку ошибок для пустых списков.

Write a Python function that takes a list of numbers and returns their average. Add error handling for empty lists.
```

### 2. Контекст / Context

Предоставьте необходимый контекст для понимания задачи.

Provide necessary context for understanding the task.

**Структура / Structure:**
- Кто вы и какова ваша роль / Who you are and your role
- Что вы хотите достичь / What you want to achieve
- Почему это важно / Why it matters
- Какие ограничения существуют / What constraints exist

### 3. Формат вывода / Output Format

Четко укажите желаемый формат ответа.

Clearly specify the desired response format.

**Пример / Example:**
```
Предоставь ответ в следующем формате:
1. Краткое резюме (2-3 предложения)
2. Детальный анализ
3. Рекомендации (маркированный список)

Provide the answer in the following format:
1. Brief summary (2-3 sentences)
2. Detailed analysis
3. Recommendations (bulleted list)
```

## 🏗️ Структура эффективного промта / Effective Prompt Structure

### Базовый шаблон / Basic Template

```
[Роль / Role]: Ты опытный [специальность] / You are an experienced [specialty]

[Контекст / Context]: Я работаю над [проект/задача] / I'm working on [project/task]

[Задача / Task]: Мне нужно [конкретное действие] / I need to [specific action]

[Требования / Requirements]:
- Требование 1 / Requirement 1
- Требование 2 / Requirement 2
- Требование 3 / Requirement 3

[Формат / Format]: Предоставь результат в виде [формат] / Provide the result as [format]

[Ограничения / Constraints]: Учти следующие ограничения / Consider the following constraints:
- Ограничение 1 / Constraint 1
- Ограничение 2 / Constraint 2
```

## 💡 Техники улучшения промтов / Prompt Improvement Techniques

### 1. Chain of Thought (Цепь рассуждений)

Попросите AI объяснить свой процесс мышления.

Ask the AI to explain its thinking process.

```
Объясни свои рассуждения шаг за шагом перед тем, как дать финальный ответ.

Explain your reasoning step by step before giving the final answer.
```

### 2. Few-Shot Learning (Обучение на примерах)

Предоставьте примеры желаемого вывода.

Provide examples of desired output.

```
Вот несколько примеров:

Входные данные: [пример 1]
Выходные данные: [результат 1]

Входные данные: [пример 2]
Выходные данные: [результат 2]

Теперь обработай: [новые данные]
```

### 3. Role-Playing (Ролевая игра)

Назначьте AI конкретную роль или экспертизу.

Assign the AI a specific role or expertise.

```
Ты опытный архитектор программного обеспечения с 15-летним опытом в разработке масштабируемых систем.

You are an experienced software architect with 15 years of experience in developing scalable systems.
```

### 4. Iterative Refinement (Итеративное улучшение)

Уточняйте и улучшайте промт на основе результатов.

Refine and improve the prompt based on results.

**Процесс / Process:**
1. Создайте начальный промт / Create initial prompt
2. Оцените результат / Evaluate result
3. Определите проблемы / Identify issues
4. Уточните промт / Refine prompt
5. Повторите / Repeat

## 🎨 Специализированные техники / Specialized Techniques

### Для кодинга / For Coding

```
Напиши [язык программирования] код для [задача].

Требования:
- Следуй [стандарту кодирования]
- Включи обработку ошибок
- Добавь комментарии
- Напиши unit-тесты
- Оптимизируй для [производительности/читаемости]

Write [programming language] code for [task].

Requirements:
- Follow [coding standard]
- Include error handling
- Add comments
- Write unit tests
- Optimize for [performance/readability]
```

### Для анализа / For Analysis

```
Проанализируй [данные/ситуацию] и предоставь:
1. Ключевые находки
2. Паттерны и тренды
3. Потенциальные проблемы
4. Рекомендации

Используй объективный, основанный на данных подход.

Analyze [data/situation] and provide:
1. Key findings
2. Patterns and trends
3. Potential issues
4. Recommendations

Use an objective, data-driven approach.
```

### Для творчества / For Creative Work

```
Создай [тип контента] на тему [тема].

Стиль: [описание стиля]
Тон: [формальный/неформальный/профессиональный]
Целевая аудитория: [описание]
Длина: [количество слов/параграфов]

Create [content type] about [topic].

Style: [style description]
Tone: [formal/informal/professional]
Target audience: [description]
Length: [word/paragraph count]
```

## ⚠️ Частые ошибки / Common Mistakes

### ❌ Слишком расплывчато / Too Vague
```
Помоги мне с кодом
Help me with code
```

### ✅ Конкретно / Specific
```
Помоги мне исправить ошибку "IndexError" в моей Python функции, которая обрабатывает список. Вот код: [код]

Help me fix an "IndexError" in my Python function that processes a list. Here's the code: [code]
```

### ❌ Слишком много задач / Too Many Tasks
```
Напиши приложение, создай документацию, протестируй его, и разверни на сервере
Write an app, create documentation, test it, and deploy to server
```

### ✅ Разбито на шаги / Broken Into Steps
```
Шаг 1: Напиши базовую структуру приложения
Step 1: Write the basic app structure
[Затем продолжить с другими задачами]
[Then continue with other tasks]
```

## 📊 Оценка качества промта / Prompt Quality Evaluation

Хороший промт должен быть / A good prompt should be:

- [ ] **Конкретным** / Specific
- [ ] **Понятным** / Clear
- [ ] **Полным** / Complete
- [ ] **Структурированным** / Structured
- [ ] **Воспроизводимым** / Reproducible

## 🔄 Итеративное улучшение / Iterative Improvement

1. **Начните просто** / Start simple
2. **Тестируйте результаты** / Test results
3. **Добавляйте детали** / Add details
4. **Уточняйте формат** / Refine format
5. **Документируйте что работает** / Document what works

## 📚 Дополнительные ресурсы / Additional Resources

- Изучайте успешные примеры в папке `examples/` / Study successful examples in the `examples/` folder
- Читайте опыт других в `experiences/` / Read others' experiences in `experiences/`
- Следите за наблюдениями в `observations/` / Follow observations in `observations/`

---

**Помните:** Идеальный промт — это результат экспериментов и итераций. Не бойтесь пробовать разные подходы!

**Remember:** The ideal prompt is the result of experimentation and iteration. Don't be afraid to try different approaches!
