from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

BLUE = "#bedcfa"
WHITE = "#f8f1f1"
FLAT = "ridge"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # Copy to the clipboard
    pyperclip.copy(password)
    
# ---------------------------- SEARCH INFO ------------------------------- #


def find_password():
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        try:
            email = data[website]['email']
            password = data[website]['password']
        except KeyError:
            messagebox.showerror(title="Error", message=f"No details for {website} exists")
        else:
            messagebox.showinfo(title=website, message=f"Email:{email}\nPassword: {password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=60, background=BLUE)

# Canvas Image
canvas = Canvas(width=200, height=200, bg=BLUE, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0, ipady=5)

# Labels
website_label = Label(text="Website: ", bg=BLUE)
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username: ", bg=BLUE)
email_label.grid(column=0, row=2)

password_label = Label(text="Password: ", bg=BLUE)
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, "cptsebas@gmail.com")
# END the last character inside the entry
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="EW")

# Buttons
add_button = Button(text="Add", width=36, bg=WHITE, relief=FLAT, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

g_password_button = Button(text="Generate Password", bg=WHITE, relief=FLAT, command=generate_password)
g_password_button.grid(column=2, row=3, sticky="EW")

search_button = Button(text="Search", bg=WHITE, relief=FLAT, command=find_password)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
