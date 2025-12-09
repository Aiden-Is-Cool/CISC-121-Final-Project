Project Explanation:

This is an interactive Python application meant to visualize to the user how a Binary Search algorithm works. It allows the user to manually, step by step see how the algorithm locates a value and discards others making the logic and decision process easy to understand.

---

Demo:

The interface allows the user to:

- Generate a sorted list of chosen length 'n'
- Choose a integer target value to search for
- Progress through the binary search showing each step of the process
- Visually see eliminated values and the current midpoint easily with colour


(Gif Attached in File Submission) :D

---

Problem Breakdown & Computational Thinking:

Decomposition:

- Generate a sorted list
- Track the search range (`low`, `high`)
- Compute the midpoint
- Compare the midpoint value with the target
- Update the search range
- Repeat until the value is found or the range is empty


Pattern Recognition:

- Calculate the midpoint
- Compare midpoint value to target
- Discard half of the search range


Abstraction:

- List generation is automated so the user can never input an unsorted list
- The visualization highlights key components of the algorithm
  - Gray italics => eliminated values
  - Blue bold underline => current midpoint


Algorithm Design:

- Instead of a while loop, the algorithm progresses a single step per click of a button. As to show the intermediate steps between
  discarding information
- State is stored using gr.State() so values persist between steps
- A step counter increases its state value every time cycled through

- Find the midpoint of the current range
- If the target equals the midpoint => found
- If the target is smaller => search the left half
- If the target is larger => search the right half

- This gives Binary Search a worst case time complexity of O(log n) since each half without the value is discarded
- It also gives a best case of O(1) if the midpoint is the target

---

Steps to Run/ UI:

The interface was built using Gradio:

- The user inputs an integer to determine the length of the list
- The user inputs a second integer to determine the target value
- The CREATE button initializes the list and resets the algorithm 
- The NEXT button performs exactly one step of binary search
- The list is rendered using HTML
  - Eliminated values are styled gray and italic
  - The current midpoint is styled blue, bold, and underlined
  - The colours are a key aspect to help the user visualize just how binary sort logically works

---

Testing & Verification:

The application was tested with:
- Different list lengths
- Targets at the beginning, middle, end
- Targets not in the list
- Repeated restarting using the CREATE button

In all cases:
- The search correctly finds the target when present
- The algorithm correctly reports when the target is not found
- The step counter updates consistently

---

Running Locally:

Repository Link: https://github.com/Aiden-Is-Cool/CISC-121-Final-Project

Hugging Face Link: https://9dd26e88b59b249595.gradio.live/

