from matplotlib import pyplot as plt


# Get the wins and losses for each character played against
def calc_win_loss(dataframe):
    opp_chars = dataframe.opp_char.unique()
    losses = []
    wins = []
    for char in opp_chars:
        games_won = dataframe.apply(lambda x: True
        if x['opp_char'] == char and x['win_loss'] == 'win' else False, axis=1)
        num_wins = len(games_won[games_won == True].index)
        games_lost = dataframe.apply(lambda x: True
        if x['opp_char'] == char and x['win_loss'] == 'loss' else False, axis=1)
        num_losses = len(games_lost[games_lost == True].index)

        wins.append(num_wins)
        losses.append(num_losses)

    return wins, losses


# Plot all characters played against by frequency
def plot_char_freq(dataframe, opponent='ALL'):
    fig, ax = plt.subplots()
    dataframe['opp_char'].value_counts().plot(ax=ax, kind='barh')
    plt.title(f'Most Played Against Characters in {str(len(dataframe))} Games')
    plt.xlabel('Games Played Against')
    plt.ylabel('Character')
    plt.gca().invert_yaxis()
    for i, v in enumerate(dataframe['opp_char'].value_counts()):
        ax.text(v + 1, i, str(v), color='black', ha='left', va='center')
    fig.canvas.set_window_title('Vs: ' + opponent)
    plt.show()


# Plot stacked bar wins/losses for each character played against
def plot_wl_by_char(dataframe, opponent='ALL'):
    x = dataframe.opp_char.unique()  # All characters played against
    win, loss = calc_win_loss(dataframe)  # Win loss records
    tot_games = [w + l for w, l in zip(win, loss)]
    wl_percent = [(w / (w + l)) * 100 if w > 0 else 0.0 for w, l in zip(win, loss)]  # Win percents for labels
    fig, ax = plt.subplots()
    ax.barh(x, tot_games, 0.75, 0.8, color='brown')
    ax.barh(x, win, 0.75, 0.8, color='limegreen')
    plt.title('Win Percentage vs All Characters Played Against')
    plt.xlabel('Games Played Against')
    plt.ylabel('Characters')
    plt.gca().invert_yaxis()
    # Label bar percentages
    for i, v in enumerate(wl_percent):
        ax.text(tot_games[i] + 1, i, str(v)[:5], color='black', ha='left', va='center')
    fig.canvas.set_window_title('Vs: ' + opponent)
    plt.show()


# Get wins/losses overall and win rate
def plot_overall_wl(dataframe, opponent='ALL'):
    x = [f'Overall Win/Loss']
    win, loss = calc_win_loss(dataframe)
    sum_win = [sum(win)]
    sum_loss = [sum(loss)]
    sum_games = [sum(win) + sum(loss)]
    wl_percent = str((sum_win[0] / sum_games[0]) * 100)[:5]
    fig, ax = plt.subplots()
    ax.barh(x, sum_games, 0.75, 0.8, color='brown')
    ax.barh(x, sum_win, 0.75, 0.8, color='limegreen')
    plt.title(f'Overall Win/Loss {wl_percent} %')
    plt.xlabel(f'Total Games Played ({str(len(dataframe))})')
    # Label games won
    for i, v in enumerate(sum_win):
        ax.text(v, i, str(v), color='black', ha='right', va='center')
    # Label games lost
    for i, v in enumerate(sum_loss):
        ax.text(sum_games[i], i, str(v), color='black', ha='right', va='center')
    fig.canvas.set_window_title('Vs: ' + opponent)
    plt.show()
