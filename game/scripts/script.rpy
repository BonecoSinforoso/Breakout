define e = Character("Eileen")

label start:

    scene bg room

    show eileen happy

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    jump play_pong

    return

label after_pong:

    e "That was fun! I hope you enjoyed it."

    return
    