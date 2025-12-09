# Final Code - Install GRADIO Before Use

import gradio as gr

# Function to format list as HTML with styling
def formatList(seq, low, high, midVal):

  """
  Takes:
    seq   - the full list of numbers
    low   - current low index of the search range
    high  - current high index of the search range
    midVal - index of the current midpoint
  Returns:
    A single HTML string with different styles for:
      - values outside [low, high]  → gray & italic
      - midpoint                    → blue, bold, underlined
      - active search range         → normal
  """

  parts = []
  for i, x in enumerate(seq):
    # Values outside of current range
    if i < low or i > high:
      style = (
          "color: gray;"
          "font-style: italic;"
          "font-size: 16px;"
      )

    # Checking mid value
    elif i == midVal:
      style = (
          "color: blue;"
          "font-weight: bold;"
          "text-decoration: underline;"
          "font-size: 16px;"
      )

    else:
      style = "font-size: 16px"
    parts.append(f"<span style='{style}'>{x}</span>")

  return " ".join(parts)


# Creates the Start/ Restart Function
def create(n, target):

  """
  This function runs when the user clicks 'CREATE'.
  It:
    - converts user inputs to integers
    - generates the sorted list [1..n]
    - initializes the state dictionary (vals)
    - returns the initial HTML message + state
  """

  # Take User Variables, make sure integers to avoid floats
  n = int(n)    # Length of list
  target = int(target)    # Target within list

  # Generate list
  seq = list(range(1, n + 1))

  # Create dictionary for all variables which do persist between button clicks
  vals = {
      'seq': seq,
      'val': target,
      'low': 0,
      'high': len(seq) - 1,
      'done': False,
      'Steps': 0,
      }

  # Format the list visually for the initial state
  # Midpoint is initially the middle of the full range
  list_html = formatList(seq, vals["low"], vals["high"], (vals["low"] + vals["high"]) // 2)

  # Initial UI Msg to player (HTML)
  msg = (
    f"<p><b>List:</b> {list_html}</p>"
    f"<p><b>Target Value:</b> {target}</p>"
    "<p>Click <b>NEXT</b> to begin Binary Search.</p>"
  )

  # Return the HTML and the state object
  return msg, vals


def nextStep(vals):

  """
  This function runs each time the user clicks 'NEXT'.
  It:
    - reads the current state (vals)
    - performs one step of binary search
    - updates low/high/done/Steps
    - returns an updated HTML message + updated state
  """

  # Unpack values from state dictionary
  seq = vals['seq']
  val = vals['val']
  low = vals['low']
  high = vals['high']
  done = vals['done']
  steps = vals['Steps']

  # If search done, show message informing user
  if done:
    # Keep a consistent visualization, using current low/hig
    list_html = formatList(seq, low, high, (low + high) // 2)
    msg = (
        f"<p>Search is already complete:</p>"
        f"<p><b>List:</b> {list_html}</p>"
        f"<p><b>Target value:</b> {val}</p>"
        "<p>Press <b>CREATE</b> to start again.</p>"
        )
    return msg, vals

  # If the low index has passed the high index → target not found
  if low > high:
        vals["done"] = True
        msg = (
            f"<p><b>List:</b> {' '.join(map(str, seq))}</p>"
            f"<p><b>Target value:</b> {val}</p>"
            f"<p><b>Value not found</b> after {steps} steps ❌</p>"
        )
        return msg, vals

  # Identify the midpoint and index it
  midPoint = (low + high) // 2
  midVal = seq[midPoint]

  # Add one tick to the total step counter
  steps += 1

  # Rebuild the styled list using the current low/high and midpoint
  list_html = formatList(seq, low, high, midPoint)

  # Basic header with list and target
  header = (
      f"<p><b>List:</b> {list_html}</p>"
      f"<p><b>Target value:</b> {val}</p>"
    )

  # Show current low, high, and mid positions
  details = (
      f"<p>Low index: {low}, High index: {high}, "
      f"Mid index: {midPoint}, Mid value: {midVal}</p>"
    )

  # Compare target with midpoint to decide which half to search
  if val < midVal:
    # Target must be in the left half
    high = midPoint - 1
    msg = (
            header +
            details +
            f"<p>Value is <b>less than {midVal}</b> → search <b>LEFT</b> half.</p>"
            f"<p>Steps taken: {steps}</p>"
        )
  # If not in left half, our value must be in the right half
  elif val > midVal:
    low = midPoint + 1
    msg = msg = (
            header +
            details +
            f"<p>Value is <b>greater than {midVal}</b> → search <b>RIGHT</b> half.</p>"
            f"<p>Steps taken: {steps}</p>"
        )

  # If our value is not in either half it must be our mid point and we have found it
  else:
    done = True
    msg = (
            header +
            details +
            f"<p><b>Value {val} found</b> at index <b>{midPoint}</b>✅</p>"
            f"<p>Total steps: {steps}</p>"
        )

  # Update vals dictionary before returning
  vals['low'] = low
  vals['high'] = high
  vals['done'] = done
  vals['Steps'] = steps

  # Return updated HTML and state
  return msg, vals

# Build the gradio interface
with gr.Blocks() as bsVis:

  # Title @ top
  gr.Markdown("# Binary Search Visualization")

  # Create a side by side interface for our list length and target inputs
  with gr.Row():
    # Input length of list
    n_input = gr.Number(label="List Length", value= 20)
    # Input target value
    target_input = gr.Number(label="Target Value", value= 5)

  # Make buttons for initialization of the list and the next step in the search
  create_button = gr.Button("CREATE")
  next_button = gr.Button("NEXT")

  # Create output area using HTML
  output = gr.HTML(label="Output")

  # Store vals between button presses
  vals = gr.State()

  # When CREATE is clicked:
  #   - call create()
  #   - pass n_input and target_input into it
  #   - update 'output' and 'vals' with what create() returns
  create_button.click(
      fn = create,
      inputs = [n_input, target_input],
      outputs = [output, vals]
  )

  # When NEXT is clicked:
  #   - call nextStep()
  #   - pass current 'vals' into it
  #   - update 'output' and 'vals' with what nextStep() returns
  next_button.click(
      fn = nextStep,
      inputs = [vals],
      outputs = [output, vals]
  )

# Launch the app
bsVis.launch(share = True)

# Added comments for increased readability