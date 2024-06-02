.data
    s: 15
    skibidi: 325
.code 
    begin:
        load 2
        store &3  
        lbl:
            load &3
            load &4
        jmp lbl
        jmp 3
        store skibidi
    end