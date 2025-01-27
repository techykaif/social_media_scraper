import os

def display_menu():
    """Display the menu options."""
    print("\nSelect an option:")
    print("1. Facebook Scraper")
    print("2. Instagram Scraper")
    print("3. YouTube Scraper")
    print("4. Exit")

def execute_script(script_name):
    """Execute the specified script."""
    try:
        os.system(f"python {script_name}")
    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")

def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            print("\nLaunching Facebook Scraper...")
            execute_script("Facebook.py")
        elif choice == "2":
            print("\nLaunching Instagram Scraper...")
            execute_script("Instagram.py")
        elif choice == "3":
            print("\nLaunching YouTube Scraper...")
            execute_script("YouTube.py")
        elif choice == "4":
            print("\nExiting the program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
