# pisp
 - Ведерников Антон Владимирович, P3223
 - Вариант: ```asm | acc | harv | hw | instr | struct | stream | mem | cstr | prob2 ```
 - Упрощенный вариант
 ## Язык
 ### Форма Бэкуса-Наура
 ```endf
 <программа> ::=
	 ".data" <перенос строки> <данные> [комментарий] <перенос строки>
	 ".code" <перенос строки> "begin:" { <инструкция> | <метка> } [комментарий] <перенос строки> "end" <перенос строки> <EOF>
<данные> ::= <метка переменной>":" <переменная> [комментарий] <перенос строки>
<инструкция> ::= <адресная команда> <операнд> [комментарий] <перенос строки> | <безадресная команда> [комментарий] <перенос строки> | <команда перехода> <метка перехода> [комментарий] <перенос строки>

<команда перехода> ::= "jmp" | "jifn" | "jifnn" | "jifz" | "jifnz"
<адресная команда> ::= "load" | "store" | "add" | "sub" | "mod"
<безадресная команда> ::= "hlt" | "nop"
<операнд> ::= <число>| "&"<число> | <метка переменной> | "&"<метка переменной>
<метка перехода> ::= <идентификатор> | "&"<число>

<метка переменной> ::= <слово>
<переменная> ::= <число> | """<слово>"""

<идентификатор> ::= <слово>
<комментарий> ::= ";" {<слово> | <число>}

<перенос строки> ::= "\n"
<слово> ::= <буква> {<буква>}
<число> ::= ["-"]<цифра> {<цифра>}
<буква> ::= a | b | c | ... | z | A | B | C | ... | Z
<цифра> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
 ```

 - Видимость данных - глобальная
 - Поддерживаются целочисленные ($-2^{31}$ до $2^{31}-1$) и строковые литералы
 - Любые символы расположенные после `;` - комментарии
 - В секции `.data` должны быть только переменные
 - В секции `.code` должны быть только команды и метки
 - Метки должны быть объявлены до применения

### Команды:
_Адресные:_  
`load` - загрузка значение из операнда или значение из ячейки памяти в аккумулятор  
`store` - выгружает значение из аккумулятора в указанную ячейку памяти  
`add` - сложение значения из операнда или значения из ячейки памяти со значением в аккумуляторе  
`sub` - вычитание значения из операнда или значения из ячейки памяти со значением в аккумуляторе  
`mod` - вычисление остатка от деления значения в аккумуляторе на значение из операнда или значение указанной ячейки память  
_Безадресные:_  
`nop` - пустышка  
`hlt` - остановить работу процессора  
_Перехода:_  
`jmp` - безусловный переход на метку или указанный адрес  
`jifz` - переход на метку или указанный адрес, при флаге Z = 1  
`jifnz` - переход на метку или указанный адрес, при флаге Z = 0  
`jifn` - переход на метку или указанный адрес, при флаге N = 1  
`jifnn` - переход на метку или указанный адрес, при флаге N = 0  
#### Метки
Метки определяются исключительно на отдельных строчках
```endf
samplelabel:
	load 5
	sub 1
	jifnz samplelabel
```
Во время трансляции `jifnz samplelabel` замениться на `jifnz &0` (при условии что `samplelabel` находиться в самом начале секции `.code`)
## Организация памяти
- Память команд и память данных разделены
- Длина машинного слова в памяти данных `32 бита`
- Адреса `0` и `1` в памяти данных являются адресами ввода и вывода соответственно 
```
        data memory
+----------------------------+
| 00 :  input address        |
| 01 :  output address       |
|         variables          |
|             .              |
|             .              |
|             .              |
| 2047 :     ...             |
+----------------------------+

     instruction memory
+----------------------------+
| 00 :  instruction 1        |
| 01 :  instruction 2        |
|       instructions         |
|             .              |
|             .              |
|             .              |
| n :        ...             |
+----------------------------+

		   Registers
+------------------------------+
| acc                          |
| cr                           |
| ar                           |
| dr                           |
| sr                           |
+------------------------------+
```

- `in` и `out` заранее зарезервированы, то есть `load &0` эквивалентно `load in`
-  Разработчику доступны только манипуляции с памятью данных и регистром `acc` 
- #### Адресация
  - `x: 3`
  - Прямая: `load x` загрузит в аккумулятор `3`
  - Косвенная:  `load &x` загрузит в аккумулятор значение из ячейки памяти по адресу `3`
- #### Регистры
   -  Аккумулятор `acc` - используется почти во всех командах (хранение данных, вывод)
   - Регистр команд `cr` - хранит текущую инструкцию
   - Регистр адреса `ar` - хранит адрес ячейки памяти
   - Регистр данных `dr` - хранит данные для передачи в аккумулятор или память
   - Регистр статуса `sr` - хранит флаги `NZC`
     - `N` - флаг отрицательности
     - `Z` - флаг нуля
     - `С` - флаг переноса  
## Система команд
 - В секции данных машинное слово - `32` бита, знаковое
 - В секции инструкций длина машинного слова - неопределенна
 - Поток управления - инкремент `ip` после каждой инструкции

На выполнение каждой инструкции есть 4 цикла:

 1. Цикл выборки инструкции. (1 такт)
 2. Цикл выборки адреса (для регистровой, относительно стека, косвенной относительной адресаций) (1 такт)
 3. Цикл выборки операнда (для всех видов адресации, кроме непосредственной) (1 такт)
 4. Цикл исполнения
### Набор команд
| Команда | Адресная | Такт |Мнемоника|
|:--|:--|:--|:--|
| load | true | 3 или 5(при косвенной адресации) | `LOAD: DR => ACC` |
| store | true | 4 | `STORE: ACC => RAM[AR]` |
| add | true | 3 или 5(при косвенной адресации) | `ADD: ACC + DR => ACC` |
| sub | true | 3 или 5(при косвенной адресации) | `SUB: ACC - DR => ACC` |
| mod | true | 3 или 5(при косвенной адресации) | `MOD: ACC % DR => ACC` |
| nop | false | 1 | `NOP` |
| hlt | false | 1 | `HLT` |
| jmp | true | 5 | `JUMP: DR => IP` |
| jifz | true | 5 | `JIFZ: Z: DR => IP` |
| jifnz | true | 5 | `JIFNZ:NOT Z: DR => IP` |
| jifn | true | 5 | `JIFN: N: DR => IP` |
| jifnn | true | 5 | `JIFNN:NOT N: DR => IP` |
### Кодирование
Команды кодируются в `.json` файлы.  
#### Пример:  
Исходный код программы `cat`:  
```
  .data
  .code 
      begin:
          load in
          store out
          jifnz &0
          hlt
      end
```
Закодированная программа `cat`:
```json
  [
      {
          "idx": 0,
          "opcode": "load",
          "operand": 0,
          "address": true,
          "relative": false
      },
      {
          "idx": 1,
          "opcode": "store",
          "operand": 1,
          "address": true,
          "relative": false
      },
      {
          "idx": 2,
          "opcode": "jifnz",
          "operand": 0,
          "address": true,
          "relative": false
      },
      {
          "idx": 3,
          "opcode": "hlt",
          "operand": null,
          "address": false,
          "relative": false
      }
  ]
```
 - `idx` - адрес ячейки памяти
 - `opcode` - команда
 - `operand` - операнд
 - `address` - показывает адресная комманда или нет
 - `relative` - используется для чтения адреса переменной



## Трансляция
Использование: `python3 translate_cl.py <source_file> <output_file>`

Реализация: [translator.py](./translator.py)

#### Принцип работы:
 1. Построчное чтение исходного файла
 2. Разбиение на секции `.data` и `.code`
 3. Транслирование секции `.data` в массив `nop` операций
 4. Транслирование секции `.code` в массив инструкций
 5. Сериализация и запись в `json` файл

#### Правила:
 - Одно выражение(т.е обьявление переменной, команда) - одна строка.
 - Метка только на отдельной строке перед командой на которую она ссылается.
 - Использование меток и переменных исключительно после их объявления.

 ## Модель процессора
 ### Data Path
 Реализован в классе [DataPath](./cpu/data_path.py)
 ```
                                                                                                                                                                             
+----------------------------------------------------------------------------------------+                                                                                  
|                                                                                        |                                                                                  
|                                                                                        v                                                                  +--------------+
|            +--------------------------+                   +------+                 +------+                +--------------------------+    +------+       |              |
|            |      Input address       |<----------+       |      |                 |      |                |                          |    |      |       |              |
|            +--------------------------+           |    +--+  AR  |<----------------+  DR  +-----+          |                          +--->|  CR  +------>| CONTROL UNIT |
|            |      Output address      |<-----+    |    |  |      |                 |      |     |          |                          |    |      |       |              |
|            +--------------------------+      |    |    |  +------+                 ++-----+     |          |                          |    +------+       |              |
|            |                          |      |    |    |  latch_ar                  |latch_dr   |          |                          |     latch_cr      +--------------+
|            |                          |      |    |    |               sel          |           |          |                          |                                   
|            |                          |      |    |    |              +-------+     |           |          |                          |                                   
|            |                          |      |    |    |              |       |     |           |          |                          |                                   
|            |                          |      |    |    |           +->|  MUX  |     |           |          |                          |                                   
+------------+                          |      |    |    |           |  |       |     |           |          |                          |                                   
              |                          |      |    |    |           |  +-----+-+     |           |          |                          |                                   
              |                          |      |    |    |           |   ^    |       |           |          |                          |                                   
    read----->|                          |      |    |    |           |   |    v       v           |          |       INSTRUCTIONS       |                                   
              |                          |      |    |    |           |   | +-------------+        |          |                          |                                   
              |          DATA            |      |    |    v           |   | |             |        |          |                          |                                   
    write---->|                          |    +-+----+-------------+  |   | |     ALU     |        |          |                          |                                   
              |                          |    |                    |  |   | |             |        |          |                          |                                   
              |                          |    |                    |  |   | +--+-------+--+        |          |                          |                                   
              |                          |    |   Address          |  |   |    |       |           |          |                          |                                   
              |                          |<---+                    |  |   |    |       |           |          |                          |                                   
              |                          |    |                    |  |   |    v       |           |          |                          |                                   
              |                          |    |        Decoder     |  |   | +------+   |           |          |                          |                                   
              |                          |    |                    |  |   +-+      |   |           |          |                          |                                   
              |                          |    |                    |  |     |  SR  |   |           |          |                          |                                   
              |                          |    |                    |  |     |      |   |           |          |                          |                                   
              |                          |    |                    |  |     +------+   |           |          |                          |                                   
              +--------------------------+    +--------------------+  |     latch_sr   |           |          +--------------------------+                                   
                     ^                                                |                |           |             ^                                                           
                     |                                                |                |           |             |                                                           
                     |                                                |                |           |             |                                                           
                     |                                              +-+-----+          |           |          +--+---+                                                       
                     |                                              |       |          |           |          |      |                                                       
                     |                                              |  ACC  |          |           |  latch_ip|  IP  +-------+                                               
                     +----------------------------------------------+       | <--------+           |          |      |       |                                               
                                                                    +-------+                      |          +------+       |                                               
                                                                   latch_acc                       |             ^           v                                               
                                                                                                   |             |         +----+                                            
                                                                                                   |             |         |    |                                            
                                                                                                   |        +----+----+    | +1 |                                            
                                                                                                   |        |         |    +--+-+                                            
                                                                                                   |        |   MUX   |       |                                              
                                                                                                   +------->|         |<------+                                              
                                                                                                            +---------+                                                      
                                                                                                              sel                                                                                                         
 ```
 ### Control Unit
 Реализован в классе [СontrolUnit](./cpu/control_unit.py)
 ```
                                                  +-----------------------------+
                                                   |                             |
                                                   |                             |
                                                   |                             |
+------------------------------+                  |                             |
|                              |                  |                             |
|                              |                  |                             |
|                              +---signals------->|                             |
|     Instruction decoder      |                  |          Data Path          |
|                              |<---flags---------+                             |
|                              |                  |                             |
+------------------------------+                  |                             |
               ^                                   |                             |
               |                                   |                             |
               |                                   |                             |
               |                                   |                             |
               |                                   +--------------+--------------+
               |                                                  |               
               |                                                  |               
               |                                                  |               
               |                                                  v               
               |                                    +---------------------------+ 
               |                                    |                           | 
               |                                    |                           | 
               |                                    |                           | 
               |                                    |                           | 
               |                                    |                           | 
               +-----------instruction--------------+     Instruction memory    | 
                                                    |                           | 
                                                    |                           | 
                                                    |                           | 
                                                    |                           | 
                                                    |                           | 
                                                    |                           | 
                                                    +---------------------------+ 
 ```
 ## Тестирование
  - Тестирование при помощи `pytest-golden`
  - [golden_test](./golden_test.py)
  - Конфигурация golden-test'ов в [директории](./golden/)

  Тесты реализованы по всем алгоритмам из варианта.

  #### Github Actions CI
  ```yml
        name: lint and test

        on: [push, pull_request]

        jobs:
                lint:
                        runs-on: ubuntu-latest

                        steps:
                        - name: Checkout code
                          uses: actions/checkout@v2

                        - name: Set up Python
                        uses: actions/setup-python@v2
                          with:
                                python-version: '3.11.8' 

                        - name: Install dependencies
                          run: |
                                python -m pip install --upgrade pip
                                pip install ruff

                        - name: Run ruff
                          run: |
                               ruff check

                test:
                        runs-on: ubuntu-latest

                        steps:
                        - name: Checkout code
                        uses: actions/checkout@v2

                        - name: Set up Python
                        uses: actions/setup-python@v2
                          with:
                                python-version: '3.11.8' 

                        - name: Install dependencies
                          run: |
                                python -m pip install --upgrade pip
                                pip install poetry
                                poetry install
                        
                        - name: Run tests
                        run: |
                                poetry run coverage run -m pytest . -v --ignore=translate_cl.py
                                poetry run coverage report -m
                        
        
 ```
#### Пример выполнения prob2:
[Исходный код](./examples/prob2.asm):
```
.data
    f: 1
    s: 2
    nxt: 2
    r: 0
.code 
    begin:
        mainloop:
            load nxt ; acc = nxt
            store s ; s = acc
            load f ; acc = f
            add s ; acc += s
            store nxt ; nxt = s
            load s ; acc = s
            store f ; f = acc
            mod 2 ; проверяем четное число или нет
            jifz &15 ; если число четное то переходим к метку count по абсолютному адресу, т.к она еще не объявлена 
        limit:
            load s ; просто проверяем что число не больше 4000000
            sub 4000000
            jifn mainloop
            load r
            store out
            hlt ; если же оно больше то прекращаем работу программы
        count:
            load r
            add s
            store r
            jmp limit
    end
```
Лог работы процессора и вывод можно увидеть в [файле](./logs/prob2_cpu.log), здесь же последние 30 строк лога и вывод. Так как лог получился слишком большой для вменяемого отображения в README.md
```log
INFO INSTRUCTION: 400 | JIFN:N: DR => IP | AR: 0 | IP: 0 | DR: 0 | ACC: -1821691 | NZC: 100 | TICK: 1780| CR:{'idx': 11, 'opcode': 'jifn', 'operand': 0, 'address': True, 'relative': False}
INFO INSTRUCTION: 401 | LOAD: DR => ACC | AR: 4 | IP: 1 | DR: 3524578 | ACC: 3524578 | NZC: 0 | TICK: 1785| CR:{'idx': 0, 'opcode': 'load', 'operand': 4, 'address': True, 'relative': False}
INFO INSTRUCTION: 402 | STORE: ACC => RAM[AR] | AR: 3 | IP: 2 | DR: 3524578 | ACC: 3524578 | NZC: 0 | TICK: 1789| CR:{'idx': 1, 'opcode': 'store', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 403 | LOAD: DR => ACC | AR: 2 | IP: 3 | DR: 2178309 | ACC: 2178309 | NZC: 0 | TICK: 1794| CR:{'idx': 2, 'opcode': 'load', 'operand': 2, 'address': True, 'relative': False}
INFO INSTRUCTION: 404 | ADD: ACC + DR => ACC | AR: 3 | IP: 4 | DR: 3524578 | ACC: 5702887 | NZC: 0 | TICK: 1799| CR:{'idx': 3, 'opcode': 'add', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 405 | STORE: ACC => RAM[AR] | AR: 4 | IP: 5 | DR: 3524578 | ACC: 5702887 | NZC: 0 | TICK: 1803| CR:{'idx': 4, 'opcode': 'store', 'operand': 4, 'address': True, 'relative': False}
INFO INSTRUCTION: 406 | LOAD: DR => ACC | AR: 3 | IP: 6 | DR: 3524578 | ACC: 3524578 | NZC: 0 | TICK: 1808| CR:{'idx': 5, 'opcode': 'load', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 407 | STORE: ACC => RAM[AR] | AR: 2 | IP: 7 | DR: 3524578 | ACC: 3524578 | NZC: 0 | TICK: 1812| CR:{'idx': 6, 'opcode': 'store', 'operand': 2, 'address': True, 'relative': False}
INFO INSTRUCTION: 408 | MOD: ACC % DR => ACC | AR: 7 | IP: 8 | DR: 2 | ACC: 0 | NZC: 10 | TICK: 1815| CR:{'idx': 7, 'opcode': 'mod', 'operand': 2, 'address': False, 'relative': False}
INFO INSTRUCTION: 409 | JIFZ: Z: DR => IP | AR: 15 | IP: 15 | DR: 15 | ACC: 0 | NZC: 10 | TICK: 1820| CR:{'idx': 8, 'opcode': 'jifz', 'operand': 15, 'address': True, 'relative': False}
INFO INSTRUCTION: 410 | LOAD: DR => ACC | AR: 5 | IP: 16 | DR: 1089154 | ACC: 1089154 | NZC: 0 | TICK: 1825| CR:{'idx': 15, 'opcode': 'load', 'operand': 5, 'address': True, 'relative': False}
INFO INSTRUCTION: 411 | ADD: ACC + DR => ACC | AR: 16 | IP: 17 | DR: 3524578 | ACC: 4613732 | NZC: 0 | TICK: 1830| CR:{'idx': 16, 'opcode': 'add', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 412 | STORE: ACC => RAM[AR] | AR: 5 | IP: 18 | DR: 3524578 | ACC: 4613732 | NZC: 0 | TICK: 1834| CR:{'idx': 17, 'opcode': 'store', 'operand': 5, 'address': True, 'relative': False}
INFO INSTRUCTION: 413 | JUMP: DR => IP | AR: 9 | IP: 9 | DR: 9 | ACC: 4613732 | NZC: 0 | TICK: 1839| CR:{'idx': 18, 'opcode': 'jmp', 'operand': 9, 'address': True, 'relative': False}
INFO INSTRUCTION: 414 | LOAD: DR => ACC | AR: 3 | IP: 10 | DR: 3524578 | ACC: 3524578 | NZC: 0 | TICK: 1844| CR:{'idx': 9, 'opcode': 'load', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 415 | SUB: ACC - DR => ACC | AR: 10 | IP: 11 | DR: 4000000 | ACC: -475422 | NZC: 100 | TICK: 1847| CR:{'idx': 10, 'opcode': 'sub', 'operand': 4000000, 'address': False, 'relative': False}
INFO INSTRUCTION: 416 | JIFN:N: DR => IP | AR: 0 | IP: 0 | DR: 0 | ACC: -475422 | NZC: 100 | TICK: 1852| CR:{'idx': 11, 'opcode': 'jifn', 'operand': 0, 'address': True, 'relative': False}
INFO INSTRUCTION: 417 | LOAD: DR => ACC | AR: 4 | IP: 1 | DR: 5702887 | ACC: 5702887 | NZC: 0 | TICK: 1857| CR:{'idx': 0, 'opcode': 'load', 'operand': 4, 'address': True, 'relative': False}
INFO INSTRUCTION: 418 | STORE: ACC => RAM[AR] | AR: 3 | IP: 2 | DR: 5702887 | ACC: 5702887 | NZC: 0 | TICK: 1861| CR:{'idx': 1, 'opcode': 'store', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 419 | LOAD: DR => ACC | AR: 2 | IP: 3 | DR: 3524578 | ACC: 3524578 | NZC: 0 | TICK: 1866| CR:{'idx': 2, 'opcode': 'load', 'operand': 2, 'address': True, 'relative': False}
INFO INSTRUCTION: 420 | ADD: ACC + DR => ACC | AR: 3 | IP: 4 | DR: 5702887 | ACC: 9227465 | NZC: 0 | TICK: 1871| CR:{'idx': 3, 'opcode': 'add', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 421 | STORE: ACC => RAM[AR] | AR: 4 | IP: 5 | DR: 5702887 | ACC: 9227465 | NZC: 0 | TICK: 1875| CR:{'idx': 4, 'opcode': 'store', 'operand': 4, 'address': True, 'relative': False}
INFO INSTRUCTION: 422 | LOAD: DR => ACC | AR: 3 | IP: 6 | DR: 5702887 | ACC: 5702887 | NZC: 0 | TICK: 1880| CR:{'idx': 5, 'opcode': 'load', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 423 | STORE: ACC => RAM[AR] | AR: 2 | IP: 7 | DR: 5702887 | ACC: 5702887 | NZC: 0 | TICK: 1884| CR:{'idx': 6, 'opcode': 'store', 'operand': 2, 'address': True, 'relative': False}
INFO INSTRUCTION: 424 | MOD: ACC % DR => ACC | AR: 7 | IP: 8 | DR: 2 | ACC: 1 | NZC: 0 | TICK: 1887| CR:{'idx': 7, 'opcode': 'mod', 'operand': 2, 'address': False, 'relative': False}
INFO INSTRUCTION: 425 | JIFZ: Z: DR => IP | AR: 8 | IP: 9 | DR: 2 | ACC: 1 | NZC: 0 | TICK: 1892| CR:{'idx': 8, 'opcode': 'jifz', 'operand': 15, 'address': True, 'relative': False}
INFO INSTRUCTION: 426 | LOAD: DR => ACC | AR: 3 | IP: 10 | DR: 5702887 | ACC: 5702887 | NZC: 0 | TICK: 1897| CR:{'idx': 9, 'opcode': 'load', 'operand': 3, 'address': True, 'relative': False}
INFO INSTRUCTION: 427 | SUB: ACC - DR => ACC | AR: 10 | IP: 11 | DR: 4000000 | ACC: 1702887 | NZC: 0 | TICK: 1900| CR:{'idx': 10, 'opcode': 'sub', 'operand': 4000000, 'address': False, 'relative': False}
INFO INSTRUCTION: 428 | JIFN:N: DR => IP | AR: 11 | IP: 12 | DR: 4000000 | ACC: 1702887 | NZC: 0 | TICK: 1905| CR:{'idx': 11, 'opcode': 'jifn', 'operand': 0, 'address': True, 'relative': False}
INFO INSTRUCTION: 429 | LOAD: DR => ACC | AR: 5 | IP: 13 | DR: 4613732 | ACC: 4613732 | NZC: 0 | TICK: 1910| CR:{'idx': 12, 'opcode': 'load', 'operand': 5, 'address': True, 'relative': False}
INFO INSTRUCTION: 430 | STORE: ACC => RAM[AR] | AR: 1 | IP: 14 | DR: 4613732 | ACC: 4613732 | NZC: 0 | TICK: 1914| CR:{'idx': 13, 'opcode': 'store', 'operand': 1, 'address': True, 'relative': False}
INFO INSTRUCTION: 431 | HLT | AR: 14 | IP: 15 | DR: 4613732 | ACC: 4613732 | NZC: 0 | TICK: 1915| CR:{'idx': 14, 'opcode': 'hlt', 'operand': None, 'address': False, 'relative': False}
INFO [4613732]
```
#### Пример работы тестов и линтера
```
============================= test session starts ==============================
platform linux -- Python 3.11.8, pytest-8.2.2, pluggy-1.5.0 -- /home/runner/.cache/pypoetry/virtualenvs/pisp-jhoDnaUe-py3.11/bin/python
cachedir: .pytest_cache
rootdir: /home/runner/work/pisp/pisp
configfile: pyproject.toml
plugins: golden-0.2.2
collecting ... collected 4 items

golden_test.py::test[golden/cat.yml] PASSED                              [ 25%]
golden_test.py::test[golden/hello_username.yml] PASSED                   [ 50%]
golden_test.py::test[golden/hello_world.yml] PASSED                      [ 75%]
golden_test.py::test[golden/prob2.yml] PASSED                            [100%]

============================== 4 passed in 0.43s ===============================

Run ruff check
All checks passed!
```

```
| ФИО                           | алг          | LoC | code инстр. | инстр. | такт. |                            вар                                         |
| Ведерников Антон Владимирович | cat          | 8   | 4           | 19     | 73    |  asm | acc | harv | hw | instr | struct | stream | mem | cstr | prob2  |
| Ведерников Антон Владимирович | hellousername| 23  | 13          | 179    | 766   |  asm | acc | harv | hw | instr | struct | stream | mem | cstr | prob2  |
| Ведерников Антон Владимирович | helloworld   | 15  | 8           | 80     | 344   |  asm | acc | harv | hw | instr | struct | stream | mem | cstr | prob2  |
| Ведерников Антон Владимирович | prob2        | 30  | 19          | 431    | 1915  |  asm | acc | harv | hw | instr | struct | stream | mem | cstr | prob2  |
```