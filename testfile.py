import random

def guess_number():
    secret = random.randint(1, 10)
    attempts = 3

    print("Guess the number (1-10). You have 3 attempts.")

    for i in range(attempts):
        guess = random.randint(1, 10)  # simulating user input
        print(f"Attempt {i + 1}: guessed {guess}")

        if guess == secret:
            print("🎉 Correct guess!")
            return
        elif guess < secret:
            print("Too low!")
        else:
            print("Too high!")

    print(f"Out of attempts. The number was {secret}.")

guess_number()
