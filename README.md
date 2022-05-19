
# Анализ отзывов на антидепрессанты

В данной работе решается задача автоматической суммаризации нескольких документов на примере отзывов на антидепрессанты
### Что такое суммаризация текста?

![Суммаризация документов](https://i.ibb.co/59hjr4m/img-sum.png)


**Автоматическая суммаризация текста** -- уменьшение размера текста с сохранением его информативности;
**Суммаризация отзывов** -- это задача суммаризации нескольких документов;
**Аспект** -- слово или словосочетание, которое является объектом характеристики в данном предложении.

**Пример аспекта:**

 - Положительный аспект

> Буквально через пару недель почувствовала, что
> **раздражительность** как рукой сняло.
>>
- Отрицательный аспект:
> В начале терапии и при увеличении дозы могут появляться тревога и
> **раздражительность**, нарушения сна, ...

<!-- 
### План работы: 
* Изучить [литературу](https://scholar.google.ru/scholar?q=antidepressants+analysis+scholar&hl=en&as_sdt=0&as_vis=1&oi=scholart) по теме
* Подготовить список антидепрессантов (например, 10 самых популярных)
* Сделать табличку с описанием из инструкции
* [Выгрузить отзывы из Twitter](https://drive.google.com/open?id=1OcO-5Ou9pvvfda-ywp0qtCchz5AFBVh3)
* Описать коллецкию данных (анализ тональности, топ-10 ключевых слов и пр.)
* Сделать табличку:  

| Название |      Цена     | Рецептурно |     Эффективность    | Продожительность |           Побочные действия           |  
|:--------:|:-------------:|:----------:|:--------------------:|:----------------:|:-------------------------------------:|  
|    ...   | дорого/дёшево |   да/нет   | помогает/не помогает |     в неделях    | частые, ближ. к тем, что в инструкции | 
* *(Бонус)* Анализ twitter в связи с COVID (панические симптомы и COVID) -->
## Данные
### Cписок анализируемых антидепрессантов
Для анализа возьмём 5 самых популярных антидепрессантов типа [СИОЗС](https://ru.wikipedia.org/wiki/Селективные_ингибиторы_обратного_захвата_серотонина):
* [Prozac (fluoxetine)](https://ru.wikipedia.org/wiki/Флуоксетин)
* [Celexa (citalopram)](https://ru.wikipedia.org/wiki/Циталопрам)
* [Zoloft (sertraline)](https://ru.wikipedia.org/wiki/Сертралин)
* [Paxil (paroxetine)](https://ru.wikipedia.org/wiki/Пароксетин)
* [Lexapro (escitalopram)](https://ru.wikipedia.org/wiki/Эсциталопрам)
Данные собирались из двух разных источников: *Twitter.com*  и *Otzovik.com*.

## Методы
В результате исследования были разработаны и реализованы два подхода: с ручным и автоматическим выделением аспектов.
### Метод, основанный на близости слов
-  Выделение аспектов вручную;
- Лемматизация и получение низкоразмерного векторного представления каждого слова в отзыве и каждого аспекта при помощи word2vec;
- Для каждого аспекта и для каждого отзыва вычисляется индикатор того, содержится ли в отзыве слово, семантически близкое к аспекту;
- Вычисление мат. ожидания от индикатора для каждого аспекта.

![Аспекты_вручную](https://i.ibb.co/RcGw3Nb/w2v-1.png)
Для примера выше в качестве результата считаем, что исследуемому препарату соответствуют следущие аспекты: тошнота, раздрожительность, аппетит, депрессия и эффективность.


### Автоматическое выделение аспектов

- Текст каждого отзыва разбивается на предложения;
- Для каждого отзыва формируется два списка: список предложений с позитивной и негативной тональностью;
- Для каждого слова в позитивных и негативных предложениях определяем часть речи;
- В каждом предложении для каждого существительного выделяется слово, ассоциирующееся с ним. Ассоциации вычисляем, применяя априорный алгоритм;
- Чтобы избежать повторений, лемматизируем слова и удалим аспекты, содержащие друг друга, оставляя аспект с бóльшей длиной ([Головная, Боль, Головная боль] -> [Головная боль])
![Аспекты_автоматически](https://i.ibb.co/4d2b9HJ/res-1.png)
В результате мы получим список положительных и отрицательных аспектов по каждому препарату.

## Выводы
Алгоритм с автоматическим выделением аспектов предпочтительнее по ряду причин
- Меньше человеческих усилий;
- Позволяет расширить задачу на суммаризацию отзывов о любых препаратах;
- В дальнешем можно использовать кластеризацию аспектов с использованием косинусного расстояния между векторизованными аспектами.
