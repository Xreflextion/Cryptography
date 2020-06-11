from tkinter import *
from tkinter import filedialog, scrolledtext
import os
import traceback
import cipher_functions
from typing import TextIO, List


# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(Frame):
    """A GUI frame with a scrollbar"""

    # Credit for this class is given to
    # https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    # with some modifications

    def __init__(self, parent: Frame) -> None:
        """Initialize a frame with a scrollbar"""

        super().__init__(parent)  # create a frame (self)

        self.canvas = Canvas(self, borderwidth=0)  # place canvas on self
        self.viewPort = Frame(self.canvas)  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = Scrollbar(self, orient="vertical",
                             command=self.canvas.yview)  # place a scrollbar on self
        self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vsb.set,
                              xscrollcommand=self.hsb.set)  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.hsb.pack(side="bottom", fill="x")  # pack scrollbar to bottom of self
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4),
                                                       window=self.viewPort,
                                                       anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.on_frame_configure)
        # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        # perform an initial stretch on render, otherwise the scroll region has
        # a tiny border until the first resize
        self.on_frame_configure(None)

    def on_frame_configure(self, event) -> None:
        """Reset the scroll region to encompass the inner frame"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event) -> None:
        """Reset the canvas window to encompass inner frame when required"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# ************************
# CipherApp Class
# ************************
class CipherApp(Frame):
    """A GUI of the Cipher application"""

    def __init__(self, root: Frame) -> None:
        """Initiate the Cipher App along with its gadgets"""

        root.title("Cryptography")
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        w, h = ws * 0.5, hs * 0.75
        self.w, self.h = w, h
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        # set the dimensions of the screen and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master = root

        Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)  # add a new scrollable frame.

        self.create_screen_components()

        # pack scrollFrame itself
        self.scrollFrame.pack(side="top", fill="both", expand=True, padx=(5, 0),
                              pady=(5, 0))

    def create_screen_components(self) -> None:
        """Create the components of the app screen including text, text boxes,
        buttons, ..."""

        # Put things in rows to organize gadgets.
        r = 0

        # Empty label for a bit of a top margin
        Label(self.scrollFrame.viewPort, text='').grid(row=r, column=0, sticky=W)
        r += 1

        # select a file Label
        Label(self.scrollFrame.viewPort,
              text='Instructions'
                   '\n1. Select a deck to use'
                   '\n2. Either select a file to process or type in the Input box below'
                   '\n3. Encrypt or decrypt',
              justify=LEFT,
              font="Arial 14").grid(row=r, column=0, sticky=W)
        r += 1

        # Empty label
        Label(self.scrollFrame.viewPort, text='').grid(row=r, column=0, sticky=W)
        r += 1

        # Deck box input
        self.deck_box = Text(self.scrollFrame.viewPort, width=int(self.w / 10),
                             height=1, fg='gray')
        self.deck_box.insert('1.0', 'select a deck to use')
        self.deck_box.config(state=DISABLED)
        self.deck_box.grid(row=r, column=0, sticky=W)

        # Deck button
        Button(self.scrollFrame.viewPort, text="Select a deck", width=int(self.w / 80),
               command=lambda: self.open_deck()).grid(row=r, column=1, sticky=W)
        r += 1

        # File box input
        self.file_box = Text(self.scrollFrame.viewPort, width=int(self.w / 10),
                             height=1, fg='gray')
        self.file_box.insert('1.0', 'select file to process')
        self.file_box.config(state=DISABLED)
        self.file_box.grid(row=r, column=0, sticky=W)

        # File button
        Button(self.scrollFrame.viewPort, text="Select a file", width=int(self.w / 80),
               command=lambda: self.open_file()).grid(row=r, column=1, sticky=W)
        r += 1

        # Empty label
        Label(self.scrollFrame.viewPort, text='').grid(row=r, column=0,
                                                       sticky=W)
        r += 1

        # Input label
        Label(self.scrollFrame.viewPort, text='Input').grid(row=r, column=0,
                                                            sticky=W)
        r += 1

        # Text box input
        self.text_input = scrolledtext.ScrolledText(self.scrollFrame.viewPort,
                                                    width=int(self.w / 10), height=int(self.h / 100))
        self.text_input.insert('1.0', 'insert text to process or load a file')
        self.text_input.grid(row=r, column=0, sticky=W, rowspan=3)

        # Encrypt button
        Button(self.scrollFrame.viewPort, text="Encrypt", width=int(self.w / 80),
               height=2, command=lambda: self.encoding(cipher_functions.ENCRYPT)). \
            grid(row=r, column=1, sticky=W + N)
        r += 2

        # Decrypt button
        Button(self.scrollFrame.viewPort, text="Decrypt", width=int(self.w / 80),
               height=2, command=lambda: self.encoding(cipher_functions.DECRYPT)). \
            grid(row=r, column=1, sticky=W + S)
        r += 1

        # Empty label
        Label(self.scrollFrame.viewPort, text='').grid(row=r, column=0, sticky=W)
        r += 1

        # Output label
        Label(self.scrollFrame.viewPort, text='Output').grid(row=r, column=0,
                                                             sticky=W)
        r += 1

        # Text box Output
        self.text_output = scrolledtext.ScrolledText(self.scrollFrame.viewPort,
                                                     width=int(self.w / 10), height=int(self.h / 100))
        self.text_output.insert('1.0', 'processed text will show here')
        self.text_output.config(state=DISABLED)
        self.text_output.grid(row=r, column=0, sticky=W, rowspan=3)
        r += 3

        # Empty label
        Label(self.scrollFrame.viewPort, text='').grid(row=r, column=0, sticky=W)
        r += 1

        # Message label
        Label(self.scrollFrame.viewPort, text='Messages from the program will '
                                              'show here').grid(row=r, column=0, sticky=W)
        r += 1

        self.error_massage = Label(self.scrollFrame.viewPort, fg='red',
                                   anchor=W, justify=LEFT)
        self.error_massage.grid(row=r, column=0, columnspan=1, sticky=W)

        # Quit
        Button(self.scrollFrame.viewPort, text="QUIT", fg="red", width=int(self.w / 80),
               height=3, command=lambda: self.master.destroy()).grid(row=r,
                                                                     column=1, sticky=W)

        self.scrollFrame.columnconfigure(0, weight=0)

    def open_file(self) -> None:
        """Prompt the user to select a file to process"""

        name = filedialog.askopenfilename(
            filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
            title="Choose a file.")

        # If a file is selected, check its validity
        if name.strip():
            try:
                f = open(name)
                self.text_input.config(fg='black')
                self.text_input.delete('1.0', END)
                self.text_input.insert('1.0', f.readlines())
                f.close()

                # Display the file name in the file box
                self.update_box(self.file_box, name)

            except:
                self.error_massage.config(fg='red')
                self.error_massage['text'] = "The selected file cannot be opened"

    def open_deck(self) -> None:
        """Prompt the user to select a deck used to process"""

        name = filedialog.askopenfilename(
            filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
            title="Choose a file.")
        self.deck_file = name

        # Display the deck name in the file box
        self.update_box(self.deck_box, name)

    def encoding(self, mode: str) -> None:
        """Perform the encryption using the deck from the attribute deck_file and
        the message from the input file_box. If MODE is 'e', the process is
        encryption; otherwise, decryption"""

        # Check if the user has entered a text or laoded a file
        if self.text_input.get("1.0", 'end').strip() == "insert text to process " \
                                                        "or load a file":
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "Insert text to process or load a file"
            return

        # Check if the user provided a file for the deck
        try:
            deck_file = open(self.deck_file, 'r')
        except:
            self.update_box(self.text_output, "")
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "No card deck was provided or the " \
                                         "supplied deck file cannot be opened"
            return

        # Check the provided deck
        try:
            deck = read_deck(deck_file)
            deck_file.close()

        # If an error occurs, display an error message at the bottom of the
        # window and print the the traceback error in the shell
        except:
            self.update_box(self.text_output, "")
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "The supplied deck file is not a valid " \
                                         "one or something went wrong when the " \
                                         "deck file was processed\n\nCheck the " \
                                         "shell for more info." \
                                         "\n\nIf you you think you have fixed " \
                                         "the coding issue, restart the app."
            traceback.print_exc()
            return

        if not cipher_functions.is_valid_deck(deck):
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "The supplied card deck is not valid"
            return

        # Put the text from the input box into a temp file to process it
        f = open('temp.txt', 'w+')
        f.write(self.text_input.get("1.0", 'end-1c'))
        f.close()
        f = open('temp.txt')
        messages = read_messages(f)
        f.close()
        os.remove('temp.txt')

        # Start the process of encoding
        try:
            coded_messages = '\n'.join(
                cipher_functions.process_messages(deck, messages, mode)).rstrip()

            # Update the output box
            self.update_box(self.text_output, coded_messages)

            # Indicate that the process has been completed
            self.error_massage.config(fg='blue')
            process = "Encryption"
            if mode == cipher_functions.DECRYPT:
                process = "Decryption"
            self.error_massage['text'] = process + " was succeful!"

        except:
            self.update_box(self.text_output, "")
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "Something went wrong with the process." \
                                         "\n\nQuick this program then check the Python shell for more info." \
                                         "\n\nIf you you think you have fixed " \
                                         "the issue, restart the app."
            traceback.print_exc()

    def update_box(self, box: scrolledtext.ScrolledText, message: str) -> None:
        """Clear the output box in the app and put the provided message inside"""

        box.config(state=NORMAL)
        box.delete('1.0', END)
        box.insert('1.0', message)
        box.config(state=DISABLED)


def read_messages(message_file: TextIO) -> List[str]:
    """Read and return the list of messages from file message_file."""
    messages = []

    for line in message_file:
        messages.append(line.strip())

    return messages


def read_deck(deck_file: TextIO) -> List[int]:
    """Read and return a deck of cards from open file deck_file."""
    deck = []

    for line in deck_file:
        for value in line.strip().split():
            deck.append(int(value))

    return deck


if __name__ == "__main__":
    root = Tk()
    CipherApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
