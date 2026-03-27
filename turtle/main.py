import turtle

t = turtle.Turtle()


def house():
    def draw_rectangle(length: int, width: int | None = None):
        if not width:
            width = length
        for _ in range(2):
            t.forward(length)
            t.right(90)
            t.forward(width)
            t.right(90)

    t.color("blue")
    draw_rectangle(100)
    t.right(180)
    t.forward(20)
    t.right(90 + 45)
    t.forward(100)
    t.right(90)
    t.forward(100)
    t.right(90 + 45)
    t.forward(20)


def star():
    colors = ["red", "blue", "green", "orange", "purple"]

    for i in range(5):
        t.color(colors[i])
        t.forward(200)
        t.right(144)


def vortex():
    t.speed(0)
    turtle.bgcolor("black")
    colors = ["red", "yellow", "blue", "green", "orange", "purple"]

    for x in range(200):
        t.pencolor(colors[x % 6])
        t.width(x / 100 + 1)
        t.forward(x)
        t.left(59)


# house()
# star()
vortex()

turtle.done()
