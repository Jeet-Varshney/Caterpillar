
import turtle as t
import random as rd

screen = t.Screen()
screen.title("Caterpillar Snake Game")
screen.bgcolor("yellow")
screen.setup(width=620, height=660)
screen.tracer(0)

watermark = t.Turtle()
watermark.hideturtle()
watermark.penup()
watermark.color("#E8D94A")
watermark.goto(0, 20)
watermark.write(
    "CATERPILLAR",
    align="center",
    font=("Arial", 42, "bold")
)


STEP = 20
LIMIT = 280
DELAY = 120

score = 0
best_score = 0
game_started = False
game_over = False
direction = (STEP, 0)
next_direction = (STEP, 0)
body_positions = []
segments = []

head = t.Turtle()
head.shape("square")
head.color("darkgreen")
head.penup()
head.speed(0)

leaf = t.Turtle()
leaf.shape("circle")
leaf.color("green")
leaf.penup()
leaf.speed(0)
leaf.shapesize(0.7, 0.7)

message = t.Turtle()
message.hideturtle()
message.penup()
message.color("black")

score_turtle = t.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.color("black")


def show_score():
    score_turtle.clear()
    score_turtle.goto(0, 290)
    score_turtle.write(
        f"Score: {score}    Best Score: {best_score}",
        align="center",
        font=("Arial", 16, "bold")
    )


def show_message(text):
    message.clear()
    message.goto(0, 0)
    message.write(
        text,
        align="center",
        font=("Arial", 17, "bold")
    )


def place_leaf():
    occupied = body_positions[:]

    while True:
        x = rd.randrange(-LIMIT, LIMIT + 1, STEP)
        y = rd.randrange(-LIMIT, LIMIT + 1, STEP)

        if (x, y) not in occupied:
            leaf.goto(x, y)
            break

    leaf.showturtle()


def clear_body():
    global segments, body_positions

    for segment in segments:
        segment.hideturtle()

    segments = []
    body_positions = []


def create_segment():
    segment = t.Turtle()
    segment.shape("square")
    segment.color("forestgreen")
    segment.penup()
    segment.speed(0)
    segment.goto(body_positions[-1])
    segments.append(segment)


def draw_body():
    for i, segment in enumerate(segments):
        segment.goto(body_positions[i + 1])


def start_game():
    global score, game_started, game_over
    global direction, next_direction, body_positions

    if game_started:
        return

    score = 0
    game_started = True
    game_over = False

    direction = (STEP, 0)
    next_direction = (STEP, 0)

    clear_body()

    head.goto(0, 0)
    head.setheading(0)
    head.showturtle()

    body_positions = [
        (0, 0),
        (-STEP, 0),
        (-2 * STEP, 0)
    ]

    create_segment()
    create_segment()

    message.clear()
    place_leaf()
    show_score()
    screen.update()

    game_loop()


def turn_up():
    global next_direction
    if direction[1] == 0:
        next_direction = (0, STEP)


def turn_down():
    global next_direction
    if direction[1] == 0:
        next_direction = (0, -STEP)


def turn_left():
    global next_direction
    if direction[0] == 0:
        next_direction = (-STEP, 0)


def turn_right():
    global next_direction
    if direction[0] == 0:
        next_direction = (STEP, 0)


def end_game():
    global game_over, game_started, best_score

    game_over = True
    game_started = False
    best_score = max(best_score, score)

    show_score()
    show_message(
        f"GAME OVER!\nScore: {score}\nPress R or SPACE to restart"
    )
    screen.update()


def game_loop():
    global score, best_score, direction, body_positions

    if not game_started or game_over:
        return

    direction = next_direction

    old_x, old_y = body_positions[0]
    new_x = old_x + direction[0]
    new_y = old_y + direction[1]

    if new_x > LIMIT:
        new_x = -LIMIT
    elif new_x < -LIMIT:
        new_x = LIMIT

    if new_y > LIMIT:
        new_y = -LIMIT
    elif new_y < -LIMIT:
        new_y = LIMIT

    new_head = (new_x, new_y)

    eating = new_head == (round(leaf.xcor()), round(leaf.ycor()))

    check_body = body_positions if eating else body_positions[:-1]

    if new_head in check_body:
        end_game()
        return

    body_positions.insert(0, new_head)

    if eating:
        score += 10
        best_score = max(best_score, score)
        create_segment()
        place_leaf()
        show_score()
    else:
        body_positions.pop()

    head.goto(new_head)
    draw_body()

    screen.update()
    screen.ontimer(game_loop, DELAY)


screen.onkey(turn_up, "Up")
screen.onkey(turn_down, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")
screen.onkey(start_game, "space")
screen.onkey(start_game, "r")
screen.onkey(start_game, "R")

head.hideturtle()
leaf.hideturtle()

show_score()
show_message("CATERPILLAR SNAKE GAME\n\nPress SPACE to start")
screen.update()

screen.listen()
screen.mainloop()
