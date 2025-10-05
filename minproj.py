import tkinter as tk
from tkinter import messagebox
import random

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        result.append('0' if a[i] == b[i] else '1')
    return ''.join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)
    return tmp

def encodeData(data, key):
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword, remainder

def decodeData(codeword, key):
    remainder = mod2div(codeword, key)
    return '0' * (len(key) - 1) == remainder

def validate_binary_string(s):
    return all(ch in '01' for ch in s) and len(s) > 0

def on_encode():
    data = data_entry.get().strip()
    key = key_entry.get().strip()

    if not (validate_binary_string(data) and validate_binary_string(key)):
        messagebox.showerror("Invalid Input", "Please enter valid binary strings (0 and 1 only).")
        return

    if len(key) < 2 or key[0] != '1':
        messagebox.showerror("Invalid Polynomial", "Generator polynomial must start with 1 and be at least length 2.")
        return

    codeword, remainder = encodeData(data, key)
    encoded_var.set(codeword)
    remainder_var.set(remainder)
    detect_var.set("")
    corrupted_var.set("")
    corrupted_detect_var.set("")

def on_check():
    codeword = encoded_var.get().strip()
    key = key_entry.get().strip()

    if not (validate_binary_string(codeword) and validate_binary_string(key)):
        messagebox.showerror("Invalid Input", "Please encode valid data first.")
        return

    if decodeData(codeword, key):
        detect_var.set("✅ No error detected in received data.")
    else:
        detect_var.set("❌ Error detected in received data.")

def on_simulate_error():
    codeword = encoded_var.get().strip()
    key = key_entry.get().strip()

    if not codeword:
        messagebox.showerror("No Data", "Please encode data before simulating error.")
        return

    # Flip a random bit
    pos = random.randint(0, len(codeword)-1)
    corrupted_codeword = (
        codeword[:pos] +
        ('1' if codeword[pos] == '0' else '0') +
        codeword[pos+1:]
    )

    corrupted_var.set(corrupted_codeword)

    if decodeData(corrupted_codeword, key):
        error_detect = "⚠️ No error detected in corrupted data."
    else:
        error_detect = "❌ Error detected in corrupted data."

    corrupted_detect_var.set(error_detect)

# GUI setup
root = tk.Tk()
root.title("CRC Error Detection")

tk.Label(root, text="Data bits (binary):").grid(row=0, column=0, sticky="e")
data_entry = tk.Entry(root, width=40)
data_entry.grid(row=0, column=1, columnspan=3)

tk.Label(root, text="Generator polynomial:").grid(row=1, column=0, sticky="e")
key_entry = tk.Entry(root, width=40)
key_entry.grid(row=1, column=1, columnspan=3)

encode_btn = tk.Button(root, text="Encode Data", command=on_encode)
encode_btn.grid(row=2, column=1)

check_btn = tk.Button(root, text="Check for Errors", command=on_check)
check_btn.grid(row=2, column=2)

simulate_btn = tk.Button(root, text="Simulate Error", command=on_simulate_error)
simulate_btn.grid(row=2, column=3)

tk.Label(root, text="Encoded Data (data + CRC):").grid(row=3, column=0, sticky="e")
encoded_var = tk.StringVar()
encoded_entry = tk.Entry(root, textvariable=encoded_var, width=50)
encoded_entry.grid(row=3, column=1, columnspan=3)

tk.Label(root, text="CRC Remainder:").grid(row=4, column=0, sticky="e")
remainder_var = tk.StringVar()
remainder_entry = tk.Entry(root, textvariable=remainder_var, width=50, state="readonly")
remainder_entry.grid(row=4, column=1, columnspan=3)

detect_var = tk.StringVar()
tk.Label(root, textvariable=detect_var, fg="blue", font=("Arial", 12)).grid(row=5, column=0, columnspan=4)

tk.Label(root, text="Corrupted Codeword:").grid(row=6, column=0, sticky="e")
corrupted_var = tk.StringVar()
corrupted_entry = tk.Entry(root, textvariable=corrupted_var, width=50, state="readonly")
corrupted_entry.grid(row=6, column=1, columnspan=3)

corrupted_detect_var = tk.StringVar()
tk.Label(root, textvariable=corrupted_detect_var, fg="red", font=("Arial", 12)).grid(row=7, column=0, columnspan=4)

exit_btn = tk.Button(root, text="Exit", command=root.quit, bg="lightgray")
exit_btn.grid(row=8, column=3, pady=10)

root.mainloop()
