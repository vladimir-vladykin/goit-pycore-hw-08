import pickle
from entities import *
from errors_helper import input_error


# Description of what program can do
SUPPORTED_COMMANDS_INFO = """
Supported list of commands:
hello -> just says hi!
add 'name' 'phone' -> create contact. Note that phone should be exactly 10 symbols long.
change 'name' 'old phone' 'new phone' -> edits phone number of contact.
phone 'name' -> outputs saved phone numbers of contacts.
add-birthday 'name' 'birthday' -> saves birthday for user, in 'DD.MM.YYYY' format.
show-birthday 'name' -> outputs birthday of user.
birthdays -> output all upcoming birthdays.
all -> output all saved contacts.
close -> finish assistant.
exit -> finish assistant.
info -> information about supported commands.

Make sure you follow the format of commands, and avoid spaces and plus in phone numbers, as they are not supported.
Note that state of your address book will be saved, but only if you closes programm with \'close\' or \'exit\' command."""

# place in file system we're gonna keep our address book
CACHE_FILE_NAME = "addressbook.pkl"

@input_error # use @input_error even for main() function to completely get rid of try/except here
def main():
    # greetings to user + list of supported commands
    print("Welcome to the assistant bot!")
    print(format_info())
    
    # this is where our contacts lives
    address_book = load_address_book(CACHE_FILE_NAME)

    # waits for user's commands forever, untill terminal command is occurred
    while True:
        user_input = input("Enter a command: ")

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_address_book(address_book, CACHE_FILE_NAME)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(find_numbers_by_name(args, address_book))
        elif command == "add-birthday":
            print(add_birthday(args, address_book))
        elif command == "show-birthday":
            print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(birthdays(args, address_book))
        elif command == "all":
            print(output_all_contacts(address_book))
        elif command == "info":
            print(format_info())
        else:
            print("Invalid command.")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, address_book: AddressBook):
    name, phone, *_ = args

    contact = None
    result_message = None
    if name in address_book.data:
        contact = address_book.find(name)
        result_message = "Contact updated."
    else:
        contact = Record(name)
        address_book.add_record(contact)
        result_message = "Contact added."

    contact.add_phone(phone)
    return result_message


@input_error
def output_all_contacts(address_book: AddressBook):
    all_contacts = address_book.all_records()
    if len(all_contacts) > 0:
        return f"Here's all added contacts:\n{all_contacts}."
    else:
        return "No contacts added so far."

@input_error
def find_numbers_by_name(args, address_book: AddressBook):
    name = args[0]
    phones = address_book.find_phones(name)
    return f"Phone numbers of {name}:\n {phones}."


@input_error
def change_contact(args, address_book: AddressBook):
    name, old_phone, new_phone, *_  = args

    contact_record = address_book.find(name)
    contact_record.edit_phone(old_phone, new_phone)
    return "Contact changed."

@input_error
def add_birthday(args, address_book: AddressBook):
    name, birthday, *_ = args

    record = address_book.find(name)
    record.add_birthday(birthday)

    return f"Birthday added for {name}"

@input_error
def show_birthday(args, address_book: AddressBook):
    name = args[0]
    user = address_book.find(name)
    birthday = user.birthday
    
    if birthday is not None:
        return f"Birthday of {name}'s is {birthday}"
    else:
        return f"No birthday added for user {name}"

@input_error
def birthdays(args, address_book: AddressBook):
    upcoming_birthdays = address_book.get_upcoming_birthdays()

    result = ""
    if upcoming_birthdays:
        result += "Upcoming birthdays:\n"
        for birthday_item in upcoming_birthdays:
            result += f"{birthday_item[USER_KEY].name}: {birthday_item[CONGRATULATION_DATE_KEY]}\n"
    else:
        result += "No upcoming birthdays for now."

    return result


@input_error
def format_info():
    return SUPPORTED_COMMANDS_INFO

# loads AddressBook's state from file, if any. 
# in case file not exists just creates empty instance of AddressBook
def load_address_book(filename: str) -> AddressBook:
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        # probably first session
        return AddressBook()
    
# dumps AddressBook into file
def save_address_book(address_book: AddressBook, filename: str):
    with open(filename, "wb") as file:
        pickle.dump(address_book, file)


if __name__ == "__main__":
    # run program
    main()