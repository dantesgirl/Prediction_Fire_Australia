import numpy as np
from datetime import datetime 
import streamlit as st
import pandas as pd
import pickle as pk
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
        super().__init__(page_title = "Relatórios", layout = "wide", page_icon = "view/img/Logo.png")

        self.df = df

        # Coordenadas New South Wales
        self.lat_nsw_min, self.lat_nsw_max = -38, -29, 
        self.lon_nsw_min, self.lon_nsw_max = 141, 154
        # Coordenadas Victoria
        self.lat_vic_min, self.lat_vic_max = -39, -34.7, 
        self.lon_vic_min, self.lon_vic_max = 141, 149
        # Coordenadas Queensland
        self.lat_qen_min, self.lat_qen_max = -29, -10, 
        self.lon_qen_min, self.lon_qen_max =  138, 155
        # Coordenadas South Australia
        self.lat_sau_min, self.lat_sau_max = -38, -26, 
        self.lon_sau_min, self.lon_sau_max = 129, 141
        # Coordenadas Western Australia
        self.lat_wea_min, self.lat_wea_max = -35, -13, 
        self.lon_wea_min, self.lon_wea_max = 112, 129
        # Coordenadas Northern Territory
        self.lat_not_min, self.lat_not_max = -26, -11, 
        self.lon_not_min, self.lon_not_max = 129, 138
        # Coordenadas Tasmania
        self.lat_tas_min, self.lat_tas_max = -44, -40, 
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

            df["states"] = np.select(conditions, self.values, default = "N/A")
            df["acq_date"] = pd.to_datetime(df["acq_date"])
            df["month_name"] = df["acq_date"].dt.month_name()
            
            return df
import plotly.graph_objects as go

        df = dataProcesing(df_origin)
        
        st.sidebar.header("⚙️ Filtros do Mapa")
class PredicitonsDashboards:
    def __init__(self, prediction):
        self.prediction = prediction

        estado_selecionado = st.sidebar.selectbox(
            "Selecione um estado:",
            options = list(self.estados.keys()),
            index = 0
        )
        
        st.sidebar.header("🗓️ Datas")
    def get_training_data(self):
        try: 
            with open("fire_model.pkl", "rb") as f:
                model_data = pk.load(f)

        years_available = sorted(df["year"].unique(), reverse = True)
        years_selec = st.sidebar.selectbox("Ano", options = years_available, index = 0)
            print("Dados do modelo carregados!")
            print(f"Tipo: {type(model_data)}")
            
            if isinstance(model_data, dict):
                df_clean = model_data.get("df_clean")
                feature_importance = model_data.get("feature_importance")
                accuracy = model_data.get("accuracy")
                cm = model_data.get("confusion_matrix")
            else:
                print("Aviso: Modelo antigo detectado (sem dados extras)")
                return None, None, None, None

            print("Dados carregados com sucesso")
            print(f"Dataset: {len(df_clean):,} registros")
            print(f"Acurácia: {accuracy*100:.2f}%")
            
            return df_clean, feature_importance, accuracy, cm
        
        except FileNotFoundError:
            print("Erro: fire_model.pkl não encontrado")
            print("Execute o treinamento primeiro: python models/PredictionModel/ModelTraining.py")
            return None, None, None, None
        except KeyError as e:
            print("Pickle antigo detectado")
            print(f"Variável '{e}' não encontrada")
            print("Treine novamente rodando: python models/PredictionModel/ModelTraining.py")
            return None, None, None, None
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None, None, None, None
    
    def predictions_dashboards(self):
        df_clean, feature_importance, accuracy, cm = self.get_training_data()

        if years_selec == "Todos":
            months_available = list(df["month_name"].unique())
        else:
            months_available = list(df.loc[df["year"] == years_selec, "month_name"].unique())
        months_selec = st.sidebar.selectbox("Mês", options = ["Todos"] + months_available, index = 0)
        if df_clean is None or feature_importance is None:
            st.error("❌ Erro ao carregar dados do modelo!")
            st.warning("Por favor, treine o modelo novamente executando: `python models/PredictionModel/ModelTraining.py`")
            return

        if months_selec == "Todos":
            days_available = sorted(df["day"].unique())
        else:
            if years_selec == "Todos":
                days_available = sorted(df.loc[df["month_name"] == months_selec, "day"].unique())
            else:
                days_available = sorted(df.loc[(df["year"] == years_selec) & (df["month_name"] == months_selec), "day"].unique())
        days_selec = st.sidebar.selectbox("Dia", options = ["Todos"] + days_available, index = 0)

        info_estado = self.estados[estado_selecionado]
        df = df[
            (df["latitude"] >= info_estado["lat_min"]) &
            (df["latitude"] <= info_estado["lat_max"]) &
            (df["longitude"] >= info_estado["lon_min"]) &
            (df["longitude"] <= info_estado["lon_max"])
        ]
        print(f"Feature importance carregado: {type(feature_importance)}")

        st.title("📈 Resultados da Predição")
        st.divider()

        filtered_df = df.copy() 
        prediction_date = self.prediction["date"]
        prediction_date = datetime.strptime(prediction_date, "%Y-%m-%d")
        day = prediction_date.day
        month = prediction_date.month
        year = prediction_date.year
        months = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
        for number, name in months.items():
            if month == number:
                month_name = name  

        if years_selec != "Todos":
            filtered_df = filtered_df[filtered_df["year"] == years_selec]
        if months_selec != "Todos":
            filtered_df = filtered_df[filtered_df["month_name"] == months_selec]
        if days_selec != "Todos":
            filtered_df = filtered_df[filtered_df["day"] == days_selec]


        # =================================================================================================================================================
        # Gráficos
        # =================================================================================================================================================

        # Gráfico de mapa de dispersão das queimadas da Austrália
        fig_map = px.scatter_map(
            filtered_df,
            lat = "latitude",
            lon = "longitude",
            color = "brightness",
            size = "frp",
            hover_name = "year",
            hover_data = ["brightness", "frp"],
            color_continuous_scale = "inferno",
            size_max = 25,
            zoom = info_estado["zoom"],
            center = {"lat": info_estado["lat"], "lon": info_estado["lon"]},
            labels = {"brightness": "Brilho Térmico"},
            map_style = "open-street-map",
            opacity = 0.7,
            title = "Visão Geral das Queimadas da Austrália"
        )
        st.markdown(f"""
            **Data da Predição:** {day} de {month_name} de {year} - {self.prediction["season"]}\n
            **Coordenadas:** {self.prediction["location"]}\n
            **Risco de Incêndio:** {self.prediction["fire_risk"]}\n
            **Intensidade Prevista:** {self.prediction["predicted_intensity"]}\n
            **Índice de Confiança:** {self.prediction["confidence_score"]}\n
            **Brilho Térmico Estimado:** {self.prediction["brightness"]}K\n
            **Temperatura Estimada:** {self.prediction["brightness"] - 273.15:.2f}°C\n
            **Confiança:** {self.prediction["confidence"]}\n
        """)    

        st.title("📊 Gráficos do Modelo")
        st.divider()

        fig_map.update_layout(
            height = 600
        ) 

        df_states = filtered_df.groupby("states").size().reset_index(name = "total").sort_values(by = "total", ascending = True)
        # Gráfico de barras do total de queimadas por estado
        fig_states = px.bar(
            df_states, 
            x = "total", 
            y = "states",
            orientation = "h",
            text = "total",
            title = "Total de Queimadas por Estado",
            labels = {"total": "Total de Queimadas", "states": "Estados"},
            color_discrete_sequence = ["#BC3952"]
        ) 

        fig_states.update_layout(
            coloraxis_showscale = False
        top_features = feature_importance.sort_values("importance", ascending=False).head(10)

        fig1 = px.bar(
            top_features,
            x="importance",
            y="feature",
            orientation="h",
            color="importance",
            title="Random Forest - Top 10 Características",
            labels={"importance": "Importância", "feature": "Característica"},
            color_continuous_scale="Reds",
        )
        fig1.update_layout(yaxis=dict(autorange="reversed"))

        df_dates = filtered_df.groupby("acq_date").size().reset_index(name = "total")
        # Gráfico linha do tempo do total de queimadas
        fig_timeline = px.area(
            df_dates,
            x = "acq_date", 
            y = "total",
            title = "Evolução Diária das Queimadas",
            labels = {"acq_date": "Data", "total": "Total de Queimadas"},
            color_discrete_sequence = ["#BC3952"],
            markers = True
        cm_df = pd.DataFrame(
            cm,
            index=["Baixo", "Alto"],
            columns=["Baixo", "Alto"]
        )
        
        # Gráfico de histograma do brilho térmico por queimadas
        fig_hist = px.histogram(
            filtered_df, 
            x = "brightness",
            nbins = 40,
            text_auto = True,
            title = "Distribuição de Brilho das Queimadas",
            labels = {"count": "Total de Queimadas", "brightness": "Brilho Térmico"},
            color_discrete_sequence = ["#BC3952"]

        fig2 = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale="YlOrRd",
            title=f"Matriz de Confusão - Acurácia: {accuracy*100:.2f}%"
        )
        fig_hist.update_yaxes(title="Total de Queimadas")

        fig_hist.update_layout(
            height = 500,
            bargap = 0.1
        monthly_fires = df_clean.groupby("month").size()
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        high_risk_months = monthly_fires[monthly_fires > monthly_fires.median()]
        
        df_month = pd.DataFrame({
            "month": months_list,
            "fires": monthly_fires,
            "risk": ["Alto" if i+1 in high_risk_months.index else "Baixo" for i in range(12)]
        })

        fig3 = px.bar(
            df_month,
            x="month",
            y="fires",
            color="risk",
            color_discrete_map={
                "Alto": "#e63946",
                "Baixo": "#f1fa8c"
            },
            title="Distribuição de Incêndios por mês",
            labels={"month": "Mês", "fires": "Incêndios", "risk": "Risco"}
        )
        fig3.add_hline(y=df_month["fires"].median(), line_dash="dash")

        fig_hist.update_traces(
            textposition = "outside"
        seasonal_fires = df_clean.groupby("season")["fire_intensity"].agg(["count", "mean"])
        seasonal_names = {0: "Inverno", 1: "Outono", 2: "Primavera", 3: "Verão"}
        
        df_seasons = pd.DataFrame({
            "season": [seasonal_names[i] for i in sorted(seasonal_fires.index)],
            "fires": [seasonal_fires.loc[i, "count"] for i in sorted(seasonal_fires.index)]
        })

        fig4 = px.bar(
            df_seasons,
            x="season",
            y="fires",
            text="fires",
            title="Distribuição do Fogo por Estação",
            labels={"season": "Estação", "fires": "Incêndios"}
        )

        # Configurações gerais do comportamento de cada gráfico
        config = {
            "responsive": True,
            "scrollZoom": True,
            "displaylogo": False,
            "displayModeBar": True
        }    
        fig4.update_traces(marker_color="#e74c3c")

        df_intensity = pd.DataFrame({
            "season": df_seasons["season"],
            "intensity": [seasonal_fires.loc[i, "mean"] * 100 for i in sorted(seasonal_fires.index)]
        })

        # =================================================================================================================================================
        # Exibição
        # =================================================================================================================================================
        # Título da página
        st.title("📊 Análise das Queimadas da Austrália")
        st.divider()
        fig5 = px.bar(
            df_intensity,
            x="season",
            y="intensity",
            text=df_intensity["intensity"].map(lambda x: f"{x:.1f}%"),
            title="Intensidade do Fogo por Estação (%)",
            labels={"season": "Estações", "intensity": "Intensidade"}
        )
        fig5.update_yaxes(range=[0, 100])

        fig5.update_traces(marker_color="#e74c3c")

        yearly_data = df_clean.groupby("year").agg({
            "fire_intensity": ["count", "mean"]
        }).reset_index()

        yearly_data.columns = ["year", "total_fires", "high_intensity_pct"]
        yearly_data["high_intensity_pct"] *= 100

        fig6 = go.Figure()

        fig6.add_trace(go.Bar(
            x=yearly_data["year"],
            y=yearly_data["total_fires"],
            name="Total de Incêndios",
            marker_color="#e74c3c"
        ))

        fig6.add_trace(go.Scatter(
            x=yearly_data["year"],
            y=yearly_data["high_intensity_pct"],
            mode="lines+markers",
            name="Alta Intensidade (%)",
            marker=dict(color="#e63946", size=8),
            line=dict(color="#e63946", width=3),
            yaxis="y2" 
        ))

        fig6.update_layout(
            title="Tendências de Incêndios ao longo dos anos",
            xaxis=dict(title="Ano"),
            yaxis=dict(
                title="Número de Incêndios",
                showgrid=False
            ),
            yaxis2=dict(
                title="Alta Intensidade (%)",
                overlaying="y",
                side="right",
                range=[0, 100], 
                showgrid=False
            ),
        )

        # Estrutura da exibição dos gráficos
        tab1, tab2, tab3, = st.tabs(["🌍 Mapa", "📅 Linha do tempo", "📈 Distribuições"])
        tab1, tab2, tab3, = st.tabs(["🧠 Modelo", "🗓️ Análise Mensal", "📆 Análise Anual"])

        with tab1:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.plotly_chart(fig_map, config = config)
            with col2:
                st.plotly_chart(fig_states, config = config)

            with col1:  
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            st.plotly_chart(fig_timeline, config = config)
    
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("**Ocorrencias por mês:**")
                for month_num, fires in monthly_fires.items():
                    st.write(f"  {months_list[month_num-1]:>3} - {fires:>8,} Incêndios ({fires/len(df_clean)*100:>5.2f}%)")
            
            with col2:
                st.plotly_chart(fig3, use_container_width=True)
            
        with tab3:
            st.plotly_chart(fig_hist, config = config)
            
            st.plotly_chart(fig6, use_container_width=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Padrões do fogo/queimadas por estação:**")
                for season, data in seasonal_fires.iterrows():
                    st.write(f"   {seasonal_names[season]:>6}: {data['count']:>8,} chamas | " + 
                        f"Intensidade alta: {data['mean']*100:>5.1f}%")
            
            with col2:
                st.plotly_chart(fig4, use_container_width=True)
