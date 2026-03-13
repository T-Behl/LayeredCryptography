#objective: build off of other. First start with hashing and show weakness from that -> improve hashing -> encrypt password with a key
#Objective cont.: create an encrypted file that requires a password to decrypt.  
import hashlib #grabs included hash algorithms and methods
from cryptography.fernet import Fernet #allows us to create a shared key ONLY DEPENDENCY!!
import platform #find out the OS for cross-platform deployment
from pathlib import Path #created to find desktop path
import shutil #move key to downloads automatically
from tkinter import * #GUI creation and management
from tkinter import ttk #default style for GUI
# Device\Users\{Actual_User}\OneDrive\Desktop <- actual path to desktop to your PC if OneDrive is Synced!
# Device\Users\{Actual_User}\Desktop <- path pattern for MAC, Local Windows, and most Linux Distros
os_type =platform.system()
desktop_path = Path.home() / "Desktop" #path can't change!! Need to create a new path
download_path = Path.home() / "Downloads"
if desktop_path.exists(): #inital check
    desktop_path = desktop_path
else:
    xdg_config = Path.home() / ".config" / "user-dirs.dirs" #special Linux distros
    if xdg_config.exists():
        with open(xdg_config, "r", encoding="utf-8") as f:
            for line in f:
                if "XDG_DESKTOP_DIR" in line:
                    path = line.split("=")[1].strip().strip('"')
                    path = path.replace("$HOME", str(Path.home()))
                    desktop_path = path
#initial file path. This will be checked later for Windows to see if file can be created with a try except clause!!
password_path = desktop_path / "GivenPasswords.txt"
#create key funtion for encryption
def write_key():
    key = Fernet.generate_key() #simple/symmetric key generation
    for widget in dynamic_frame.winfo_children(): #remove all elements within dynamic frame
        widget.destroy()
    if new_desktop_path.exists():
        global key_path
        key_path = new_desktop_path / "SharedKey.key"
    else:
        key_path = desktop_path / "SharedKey.key"
    with key_path.open(mode="wb") as key_file: #saves the key in a binary file called 'SharedKey.key'
        key_file.write(key)
    ttk.Label(dynamic_frame, text="Key created and stored on desktop!").grid(column=0,row=0, sticky=W)
#load key from key file
new_key_path = None
def load_key():
    global key_path
    return key_path.open(mode="rb").read()
def move_key():
    global key_path
    for widget in dynamic_frame.winfo_children(): #remove all elements within dynamic frame
        widget.destroy()
    label_created = False
    try:
        shutil.move(key_path, download_path)
    except shutil.Error:
        #DELETE DOWNLOADS KEY THEN MOVE DESKTOP KEY -> DOWNLOADS
        download_key = download_path / "SharedKey.key"
        download_key.unlink()
        shutil.move(key_path, download_path)
        ttk.Label(dynamic_frame,text="Moved new key into downloads directory").grid(column=0,row=1)
        label_created = True
    except FileNotFoundError:
        ttk.Label(dynamic_frame,text="No key found in desktop directory!").grid(column=0,row=1)
        label_created = True
    if label_created == False:
        ttk.Label(dynamic_frame,text="Moved key into downloads directory").grid(column=0,row=1)
#encrypt data with key:
def encrypt_file(path):
    for widget in dynamic_frame.winfo_children(): #remove all elements within dynamic frame
        widget.destroy()
    try:
        given_key = Fernet(load_key())
    except FileNotFoundError:
        ttk.Label(dynamic_frame,text="Key not found! Cannot encrypt stored accounts!").grid(column=0,row=1)
        return
    with path.open(mode="rb") as file:
        file_data = file.read()
    encrypted_data = given_key.encrypt(file_data)
    with path.open(mode = "wb") as file:
        file.write(encrypted_data)
    ttk.Label(dynamic_frame, text="Encrypted stored accounts!").grid(column=0,row=1)
def decrypt_file(path):
    for widget in dynamic_frame.winfo_children(): #remove all elements within dynamic frame
        widget.destroy()
    try:
        given_key = Fernet(load_key())
    except FileNotFoundError:
        ttk.Label(dynamic_frame,text="Key not found! Cannot decrypt stored accounts!").grid(column=0,row=1)
        return
    with path.open(mode="rb") as file:
        file_data = file.read()
    encrypted_data = given_key.decrypt(file_data)
    with path.open(mode = "wb") as file:
        file.write(encrypted_data)
    ttk.Label(dynamic_frame, text="Decrypted stored accounts!").grid(column=0,row=1)
#hash formulas
def hashSHA256(data):
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data
def hashSHA1(data):
    hashed_data = hashlib.sha1(data.encode()).hexdigest()
    return hashed_data
def hashblake2(data):
    hashed_data = hashlib.blake2b(data.encode()).hexdigest()
    return hashed_data
#test tuples for updating file and encryption
all_accounts = [("Username", "Password"),("User01","SecuredCodeOnly101"),
                 ("User02","Goodbye"),("User03","SecurePassesHereOnly110"),
                 ("User04","Nerds"),("User05","People"), ("User06", "TestingFunctions"),
                 ("User07", "DebuggingHell")]
#hash first 5 'passwords' to speed up calls for previews
SHA1_list = []
SHA256_list = []
Blake2_list = []
current_hash = None
for i in range(1,7): #edit this to only being the first 5 passwords in file!
    password = all_accounts[i][1]
    password = str(password)
    SHA1_i = hashSHA1(password) #issue: hashes are very different from preview to file!!
    SHA256_i = hashSHA256(password)
    Blake2_i = hashblake2(password)
    SHA1_list.append((all_accounts[i][0],SHA1_i))
    SHA256_list.append((all_accounts[i][0],SHA256_i))
    Blake2_list.append((all_accounts[i][0],Blake2_i))
plaintext = all_accounts[1:7]
messages = plaintext #initialize previews
def hashingfile(action):
    global messages
    global current_hash
    dynamic_text_frame.delete("1.0",END)
    match action:
        case "plaintext": #shift to plaintext
            messages = plaintext
            current_hash = None
            dynamic_text_frame.insert(index=END,chars="This is human readable! Keeping any password like this for your website is extremely insecure! Check out one of the hashes to start securing those passwords!")
        case "SHA1": #shift to SHA1
            messages = SHA1_list
            current_hash = "SHA1"
            dynamic_text_frame.insert(index=END,chars="The character length of these digests makes it super easy to create a copy with completely different inputted data. This is called collision and is something that should be avoided with your hashing. The NIST framework has already deprecated this algorithm because of this so let’s do the same!")
        case "SHA256": #shift to SHA256
            messages = SHA256_list
            current_hash = "SHA256"
            dynamic_text_frame.insert(index=END,chars="This is the most common hashing algorithm. This is because it’s so quick and still gives you plenty of characters to have the digest be secure!")
        case "Blake2": #shift to SHA256
            messages = Blake2_list
            current_hash = "Blake2"
            dynamic_text_frame.insert(index=END,chars="This algorithm is used when time is an extremely important consideration when hashing data. When your application needs real-time processes, use this algorithm to keep up with the pace! ")
    message_list ()
#create function to push hash to file
def editStoredAccounts(action=False): #edit passwords of all accounts
    edited_accounts = []
    for i in range(1,len(all_accounts)): #iterate over accounts, ignoring the first index [0]
        password = all_accounts[i][1] #grab only password
        if current_hash == "SHA1":
            new_password = hashSHA1(password) #SHA1 hash
        elif current_hash == "SHA256":
            new_password = hashSHA256(password) #SHA256 hash
        elif current_hash == "Blake2":
            new_password = hashblake2(password)
        else:
            new_password = password
        edited_accounts.append((all_accounts[i][0],new_password)) #rebuild entry with edited password
    column_widths =[max(len(str(account)) for account in column) for column in zip(*edited_accounts)] #edit columns to all be aligned
    if new_desktop_path.exists():
            with new_file_path.open(mode="w", encoding="utf-8") as file: #write test list. Fix with dictionary or tuple list (?)    
                for row in edited_accounts: #only hash the 'password' part of the file
                    formatted_row = " | ".join(str(account).ljust(width) for account, width in zip(row, column_widths))
                    file.write(f"{formatted_row}\n")
    else:
            with password_path.open(mode="w", encoding="utf-8") as file: #write test list. Fix with tuple list (?)
                for row in edited_accounts: #only hash the 'password' part of the file
                    formatted_row = " | ".join(str(account).ljust(width) for account, width in zip(row, column_widths))
                    file.write(f"{formatted_row}\n")
    if action==True:
        if current_hash is not None:
            dynamic_text_frame.insert(index=END, chars=f"\nYour file has been hashed with the {current_hash} algorithm.")
        else:
            dynamic_text_frame.insert(index=END,chars="\nYour file has been converted back to plaintext.")
        start_index = f"{float(dynamic_text_frame.index('end'))-1} linestart"
        end_index = "end-1c"
        dynamic_text_frame.tag_add("red_text", start_index, end_index)
        #ISSUE: first build has the convert to plaintext dialog. Should not be happening
    else:
        return
def AddAccount():
    password = input_password.get()
    check_password = validate_password.get()
    warning_text.config(text =" ")
    if password == check_password:
        all_accounts.append((input_username.get(),input_password.get()))
        editStoredAccounts() #edit stored accounts and then clear input fields
        input_username.delete(0, END)
        input_password.delete(0,END)
        validate_password.delete(0,END)
        gui_mainframe.focus_get()
        handle_focus("Out",input_username,"Enter username...")
        handle_focus("Out",input_password,"Enter password...")
        handle_focus("Out",validate_password,"Re-enter password...")
    else:
        input_password.delete(0,END)
        validate_password.delete(0,END)
        handle_focus("Out",input_password,"Enter password...")
        handle_focus("Out",validate_password,"Re-enter password...")
        warning_text.config(text="Passwords do not match!")
def LoginFunc():
    for widget in dynamic_frame.winfo_children(): #remove all elements within dynamic frame
        widget.destroy()
    input_username = login_username.get()
    input_password = login_password.get()
    if current_hash == "SHA1":
            input_hash = hashSHA1(input_password) #SHA1 hash
    elif current_hash == "SHA256":
            input_hash = hashSHA256(input_password) #SHA256 hash
    elif current_hash == "Blake2":
            input_hash = hashblake2(input_password) #SHA256 hash
    else:
            input_hash = input_password
    found_lines = []
    found_usernames = []
    found_passwords = []
    if new_desktop_path.exists():
        with new_file_path.open(mode="r", encoding="utf-8") as file:
            for account_entry, account in enumerate(file, start=1):
                found_lines.append(account.strip())
    else:
        with password_path.open(mode="r",encoding="utf-8") as file:
            for account_entry, account in enumerate(file, start=1):
                found_lines.append(account.strip())
    for i in range(len(found_lines)):
        account_full = found_lines[i].split("|")
        username = account_full[0].strip(" ")
        password = account_full[1].strip(" ")
        found_usernames.append(username.lower())
        found_passwords.append(password)
    account_index = None
    Login_status = None
    if input_username in found_usernames:
        account_index = found_usernames.index(input_username)
    if input_hash in found_passwords:
        password_index = found_passwords.index(input_hash)
        ttk.Label(dynamic_frame, text=f"Found matching digest at account entry {password_index+1}").grid(column=0,row=3)
        if account_index != password_index:
            Login_status ="Failed login due to inncorrect credintials: username"
        else:
            Login_status = "Successful login!"
    else:
        password_index = "Failed"
        ttk.Label(dynamic_frame, text="No matching digest!").grid(column=0,row=3)
        if account_index is not None:
            Login_status = "Failed login due to inncorrect credintials: password"
        else:
            Login_status = f"No account for username: {input_username.lower()} found!"
    ttk.Label(dynamic_frame,text="Login Process").grid(column=0,row=0)
    ttk.Label(dynamic_frame,text=f"hashing password:\n{input_password} -> {input_hash}").grid(column=0,row=1)
    ttk.Label(dynamic_frame, text="Searching for matching digest within stored account files").grid(column=0,row=2)
    ttk.Label(dynamic_frame, text= Login_status).grid(column=0,row=4)
def handle_focus(mode,element,new_text=None):
    if mode.lower() == "in":
        element.delete(0, END)
        element.config(style="TEntry")
    if mode.lower() == "out":
        if element.get() == "" or element.get() == " ":
            element.insert(0,f"{new_text}")
            element.config(style="Placeholder.TEntry")
def clearpage(): #reset GUI to be built for next page
    for widget in dynamic_frame.winfo_children(): #remove all elements within dynamic frame
        widget.destroy()
    for widget in iteractive_frame.winfo_children(): #remove all elements within iteractive frame
        widget.destroy()
    text_frame.delete("1.0",END) #clear text frame
def pagemovement(version):
    match version:
        case 1: #disclaimer -> startup
            clearpage()
            text_frame.config(height=12)
            text_frame.insert(index=END,chars="The main purpose of cryptography is to protect data that needs to be confidential by making the data unreadable and incoherent to the human eye. The two ways of doing this are hashing and encryption. In some cases, using both is highly recommended.\n")
            text_frame.insert(index=END, chars="\nOne example is securing account login data. Leaving this data where anyone can read it, called plaintext, is extremely risky and seen as breaking a lot of frameworks and regulations. Yet we still need to use this data because it is how anyone logs in to the software or website. So how can we hide the data but still be able to use the data?\n")
            text_frame.insert(index=END, chars="\nBy hashing of course!")
            NextPage.config(command=lambda: pagemovement(2)) #update Next Page button for another page turn
        case 2: #startup -> hashing
            try: #check if desktop is with OneDrive
                with password_path.open(mode="w", encoding="utf-8") as file: #check OG path can create file
                    file.read() #should come as empty
            except FileNotFoundError: #if file can't be created do all this ->
                global new_desktop_path #new global to check if it exists
                global new_file_path #used and checked for updating hashes and encryption
                new_desktop_path = Path.home() / "OneDrive" / "Desktop"
                new_file_path = new_desktop_path / "GivenAccounts.txt"
            clearpage()
            global dynamic_text_frame #initalize dynamic text frame
            dynamic_text_frame = Text(gui_mainframe, height=5,wrap="word")
            editStoredAccounts() #create files
            dynamic_text_frame.grid(column=1,row=7,sticky=W)
            dynamic_text_frame.tag_config("red_text", foreground="red")
            dynamic_text_frame.insert(index=END,chars="This is human readable! Keeping any password like this for your website is extremely insecure! Check out one of the hashes to start securing those passwords!")
            text_frame.config(height=13)
            text_frame.insert(index=END,chars="Hashing is taking data and running an algorithm that jumbles the data into a certain character length. This process creates something called a digest and can’t be undone. But we can compare hashes to see if what we have stored matches what was input.\n")
            text_frame.insert(index=END,chars="\nOn your desktop, there should now be a text file called ‘GivenAccounts.txt’ which we will use as our account login data. This file has usernames and passwords for all the accounts for a fake company’s website. We will use this file for real life practice of cryptography\n")
            text_frame.insert(index=END,chars="\nStart hashing with the interface below! See all the different hashes you could use with the click of the button. Once you have decided which hash to use, just click the ‘Hash File’ button and go check out the file!")
            #create interactive buttons for user to preview hashes and hash file
            ttk.Button(iteractive_frame,text="Plaintext", command=lambda: hashingfile("plaintext")).grid(column=0,row=0, sticky=W)
            ttk.Button(iteractive_frame,text="SHA1", command=lambda: hashingfile("SHA1")).grid(column=0,row=1, sticky=W)
            ttk.Button(iteractive_frame,text="SHA256",command=lambda: hashingfile("SHA256")).grid(column=0,row=2, sticky=W)
            ttk.Button(iteractive_frame, text="Blake2",command=lambda: hashingfile("Blake2")).grid(column=0,row=3,sticky=W)
            ttk.Button(iteractive_frame, text="Hash File",command=lambda: editStoredAccounts(action=True)).grid(column=0,row=4,sticky=W)
            message_list() #create initail preview of hashes [no hash algorithm used - plaintext/normal]
            NextPage.config(command=lambda: pagemovement(3)) #update Next Page button for another page turn
        case 3: #hashing -> password matching
            clearpage()
            dynamic_text_frame.destroy()
            text_frame.config(height=16)
            text_frame.insert(index=END,chars="Now that we have the file hashed, let’s use the digests for logins and account creation!\n")
            text_frame.insert(index=END,chars="\nSince we already know what algorithm we use to store passwords, any new password will just automatically be hashed when uploaded to the accounts file. This will allow us to quickly create new accounts. Try making one yourself!\n")
            text_frame.insert(index=END,chars="\nFor logins, we will use the hashing algorithm to create a digest from the password from the login form. With this digest, the program will search through the file to see if any digest matches the one given. If so, it will remember which row it was found and see if the given username matches the stored one. If so, then the login is successful.\n")
            text_frame.insert(index=END,chars="\nIf any of these parts fail, like there is no matching digest or the usernames don’t match, then the login will fail. Try logging in and see the steps play out!")
            NextPage.config(command=lambda: pagemovement(4))
            ttk.Label(iteractive_frame,text="Create Account").grid(column=0,row=0)
            ttk.Button(iteractive_frame,text="Submit",command=AddAccount).grid(column=0,row=5)
            ttk.Label(iteractive_frame,text="Login Portal").grid(column=2,row=0)
            ttk.Button(iteractive_frame,text="Login", command=LoginFunc).grid(column=2,row=3)
            global warning_text #below label is dynamic when trying to submit new account!!
            warning_text = ttk.Label(iteractive_frame, text=" ")
            warning_text.grid(column=0,row=6,sticky=(N,W))
            global input_username #creating global calls
            global input_password
            global validate_password
            global login_username
            global login_password
            input_username=  ttk.Entry(iteractive_frame) #creating input fields
            input_password= ttk.Entry(iteractive_frame) #create
            validate_password= ttk.Entry(iteractive_frame) #create
            login_username= ttk.Entry(iteractive_frame) #login
            login_password= ttk.Entry(iteractive_frame) #login
            input_password.grid(column=0, row=2, sticky=W) #graphing input fields
            validate_password.grid(column=0,row=3, sticky=W)
            input_username.grid(column=0,row=1, sticky=W)
            login_username.grid(column=2, row=1, sticky=W) #login
            login_password.grid(column=2, row=2, sticky=W)
            input_username.insert(0, "Enter username...") #handling placeholder text: username
            input_username.config(style="Placeholder.TEntry")
            input_username.bind("<FocusOut>", lambda event:handle_focus("Out",input_username,"Enter username..."))
            input_username.bind("<FocusIn>",lambda event:handle_focus("In",input_username))
            input_password.insert(0, "Enter password...") #handling placeholder text: password
            input_password.config(style="Placeholder.TEntry")
            input_password.bind("<FocusOut>", lambda event:handle_focus("Out",input_password,"Enter password...")) #handling placeholder text: password
            input_password.bind("<FocusIn>",lambda event:handle_focus("In",input_password))
            validate_password.insert(0, "Re-enter password...")
            validate_password.config(style="Placeholder.TEntry")
            validate_password.bind("<FocusOut>", lambda event:handle_focus("Out",validate_password,"Re-enter password..." ))
            validate_password.bind("<FocusIn>",lambda event:handle_focus("In",validate_password))
            login_username.insert(0, "Enter username...") #handling placeholder text: username for login
            login_username.config(style="Placeholder.TEntry")
            login_username.bind("<FocusOut>",lambda event:handle_focus("Out",login_username,"Enter username..."))
            login_username.bind("<FocusIn>",lambda event:handle_focus("In",login_username))
            login_password.insert(0, "Enter password...") #handling placeholder text: password for login
            login_password.config(style="Placeholder.TEntry")
            login_password.bind("<FocusOut>", lambda event:handle_focus("Out",login_password,"Enter password..."))
            login_password.bind("<FocusIn>",lambda event:handle_focus("In",login_password))
        case 4: #password matching -> key creation
            clearpage()
            text_frame.config(height=23)
            text_frame.insert(index=END,chars="Now that we hashed the passwords, we can secure the file even more with encryption. This makes not a single portion of the file unreadable, but the whole file itself using something called a key. Without this key, you can’t decrypt the file and be able to read it. There are two types of encryption methods: symmetric and asymmetric.\n")
            text_frame.insert(index=END,chars="\nSymmetric encryption is using a single key for encrypting and decrypting. This type of encryption can also be called single key encryption. The most common type of symmetric key system is called AES.\n")
            text_frame.insert(index=END,chars="\nAsymmetric encryption has two separate keys, called a key pair, for encrypting and decrypting. The encrypting key is called the public key while the decrypting key is the private key. This type of encryption can also be called public key encryption. The most common type of symmetric key system is called RSA.\n")
            text_frame.insert(index=END,chars="\nFor our example, we’ll create a symmetric key called ‘SharedKey’ that will be stored on your desktop. Do this by clicking the ‘Create Key’ button.\n")
            text_frame.insert(index=END,chars="\nOnce you have created the key, we’ll then encrypt the accounts files with the ‘Encrypt File’ button. You will then see that the accounts file is a lot shorter and incoherent. Now no one without the key will be able to understand the file!\n")
            text_frame.insert(index=END,chars="\nIf you want to decrypt the file just click the ‘Decrypt File’ button do due so.")
            NextPage.config(command=lambda: pagemovement(5))
            ttk.Button(iteractive_frame,text="Create Key",command=write_key).grid(column=0,row=0)
            if new_desktop_path.exists:
                account_path = new_file_path
            else:
                account_path = password_path
            ttk.Button(iteractive_frame,text="Encrypt File",command=lambda: encrypt_file(account_path)).grid(column=0,row=1)
            ttk.Button(iteractive_frame,text="Decrypt File", command=lambda: decrypt_file(account_path)).grid(column=0,row=2)
            #key creation goes here with a label popup about the file created
        case 5: #key creation -> key management
            clearpage()
            text_frame.config(height=18)
            text_frame.insert(index=END,chars="Now we need to manage our key so it’s not so easy for anyone to grab it. Most organizations do with by moving their keys into a separate hard drive that is then physically secure. Or these keys are kept on an extremely secure computer that requires anyone needing these keys to authenticate themselves and log all their actions.\n")
            text_frame.insert(index=END,chars="\nFor our example, we’ll only move the key file into a different directory than the desktop. You can either manually move the folder off the desktop or click the ‘Move Key’ button to move it into your downloads directory.\n")
            text_frame.insert(index=END,chars="\nOnce you move the key file, try decrypting the accounts file once more. But the preview next to the interface does not change and you get an error!\n")
            text_frame.insert(index=END,chars="\nIf you manuallymove the key file back to the desktop directory you should then be able to decrypt the file and read the account information again.\n")
            text_frame.insert(index=END,chars="\nRemember, know where your key is stored if you ever want to decrypt any of your data again. And make sure where you store it is as secure as you can get it!")
            NextPage.config(command=lambda: pagemovement(6))
            if new_desktop_path.exists:
                account_path = new_file_path
            else:
                account_path = password_path
            global dynamic_label
            dynamic_label = dynamic_label = ttk.Label(dynamic_frame,text=" ")
            dynamic_label.grid(column=0,row=1)
            ttk.Button(iteractive_frame,text="Encrypt File",command=lambda: encrypt_file(account_path)).grid(column=0,row=1)
            ttk.Button(iteractive_frame,text="Decrypt File", command=lambda: decrypt_file(account_path)).grid(column=0,row=2)
            ttk.Button(iteractive_frame,text="Move key", command=lambda: move_key()).grid(column=0,row=3)
            #actually read first 3 lines of file. Have user move key to another directory. Then preview it again, with it showing only encryption
        case 6: #key management -> recap & expand
            clearpage()
            text_frame.insert(index=END,chars="As you can see, cryptography is a very important section and tool in cybersecurity.\n")
            text_frame.insert(index=END,chars="\nHashing allows us to quickly make data unreadable to the human eye yet still be able to use the data by comparing the stored digests and the digest created from input.\n")
            text_frame.insert(index=END,chars="\nThis program showed these concepts with a simple login feature using a text file that would typically be a database in real-world applications.\n")
            text_frame.insert(index=END,chars="\nNext, we secured our text file full of account information with encryption. This made sure that even if someone gets the file, they won’t be able to understand any of it due to not having access to the key.\n")
            text_frame.insert(index=END,chars="\nI hope this program helped you understand different cryptography techniques and what could be used in real-world applications!")
            NextPage.destroy()
#create GUI foundations
gui_root = Tk()
styles = ttk.Style()
gui_root.title("Layered Cryptography Lab")
gui_root.geometry("1000x500")
styles.configure("Placeholder.TEntry",foreground="grey")
gui_mainframe = ttk.Frame(gui_root, padding=(3,3,12,12))
gui_mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
#create frames to segment different areas of GUI
text_frame = Text(gui_mainframe, height=12, wrap="word")
text_frame.insert(index=END,chars=f"This program, Layered Cryptography, is designed to give hands-on experience with a computer lab focused on basic cryptography concepts and methods. There is a supplemented presentation with this lab for more context but is not required.\n")
text_frame.insert(index=END, chars=f"\nThis program will create 2 files on your computer:\n")
text_frame.insert(index=END,chars=f"     • ‘GivenAccounts.txt’ which is a text file that will be created and stored in your desktop directory.\n")
text_frame.insert(index=END, chars=f"    • ‘SharedKey.key’ which is a key file that will be created in your desktop directory but later moved into your downloads directory.\n")
text_frame.insert(index=END, chars=f"\nBy continuing to the next page, you understand that these files will be created and used by this program.")
text_frame.grid(column=0,row=0,columnspan=3)
dynamic_frame = ttk.Frame(gui_mainframe,borderwidth=2)
dynamic_frame.grid(column=1,row=1,sticky=(N,S,W),columnspan=2)
iteractive_frame = ttk.Frame(gui_mainframe, borderwidth=2)
iteractive_frame.grid(column=0,row=1, sticky=(N,S,W))
navigate_frame = ttk.Frame(gui_mainframe,borderwidth=2)
navigate_frame.grid(column=0,row=8,columnspan=3)
#create inital button to move through 'pages'
NextPage = ttk.Button(navigate_frame,text="Next Page",command=lambda: pagemovement(1))
NextPage.grid(column=2,row=0,sticky=E)
#create a dynamic list of the first 5 passwords in 'GivenPasswords.txt' file
def message_list ():
    row_value = 0
    for widget in dynamic_frame.winfo_children():
        widget.destroy()
    for i in range(len(messages)):
        row_value = row_value+1
        formatted_entry = " | ".join(str(info) for info in messages[i])
        iLabel = Label(dynamic_frame, text= formatted_entry)
        iLabel.grid(row = row_value, column=0, sticky=W)
#run GUI
gui_root.mainloop()
