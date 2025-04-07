# Налаштування середовища для написання коду з Python

Налаштування власного середовища для програмування методів "Інтелектуальний аналіз даних" може бути досить складним завданням.

В цьому туторіалі ми розглянемо налаштування середовища на власному локальному/віддаленому ПК. За такого підходу ви матимете більше гнучкості щодо розроблення та тестування вашого програмного коду.

Зауважу, що це **налаштування опирається на операційну систему Windows**. Якщо ви використовуєте macOS або Linux, вам варто звернутися до документації Python.

## Етапи локального налаштування для системи Windows

1. [Інсталюйте Anaconda](https://www.anaconda.com/products/distribution).
Головне тут - це отримати доступ до віртуального середовища `conda` в командному рядку. Наполегливо рекомендую інсталювати Anaconda за тим шляхом, який вказано за замовчуванням. Це дасть змогу уникати багатьох проблем з OS Windows.

>*Примітка:* Якщо у вас недостатньо фізичної пам'яті на диску `C:\`, ви можете завантажити та інсталювати *легший* дистрибутив під назвою [miniconda](https://docs.anaconda.com/free/miniconda/index.html).

2. Створіть теку для матеріалів курсу; ви можете назвати її як завгодно. Наприклад,

```bash
mkdir ida-course
cd ida-course
```

3. Створіть віртуальне середовище `conda`. Наступна команда створить середовище `ida-course`, яке перебуватиме в теці `anaconda3` на вашому ПК за шляхом `C:\Users\[userName]`. Натисніть `y`, коли команда нижче запитає `y/n?`.

```bash
conda create -n ida-course python=3.10
```

4. Активуйте щойно створене середовище.

```bash
conda activate ida-course
```

5. Інсталюйте необхідні залежні бібліотеки, які вам знадобляться для курсу. Ви можете запустити все це одночасно:

```bash
pip install pandas numpy matplotlib scikit-learn jupyterlab
```

6. Переконайтеся, що встановлення Anaconda та інших бібліотек виконано правильно, запустивши сервер Jupyter Lab:

```bash
jupyter lab
```

7. Після запуску Jupyter Lab, запустіть Jupyter Launcher і виконайте такий фрагмент коду в комірці.

```python
import importlib

libraries = ['pandas', 'numpy', 'matplotlib', 'sklearn', 'jupyterlab']

for lib in libraries:
    spec = importlib.util.find_spec(lib)
    if spec is None:
        print(f"{lib} is not installed.")
    else:
        print(f"{lib} is installed.")
```

8. Інсталюйте Visual Studio Code з офіційного вебсайту за [посиланням](https://code.visualstudio.com/).

9. У Visual Studio Code Marketplace інсталюйте extensions [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) та [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) за посиланням.

10. Підключіть Visual Studio Code до віртуального середовища `conda`, відповідно до [туторіалу](https://code.visualstudio.com/docs/python/environments).
