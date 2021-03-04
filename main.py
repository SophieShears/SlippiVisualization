from tkinter import *

from loadDF import get_df, get_opp_df
from plot import plot_char_freq, plot_wl_by_char, plot_overall_wl


# Main window
window = Tk()

# Window Title
window.title('Slippi Visualization')

# Set display dimensions
window.geometry("300x300")

# Set icon of window
pic = PhotoImage(file='icon.png')
window.iconphoto(False, pic)


# Create dataframe or load existing csv as dataframe
df = get_df()

# Get a list of all opponents by most frequent
all_opp = df.opp_name.value_counts()
opp_list = all_opp.index.tolist()


# Create drop down opponent selector
opponent = StringVar()
opponent.set(opp_list[0])
drop = OptionMenu(window, opponent, *opp_list)

# Create buttons to display plot
overall_char_freq_button = Button(master=window,
                                  command=(lambda: plot_char_freq(df)),
                                  height=2,
                                  width=35,
                                  text='Overall Opponent Character Frequency')

opp_char_freq_button = Button(master=window,
                              command=(lambda: plot_char_freq(get_opp_df(df, opponent.get()), opponent.get())),
                              height=2,
                              width=35,
                              text='Selected Opponent Character Frequency')

overall_wl_char_button = Button(master=window,
                                command=(lambda: plot_wl_by_char(df)),
                                height=2,
                                width=35,
                                text='Overall Win/Loss by Character')

opp_wl_char_button = Button(master=window,
                            command=(lambda: plot_wl_by_char(get_opp_df(df, opponent.get()), opponent.get())),
                            height=2,
                            width=35,
                            text='VS Opponent W/L by Character')

overall_wl_tot_button = Button(master=window,
                               command=(lambda: plot_overall_wl(df)),
                               height=2,
                               width=35,
                               text='Overall Win/Loss')

opp_wl_tot_button = Button(master=window,
                           command=(lambda: plot_overall_wl(get_opp_df(df, opponent.get()), opponent.get())),
                           height=2,
                           width=35,
                           text='VS Opponent Win/Loss')


# Place buttons/drop down on window
overall_char_freq_button.pack()
overall_wl_char_button.pack()
overall_wl_tot_button.pack()

drop.pack()

opp_char_freq_button.pack()
opp_wl_char_button.pack()
opp_wl_tot_button.pack()


# run gui
window.mainloop()
