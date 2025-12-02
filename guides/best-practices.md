# Лучшие практики / Best Practices

## 🌟 Золотые правила промт-инжиниринга / Golden Rules of Prompt Engineering

### 1. Будьте специфичны / Be Specific

Чем конкретнее запрос, тем точнее результат.

The more specific the request, the more accurate the result.

### 2. Предоставляйте контекст / Provide Context

AI работает лучше, когда понимает полную картину.

AI works better when it understands the full picture.

### 3. Используйте примеры / Use Examples

Покажите, что вы хотите получить.

Show what you want to get.

### 4. Структурируйте промт / Structure Your Prompt

Организованный промт → организованный ответ.

Organized prompt → organized response.

### 5. Итерируйте / Iterate

Первая версия редко бывает идеальной.

The first version is rarely perfect.

## 💼 Практики для разных сценариев / Practices for Different Scenarios

### Разработка кода / Code Development

**✅ Делать / Do:**
- Указывать язык программирования / Specify programming language
- Описывать ожидаемое поведение / Describe expected behavior
- Упоминать требования к производительности / Mention performance requirements
- Просить о тестах / Ask for tests
- Указывать стиль кодирования / Specify coding style

**❌ Не делать / Don't:**
- Использовать расплывчатые термины / Use vague terms
- Пропускать edge cases / Skip edge cases
- Игнорировать контекст проекта / Ignore project context

### Написание текстов / Text Writing

**✅ Делать / Do:**
- Определять целевую аудиторию / Define target audience
- Указывать тон и стиль / Specify tone and style
- Устанавливать ограничения по длине / Set length constraints
- Описывать цель текста / Describe text purpose

**❌ Не делать / Don't:**
- Оставлять тон неопределенным / Leave tone undefined
- Забывать про структуру / Forget about structure

### Анализ данных / Data Analysis

**✅ Делать / Do:**
- Описывать источник данных / Describe data source
- Указывать метрики интереса / Specify metrics of interest
- Определять формат вывода / Define output format
- Запрашивать визуализации при необходимости / Request visualizations when needed

**❌ Не делать / Don't:**
- Предоставлять неполные данные / Provide incomplete data
- Пропускать единицы измерения / Skip units of measurement

## 🎯 Оптимизация промтов / Prompt Optimization

### Техника SMART

Ваш промт должен быть / Your prompt should be:

- **S**pecific (Конкретный / Specific)
- **M**easurable (Измеримый / Measurable)
- **A**chievable (Достижимый / Achievable)
- **R**elevant (Релевантный / Relevant)
- **T**ime-bound (Ограниченный по времени / Time-bound)

### Принцип 4C

- **Clear** (Ясный / Clear) — нет двусмысленности / no ambiguity
- **Concise** (Краткий / Concise) — без лишних слов / without extra words
- **Complete** (Полный / Complete) — вся необходимая информация / all necessary information
- **Contextual** (Контекстный / Contextual) — с релевантным контекстом / with relevant context

## 🔍 Отладка промтов / Debugging Prompts

Если результат не соответствует ожиданиям / If the result doesn't meet expectations:

1. **Проверьте ясность** / Check clarity
   - Промт понятен? / Is the prompt clear?
   - Есть ли двусмысленность? / Is there ambiguity?

2. **Добавьте детали** / Add details
   - Достаточно ли контекста? / Is there enough context?
   - Нужны ли примеры? / Are examples needed?

3. **Уточните формат** / Clarify format
   - Четко ли определен желаемый формат? / Is the desired format clearly defined?
   - Нужна ли структура? / Is structure needed?

4. **Проверьте область действия** / Check scope
   - Не слишком ли широкий запрос? / Is the request too broad?
   - Можно ли разбить на части? / Can it be broken down?

## 📝 Шаблоны для быстрого старта / Quick Start Templates

### Шаблон для задач / Task Template

```
Задача: [Что нужно сделать]
Контекст: [Почему и для чего]
Входные данные: [Что есть]
Ожидаемый результат: [Что должно получиться]
Ограничения: [Что нужно учесть]

Task: [What needs to be done]
Context: [Why and what for]
Input: [What you have]
Expected result: [What should be obtained]
Constraints: [What needs to be considered]
```

### Шаблон для исследования / Research Template

```
Тема: [О чем]
Цель: [Зачем]
Фокус: [На что обратить внимание]
Формат: [Как представить]
Источники: [Откуда брать информацию]

Topic: [About what]
Purpose: [Why]
Focus: [What to pay attention to]
Format: [How to present]
Sources: [Where to get information]
```

### Шаблон для креатива / Creative Template

```
Тип: [Что создать]
Стиль: [Как это должно выглядеть]
Аудитория: [Для кого]
Ключевое сообщение: [Что донести]
Ограничения: [Рамки творчества]

Type: [What to create]
Style: [How it should look]
Audience: [For whom]
Key message: [What to convey]
Constraints: [Creative boundaries]
```

## 🚀 Продвинутые техники / Advanced Techniques

### Многоступенчатые промты / Multi-step Prompts

Разбивайте сложные задачи на последовательность простых шагов.

Break complex tasks into a sequence of simple steps.

```
Шаг 1: [Первое действие]
Шаг 2: [Второе действие, основанное на результате шага 1]
Шаг 3: [Третье действие, основанное на результате шага 2]

Step 1: [First action]
Step 2: [Second action based on step 1 result]
Step 3: [Third action based on step 2 result]
```

### Условная логика / Conditional Logic

Добавляйте условия для разных сценариев.

Add conditions for different scenarios.

```
Если [условие], то [действие 1]
Иначе [действие 2]

If [condition], then [action 1]
Else [action 2]
```

### Мета-промты / Meta-prompts

Просите AI помочь улучшить сам промт.

Ask AI to help improve the prompt itself.

```
Вот мой промт: [промт]
Как я могу его улучшить, чтобы получить более точные результаты?

Here's my prompt: [prompt]
How can I improve it to get more accurate results?
```

## 📊 Метрики успеха / Success Metrics

Оценивайте качество промтов по / Evaluate prompt quality by:

- **Точность** / Accuracy — правильность результата / correctness of result
- **Релевантность** / Relevance — соответствие запросу / match to request
- **Полнота** / Completeness — наличие всего необходимого / presence of everything needed
- **Воспроизводимость** / Reproducibility — стабильность результатов / stability of results
- **Эффективность** / Efficiency — качество vs длина промта / quality vs prompt length

## 🎓 Обучение и развитие / Learning and Development

### Рекомендации / Recommendations

1. **Экспериментируйте** / Experiment
   - Пробуйте разные подходы / Try different approaches
   - Документируйте результаты / Document results

2. **Учитесь у других** / Learn from others
   - Изучайте примеры / Study examples
   - Читайте опыт сообщества / Read community experiences

3. **Делитесь знаниями** / Share knowledge
   - Публикуйте свои находки / Publish your findings
   - Помогайте другим / Help others

4. **Следите за трендами** / Follow trends
   - Новые техники / New techniques
   - Лучшие практики / Best practices

## 💡 Чек-лист качественного промта / Quality Prompt Checklist

Перед отправкой промта проверьте / Before sending a prompt, check:

- [ ] Цель четко определена / Goal clearly defined
- [ ] Контекст предоставлен / Context provided
- [ ] Формат вывода указан / Output format specified
- [ ] Примеры включены (при необходимости) / Examples included (if needed)
- [ ] Ограничения упомянуты / Constraints mentioned
- [ ] Нет двусмысленности / No ambiguity
- [ ] Запрос разумного размера / Request is reasonable size
- [ ] Используется правильная терминология / Correct terminology used

---

**Помните:** Лучшие практики — это отправная точка, а не жесткие правила. Адаптируйте их под свои нужды!

**Remember:** Best practices are a starting point, not rigid rules. Adapt them to your needs!
