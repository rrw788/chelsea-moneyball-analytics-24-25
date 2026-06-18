import pandas as pd
import os

def run_cleaning_pipeline():
    print("Mulai Membaca Data Mentah.......")


    # 1 menentukan path file 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(script_dir, "../data/raw/")
    processed_dir = os.path.join(script_dir, "../data/processed/")

    # 2 load data mentah
    df_info = pd.read_csv(os.path.join(raw_dir, "premier_player_info.csv"))
    df_stats = pd.read_csv(os.path.join(raw_dir, "player_stats_2024_2025_season.csv"))

    # 3 Proses Penggabungan inner join
    print("Menggabungkan data pemain dan statistik....")
    df_merge = pd.merge(df_info, df_stats, on="player_name", how="inner")

    # 4 Proses Filter Khusus Chelsea
    df_chelsea = df_merge[df_merge['player_club'] == 'Chelsea'].copy()

    # 5 Handling Data Types & Missing Values
    df_chelsea['Minutes Played'] = df_chelsea['Minutes Played'].fillna(0).astype(int)

    # 6 Menyimpan hasil data yang sudah bersih
    output_path = os.path.join(processed_dir, "chelsea_clean.csv")
    df_chelsea.to_csv(output_path, index=False)

    print(f"Selesai! Data Bersih disimpan di: {output_path}")

if __name__ == "__main__":
    run_cleaning_pipeline()
