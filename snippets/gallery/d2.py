import os  # markdown-exec: hide
if "CI" in os.environ:  # markdown-exec: hide
    print("D2 is not installed in CI, skipping this gallery example.")  # markdown-exec: hide
    raise SystemExit(0)  # markdown-exec: hide
import subprocess

diagram = """
direction: right

Before and after becoming friends: {
  2007: Office chatter in 2007 {
    shape: sequence_diagram
    alice: Alice
    bob: Bobby

    awkward small talk: {
      alice -> bob: uhm, hi
      bob -> alice: oh, hello

      icebreaker attempt: {
        alice -> bob: what did you have for lunch?
      }

      unfortunate outcome: {
        bob -> alice: that's personal
      }
    }
  }

  2012: Office chatter in 2012 {
    shape: sequence_diagram
    alice: Alice
    bob: Bobby
    alice -> bob: Want to play with ChatGPT?
    bob -> alice: Yes!
    bob -> alice.play: Write a play...
    alice.play -> bob.play: about 2 friends...
    bob.play -> alice.play: who find love...
    alice.play -> bob.play: in a sequence diagram
  }

  2007 -> 2012: Five\nyears\nlater
}
"""

# We simply run `d2` in a subprocess, passing it our diagram as input and capturing its output to print it.
svg = subprocess.check_output(["d2", "-", "-"], input=diagram, stderr=subprocess.DEVNULL, text=True)
print(svg)
