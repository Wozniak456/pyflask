<h1 align="center">Фінальний проект з дисципліни "Технології розробки серверного програмного забезпечення"</h1>
<h3 align="center">Виконала студентка групи іс-01 <br>Возняк Софія</h3>
<p>У даному проекті виконано 3 лабораторні роботи. <br>
<b>Визначення варіанту:</b> Номер групи: 1, 1 mod 3 = 1. Отже, функціонал по варіанту - Валюти.
</p>
<h3 align="center">Інструкції з запуску:</h3>
<p>1. З папки dist завантажте файл pyflask3-1.0.0-py3-none-any.whl<br>
2. У папці, де знаходиться цей файл, створіть та активуйте віртуальне середовище
  
```cmd
> py -3 -m venv venv

``` 
  ```cmd
> venv/Scripts/activate
  ``` 
3. Завантажте pyflask3-1.0.0-py3-none-any.whl з допомогою pip
  ```cmd
> pip install pyflask3-1.0.0-py3-none-any.whl
  ``` 
4. Ініціалізуйте базу даних sqlite за допомогою команди
  ```cmd
> flask --app pyflask3 init-db
  ``` 
5. Запустіть застосунок
  ```cmd
> flask --app pyflask3 --debug run
  ``` 
6. Перейдіть до http://127.0.0.1:5000/ <br>
  
<p align="center">
  <img src="/images/index.jpg" width="600" align="center"/><br>
  <i>Головна сторінка - записи</i>
</p>
  
</p>

Ахтунг! Для успішного тестування зареєструйтесь у застосунку (наприклад, username='user', password='pass') та залогіньтесь.
<p>Далі усі ендпойнти і функціонал застосунку описано у файлі <b>insomnia.json</b></p><br>

> <p align="center"><b>Інструкція з користування insomnia.json </b></p>
> 1. Відкрийте застосунок Insomnia <br>
> 2. Імпортуйте файл insomnia.json. Стануть доступними 4 папки: Records, Authorization, Categories <br>
> 3. Відвідайте кожен запит у папках, перемикаючись на вкладення Docs. Тут я описала як працює кожен ендпойнт. <br><br>
> <p align="center">
>  <img src="/images/docs_preview.jpg" width="600" align="center"/><br>
>  <i>Вигляд опису до запитів</i>
> </p>
