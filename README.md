# Проект по анализу данных гонок Формулы-2

## Данные, которые мы собирали:

### Для трассы:

**Источник данных:** Сбор данных об играх с официального сайта Formula-2

**Название трека:** Уникальное название каждой игры

**Страна:** Компания, разработавшая игру

**Город:** Дата, когда игра была выпущена на рынок/добавлена в магазин

**Дата:** Категория игры

### Для гонщика:

**Позицию:** Позицию гонщика на финише

**Номер болида:** Номер болида

**Имя гонщика:** Имя гонщика в формате И. Фамилия

**Название команды:** Название конманды к которой прикреплён гонщик

**Кол-во кругов:** Кол-во кругов, которое проехал гонщик

**Время:** За сколько по времени гонщик проехал всю гонку

**Отставание от впереди идущего:** Отставание от впереди идущего

**Отставание от первого:** Отставание от первого

**Средняя скорость:** Средняя скорость по всей гонки

**Время лучшего круга:** Время за которое был проехан лучший круг

## Гипотезы:

1. Консистентность результатов в разных форматах гонок. Позиция в квалификации не сильно коррелирует
   с позицией в спринтерской гонке, но слабо коррелирует с позицией в основной гонке
2. Влияние длины трассы на время гонки. Вывод: Длина трассы очень слабо коррелирует с временем
   гонки, что отвергает нашу гипотезу
3. Влияние команды на результаты гонки. Вывод: Некоторые команды стабильно показывают лучшие
   результаты по сравнению с другими, независимо от трассы или типа гонки
4. Индивидуальное мастерство гонщика влияет на результаты гонки. Вывод: Некоторые гонщики стабильно
   превосходят своих напарников по команде, что говорит о значительной роли индивидуального
   мастерства в результатах гонок
5. Корреляция лучшего времени круга с итоговой позицией в гонке очень высока: Лучшее время круга,
   показанное гонщиком во время гонки, сильно коррелирует с его итоговой позицией в этой гонке

## Предсказательная переменная:

Позиция гонщика в гонке

# Обновление файла requirements.txt

Наша команда советует обновить этот файл на всякий случай. Для этого нужно выполнить следующие
команды:

```bash
source venv/bin/activate
pip freeze > requirements.txt
```

# Рассмотрим проект более подробно:

## 1. Подготовка данных

### `parser.py`

Этот файл содержит класс `DataParser`, который извлекает информацию о видеоиграх с веб-сайта и
сохраняет данные в формате JSON. Основные функции включают:

Установка базового URL и файла для сохранения данных.

Загрузка HTML-контента страницы.

Извлечение данных о видеоигре с помощью BeautifulSoup.

Сохранение данных в JSON-файл, обновляя существующий файл или создавая новый.

## 2. Сбор данных

`output_maker.ipynb` использует парсер для сбора данных с веб-сайта, генерируя список URL-адресов,
которые необходимо просканировать, и собирает данные о видеоиграх.

## 3. Анализ данных

### `EDA.ipynb`

Была сделана:

Очистка данных от дубликатов, ошибок и несоответствий.

Статистический анализ и визуализация данных для получения инсайтов.

Проверка различных гипотез, на основе данных.

## 4. Машинное обучение

На основе обработанных данных проводится обучение модели машинного обучения для предсказания
места в гонке. Используются различные модели, такие как Linear Regression, Decision Tree, XGBoost,
Gradient Boosting. Наилучшие результаты были достигнуты с использованием XGBoost, а затем улучшены с
помощью `XGBRegressor`.
