.data
    greeting: "What is your name? Hello, "
    excl: "!"
    gtmp: 2
.code
        load greeting
        greet:
            store out
            load gtmp
            add 1
            store gtmp
            load  &gtmp        
            jifnz greet
        uname:
            load 0
            load in
            store out
            jifnz uname
            load excl
            store out
            hlt
    end