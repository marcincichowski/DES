from tkinter import messagebox
import utils
from tkinter import *
import locale
import DES_encryption
class Window:
    def __init__(self, master):
        locale.setlocale(locale.LC_NUMERIC, "pl_PL")
        # rozdzielczość okna i lokalizacja początkowa okna
        self.master = master
        self.master.geometry('500x200+0+0')
        # nagłówek okna
        master.title("Szyfrowanie DES")
        data_label = Label(master, text="Klucz szyfrujący").grid(row=0, column=0)
        key_label = Label(master, text="Informacja").grid(row=1, column=0)
        self.data = Entry(master)
        self.data.grid(row=0, column=1)

        self.key = Entry(master)
        self.key.grid(row=1, column=1)
        button_encrypt = Button(master, text='Zaszyfruj', command=lambda: self.callback_encrypt())
        button_encrypt.grid(row=3, column=1)

        data_decrypted = Label(master, text="Informacja zaszyfrowana").grid(row=0, column=3)
        self.decrypted_input = Entry(master)
        self.decrypted_input.grid(row=0, column=4)

        button_decrypt = Button(master, text='Deszyfruj', command=lambda: self.callback_decrypt())
        button_decrypt.grid(row=1, column=4)

    def callback_encrypt(self):
        if not self.key.get() or not self.data.get():
            print('error inputs')
            return messagebox.showinfo('Błąd!', 'Wprowadź dane!')
        else:
            key_to_encrypt = utils.hex2bin(self.key.get())  # get from input
            key_to_encrypt = utils.permute(key_to_encrypt, utils.keyp, 56)
            left = key_to_encrypt[0:28]
            right = key_to_encrypt[28:56]
            rkb = []
            rk = []
            for i in range(0, 16):
                left = utils.shift_left(left, utils.shift_table[i])
                right = utils.shift_left(right, utils.shift_table[i])
                combine_str = left + right
                round_key = utils.permute(combine_str, utils.key_comp, 48)
                rkb.append(round_key)
                rk.append(utils.bin2hex(round_key))
            cipher_text = utils.bin2hex(DES_encryption.encrypt(self.data.get(), rkb, rk))
            self.decrypted_input.delete(0, END)
            self.decrypted_input.insert(0, cipher_text)

    def callback_decrypt(self):
        if (not self.key.get() or not self.decrypted_input.get()):
            print('error inputs')
            return messagebox.showinfo('Błąd!', 'Wprowadź dane!')
        else:
            key_to_decrypt = utils.hex2bin(self.key.get())  # get from input
            key_to_decrypt = utils.permute(key_to_decrypt, utils.keyp, 56)
            left = key_to_decrypt[0:28]
            right = key_to_decrypt[28:56]
            rkb = []
            rk = []
            for i in range(0, 16):
                left = utils.shift_left(left, utils.shift_table[i])
                right = utils.shift_left(right, utils.shift_table[i])
                combine_str = left + right
                round_key = utils.permute(combine_str, utils.key_comp, 48)
                rkb.append(round_key)
                rk.append(utils.bin2hex(round_key))
            rkb_rev = rkb[::-1]
            rk_rev = rk[::-1]
            decoded_cipher = utils.bin2hex(DES_encryption.encrypt(self.decrypted_input.get(), rkb_rev, rk_rev))
            self.data.delete(0, END)
            self.data.insert(END, decoded_cipher)

root = Tk()
root.minsize('500', '200')
my_gui = Window(root)
root.mainloop()
