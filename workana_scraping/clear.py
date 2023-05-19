import pandas as pd


class Clear:
    def clear():
        # read csv
        # df_raw = pd.read_csv('workana_scraping/data/data_raw.csv')
        df_raw = pd.read_csv("workana_scraping/data/data_teste.csv")

        # create a copy from original data
        df = df_raw.copy()

        # dict pt x en
        months = {
            "Janeiro": "January",
            "Fevereiro": "February",
            "Março": "March",
            "Abril": "April",
            "Maio": "May",
            "Junho": "June",
            "Julho": "July",
            "Agosto": "August",
            "Setembro": "September",
            "Outubro": "October",
            "Novembro": "November",
            "Dezembro": "December",
        }

        # replaces month names in portuguese with their english equivalents
        for m_pt, m_en in months.items():
            df["Publish Date"] = df["Publish Date"].str.replace(m_pt, m_en)
            df["Publish Date"] = df["Publish Date"].str.replace(" de ", " ")

        # change type
        df["Publish Date"] = pd.to_datetime(df["Publish Date"], format="%d %B %Y %H:%M")
        df["Publish Date"]

        # where exists 'Categoria'
        count_cat = df[df["Summary"].str.contains("Categoria")].index.tolist()
        # print(f'A palavra "Categoria" aparece nas linhas: {count_cat}')

        # extract data
        df["Category"] = df["Summary"].str.extract("Categoria:\s*(.*)\n")
        df["Category"] = df["Category"].fillna("N/I")

        # print(df['Category'])

        return df
