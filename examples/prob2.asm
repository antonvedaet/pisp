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