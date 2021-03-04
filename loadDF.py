from tkinter import filedialog, messagebox
import pandas as pd

from createDF import get_slp_files, data_to_df, create_columns


# Get all usernames
def get_names():
    with open(filedialog.askopenfilename(title='Select names txt file'), 'r') as read_file:
        names = read_file.readlines()
    names = [names[i].rstrip() for i in range(len(names))]
    return names


# Create a new dataframe instance
def create_new_df(slp_folder):
    slp_files = get_slp_files(slp_folder)
    dataframe = data_to_df(slp_files, slp_folder)
    create_columns(dataframe, get_names())
    dataframe.to_csv(slp_folder + '//' + 'out.csv')
    dataframe = pd.read_csv(slp_folder + '//' + 'out.csv')
    return dataframe


# Creates a new dataframe or loads and old one based on user response
def get_df():
    # Set Replay Folder
    slp_folder = filedialog.askdirectory(title='Select Replay Folder')

    # Ask if user would like to analyse new data or use old data
    new_df = messagebox.askyesno('Create New Data?', 'Would you like to analyze new data (Y), '
                                                     'or use existing data (N)? '
                                                     'If never ran before click: Yes. May take a while.')

    if not new_df:
        # Try to use existing csv dataframe if possible if not create one
        try:
            dataframe = pd.read_csv(slp_folder + '//' + 'out.csv')
            return dataframe
        except FileNotFoundError:
            print('Existing csv file not found, creating new one.')
            return create_new_df(slp_folder)

    else:
        # Create new dataframe on request
        return create_new_df(slp_folder)


# Get a mask of the data frame with only games by a specific opponent
def get_opp_df(dataframe, opponent_name):
    df_mask = (dataframe['opp_name'] == opponent_name)
    df_opp = dataframe.loc[df_mask]

    return df_opp
