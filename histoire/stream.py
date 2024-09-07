import streamlit as st
import random

# Define the Question class
class Question:
    def __init__(self, question, answer, period, score):
        self.question = question
        self.answer = answer
        self.period = period
        self.score = score

# Example questions dictionary
question_dict = {
    "q1": Question("What is the capital of France?", "Paris", "Modern", 10),
    "q2": Question("Who wrote 'Macbeth'?", "Shakespeare", "Renaissance", 15),
    "q3": Question("What is the chemical symbol for water?", "H2O", "Science", 5),
    "q4": Question("What is the square root of 16?", "4", "Mathematics", 10),
}

# Initialize session state variables if they don't exist
if 'question_order' not in st.session_state:
    st.session_state.question_order = random.sample(list(question_dict.keys()), len(question_dict))
    st.session_state.current_question_index = 0

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'incorrect_questions' not in st.session_state:
    st.session_state.incorrect_questions = []

if 'answer' not in st.session_state:
    st.session_state.answer = ""

def submit_answer():
    current_question_key = st.session_state.question_order[st.session_state.current_question_index]
    current_question = question_dict[current_question_key]

    # Check the user's answer
    if st.session_state.answer.strip().lower() == current_question.answer.lower():
        st.success("Correct!")
        st.session_state.score += current_question.score
    else:
        st.error(f"Incorrect! The correct answer is {current_question.answer}.")
        st.session_state.incorrect_questions.append(current_question_key)

    # Move to the next question or repeat incorrect ones
    st.session_state.current_question_index += 1

    if st.session_state.current_question_index >= len(st.session_state.question_order):
        if st.session_state.incorrect_questions:
            # Restart the quiz with incorrect questions
            st.session_state.question_order = st.session_state.incorrect_questions
            st.session_state.incorrect_questions = []
            st.session_state.current_question_index = 0
        else:
            st.session_state.current_question_index = len(st.session_state.question_order)

    st.session_state.answer = ""  # Clear the input for the next question

def display_question():
    # Get the current question key and question object
    current_question_key = st.session_state.question_order[st.session_state.current_question_index]
    current_question = question_dict[current_question_key]

    # Display the question
    st.write(f"Question {st.session_state.current_question_index + 1}: {current_question.question}")

    # Input field for the user's answer
    st.text_input("Your answer:", key="answer", 
                  value=st.session_state.answer, 
                  on_change=submit_answer)

def display_final_score():
    st.write(f"Your final score is: {st.session_state.score}")
    if st.button("Restart Quiz"):
        st.session_state.question_order = random.sample(list(question_dict.keys()), len(question_dict))
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.answer = ""
        st.session_state.incorrect_questions = []

# Streamlit app
def main():
    st.title("Randomized Quiz App")

    if st.session_state.current_question_index < len(st.session_state.question_order):
        display_question()
    else:
        display_final_score()

if __name__ == "__main__":
    main()
