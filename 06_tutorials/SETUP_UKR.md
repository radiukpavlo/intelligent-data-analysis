# Налаштування середовища для Python та Anaconda (Windows/macOS/Linux)

Нижче — покроковий, детальний гайд із налаштування робочого середовища для Python із використанням Anaconda/Miniconda, JupyterLab та Visual Studio Code. Матеріал орієнтований на студентів і початківців, але включає технічні деталі, які корисні й досвідченим користувачам.

Зображення для орієнтації:

- Python: https://www.python.org/static/community_logos/python-logo.png
- Jupyter: https://jupyter.org/assets/homepage/main-logo.svg
- VS Code: https://code.visualstudio.com/assets/images/code-stable.png
- Anaconda installer (приклад): https://docs.anaconda.com/_images/install_Anaconda.png
- Miniconda installer (приклад): https://docs.anaconda.com/_images/install_Miniconda.png
- Перші кроки встановлення в Windows (приклад): https://docs.anaconda.com/_images/win-install-01.png
- Anaconda Navigator (огляд): https://docs.anaconda.com/_images/navigator.png


## 1) Що саме встановлюємо і навіщо

- Python: інтерпретатор мови та стандартна бібліотека.
- Conda (Anaconda/Miniconda): менеджер середовищ і пакетів; дозволяє створювати ізольовані середовища з різними версіями Python і бібліотек.
- JupyterLab: інтерактивні ноутбуки для досліджень, аналізу даних і демонстрацій.
- Visual Studio Code: редактор коду, налагодження, інтеграція з Python і Jupyter.

Корисні посилання:

- Python: https://www.python.org/downloads/
- Miniconda: https://docs.anaconda.com/free/miniconda/
- Anaconda Distribution: https://www.anaconda.com/download
- JupyterLab: https://jupyter.org/install
- Visual Studio Code: https://code.visualstudio.com/


## 2) Anaconda чи Miniconda — що обрати

- Anaconda: велика збірка з багатьма пакетами «з коробки» (зручно, але займає більше місця).
- Miniconda: мінімальна установка (conda + Python); ставите тільки потрібне. Рекомендовано для навчальних курсів і репродуктивності.

Рекомендація курсу: Miniconda — менше, швидше, повний контроль залежностей; за потреби завжди можна встановити Anaconda Navigator (GUI) окремо або додати пакети з каналів `conda-forge` / `defaults`.


## 3) Встановлення Miniconda/Anaconda

Нижче — короткі інструкції для кожної ОС. Після інсталяції обов’язково виконайте «Ініціалізацію conda» (розділ 4).

### Windows

1. Завантажте інсталятор:
   - Miniconda: https://docs.anaconda.com/free/miniconda/
   - Anaconda: https://www.anaconda.com/download

2. Запустіть `.exe` інсталятор. На кроці «Advanced Options» рекомендується:
   - Не додавати conda до PATH (галочка «Add Anaconda/Miniconda to my PATH» — знята). Це зменшує конфлікти.
   - Дозволити реєстрацію як «default Python» можна або ні — не критично, ми явно обиратимемо інтерпретатор у VS Code.

3. Після встановлення відкрийте «Anaconda Prompt» або PowerShell і виконайте ініціалізацію (див. розділ 4).

Ілюстративні зображення:

- Інсталятор Anaconda: https://docs.anaconda.com/_images/install_Anaconda.png
- Інсталятор Miniconda: https://docs.anaconda.com/_images/install_Miniconda.png
- Приклад кроків у Windows: https://docs.anaconda.com/_images/win-install-01.png

### macOS

1. Завантажте інсталятор (`.pkg` або командний інсталятор):
   - Miniconda: https://docs.anaconda.com/free/miniconda/
   - Anaconda: https://www.anaconda.com/download

2. Встановіть за допомогою GUI (`.pkg`) або через термінал (`.sh`).

3. Відкрийте термінал і виконайте ініціалізацію conda (розділ 4).

### Linux

1. Завантажте інсталятор (`.sh`) для вашої архітектури з:
   - Miniconda: https://docs.anaconda.com/free/miniconda/
   - Anaconda: https://www.anaconda.com/download

2. Встановіть через термінал, наприклад:

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

3. Ініціалізуйте conda (розділ 4), перезапустіть термінал.


## 4) Ініціалізація conda і перевірка встановлення

Після інсталяції потрібно ініціалізувати ваш shell, щоби команда `conda` була доступна автоматично.

Перевірте наявність conda:

```bash
conda --version
```

Якщо команда не знайдена — ініціалізуйте shell.

Ініціалізація для різних оболонок:

```powershell
# PowerShell (Windows)
conda init powershell
```

```bash
# cmd.exe (Windows)
conda init cmd.exe

# Bash (Linux/macOS)
conda init bash

# Zsh (macOS, іноді Linux)
conda init zsh
```

Після цього закрийте та знову відкрийте термінал/профіль. Повторно перевірте версії:

```bash
conda --version
python --version
```


## 5) Створення окремого середовища для курсу

Створіть окреме середовище з конкретною версією Python (рекомендовано уникати використання «base» для проєктів):

```bash
conda create -n ida-course python=3.10
```

Активуйте середовище:

```bash
conda activate ida-course
```

Базові пакети для аналізу даних та навчання:

```bash
# Вариант 1: conda з каналом conda-forge (часто свіжіші збірки)
conda install -c conda-forge numpy pandas matplotlib scikit-learn jupyterlab ipykernel

# Вариант 2: pip (уже всередині активованого середовища)
pip install numpy pandas matplotlib seaborn scikit-learn jupyterlab ipykernel
```

Примітки:

- Якщо встановлюєте через `pip`, робіть це тільки в активованому середовищі conda, щоби уникнути конфліктів системних пакетів.
- Канал `conda-forge` містить багато актуальних пакетів; можна вмикати його глобально: `conda config --add channels conda-forge` і `conda config --set channel_priority flexible`.


## 6) Налаштування JupyterLab і ядра (kernel)

Запустіть JupyterLab з активованого середовища:

```bash
jupyter lab
```

Щоб явним чином додати ядро цього середовища до списку в Jupyter (видиме як окремий інтерпретатор):

```bash
python -m ipykernel install --user --name ida-course --display-name "Python (ida-course)"
```

У JupyterLab у «Launcher» обирайте ядро «Python (ida-course)» для створення ноутбуків із правильним середовищем.


## 7) Налаштування Visual Studio Code

1. Встановіть VS Code: https://code.visualstudio.com/
2. Додайте розширення:
   - Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python
   - Jupyter: https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter
3. Виберіть інтерпретатор середовища `ida-course`:
   - Команда: «Python: Select Interpreter» і виберіть інтерпретатор із шляху `.../envs/ida-course/bin/python` (Linux/macOS) або `...\Anaconda3\envs\ida-course\python.exe` (Windows).
4. Для ноутбуків у VS Code оберіть Jupyter Kernel «Python (ida-course)» у верхньому правому куті редактора.


## 8) Типові робочі команди та перевірка

Перевірка доступності ключових бібліотек у Python:

```python
import importlib
libs = ["numpy", "pandas", "matplotlib", "sklearn", "jupyterlab"]
for lib in libs:
    print(lib, "OK" if importlib.util.find_spec(lib) else "MISSING")
```

Керування середовищами та пакетами (часті команди):

```bash
# Список середовищ
conda env list

# Оновлення conda
conda update -n base -c defaults conda

# Встановлення пакетів
conda install -n ida-course -c conda-forge seaborn xgboost

# Видалення пакета
conda remove -n ida-course seaborn

# Експорт середовища в YAML (для поділу з одногрупниками/CI)
conda env export -n ida-course > environment.yml

# Створення середовища з YAML
conda env create -f environment.yml

# Видалення середовища
conda remove -n ida-course --all
```


## 9) Рекомендації та кращі практики

- Окреме середовище на кожен проєкт/курс. Не використовуйте `base` для розробки.
- Якщо можливо — надавайте перевагу `conda` (або швидшому «mamba») для встановлення наукових пакетів; `pip` — для чистих Python-пакетів. Не змішуйте без потреби.
- Фіксуйте версію Python (наприклад, `python=3.10`) і зберігайте `environment.yml` в репозиторії.
- Для Windows зручно працювати в «Anaconda Prompt» або PowerShell після `conda init powershell`.
- Якщо працюєте через проксі/корпоративну мережу — налаштуйте змінні `HTTP_PROXY`/`HTTPS_PROXY` для conda і pip.


## 10) Поширені проблеми і їх вирішення

- Команда `conda` не знаходиться: виконайте `conda init <ваш shell>` і перезапустіть термінал; переконайтесь, що встановлено для вашого користувача.
- Конфлікти залежностей/повільне розв’язання: спробуйте канал `conda-forge`, або встановіть «mamba» у середовище `base` (`conda install -n base -c conda-forge mamba`) і використовуйте `mamba install ...`.
- Jupyter не бачить потрібне ядро: перевстановіть kernel командою `python -m ipykernel install --user --name ida-course --display-name "Python (ida-course)"` в активному середовищі.
- VS Code не бачить інтерпретатор: перевстановіть розширення Python, перезапустіть VS Code, вручну вкажіть шлях до інтерпретатора середовища `ida-course`.
- Windows «Long Path» помилки: за потреби увімкніть «LongPathsEnabled» у реєстрі або працюйте ближче до кореня диска (коротші шляхи).


## 11) Швидкий чек-лист (1 хвилина)

1. Встановити Miniconda/Anaconda.
2. `conda init <shell>` і перезапустити термінал.
3. `conda create -n ida-course python=3.10`
4. `conda activate ida-course`
5. Встановити пакети (`conda install -c conda-forge numpy pandas matplotlib scikit-learn jupyterlab ipykernel`).
6. `python -m ipykernel install --user --name ida-course --display-name "Python (ida-course)"`
7. Запустити `jupyter lab` і/або налаштувати VS Code (обрати інтерпретатор/ядро).


---

Після виконання цього гайду у вас буде ізольоване, відтворюване середовище для курсу з аналізу даних на Python з готовим JupyterLab і зручним налаштуванням у VS Code. Збережіть `environment.yml` у репозиторії, щоб легко відновлювати середовище на інших машинах.

