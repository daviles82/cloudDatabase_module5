from pymongo import MongoClient
from tkinter import *
from dotenv import load_dotenv
import os

root = Tk()
root.title("To Do List App")
root.geometry("300x600")

# TOP-------------------------CLOUD DATABASE------------------------------------
load_dotenv()
api_key = os.getenv("API_KEY")
client = MongoClient(api_key)

# database
db = client["to_do_list"]

# collection
collection = db["users_todos"]

# Create a collection ////////////////
# db.create_collection(collection)

# BOTTOM----------------------CLOUD DATABASE------------------------------------

# TOP-------------------------FUNCTIONALITY-------------------------------------

# insert to do
def add_to_todo():
    global label2
    todo_input = e.get()

    if todo_input:
        document = {"input": todo_input}
        collection.insert_one(document)
        label2.config(text=f"Added '{todo_input}'")
        e.delete(0, 'end')
    else:
        label2.config(text="Please add a To Do")
    show_list(collection) 

# delete to do
def delete_a_todo(delete_collection):
    for var, checked in delete_collection:
        if var.get():
            result = collection.delete_one({"input": checked})
            if result.deleted_count > 0:
                label2.config(text=f"Deleted '{checked}'")
            else:
                label2.config(f"No matching todo found for: {checked}")
    show_list(collection) 

r = StringVar(value="")

# show list
def show_list(collection):
    global delete_collection, list_frame, radio
    row_number = 5

    # repopulate list
    for widget in list_frame.winfo_children():
        widget.destroy()

    delete_collection = []
    for document in collection.find():
        row_number += 1

        v = BooleanVar()
        delete_collection.append((v, document["input"]))

        label3 = Checkbutton(list_frame, text=document["input"], variable=v)
        label3.deselect()
        label3.grid(row=row_number, column=0, sticky=W)

        radio = Radiobutton(list_frame, text="", variable=r, 
                            value=document["input"])
        radio.grid(row=row_number, column=1, sticky=E, padx=(50, 0))

        radio.select()

# edit to do
def edit_todo(edit_entry):
    edit_input = r.get()

    pass_entry = edit_entry.get()
    edit_document = collection.find_one({"input": edit_input})

    if edit_document:
        collection.update_one({"input": edit_input}, 
                              {"$set": {"input": pass_entry}})
        label2.config(text=f"Edited '{edit_input}'")
        edit_entry.delete(0, 'end')
    else:
        label2.config(text="NOT FOUND")
    show_list(collection) 
    
# BOTTOM----------------------FUNCTIONALITY-------------------------------------

# TOP-----------------------------GUI------------------------------------------- 

my_playList = Label(root, text="To Do List", font=("Helvetica", 20))
my_playList.grid(row=0, column=1,pady=10)

label = Label(root, text="ADD TO DO")
label.grid(row=1, column=1)
e = Entry(root, width=20)
e.grid(row=2, column=1)

my_detailList = Button(root, text="COMMIT TO LIST", command=add_to_todo)
my_detailList.grid(row=3, column=1,pady=10)

label2 = Label(root, text="")
label2.grid(row=4, column=1)

label3 = Label(root, text="Delete", font=("Helvetica", 8))
label3.grid(row=5, column=1, sticky=W)

label5 = Label(root, text="Edit", font=("Helvetica", 8))
label5.grid(row=5, column=1, sticky=E)

delete_collection = []

list_frame = Frame(root)
list_frame.grid(row=6, column=1, sticky=W)

# BOTTOM--------------------------GUI------------------------------------------- 

show_list(collection)

delete_button = Button(root, text="Delete Selected", 
                       command=lambda: delete_a_todo(delete_collection))
delete_button.grid(row=10, column=1,pady=10)

label4 = Label(root, text="EDIT A TO DO")
label4.grid(row=11, column=1)
edit_entry = Entry(root, width=20)
edit_entry.grid(row=12, column=1)
update_button = Button(root, text="Update Selected", 
                       command=lambda: edit_todo(edit_entry))
update_button.grid(row=13, column=1)

root.mainloop()

client.close()
