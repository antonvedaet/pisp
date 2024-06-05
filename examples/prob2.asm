.data
    f: 1
    s: 2
    nxt: 2
    r: 0
.code 
    begin:
        mainloop:
            load nxt
            store s
            load f
            add s
            store nxt
            load s
            store f
            mod 2
            jifz &15
        limit:
            load s
            sub 4000000
            jifn mainloop
            load r
            store out
            hlt
        count:
            load r
            add s
            store r
            jmp limit
    end