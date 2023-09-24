import TaskPuzzle.streamlit as st
from simpleai.search import CspProblem, backtrack
import time 

st.set_page_config(page_title="Cryptarithmetic Puzzle Solver", page_icon="🧩", layout="centered")

def solve_cryptoarithmetic_puzzle(puzzle_input, equation_input):
    #splitting the words
    words = puzzle_input.split(" ")

    my_words = []

    for word in words:
        my_words.append(word)

    #making a set with all the unique letters that later will be the variables
    unique_letters = set()
    for word in my_words:
        for char in word:
            unique_letters.add(char)

    #define the variables
    variables = tuple(unique_letters)

    #find the first letters of the words because these can't be 0 in the puzzle (1-9)
    first_letters = [word[0] for word in my_words]

    domains = {}

    for letter in first_letters:    
        domains[letter] = list(range(1,10))

    #if it's not the first letter it can be a number from 0 - 9
    for letter in unique_letters:   
        if letter not in domains:
            domains[letter] = list(range(0,10))

    #check if all letters are unique
    def constraint_unique(variables, values):   
        return len(values) == len(set(values))

    #constraint for solving the puzzle
    def constraint_result(variables, values):
        #dictionary char:value
        char_to_value = {char: val for char, val in zip(variables, values)}

        #get the words out of the list
        first_word = my_words[0]
        second_word = my_words[1]
        third_word = my_words[2]

        #extract values for characters in the words
        first_word_values = [char_to_value[char] for char in first_word]
        second_word_values = [char_to_value[char] for char in second_word]
        third_word_values = [char_to_value[char] for char in third_word]

        #convert the extracted values to integers
        first_value = int(''.join(map(str, first_word_values)))
        second_value = int(''.join(map(str, second_word_values)))
        result = int(''.join(map(str, third_word_values)))

        #check the sign to see if we need to add, substract...
        if equation_input == '+':
            return (first_value + second_value) == result
        elif equation_input == '-':
            return (first_value - second_value) == result
        elif equation_input == '*':
            return(first_value * second_value) == result
        elif equation_input == '/':
            return(first_value / second_value) == result
        return True

    constraints = [
        (variables, constraint_unique),
        (variables, constraint_result),
    ]

    problem = CspProblem(variables, domains, constraints)

    output = backtrack(problem)
    return output

header = st.container()

solution = st.container()

col1, col2 = st.columns(2)

solve_button = st.button("Solve")


with header:
    st.title("Welcome to my cryptarithmetic puzzle solver!")

with col1:
    puzzle_input = st.text_input("Enter the three words for the puzzle: ")

with col2:
    equation_input = st.selectbox("Choose the equation sign: ", options=['+','-','*','/'])

if solve_button and puzzle_input:
    solution = solve_cryptoarithmetic_puzzle(puzzle_input, equation_input)
    if solution:
        # Format the solution as a table for better readability
        st.subheader("Solution:")
        import pandas as pd
        df = pd.DataFrame({"Letter": solution.keys(), "Value": solution.values()})
        table = df.to_html(index=False, escape=False, classes=["styled-table"])
        st.write(table, unsafe_allow_html=True)
        st.write()
    else:
        st.write("There is no solution for this puzzle.")



m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #ffffff;
    color:#0099ff;   
    border: #0099ff 1px solid;
}
div.stButton > button:active {
    background-color: #0099ff;;
    color:#fff;   
    border: #0099ff 1px solid;
}
div.stButton > button:focus {
    background-color: #0099ff;
    color:#fff;   
    border: #0099ff 1px solid;
}

table {
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }
    th {
        background-color: #0099ff;
        color: black;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
                

</style>""", unsafe_allow_html=True)


footer="""<style>

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}


</style>
<div class="footer">
<p>Iris Loret - 2023</p>
</div>


"""
st.markdown(footer,unsafe_allow_html=True)