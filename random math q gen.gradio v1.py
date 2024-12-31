import gradio as gr
import random
import time

# Constants
min_val = 0
max_val = 20
generated_equations = set()

# Timer functionality
def timer_interface(totalqs, questions):
    alert_message = []
    for i in range(int(totalqs)):
        time.sleep(5)  # Wait for 5 seconds for each question
        alert_message.append(f"Time up for Question #{i + 1}: Moving to the next question!")
    return alert_message

# Generate Expressions
def generate_eq():
    while True:
        left = random.randint(min_val, max_val)
        right = random.randint(min_val, max_val)
        OPERATORS = ["+", "-", "*"]
        operator = random.choice(OPERATORS)
        exp = f"{left}{operator}{right}"
        # Ensure the equation is unique
        if exp not in generated_equations:
            generated_equations.add(exp)
            ans = eval(exp)
            return exp, ans

# Generate Squares
def generate_squ():
    a = random.randint(min_val, max_val)
    exp = f"{a} * {a}"
    ans = eval(exp)
    return exp, ans

# Generate Cubes
def generate_cube():
    a = random.randint(min_val, max_val)
    exp = f"{a} * {a} * {a}"
    ans = eval(exp)
    return exp, ans

# Function to generate problems and answers
def generate_problems(option, totalqs):
    questions = []
    answers = []
    for i in range(int(totalqs)):
        if option == "Expressions":
            exp, ans = generate_eq()
        elif option == "Squares":
            exp, ans = generate_squ()
        elif option == "Cubes":
            exp, ans = generate_cube()
        else:
            return ["Invalid Option"], []
        questions.append(f"Problem #{i + 1}: {exp} = ?")
        answers.append(ans)
    return questions, answers

# Function to check a single answer
def check_single_answer(problem_index, user_guess, answers):
    try:
        correct_answer = answers[int(problem_index)]
        if str(correct_answer) == user_guess:
            return "Correct!"
        else:
            return f"Try Again! The correct answer was {correct_answer}."
    except IndexError:
        return "Invalid Problem Index."
    except Exception as e:
        return f"Error: {str(e)}"
# Interface for generating questions
def generate_interface(option, totalqs):
    questions, answers = generate_problems(option, totalqs)
    return questions, answers
# Gradio app
with gr.Blocks() as app:
    # States for questions and answers
    state_questions = gr.State([])
    state_answers = gr.State([])
    # Section to generate questions
    with gr.Row():
        option = gr.Dropdown(["Expressions", "Squares", "Cubes"], label="Choose a Type of Problem")
        totalqs = gr.Number(label="Total Number of Questions", value=1, precision=0)
        generate_btn = gr.Button("Generate Questions")
    output_questions = gr.JSON(label="Generated Questions")
    # Section for the timer
    timer_output = gr.JSON(label="Timer Alerts")
    # Section for submitting answers
    with gr.Row():
        problem_index = gr.Number(label="Problem Index", value=0, precision=0)
        user_guess = gr.Textbox(label="Your Answer")
        submit_btn = gr.Button("Submit Answer")
    result_output = gr.Textbox(label="Result")
    # Generate button click events
    generate_btn.click(
        fn=generate_interface,
        inputs=[option, totalqs],
        outputs=[output_questions, state_answers],
        queue=False
    )
    generate_btn.click(
        fn=timer_interface,
        inputs=[totalqs, state_questions],
        outputs=[timer_output],
        queue=False
    )
    # Submit button click event
    submit_btn.click(
        fn=check_single_answer,
        inputs=[problem_index, user_guess, state_answers],
        outputs=result_output,
        queue=False
    )
# Launch the Gradio app
app.launch()
