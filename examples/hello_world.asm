.data
    hello: "Hello, world!"
    tmp: 2
.code 
    begin:
        load hello
        mainloop:
            store out
            load tmp
            add 1
            store tmp
            load  &tmp        
            jifnz mainloop
            hlt
    end