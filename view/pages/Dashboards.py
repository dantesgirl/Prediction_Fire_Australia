import datetime as dt # -> Manipulação de datas
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st # -> Criação fácil de aplicações web

from models.Datas import Datas
from view.src.Base import BasePage

class DashboardsPage(BasePage):
    # =================================================================================================================================================
    # Inicialização
    # =================================================================================================================================================
    def __init__(self, df):
        # Aplica configurações de página
        super().__init__(page_title="Relatórios", layout="wide", page_icon="view/img/Logo.png")

        self.df = df

        # Coordenadas New South Wales
        self.lat_nsw_min, self.lat_nsw_max = -38, -29
        self.lon_nsw_min, self.lon_nsw_max = 141, 154
        # Coordenadas Victoria
        self.lat_vic_min, self.lat_vic_max = -39, -34.7
        self.lon_vic_min, self.lon_vic_max = 141, 149
        # Coordenadas Queensland
        self.lat_qen_min, self.lat_qen_max = -29, -10
        self.lon_qen_min, self.lon_qen_max = 138, 155
        # Coordenadas South Australia
        self.lat_sau_min, self.lat_sau_max = -38, -26
        self.lon_sau_min, self.lon_sau_max = 129, 141
        # Coordenadas Western Australia
        self.lat_wea_min, self.lat_wea_max = -35, -13
        self.lon_wea_min, self.lon_wea_max = 112, 129
        # Coordenadas Northern Territory
        self.lat_not_min, self.lat_not_max = -26, -11
        self.lon_not_min, self.lon_not_max = 129, 138
        # Coordenadas Tasmania
        self.lat_tas_min, self.lat_tas_max = -44, -40
        self.lon_tas_min, self.lon_tas_max = 144, 149

        # Lista de valores a serem atribuídos para cada condição
        self.values = [
            "New South Wales",
            "Victoria",
            "Queensland",
            "South Australia",
            "Western Australia",
            "Northern Territory",
            "Tasmania"
        ]

        # Dicionário com os valores de localidade referentes a cada estado
        self.estados = {
            "Austrália (Total)": {"lat": -28.0, "lon": 133.5, "zoom": 2.8, "lat_min": -45, "lat_max": -10, "lon_min": 110, "lon_max": 155},
            "New South Wales": {"lat": -33.0, "lon": 147.0, "zoom": 4.3, "lat_min": -38, "lat_max": -29, "lon_min": 141, "lon_max": 154},
            "Victoria": {"lat": -37.0, "lon": 145.0, "zoom": 4.8, "lat_min": -39, "lat_max": -34.7, "lon_min": 141, "lon_max": 149},
            "Queensland": {"lat": -21.0, "lon": 144.0, "zoom": 3.9, "lat_min": -29, "lat_max": -10, "lon_min": 138, "lon_max": 155},
            "South Australia": {"lat": -31.5, "lon": 135.0, "zoom": 4.2, "lat_min": -38, "lat_max": -26, "lon_min": 129, "lon_max": 141},
            "Western Australia": {"lat": -25.0, "lon": 121.0, "zoom": 3.6, "lat_min": -35, "lat_max": -13, "lon_min": 112, "lon_max": 129},
            "Northern Territory": {"lat": -19.0, "lon": 134.0, "zoom": 4.1, "lat_min": -26, "lat_max": -11, "lon_min": 129, "lon_max": 138},
            "Tasmania": {"lat": -42.0, "lon": 146.5, "zoom": 6, "lat_min": -44, "lat_max": -40, "lon_min": 144, "lon_max": 149},
        }

    # =================================================================================================================================================
    # Execução
    # =================================================================================================================================================
    def run(self):
        self.apply_config()
        
        # Define os estados de sessão iniciais
        if "df" not in st.session_state:
            st.session_state.df = Datas().importDatasetsOnFirms()
            
        df_origin = st.session_state.df

        def dataProcesing(df):
            # Lista de condições
            conditions = [
                (df["latitude"].between(self.lat_nsw_min, self.lat_nsw_max)) & (df["longitude"].between(self.lon_nsw_min, self.lon_nsw_max)),
                (df["latitude"].between(self.lat_vic_min, self.lat_vic_max)) & (df["longitude"].between(self.lon_vic_min, self.lon_vic_max)),
                (df["latitude"].between(self.lat_qen_min, self.lat_qen_max)) & (df["longitude"].between(self.lon_qen_min, self.lon_qen_max)),
                (df["latitude"].between(self.lat_sau_min, self.lat_sau_max)) & (df["longitude"].between(self.lon_sau_min, self.lon_sau_max)),
                (df["latitude"].between(self.lat_wea_min, self.lat_wea_max)) & (df["longitude"].between(self.lon_wea_min, self.lon_wea_max)),
                (df["latitude"].between(self.lat_not_min, self.lat_not_max)) & (df["longitude"].between(self.lon_not_min, self.lon_not_max)),
                (df["latitude"].between(self.lat_tas_min, self.lat_tas_max)) & (df["longitude"].between(self.lon_tas_min, self.lon_tas_max)),
            ]

            df["states"] = np.select(conditions, self.values, default="N/A")
            df["acq_date"] = pd.to_datetime(df["acq_date"])
            df["month_name"] = df["acq_date"].dt.month_name()
            
            return df

        df = dataProcesing(df_origin)
        
        st.sidebar.header("⚙️ Filtros do Mapa")

        estado_selecionado = st.sidebar.selectbox(
            "Selecione um estado:",
            options=list(self.estados.keys()),
            index=0
        )
        
        st.sidebar.header("🗓️ Datas")

        years_available = sorted(df["year"].unique(), reverse=True)
        years_selec = st.sidebar.selectbox("Ano", options=years_available, index=0)

        if years_selec == "Todos":
            months_available = list(df["month_name"].unique())
        else:
            months_available = list(df.loc[df["year"] == years_selec, "month_name"].unique())
        months_selec = st.sidebar.selectbox("Mês", options=["Todos"] + months_available, index=0)

        if months_selec == "Todos":
            days_available = sorted(df["day"].unique())
        else:
            if years_selec == "Todos":
                days_available = sorted(df.loc[df["month_name"] == months_selec, "day"].unique())
            else:
                days_available = sorted(df.loc[(df["year"] == years_selec) & (df["month_name"] == months_selec), "day"].unique())
        days_selec = st.sidebar.selectbox("Dia", options=["Todos"] + days_available, index=0)

        info_estado = self.estados[estado_selecionado]
        df = df[
            (df["latitude"] >= info_estado["lat_min"]) &
            (df["latitude"] <= info_estado["lat_max"]) &
            (df["longitude"] >= info_estado["lon_min"]) &
            (df["longitude"] <= info_estado["lon_max"])]
