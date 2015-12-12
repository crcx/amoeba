# Amoeba

The Parable language does not specify a user interface or I/O model. This is left up to the separate *interface layers* to implement in whatever means are best for each platform. This also opens up some interesting possibilities. Amoeba is an interface with a twist: it extends the language to provide an experience closer to classical Forth.


    : name .... ;
    [ .... ] 'name' define

    ( comment )
    "comment"

    if ... then
    [ ... ] if-true

    if ...1... else ...2... then
    [ ...1... ] [ ...2... ] then

    .s

    words


