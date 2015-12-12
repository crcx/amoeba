# Amoeba

The Parable language does not specify a user interface or I/O 
model. This is left up to the separate *interface layers* to 
implement in whatever means are best for each platform. This 
also opens up some interesting possibilities. Amoeba is an 
interface with a twist: it extends the language to provide an 
experience closer to classical Forth.

# Requirements

* Python 2.x
* Parable (a copy is included)
* Parable Standard Library (a copy is included)

# Notes

This has an integral translation layer that attempts to convert
Forth style syntax into Parable code. Because of this standard
Parable code will not work with it.

At present this has:

* Colon Definitions

    : name .... ;

* IF/ELSE/THEN conditionals

    ( flag ) IF ...true... ELSE ...false... THEN

* Comments

    ( ... )
    \ ...

* Ok prompt
* Stack display via .s
* Function list via words
* Exit via bye

# Future

In the future this should expand to cover more Forth syntax and
functionality. Specifically I am looking into:

* Emulating a return stack
* Loop forms
* Forth-style variables
* Allowing usage for scripting purposes
* File I/O (probably backport from Ika)
