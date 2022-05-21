print()
print("a   | b   | a \\|\\| b")
print("--- | --- | ---")
for a in (True, False):
    for b in (True, False):
        print(f"{a} | {b} | {a or b}")
print()
