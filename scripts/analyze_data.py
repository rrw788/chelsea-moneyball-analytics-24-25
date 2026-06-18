from pathlib import Path
import pandas as pd
import numpy as np


def load_clean_data():
    file_path = (
        Path(__file__).resolve().parent
        / "../data/processed/chelsea_clean.csv"
    ).resolve()

    return pd.read_csv(file_path)

def metrics(df):
    df_copy = df.copy()

    # avoid division by zero
    mins = df_copy['Minutes Played'].replace(0, np.nan)

    # ======================
    # GENERAL METRICS
    # ======================

    df_copy['GA'] = df_copy['Goals'] + df_copy['Assists']
    df_copy['xGI'] = df_copy['XG'] + df_copy['XA']

    df_copy['Goals90'] = ((df_copy['Goals'] / mins) * 90).round(2)

    df_copy['xG90'] = ((df_copy['XG'] / mins) * 90).round(2)
    df_copy['xA90'] = ((df_copy['XA'] / mins) * 90).round(2)
    df_copy['xGI90'] = (df_copy['xG90'] + df_copy['xA90']).round(2)

    # ======================
    # ATTACKING METRICS
    # ======================

    df_copy['ShotsOnTarget'] = (
        df_copy['Shots On Target Inside the Box']
        + df_copy['Shots On Target Outside the Box']
    )

    df_copy['Shots90'] = (
        df_copy['ShotsOnTarget'] / mins * 90
    ).round(2)

    df_copy['Pass90'] = (
        df_copy['pass_attempts'] / mins * 90
    ).round(2)

    df_copy['Dribble90'] = (
        df_copy['dribble_attempts'] / mins * 90
    ).round(2)

    # ======================
    # DEFENSIVE METRICS
    # ======================

    df_copy['Tackles90'] = (
        df_copy['Total Tackles'] / mins * 90
    ).round(2)

    df_copy['Interceptions90'] = (
        df_copy['Interceptions'] / mins * 90
    ).round(2)

    df_copy['Blocks90'] = (
        df_copy['Blocks'] / mins * 90
    ).round(2)

    df_copy['DuelsWon90'] = (
        df_copy['Duels Won'] / mins * 90
    ).round(2)

    df_copy['Fouls90'] = (
        df_copy['Fouls'] / mins * 90
    ).round(2)

    df_copy['DefensiveScore'] = (
        df_copy['Tackles90']
        + df_copy['Interceptions90']
        + df_copy['Blocks90']
        + df_copy['DuelsWon90']
        - df_copy['Fouls90']
    ).round(2)

    return df_copy

def top_stats(df, top_n=15):
    df_copy = metrics(df)

    result = (
        df_copy.sort_values(by='xGI', ascending=False)
        [['player_name', 'appearances_', 'Goals', 'Assists', 'GA',
          'XG', 'XA', 'xGI', 'xG90', 'xA90', 'xGI90', 'Minutes Played']]
        .head(top_n)
        .reset_index(drop=True)
    )

    result.index = result.index + 1
    return result

def get_over_under(df):
    df_copy = metrics(df)

    df_copy = df_copy[df_copy['appearances_'] > 10]

    cols = [
        'player_name', 'appearances_', 'Goals', 'Assists', 'GA', 'XG', 'XA', 'xGI', 'xG90', 'xA90', 'xGI90','Minutes Played'
    ]

    over = (
        df_copy[cols]
        .sort_values(by='xGI', ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    over.index = over.index + 1

    under = (
        df_copy[cols]
        .sort_values(by='xGI') 
        .head(5)
        .reset_index(drop=True)
    )
    under.index = under.index + 1

    return over, under

def top_attackers(df, top_n=5):
    df_copy = metrics(df)

    df_copy = df_copy[df_copy['appearances_'] > 10]

    result = (
        df_copy[
            [
                'player_name',
                'appearances_',
                'Minutes Played',
                'Goals',
                'Assists',
                'xG90',
                'xA90',
                'xGI90',
                'Goals90',
                'Shots90',
                'Dribble90'
            ]
        ]
        .sort_values(by='xGI90', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    result.index += 1
    return result

def top_defenders(df, top_n=5):
    df_copy = metrics(df)

    df_copy = df_copy[df_copy['appearances_'] > 10]

    result = (
        df_copy[
            [
                'player_name',
                'appearances_',
                'Minutes Played',
                'Tackles90',
                'Interceptions90',
                'Blocks90',
                'DuelsWon90',
                'Fouls90',
                'DefensiveScore'
            ]
        ]
        .sort_values(by='DefensiveScore', ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    result.index += 1
    return result







if __name__ == "__main__":
    data = load_clean_data()
    print("\n--- Top Stats ---")
    print(top_stats(data, top_n=5))

    over, under = get_over_under(data)
    print("\n=== OVERPERFORMERS ===")
    print(over)

    print("\n=== UNDERPERFORMERS ===")
    print(under)

    print("\n=== TOP ATTACKERS ===")
    print(top_attackers(data))

    print("\n=== TOP DEFENDERS ===")
    print(top_defenders(data))