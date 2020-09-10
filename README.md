# Simple-Time-Optimization-Task

# Demonstration

- images and gifs

# Technical Task (The original version is written in Russian)

An employee of the statistical office was instructed to prepare N documents.
Documents with numbers K and L must be prepared by a certain date V.
We know the time Tij (I, j = 1,2, ..., N) required to prepare the I-th document in
j-th queue. Start time of work on the documents is U.
Determine the preparation order, in which all documents will be prepared on time and in the shortest possible time.


Develop an ability to set arbitrary input data both manually and
automatically (for example, from a file). You can use the proposed
initial data to check the work of an app.


***Design a graphical user interface.***


# Техническое задание

Работнику статистического отдела поручено подготовить N справок. Справки
с номерами K и L должны быть подготовлены к определенному сроку V.
Известно время Tij (I,j=1,2,...,N), необходимое на подготовку I-ой справки в
j-ю очередь. Время начала работы над справками U. Определить порядок
подготовки справок, при котором все справки будут подготовлены в срок и за
наименьшее время.

Разработать возможность задавать произвольные исходные данные как в ручную, так и
автоматически (например, из файла). Для проверки можно использовать предложенные
исходные данные.


***Разработать графический интерфейс пользователя.***


# Initial data (Исходные данные)

N = 5; U= 0; V = 4; K = 2; L = 4; T = 

 | 2 2 1 1 1 |
 
 | 1 1 0.5 0.5 0.5 |
 
 | 2 2 4 4 4 |
 
 | 1 1 1 0.5 o.5 |
 
 | 1 2 2 2 2 |
 
(And the answer is: | 1 1 0.5 0.5 0.5 | )


# Results
- All tasks are fully completed within the deadline (Dec of 2019)
- I'm sorry that I didn't add the README file initially


# Additional features
- An interface is written both in Russian and in English (switch the dictionaries in the source code)
- This is a crossplatform desktop application based on PyQt5


# How to run the code
The following steps assume using VS Code
```
python3 -m venv venv
pip install -r requirements.txt
run main.py
```