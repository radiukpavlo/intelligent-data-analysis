# Налаштування середовища для написання коду з Python

Налаштування власного середовища для програмування методів "Дослідження операцій та основ теорії прийняття рішень" може бути досить складним завданням.

В цьому туторіалі ми розглянемо налаштування середовища на власному локальному/віддаленому ПК. За такого підходу ви матимете більше гнучкості щодо розроблення і тестування вашого коду.

Зауважу, що це **налаштування опирається на операційну систему Windows**. Якщо ви використовуєте macOS або Linux, вам варто звернутися до документації Python.

## Етапи локального налаштування для системи Windows

1. [Інсталюйте Anaconda](https://www.anaconda.com/products/distribution).
Головне тут - це отримати доступ до віртуального середовища `conda` в командному рядку. Інсталювати Anaconda потрібно за шляхом, який стоїть за замовчуванням.

>*Примітка:* Якщо у вас недостатньо фізичної пам'яті на диску `C:\`, ви можете завантажити та інсталювати полегшений дистрибутив під назвою [miniconda](https://docs.anaconda.com/free/miniconda/index.html).

2. Створіть теку для матеріалів курсу; ви можете назвати її якзавгодно. Наприклад,

```bash
mkdir or-course
cd or-course
```

3. Створіть віртуальне середовище `conda`. Наступна команда створить середовище `my-course`, яке перебуватиме в теці `anaconda3` на вашому ПК за шляхом `C:\Users\[userName]`. Натисніть `y`, коли команда нижче запитає `y/n?`.

```bash
conda create -n my-course python=3.9
```

4. Активуйте щойно створене середовище.

```bash
conda activate my-course
```

5. Інсталюйте необхідні залежні бібліотеки, які вам знадобляться для курсу, наприклад, [PuLP](https://coin-or.github.io/pulp/). Ви можете запустити все це одночасно:

```bash
pip install pandas numpy matplotlib scikit-learn jupyterlab pulp
```

6. Переконайтеся, що встановлення Anaconda та супутних бібліотек виконано правильно, запустивши сервер Jupyter Lab:

```bash
jupyter lab
```

7. Після запуску Jupyter Lab, запустіть Jupyter Launcher і виконайте наступний фрагмент коду в комірці.

```python
import pandas as pd
import numpy as np
import pulp as pl
import matplotlib

# Перевірте доступ до PuLP
# Нижче виведмо список усіх доступних солверів
solver_list = pl.listSolvers()
print(solver_list)
```

8. Інсталюйте Visual Studio Code з офіціного сайту за [посиланням](https://code.visualstudio.com/).

9. У Visual Studio Code Marketplace інсталюйте extensions [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) та [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) за посиланням.

10. Підключіть Visual Studio Code до віртуального середовища `conda`, відповідно до [туторіала](https://code.visualstudio.com/docs/python/environments).
