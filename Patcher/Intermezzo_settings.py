import Modules.constants as cs
import Modules.setting as st

def main():
    while True:
        
        # Print setting selection screen
        print("Current settings: ")
        for setting, x in zip(cs.settings, range(len(cs.settings))):
            print(f"{chr(x + 65)}. {st.Setting().create(f'{setting}')}")
        print("S. Set default settings")
        print("X. Exit the menu")
        
        while True:
            choice = str(input("Which setting should be edited? (Enter the corresponding option): ")).upper()
            
            if choice in [chr(x + 65) for x in range(len(cs.settings))]:
                option = cs.settings[ord(choice) - 65]
                break
            elif choice == "S":
                option = "standard"
                break
            elif choice == "X":
                option = "exit"
                break
            else:
                print("This is not an option. Please try again.")
        
        if option == "standard":
            for setting in cs.settings:
                st.Setting().create(setting).set_default()
        elif option == "exit":
            break
        else:
            st.Setting().create(option).set_value()
    
    input("All done!")

if __name__ == "__main__":
    main()
