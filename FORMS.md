# Overview

Forth and Parable have some differences that need to be addressed for this to work.

This document contains my notes on translating the forms. There's still a significant amount of work to be done.

Amoeba will not be a fully classical Forth: it'll still have types, and fundamentally be Parable. But it'll use Forth style syntax and some functions will be added to facilitate a more Forth like environment.

# Forms

## Function Definition

Parable uses a form like:

    [ ... ] 'name' define

Forth uses:

    : name ... ;

Translating this requires:

* Find the :
* Grab the name
* Start a quote
* When ; is encountered end the quote
* Write the name as a string and call define

## Conditionals

The core form of conditional in Parable is **if**. Two primary variant forms exist: **if-true** and **if-false**. These look like:

    "something that generates a flag"
    [ ...true... ] [ ...false... ] if

    "something that generates a flag"
    [ ... ] if-true

In Forth, these would be constructed using an **if** **else** **then** form:

    ( something that generates a flag )
    if ...true... else ...false... then

    ( something that generates a flag )
    if ...true... then

This is a little trickier since nesting needs to be dealt with. I'm still working on implementing this in a way that I like.

## Comments

This is pretty easy. In Parable comments are enclosed in quotation marks. In Forth, they are wrapped in parenthesis (surrounded by whitespace.)

Parable:

    "this is a comment"

Forth:

    ( so is this )

Translating this is just a matter of finding the ( and ) and replacing them with quotation marks.

## Pointers

Parable:

    &define

Forth:

    ['] define

Translating:

* Find the [']
* Replace with & and remove the whitespace

## Return Stack

This is currently unimplemented.

Some things are fairly easy to do by hand (Forth, followed by Parable):

    >r ... r>
    [ ... ] dip

    dup >r ... r>
    [ ... ] sip

Others are harder:

    >r ... r@ ... r>

For this, I will probably implement a simulated return stack (using a dedicated slice, **push**, **pop**, and some helper functions)

## Loops

Forth has a bunch of looping structures including (but not limited to):

    begin ... again
    do ... loop
    for ... next
    begin ... while ... repeat

These can also be mixed in various ways. This allows for a really flexible set of functionality, but this makes translations much more difficult. I have not yet begun to work on these forms.

