На вход подаётся файл input.json:
- N - номер студента;
- DD - день рождения;
- MM - месяц рождения;
- YYYY - год рождения.

На выходе создаётся файл output.csv, который спокойно открывается в exel. 
Все необходимые данные там есть. 

Итоговую формулу выводите сами!

После сохранения данных, открывается окно с необходимыми графиками в
чёрно-белом цвете.
Рекомендуется раскрыть его в полный экран.

Также в самом файле.py есть константы PLOT_STEPS_X и PLOT_STEPS_Y,
используемые для перерасчёта шагов для построения графика.
Могут быть разными.

Рекомендуется использовать значения от 50 до 70.
Если ввести значения 1 или меньше, то расчёт будет вестись по истинному 
количеству шагов. 

Графики скорее всего будут сильно меняться - это нормально и является
свойством предложенной Инютиным явной схемы.
Можно использовать это и подобрать наиболее "видимый" график
(чтобы он не был почти весь чёрный или почти весь белый).