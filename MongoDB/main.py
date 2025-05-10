from parser import handle_input 

def main():
    print("Welcome to ChatDB (Mongo Edition)!")
    while True:
        user_input = input("\nWhat would you like to do? (type 'exit' to quit)\n> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = handle_input(user_input)
        print("\nResult:\n", response)

if __name__ == "__main__":
    main()
