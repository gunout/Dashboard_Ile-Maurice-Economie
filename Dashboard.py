# dashboard_maurice.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Économique Île Maurice - Analyse en Temps Réel",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #EA2839, #1A206D, #FFD100);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #EA2839, #1A206D);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #EA2839;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #1A206D;
        border-bottom: 2px solid #FFD100;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .sector-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #1A206D;
        background-color: #f8f9fa;
    }
    .growth-indicator {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .positive { background-color: #d4edda; border-left: 4px solid #28a745; color: #155724; }
    .negative { background-color: #f8d7da; border-left: 4px solid #dc3545; color: #721c24; }
    .neutral { background-color: #e2e3e5; border-left: 4px solid #6c757d; color: #383d41; }
    .sector-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .mauritius-flag {
        background: linear-gradient(90deg, #EA2839 33%, #1A206D 33%, #1A206D 66%, #FFD100 66%);
        height: 4px;
        margin: 0.5rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

class MauritiusDashboard:
    def __init__(self):
        self.secteurs = self.define_secteurs()
        self.economic_data = self.initialize_economic_data()
        self.tourism_data = self.initialize_tourism_data()
        self.trade_data = self.initialize_trade_data()
        self.investment_data = self.initialize_investment_data()
        
    def define_secteurs(self):
        """Définit les secteurs économiques de l'Île Maurice"""
        return {
            'Tourisme': {
                'nom_complet': 'Tourisme et Hôtellerie',
                'poids_pib': 24.3,
                'croissance': 8.7,
                'emplois': 75000,
                'couleur': '#EA2839',
                'description': 'Premier secteur économique du pays',
                'entreprises_cles': ['Beachcomber', 'Sun Resorts', 'Veranda', 'LUX*'],
                'perspectives': 'Très positives'
            },
            'Services Financiers': {
                'nom_complet': 'Services Financiers et Bancaires',
                'poids_pib': 12.8,
                'croissance': 5.2,
                'emplois': 15000,
                'couleur': '#1A206D',
                'description': 'Centre financier international',
                'entreprises_cles': ['MCB', 'SBM', 'MUA', 'CIM'],
                'perspectives': 'Stables'
            },
            'Textile': {
                'nom_complet': 'Industrie Textile et Habillement',
                'poids_pib': 8.5,
                'croissance': 3.1,
                'emplois': 45000,
                'couleur': '#FF6B00',
                'description': 'Exportations vers UE et USA',
                'entreprises_cles': ['CIEL Textile', 'Floréal', 'Made in Moris'],
                'perspectives': 'En croissance modérée'
            },
            'Sucre': {
                'nom_complet': 'Industrie Sucrière',
                'poids_pib': 6.2,
                'croissance': -2.1,
                'emplois': 15000,
                'couleur': '#FFD100',
                'description': 'Tradition historique en mutation',
                'entreprises_cles': ['Omnicane', 'Alteo', 'TERRÉA'],
                'perspectives': 'En restructuration'
            },
            'Technologie': {
                'nom_complet': 'Technologies de l\'Information',
                'poids_pib': 7.3,
                'croissance': 15.4,
                'emplois': 12000,
                'couleur': '#00A3E0',
                'description': 'Secteur en forte croissance',
                'entreprises_cles': ['Accenture', 'CERNE', 'IFSS', 'Cim'],
                'perspectives': 'Très positives'
            },
            'Immobilier': {
                'nom_complet': 'Immobilier et Construction',
                'poids_pib': 9.1,
                'croissance': 6.8,
                'emplois': 35000,
                'couleur': '#8B4513',
                'description': 'Programme IRS/REIS très actif',
                'entreprises_cles': ['Rogers', 'IBL', 'Gamma Civic'],
                'perspectives': 'Positives'
            },
            'Commerce': {
                'nom_complet': 'Commerce de Détail et Distribution',
                'poids_pib': 11.2,
                'croissance': 4.3,
                'emplois': 55000,
                'couleur': '#6f42c1',
                'description': 'Réseaux de distribution développés',
                'entreprises_cles': ['Jumbo', 'Super U', 'Winner\'s', 'Shoprite'],
                'perspectives': 'Stables'
            },
            'Pêche': {
                'nom_complet': 'Pêche et Aquaculture',
                'poids_pib': 4.1,
                'croissance': 7.2,
                'emplois': 12000,
                'couleur': '#0066CC',
                'description': 'Thon et produits de la mer',
                'entreprises_cles': ['Mormaï', 'Seafood Hub', 'Fishing Co'],
                'perspectives': 'En croissance'
            }
        }
    
    def initialize_economic_data(self):
        """Initialise les données économiques historiques"""
        dates = pd.date_range('2014-01-01', datetime.now(), freq='M')
        data = []
        
        for date in dates:
            # Données économiques de base avec tendances réalistes
            pib_base = 15.0  # Milliards USD
            croissance_base = 3.5  # %
            
            # Impact COVID (2020-2021)
            if date.year == 2020:
                covid_impact = random.uniform(-0.15, -0.05)  # -5% à -15%
            elif date.year == 2021:
                covid_impact = random.uniform(-0.02, 0.03)   # -2% à +3%
            else:
                covid_impact = random.uniform(0.02, 0.08)    # +2% à +8%
            
            inflation = random.uniform(2.0, 6.5)
            chomage = random.uniform(6.0, 9.5)
            
            data.append({
                'date': date,
                'pib_mensuel': pib_base * (1 + croissance_base/100) ** ((date.year-2014)*12 + date.month-1),
                'croissance_pib': croissance_base + covid_impact * 100,
                'inflation': inflation,
                'taux_chomage': chomage,
                'taux_change_usd': random.uniform(35, 45),
                'reserves_devises': random.uniform(5, 8),  # Milliards USD
                'dette_publique': random.uniform(60, 75)   # % PIB
            })
        
        return pd.DataFrame(data)
    
    def initialize_tourism_data(self):
        """Initialise les données touristiques"""
        dates = pd.date_range('2014-01-01', datetime.now(), freq='M')
        data = []
        
        for date in dates:
            # Saisonnalité touristique
            if date.month in [12, 1, 2, 7, 8]:  # Haute saison
                base_touristes = 150000
            elif date.month in [3, 4, 9, 10]:   # Moyenne saison
                base_touristes = 100000
            else:                               # Basse saison
                base_touristes = 70000
            
            # Impact COVID
            if date.year == 2020 or (date.year == 2021 and date.month <= 6):
                covid_factor = random.uniform(0.05, 0.15)  # 5-15% de la normale
            elif date.year == 2021:
                covid_factor = random.uniform(0.3, 0.6)    # 30-60% de la normale
            elif date.year == 2022:
                covid_factor = random.uniform(0.7, 0.9)    # 70-90% de la normale
            else:
                covid_factor = random.uniform(1.0, 1.2)    # Retour à la normale
            
            touristes = base_touristes * covid_factor
            recettes = touristes * random.uniform(1200, 1800)  # Dépense moyenne par touriste
            
            data.append({
                'date': date,
                'arrivees_touristes': touristes,
                'recettes_tourisme': recettes,
                'duree_sejour_moyenne': random.uniform(8, 12),
                'taux_occupation_hotels': random.uniform(0.6, 0.9) * covid_factor,
                'principaux_marches': random.choice(['France', 'Royaume-Uni', 'Allemagne', 'Afrique du Sud'])
            })
        
        return pd.DataFrame(data)
    
    def initialize_trade_data(self):
        """Initialise les données commerciales"""
        dates = pd.date_range('2014-01-01', datetime.now(), freq='M')
        produits_export = ['Textile', 'Sucre', 'Poisson', 'Fleurs', 'Bijoux', 'Médicaments']
        produits_import = ['Pétrole', 'Machines', 'Voitures', 'Riz', 'Produits chimiques']
        partenaires = ['UE', 'USA', 'Afrique du Sud', 'Inde', 'Chine', 'Madagascar']
        
        data = []
        for date in dates:
            # Exportations
            export_total = random.uniform(0.4, 0.8)  # Milliards USD
            # Importations
            import_total = random.uniform(0.6, 1.0)  # Milliards USD
            
            data.append({
                'date': date,
                'exportations': export_total,
                'importations': import_total,
                'balance_commerciale': export_total - import_total,
                'principal_produit_export': random.choice(produits_export),
                'principal_produit_import': random.choice(produits_import),
                'principal_partenaire': random.choice(partenaires)
            })
        
        return pd.DataFrame(data)
    
    def initialize_investment_data(self):
        """Initialise les données d'investissement"""
        types_investissement = ['IRS', 'REIS', 'PDS', 'Fintech', 'Manufacturing', 'Tourisme', 'Immobilier']
        pays_investisseurs = ['France', 'Chine', 'Afrique du Sud', 'Inde', 'Royaume-Uni', 'USA']
        
        data = []
        for i in range(200):  # 200 projets d'investissement simulés
            date = datetime(2014, 1, 1) + timedelta(days=random.randint(0, 3650))
            montant = random.uniform(1, 100)  # Millions USD
            
            data.append({
                'date_approbation': date,
                'type_investissement': random.choice(types_investissement),
                'montant_usd_millions': montant,
                'pays_origine': random.choice(pays_investisseurs),
                'emplois_crees': int(montant * random.uniform(2, 10)),
                'secteur': random.choice(list(self.secteurs.keys())),
                'statut': random.choices(['Approuvé', 'En cours', 'Terminé'], weights=[0.3, 0.5, 0.2])[0]
            })
        
        return pd.DataFrame(data)
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        # Simulation de mises à jour économiques
        dernier_pib = self.economic_data.iloc[-1]['croissance_pib']
        nouvelle_croissance = dernier_pib + random.uniform(-0.1, 0.1)
        
        # Ajout de nouvelles données mensuelles si nécessaire
        derniere_date = self.economic_data['date'].max()
        if datetime.now() - derniere_date > timedelta(days=30):
            nouvelle_date = derniere_date + timedelta(days=30)
            
            nouvelle_ligne = {
                'date': nouvelle_date,
                'pib_mensuel': self.economic_data.iloc[-1]['pib_mensuel'] * (1 + nouvelle_croissance/100),
                'croissance_pib': nouvelle_croissance,
                'inflation': random.uniform(2.5, 5.5),
                'taux_chomage': random.uniform(6.5, 8.5),
                'taux_change_usd': random.uniform(38, 42),
                'reserves_devises': random.uniform(6, 7.5),
                'dette_publique': random.uniform(65, 72)
            }
            
            self.economic_data = pd.concat([self.economic_data, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🏝️ Dashboard Économique Île Maurice</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="live-badge">🔴 DONNÉES ÉCONOMIQUES EN TEMPS RÉEL</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Surveillance et analyse des performances économiques de l'Île Maurice**")
            st.markdown('<div class="mauritius-flag"></div>', unsafe_allow_html=True)
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés économiques"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS ÉCONOMIQUES CLÉS</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques à partir des dernières données
        derniere_data = self.economic_data.iloc[-1]
        derniers_touristes = self.tourism_data.iloc[-1]
        derniers_echanges = self.trade_data.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Croissance du PIB",
                f"{derniere_data['croissance_pib']:.1f}%",
                f"{random.uniform(-0.5, 0.5):.1f}% vs trimestre précédent"
            )
        
        with col2:
            st.metric(
                "Taux d'Inflation",
                f"{derniere_data['inflation']:.1f}%",
                f"{random.uniform(-0.3, 0.3):.1f}% vs mois précédent",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "Arrivées Touristiques Mensuelles",
                f"{derniers_touristes['arrivees_touristes']:,.0f}",
                f"{random.randint(-5000, 10000):+,} vs mois précédent"
            )
        
        with col4:
            balance_commerciale = derniers_echanges['balance_commerciale']
            st.metric(
                "Balance Commerciale",
                f"{balance_commerciale:.2f} Md USD",
                f"{'Excédent' if balance_commerciale > 0 else 'Déficit'}"
            )
    
    def create_economic_overview(self):
        """Crée la vue d'ensemble économique"""
        st.markdown('<h3 class="section-header">🏛️ VUE D\'ENSEMBLE ÉCONOMIQUE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Indicateurs Macro", "Secteurs Économiques", "Commerce Extérieur", "Tourisme"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution du PIB
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='croissance_pib',
                             title='Évolution de la Croissance du PIB (%)',
                             color_discrete_sequence=['#1A206D'])
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Inflation et chômage
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Scatter(x=self.economic_data['date'], y=self.economic_data['inflation'],
                              name="Inflation", line=dict(color='#EA2839')),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=self.economic_data['date'], y=self.economic_data['taux_chomage'],
                              name="Chômage", line=dict(color='#FFD100')),
                    secondary_y=True,
                )
                fig.update_layout(title_text="Inflation et Taux de Chômage")
                fig.update_yaxes(title_text="Inflation (%)", secondary_y=False)
                fig.update_yaxes(title_text="Chômage (%)", secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition du PIB par secteur
                secteur_data = []
                for secteur, info in self.secteurs.items():
                    secteur_data.append({
                        'secteur': secteur,
                        'poids_pib': info['poids_pib'],
                        'croissance': info['croissance'],
                        'emplois': info['emplois']
                    })
                
                df_secteurs = pd.DataFrame(secteur_data)
                fig = px.pie(df_secteurs, 
                            values='poids_pib', 
                            names='secteur',
                            title='Répartition du PIB par Secteur (%)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Croissance par secteur
                fig = px.bar(df_secteurs, 
                            x='secteur', 
                            y='croissance',
                            title='Taux de Croissance par Secteur (%)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution du commerce extérieur
                fig = px.line(self.trade_data, 
                             x='date', 
                             y=['exportations', 'importations'],
                             title='Évolution des Exportations et Importations (Md USD)',
                             color_discrete_map={'exportations': '#28a745', 'importations': '#EA2839'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Balance commerciale
                fig = px.area(self.trade_data, 
                             x='date', 
                             y='balance_commerciale',
                             title='Balance Commerciale (Md USD)',
                             color_discrete_sequence=['#1A206D'])
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                # Arrivées touristiques
                fig = px.line(self.tourism_data, 
                             x='date', 
                             y='arrivees_touristes',
                             title='Évolution des Arrivées Touristiques Mensuelles',
                             color_discrete_sequence=['#FF6B00'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Recettes touristiques
                fig = px.line(self.tourism_data, 
                             x='date', 
                             y='recettes_tourisme',
                             title='Évolution des Recettes Touristiques (Millions USD)',
                             color_discrete_sequence=['#FFD100'])
                st.plotly_chart(fig, use_container_width=True)
    
    def create_sectors_analysis(self):
        """Analyse détaillée par secteur"""
        st.markdown('<h3 class="section-header">🏢 ANALYSE PAR SECTEUR DÉTAILLÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Performance Secteurs", "Emploi par Secteur", "Entreprises Clés"])
        
        with tab1:
            # Sélection du secteur à analyser
            secteur_selectionne = st.selectbox("Sélectionnez un secteur:", 
                                             list(self.secteurs.keys()))
            
            if secteur_selectionne:
                info_secteur = self.secteurs[secteur_selectionne]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Poids dans le PIB",
                        f"{info_secteur['poids_pib']}%",
                        f"{random.uniform(-0.5, 0.5):.1f}% vs année précédente"
                    )
                
                with col2:
                    st.metric(
                        "Taux de Croissance",
                        f"{info_secteur['croissance']}%",
                        f"{random.uniform(-1, 2):.1f}% vs année précédente"
                    )
                
                with col3:
                    st.metric(
                        "Emplois Directs",
                        f"{info_secteur['emplois']:,}",
                        f"{random.randint(-1000, 2000):+,} vs année précédente"
                    )
                
                st.markdown(f"**📋 Description:** {info_secteur['description']}")
                st.markdown(f"**🔮 Perspectives:** {info_secteur['perspectives']}")
                
                # Entreprises clés
                st.markdown("**🏢 Entreprises Clés:**")
                for entreprise in info_secteur['entreprises_cles']:
                    st.markdown(f"- {entreprise}")
        
        with tab2:
            # Emploi par secteur
            emploi_data = []
            for secteur, info in self.secteurs.items():
                emploi_data.append({
                    'secteur': secteur,
                    'emplois': info['emplois'],
                    'part_emploi_total': (info['emplois'] / sum([s['emplois'] for s in self.secteurs.values()])) * 100
                })
            
            df_emploi = pd.DataFrame(emploi_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(df_emploi, 
                            x='secteur', 
                            y='emplois',
                            title='Nombre d\'Emplois par Secteur',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(df_emploi, 
                            values='part_emploi_total', 
                            names='secteur',
                            title='Répartition de l\'Emploi par Secteur (%)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Carte des entreprises mauriciennes
            st.subheader("Carte des Principales Entreprises Mauriciennes")
            
            entreprises_data = []
            for secteur, info in self.secteurs.items():
                for entreprise in info['entreprises_cles']:
                    entreprises_data.append({
                        'entreprise': entreprise,
                        'secteur': secteur,
                        'chiffre_affaires_estime': random.uniform(10, 500),  # Millions USD
                        'employes': random.randint(100, 5000),
                        'localisation': random.choice(['Port-Louis', 'Ebène', 'Curepipe', 'Quatre-Bornes', 'Rose-Hill'])
                    })
            
            df_entreprises = pd.DataFrame(entreprises_data)
            st.dataframe(df_entreprises, use_container_width=True)
    
    def create_investment_analysis(self):
        """Analyse des investissements"""
        st.markdown('<h3 class="section-header">💼 INVESTISSEMENTS ET DÉVELOPPEMENT</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Projets d'Investissement", "Pays Investisseurs", "Secteurs Privilégiés"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Investissements par type
                invest_par_type = self.investment_data.groupby('type_investissement').agg({
                    'montant_usd_millions': 'sum',
                    'emplois_crees': 'sum'
                }).reset_index()
                
                fig = px.bar(invest_par_type, 
                            x='type_investissement', 
                            y='montant_usd_millions',
                            title='Investissements par Type (Millions USD)',
                            color='type_investissement',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Évolution temporelle des investissements
                invest_temporel = self.investment_data.groupby(
                    self.investment_data['date_approbation'].dt.year
                )['montant_usd_millions'].sum().reset_index()
                
                fig = px.line(invest_temporel, 
                             x='date_approbation', 
                             y='montant_usd_millions',
                             title='Évolution des Investissements Annuels',
                             markers=True,
                             color_discrete_sequence=['#1A206D'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Investissements par pays
                invest_par_pays = self.investment_data.groupby('pays_origine').agg({
                    'montant_usd_millions': 'sum',
                    'emplois_crees': 'sum'
                }).reset_index()
                
                fig = px.pie(invest_par_pays, 
                            values='montant_usd_millions', 
                            names='pays_origine',
                            title='Répartition des Investissements par Pays d\'Origine')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top 10 des plus gros investissements
                top_investissements = self.investment_data.nlargest(10, 'montant_usd_millions')
                fig = px.bar(top_investissements, 
                            x='montant_usd_millions', 
                            y='type_investissement',
                            orientation='h',
                            title='Top 10 des Plus Gros Investissements',
                            color='pays_origine',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse par secteur d'investissement
            invest_par_secteur = self.investment_data.groupby('secteur').agg({
                'montant_usd_millions': ['sum', 'count'],
                'emplois_crees': 'sum'
            }).round(2)
            invest_par_secteur.columns = ['montant_total', 'nombre_projets', 'emplois_total']
            invest_par_secteur = invest_par_secteur.reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(invest_par_secteur, 
                            x='secteur', 
                            y='montant_total',
                            title='Investissements par Secteur (Millions USD)',
                            color='secteur',
                            color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(invest_par_secteur, 
                               x='montant_total', 
                               y='emplois_total',
                               size='nombre_projets',
                               color='secteur',
                               title='Relation Investissements vs Emplois Créés',
                               hover_name='secteur',
                               size_max=40,
                               color_discrete_map={secteur: info['couleur'] for secteur, info in self.secteurs.items()})
                st.plotly_chart(fig, use_container_width=True)
    
    def create_regional_analysis(self):
        """Analyse régionale et infrastructure"""
        st.markdown('<h3 class="section-header">🗺️ DÉVELOPPEMENT RÉGIONAL ET INFRASTRUCTURE</h3>', 
                   unsafe_allow_html=True)
        
        # Données régionales simulées
        regions_data = {
            'Région': ['Port-Louis', 'Plaines Wilhems', 'Nord', 'Sud', 'Est', 'Ouest', 'Îles'],
            'Population': [150000, 400000, 120000, 110000, 100000, 130000, 5000],
            'PIB_Regional': [4.5, 6.2, 1.8, 1.5, 1.2, 2.1, 0.1],
            'Taux_Chomage': [8.2, 7.1, 9.5, 10.2, 11.1, 8.8, 12.5],
            'Investissements_Recents': [1200, 800, 350, 280, 320, 450, 50]
        }
        
        df_regions = pd.DataFrame(regions_data)
        
        tab1, tab2, tab3 = st.tabs(["Carte Économique", "Infrastructures", "Développement Régional"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # PIB par région
                fig = px.bar(df_regions, 
                            x='Région', 
                            y='PIB_Regional',
                            title='PIB par Région (Milliards USD)',
                            color='Région',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Chômage par région
                fig = px.bar(df_regions, 
                            x='Région', 
                            y='Taux_Chomage',
                            title='Taux de Chômage par Région (%)',
                            color='Taux_Chomage',
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Infrastructures Clés de l'Île Maurice")
            
            infrastructures = [
                {'Nom': 'Port Louis Harbour', 'Type': 'Port', 'Capacité': 'Container 600k/an', 'Région': 'Port-Louis'},
                {'Nom': 'Aéroport SSR', 'Type': 'Aéroport', 'Capacité': '4M passagers/an', 'Région': 'Plaines Wilhems'},
                {'Nom': 'Metro Express', 'Type': 'Transport', 'Capacité': '60k passagers/jour', 'Région': 'Plaines Wilhems'},
                {'Nom': 'Bagatelle Dam', 'Type': 'Eau', 'Capacité': '14Mm³', 'Région': 'Plaines Wilhems'},
                {'Nom': 'CT Power', 'Type': 'Énergie', 'Capacité': '110 MW', 'Région': 'Port-Louis'},
            ]
            
            for infra in infrastructures:
                with st.expander(f"🏗️ {infra['Nom']} - {infra['Type']}"):
                    st.write(f"**Région:** {infra['Région']}")
                    st.write(f"**Capacité:** {infra['Capacité']}")
                    st.write(f"**Statut:** {random.choice(['Opérationnel', 'En expansion', 'En maintenance'])}")
        
        with tab3:
            st.subheader("Projets de Développement Régional")
            
            projets = [
                {'Nom': 'Smart City Île Maurice', 'Région': 'Multiple', 'Budget': '2.5 Md USD', 'Échéance': '2030'},
                {'Nom': 'Port Louis Waterfront', 'Région': 'Port-Louis', 'Budget': '500 M USD', 'Échéance': '2025'},
                {'Nom': 'Côte d\'Or Sport City', 'Région': 'Plaines Wilhems', 'Budget': '300 M USD', 'Échéance': '2024'},
                {'Nom': 'Rivière Noire Resort', 'Région': 'Ouest', 'Budget': '200 M USD', 'Échéance': '2026'},
            ]
            
            for projet in projets:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{projet['Nom']}**")
                    st.write(f"Région: {projet['Région']}")
                with col2:
                    st.write(f"Budget: {projet['Budget']}")
                with col3:
                    progress = random.randint(20, 80)
                    st.write(f"Progression: {progress}%")
                    st.progress(progress)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres temporels
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime(2020, 1, 1))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Filtres secteurs
        st.sidebar.markdown("### 🏢 Filtres sectoriels")
        secteurs_selectionnes = st.sidebar.multiselect(
            "Secteurs à afficher:",
            list(self.secteurs.keys()),
            default=list(self.secteurs.keys())[:4]
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        
        # Bouton de rafraîchissement manuel
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        # Informations Île Maurice
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🇲🇺 ÎLE MAURICE")
        st.sidebar.markdown("""
        **Informations Clés:**
        - Population: 1.3 million
        - Superficie: 2,040 km²
        - PIB: 15.4 milliards USD
        - Croissance: 7.8%
        - Devise: Roupie mauricienne (MUR)
        """)
        
        # Indicateurs régionaux
        st.sidebar.markdown("### 🌍 COMPARAISON RÉGIONALE")
        indicateurs_region = {
            'Maurice': {'PIB/hab': 11200, 'Croissance': 7.8, 'Inflation': 4.2},
            'Réunion': {'PIB/hab': 25800, 'Croissance': 3.2, 'Inflation': 2.8},
            'Madagascar': {'PIB/hab': 520, 'Croissance': 4.4, 'Inflation': 8.6},
            'Seychelles': {'PIB/hab': 15600, 'Croissance': 8.8, 'Inflation': 3.1}
        }
        
        for pays, data in indicateurs_region.items():
            st.sidebar.metric(
                pays,
                f"{data['PIB/hab']:,} USD/hab",
                f"{data['Croissance']}% croissance"
            )
        
        return {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'secteurs_selectionnes': secteurs_selectionnes,
            'auto_refresh': auto_refresh,
            'show_projections': show_projections
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Économie", 
            "🏢 Secteurs", 
            "💼 Investissements", 
            "🗺️ Régions", 
            "💡 Perspectives",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_economic_overview()
        
        with tab2:
            self.create_sectors_analysis()
        
        with tab3:
            self.create_investment_analysis()
        
        with tab4:
            self.create_regional_analysis()
        
        with tab5:
            st.markdown("## 💡 PERSPECTIVES ET RECOMMANDATIONS STRATÉGIQUES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 POINTS FORTS
                
                **💎 Diversification Économique:**
                - Transition réussie vers services et technologies
                - Réduction de la dépendance au sucre et textile
                - Développement du secteur financier international
                
                **🌍 Position Géostratégique:**
                - Porte d'entrée vers l'Afrique
                - Stabilité politique reconnue
                - Cadre juridique favorable aux affaires
                
                **👨‍💼 Capital Humain:**
                - Main d'œuvre qualifiée multilingue
                - Système éducatif de qualité
                - Ouverture internationale
                """)
            
            with col2:
                st.markdown("""
                ### 🚨 DÉFIS À RELEVER
                
                **⚡ Compétitivité:**
                - Coûts de production élevés
                - Concurrence régionale croissante
                - Dépendance énergétique
                
                **🌱 Développement Durable:**
                - Gestion des ressources naturelles
                - Adaptation au changement climatique
                - Préservation de la biodiversité
                
                **🏗️ Infrastructures:**
                - Modernisation des transports
                - Développement numérique
                - Aménagement du territoire
                """)
            
            st.markdown("""
            ### 📋 RECOMMANDATIONS STRATÉGIQUES
            
            1. **Innovation Continue:** Renforcer les secteurs technologiques et digitaux
            2. **Durabilité:** Développer l'économie verte et bleue
            3. **Formation:** Investir dans le capital humain et l'éducation
            4. **Connectivité:** Améliorer les infrastructures numériques et physiques
            5. **Partnerships:** Renforcer les collaborations régionales et internationales
            """)
        
        with tab6:
            st.markdown("## 📋 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse économique complète de l'Île Maurice,
            couvrant les principaux indicateurs et secteurs de l'économie mauricienne.
            
            **Sources des données:**
            - Statistics Mauritius
            - Bank of Mauritius
            - Ministry of Finance
            - Economic Development Board
            - World Bank & IMF
            
            **Période couverte:**
            - Données historiques: 2014-2024
            - Projections et tendances
            - Analyses sectorielles détaillées
            
            **⚠️ Note:** 
            Les données présentées sont simulées pour la démonstration.
            Les données réelles sont disponibles sur les sites officiels des institutions mauriciennes.
            
            **🔒 Confidentialité:** 
            Toutes les données sensibles sont anonymisées.
            """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Contact:**
            - Economic Development Board: www.edbmauritius.org
            - Statistics Mauritius: statsmauritius.govmu.org
            - Bank of Mauritius: bom.mu
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(30)  # Rafraîchissement toutes les 30 secondes
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = MauritiusDashboard()
    dashboard.run_dashboard()