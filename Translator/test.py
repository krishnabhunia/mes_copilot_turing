import time

for i in range(0, 101, 10):  # Progress increments from 0% to 100% in steps of 10%
    print(f"Process: {i}%", end="\r")
    time.sleep(0.5)  # Simulate processing time

print("\nDone!")  # Move to a new line after the loop completes
