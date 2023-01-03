from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    
    password_input.delete(0,'end')
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)
    
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_information():
    wb = website_input.get().lower()
    email = email_input.get()
    pswd = password_input.get()
    
    new_data = {wb:{
        "email": email,
        "password": pswd
    }}
    
    if len(wb) != 0 and len(email) != 0 and len(pswd) != 0:
        
        try:     
            with open("information.json", "r") as file:
                #reading old data
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):       
            with open("information.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            #Check if the website is in the database
            if wb in data:
                update = messagebox.askyesno("Warning", f"There is already a password saved for\nWould you like to overwrite?")
                if update:
                    data[wb]["email"] = email
                    data[wb]["password"] = pswd
                else:
                    return
            
            #Updating old data with new data
            data.update(new_data)
            
            with open("information.json", "w") as file:
                #Saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_input.delete(0,'end')
            password_input.delete(0,'end')
        
    else:
        messagebox.showwarning(title="Opps", message="Please don't leave any fields empty!")
        
# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    wb = website_input.get().lower()
    try:     
        with open("information.json", "r") as file:
            #reading old data
            data = json.load(file)
            
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showwarning("Error", "There is no data")
    
    else:
        if wb in data:
            messagebox.showinfo(wb.title(), f'Email: {data[wb]["email"]}\nPassword: {data[wb]["password"]}')
        else:
            messagebox.showwarning("Error", "There is no coincidences")
        
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=30,pady=30)

canvas = Canvas(width=200, height=200)
pass_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=pass_img)
canvas.grid(row=0, column=1)

website_txt = Label(text="Website: ", font=("Cascadia", 10, "normal"))
website_txt.grid(row=1, column=0)

email_txt = Label(text="Email/Username: ", font=("Cascadia", 10, "normal"))
email_txt.grid(row=2, column=0)

password_txt = Label(text="Password: ", font=("Cascadia", 10, "normal"))
password_txt.grid(row=3, column=0)

website_input = Entry()
website_input.grid(row=1, column=1, sticky=EW)
website_input.focus()

btn_search = Button(text="Search", command=find_password)
btn_search.grid(row=1, column=2, sticky=EW)

email_input = Entry()
email_input.grid(row=2, column=1, columnspan=2, sticky=EW)
email_input.insert(0, "example@email.com")

password_input = Entry()
password_input.grid(row=3, column=1, sticky=EW)

btn_generate = Button(text="Generate Password", command=generate_password)
btn_generate.grid(row=3, column=2, sticky=EW)

btn_add = Button(text="Add", command=save_information)
btn_add.grid(row=4, column=1, columnspan=2, sticky=EW)

window.mainloop()