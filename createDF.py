import numpy as np
import pandas as pd
import os
import slippi as slp


# Get all file names in specified Slippi Replay folder
def get_slp_files(folder_path):
    return [path for path in os.listdir(folder_path)]


# Get metadata from every file and return data frame
def data_to_df(files, folder):
    # Initialize lists for all relevant data, used to make the data frame
    game_id, date, duration, p1_char, p1_name, p2_char, p2_name, p3_char, p3_name, p4_char, p4_name, \
        stage, result, winner = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for file in files:
        # Try to load it as a slp file unless it's an unrecognized file type
        print(f"Trying to open {file}")
        try:
            game = slp.Game(os.path.join(folder, file))
        except:
            print("Skipping invalid slp file...")
            continue

        # Get game file ID
        game_id.append(file)
        # Get date played
        date.append(game.metadata.date)
        # Get game time (in frames)
        duration.append(game.metadata.duration)

        # Get a list of used ports
        ports = []
        players = game.start.players
        for port in players:
            if port == None:
                ports.append(None)
            elif players.index(port) not in ports:
                ports.append(players.index(port))
            elif players.index(port) in ports:  # If same character, same color
                ports.append(players.index(port) + 1)

        # Get a list of characters per port
        characters = [game.start.players[port].character.name if port != None
                      else port for port in ports]
        p1_char.append(characters[0])
        p2_char.append(characters[1])
        p3_char.append(characters[2])
        p4_char.append(characters[3])

        # Get netplay names if it was a netplay game
        try:
            names = [game.metadata.players[port].netplay.name if port != None
                     else port for port in ports]
            p1_name.append(names[0])
            p2_name.append(names[1])
            p3_name.append(names[2])
            p4_name.append(names[3])

        except AttributeError:
            print('Not a netplay game.')
            names = []
            p1_name.append(None)
            p2_name.append(None)
            p3_name.append(None)
            p4_name.append(None)

        # Get stage played on
        stage.append(game.start.stage.name)

        # Get game result if the game ended, doesn't support teams
        if not game.end:
            result.append(None)
            winner.append(None)
        else:
            result.append(game.end.method.name)

            # Determine which player(s) won the game, if any
            winning_ports = []
            # Check to see if an actual game longer than 20 sec was played
            if int(game.metadata.duration) <= 1200:
                winning_ports.append(None)
            else:
                # Get var of how game ended then calc who won
                game_result = game.end.method.name

                # If game ended in a tie no winner
                if game_result == 'INCONCLUSIVE':
                    winning_ports.append(None)

                # If someone LRAS'd the other players win
                elif game_result == 'NO_CONTEST':
                    if game.end.lras_initiator == None:
                        winning_ports.append(None)
                    else:
                        for port in ports:  # Each port who didn't LRAS wins
                            if port != game.end.lras_initiator and port != None:
                                winning_ports.append(port)

                # If game goes to time player with the most stocks and lower percent wins
                elif game_result == 'TIME':
                    stock_percent = [0, 0]
                    win_port = None

                    for port in ports:
                        if port != None:
                            # Check last frame to see winner,
                            # port who has the most stocks or is tied and has lowest percent
                            stocks = game.frames[-1].ports[port].leader.post.stocks
                            percent = game.frames[-1].ports[port].leader.post.damage

                            # If port has the best stocks and percent combo keep track of all three
                            if stocks > stock_percent[0] or (stocks == stock_percent[1] and percent < stock_percent[1]):
                                stock_percent[0] = stocks
                                stock_percent[1] = percent
                                win_port = port

                    # Add winning port, with highest stocks lowest percent to list
                    winning_ports.append(win_port)

                # For all games won by one or more players check who won by who has stocks at the end
                elif game_result == 'GAME' or result[file] == 'CONCLUSIVE':
                    for port in ports:
                        if port != None:
                            stocks = game.frames[-1].ports[port].leader.post.stocks
                            if stocks != 0:
                                winning_ports.append(port)

            # If the game somehow didn't have official end, the winner is None
            if len(winning_ports) == 0:
                winning_ports.append(None)

            # Convert ports of winners to winners names
            if names:
                for idx, port in enumerate(winning_ports):
                    if port != None:
                        winning_ports[idx] = names[port]

            # Get game winners, if any
            winner.append(winning_ports[0])

    # Return all lists as data frame
    return pd.DataFrame(data={
        'game_id': game_id,
        'date': date,
        'duration': duration,
        'p1_char': p1_char,
        'p1_name': p1_name,
        'p2_char': p2_char,
        'p2_name': p2_name,
        'p3_char': p3_char,
        'p3_name': p3_name,
        'p4_char': p4_char,
        'p4_name': p4_name,
        'stage': stage,
        'result': result,
        'winner': winner
    })


# Turn all instances of Wolf from '0' to 'WOLF'
def clean_wolf(dataframe):
    dataframe['p1_char'] = dataframe['p1_char'].str.replace('MASTER_HAND', 'WOLF')
    dataframe['p2_char'] = dataframe['p2_char'].str.replace('MASTER_HAND', 'WOLF')


# Remove all instances of neither player having a netplay name
def clean_nonames(dataframe):
    dataframe.drop(dataframe[dataframe['p1_name'].isnull()].index, inplace=True)
    dataframe.drop(dataframe[dataframe['p2_name'].isnull()].index, inplace=True)


# Create columns tracking your character and opponent's name/character, as well as win/loss
def create_columns(dataframe, names):

    # Change Master Hand values to Wolf
    clean_wolf(dataframe)

    # Create column for opponent name
    conditions = [
        (dataframe['p1_name'].isin(names)),
        (dataframe['p2_name'].isin(names)),
    ]
    values = [dataframe['p2_name'], dataframe['p1_name']]
    dataframe['opp_name'] = np.select(conditions, values)

    # Create column for my character
    conditions = [
        (dataframe['p1_name'].isin(names)),
        (dataframe['p2_name'].isin(names)),
    ]
    values = [dataframe['p1_char'], dataframe['p2_char']]
    dataframe['my_char'] = np.select(conditions, values)

    # Create column for opp character
    conditions = [
        (dataframe['p1_name'].isin(names)),
        (dataframe['p2_name'].isin(names)),
    ]
    values = [dataframe['p2_char'], dataframe['p1_char']]
    dataframe['opp_char'] = np.select(conditions, values)

    # Create win or loss column
    conditions = [
        (dataframe['winner'].isin(names)),
        (dataframe['winner'] == dataframe['opp_name']),
        (dataframe['winner'].isnull())

    ]
    values = ['win', 'loss', None]
    dataframe['win_loss'] = np.select(conditions, values)

    # Remove any rows where neither player is named
    clean_nonames(dataframe)
