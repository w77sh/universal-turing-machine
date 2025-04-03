import matplotlib.pyplot as plt
import matplotlib.patches as patches


class TuringMachine:
    def __init__(self, states, transitions, start_state, accept_state, reject_state, blank_symbol='_'):
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.current_state = start_state
        self.tape = []
        self.head_position = 0
        self.direction = None  # Tracks head movement direction (None initially)

    def load_tape(self, input_tape):
        self.tape = list(input_tape) + [self.blank_symbol] * 10
        self.head_position = 0

    def step(self):
        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)

        if key not in self.transitions:
            return False  # Halting

        new_state, write_symbol, direction = self.transitions[key]
        self.tape[self.head_position] = write_symbol
        self.current_state = new_state
        self.direction = direction  # Set direction of movement

        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1

        # Ensure head doesn't go out of bounds
        if self.head_position < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)

        return True

    def visualize(self):
        # Create a figure and axis for visualization
        fig, ax = plt.subplots(figsize=(12, 2))

        # Create the tape
        tape_str = ''.join(self.tape).rstrip(self.blank_symbol)
        num_cells = len(tape_str)

        # Draw each cell of the tape
        for i in range(num_cells):
            color = 'white' if self.tape[i] != 'X' else 'green'
            if self.tape[i] == '1' and self.head_position == i:
                color = 'yellow'  # Highlight the current symbol
            ax.add_patch(patches.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black'))
            ax.text(i + 0.5, 0.5, self.tape[i], ha='center', va='center', fontsize=12)

        # Draw the tape head as an arrow
        ax.arrow(self.head_position, 1.1, 0, 0.5, head_width=0.05, head_length=0.1, fc='red', ec='red')

        # Draw the current state label
        ax.text(num_cells / 2, 1.6, f"Current State: {self.current_state}", ha='center', va='center', fontsize=14,
                color='blue')

        # Set axis limits and remove axis labels
        ax.set_xlim(-1, num_cells)
        ax.set_ylim(0, 2)
        ax.set_aspect('equal')
        ax.axis('off')

        # Show the plot
        plt.show()

    def run(self, max_steps=100):
        print("Starting Turing Machine Simulation...\n")
        steps = 0
        while steps < max_steps:
            # Print the current state and tape in the console
            print(f"\nStep {steps + 1}:")
            print(f"Current State: {self.current_state}")
            print(f"Tape: {''.join(self.tape)}")
            print(f"Head Position: {self.head_position}")

            # Print the transition in the desired format
            current_symbol = self.tape[self.head_position]
            key = (self.current_state, current_symbol)
            if key in self.transitions:
                new_state, write_symbol, direction = self.transitions[key]
                print(f"{current_symbol} -->> {write_symbol},{direction}")

            # Visualize the tape with matplotlib
            self.visualize()

            # Check for acceptance, rejection, or halting
            if self.current_state == self.accept_state:
                print("\nResult: Accepted!")
                return "ACCEPTED"
            elif self.current_state == self.reject_state:
                print("\nResult: Rejected!")
                return "REJECTED"

            if not self.step():
                print("\nResult: Halting!")
                return "HALTING"

            steps += 1
            input("\nPress Enter to continue...")  # Step-by-step visualization

        print("\nResult: Infinite Loop!")
        return "INFINITE LOOP"


# Example configuration
if __name__ == "__main__":
    states = {"q0", "q1", "q_accept", "q_reject"}
    start_state = "q0"
    accept_state = "q_accept"
    reject_state = "q_reject"
    transitions = {
        # (current_state, current_symbol): (new_state, write_symbol, direction)
        ("q0", "1"): ("q1", "X", "R"),
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "_"): ("q_accept", "_", "N"),  # Ensure there's a proper transition for blank
    }

    tm = TuringMachine(states, transitions, start_state, accept_state, reject_state)
    user_tape = input("Enter the input tape (e.g., 111): ")
    tm.load_tape(user_tape)
    result = tm.run()
    print(f"\nFinal Result: {result}")