# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Analisi Dividendi ENAV",
    page_icon="✈️",
    layout="wide"
)

# --- Dati Chiave Estratti ---
TICKER = "ENAV.MI"
NOME_SOCIETA = "ENAV S.p.A."
SETTORE = "Infrastrutture di Trasporto - Controllo del Traffico Aereo"
ULTIMO_DPS_PAGATO_VAL = 0.23  # Relativo all'esercizio 2023
ANNO_ULTIMO_DPS = 2023
PREZZO_RIFERIMENTO_APPROX = 3.60  # Prezzo attuale approssimativo
POLITICA_PAYOUT = "80% del Free Cash Flow"
DPS_ATTESO_2024_VAL = 0.27  # Proposto per esercizio 2024
CRESCITA_ATTESA_DPS_2024 = "+17.4%"  # Crescita rispetto al 2023
YIELD_ATTUALE = round((ULTIMO_DPS_PAGATO_VAL / PREZZO_RIFERIMENTO_APPROX) * 100, 2)
YIELD_FORWARD = round((DPS_ATTESO_2024_VAL / PREZZO_RIFERIMENTO_APPROX) * 100, 2)

# Dati storici Dividendo Per Azione (DPS)
dps_storico_data = {
    'Anno Esercizio': [2019, 2020, 2021, 2022, 2023, 2024],
    'DPS (€)': [0.0, 0.0, 0.1081, 0.1967, 0.23, 0.27],  # 2024 proposto
    'Nota': ['Pre-Covid', 'Covid (Cancellato)', 'Ripresa', 'Crescita', 'Record', 'Proposto'],
    'Tipo': ['Storico', 'Storico', 'Storico', 'Storico', 'Storico', 'Proposto']
}
df_dps = pd.DataFrame(dps_storico_data)

# Dati Finanziari Chiave
fin_data = {
    'Metrica': [
        'Ricavi Totali (€M)',
        'EBITDA (€M)',
        'Utile Netto (€M)',
        'EPS Diluito (€)',
        'Cash Flow Operativo (CFO, €M)',
        'Capex (€M)',
        'Free Cash Flow (FCF, €M)',
        'Debito Netto / EBITDA (Leva)',
        'Dividendo per Azione (DPS, €)'
    ],
    '2019': [
        911.91,  # Revenue
        312.27,  # EBITDA
        118.43,  # Net Income
        0.22,    # Diluted EPS
        341.63,  # CFO
        -101.76, # Capex
        225.32,  # FCF
        'Cassa Netta', # Leva
        0.0      # DPS
    ],
    '2020': [
        780.87,  # Revenue
        210.42,  # EBITDA
        54.28,   # Net Income
        0.10,    # Diluted EPS
        -173.06, # CFO
        -74.0,   # Capex
        -264.55, # FCF
        '1.45x', # Leva
        0.0      # DPS (cancellato)
    ],
    '2021': [
        845.11,  # Revenue
        238.83,  # EBITDA
        78.37,   # Net Income
        0.14,    # Diluted EPS
        -157.15, # CFO
        -71.50,  # Capex
        -242.78, # FCF
        '1.85x', # Leva
        0.1081   # DPS
    ],
    '2022': [
        952.78,  # Revenue
        284.38,  # EBITDA
        105.0,   # Net Income
        0.19,    # Diluted EPS
        236.90,  # CFO
        -79.76,  # Capex
        139.13,  # FCF
        '1.1x',  # Leva
        0.1967   # DPS
    ],
    '2023': [
        1011.31, # Revenue
        313.23,  # EBITDA
        112.92,  # Net Income
        0.21,    # Diluted EPS
        210.62,  # CFO
        -83.83,  # Capex
        100.14,  # FCF
        '0.8x',  # Leva
        0.23     # DPS
    ],
    '2024E': [
        1037.0,  # Revenue (stima)
        311.0,   # EBITDA (stima)
        126.0,   # Net Income (stima)
        0.23,    # Diluted EPS (stima)
        257.44,  # CFO (stima)
        -85.0,   # Capex (stima)
        199.0,   # FCF (stima da piano industriale)
        '<0.8x', # Leva (stima)
        0.27     # DPS proposto
    ]
}
df_fin = pd.DataFrame(fin_data)

# Creazione di un DataFrame più pulito per grafici finanziari
df_fin_clean = pd.DataFrame({
    'Anno': ['2019', '2020', '2021', '2022', '2023', '2024E'],
    'Ricavi (€M)': [911.91, 780.87, 845.11, 952.78, 1011.31, 1037.0],
    'EBITDA (€M)': [312.27, 210.42, 238.83, 284.38, 313.23, 311.0],
    'Utile Netto (€M)': [118.43, 54.28, 78.37, 105.0, 112.92, 126.0],
    'EPS (€)': [0.22, 0.10, 0.14, 0.19, 0.21, 0.23],
    'FCF (€M)': [225.32, -264.55, -242.78, 139.13, 100.14, 199.0],
    'DPS (€)': [0.0, 0.0, 0.1081, 0.1967, 0.23, 0.27]
})

# Calcoliamo il payout ratio (DPS/EPS e DPS/FCF)
df_payout = pd.DataFrame({
    'Anno': [2019, 2020, 2021, 2022, 2023, 2024],
    'EPS (€)': [0.22, 0.10, 0.14, 0.19, 0.21, 0.23],
    'DPS (€)': [0.0, 0.0, 0.1081, 0.1967, 0.23, 0.27],
    'FCF per Share (€)': [0.42, -0.49, -0.45, 0.26, 0.19, 0.37]
})

df_payout['Payout Ratio (% di EPS)'] = (df_payout['DPS (€)'] / df_payout['EPS (€)']) * 100
df_payout['Payout Ratio (% di FCF)'] = (df_payout['DPS (€)'] / df_payout['FCF per Share (€)']) * 100
df_payout.loc[df_payout['FCF per Share (€)'] <= 0, 'Payout Ratio (% di FCF)'] = 0  # Gestisce divisione per zero o FCF negativo

# Dati proiezione dividendi futuri basati sul piano industriale
df_dps_projection = pd.DataFrame({
    'Anno': [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029],
    'DPS (€)': [0.0, 0.0, 0.1081, 0.1967, 0.23, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32],
    'Tipo': ['Storico', 'Storico', 'Storico', 'Storico', 'Storico', 'Proposto', 'Piano', 'Piano', 'Piano', 'Piano', 'Piano']
})

# Dati Yield annuale
df_yield = pd.DataFrame({
    'Anno': ['2021', '2022', '2023', '2024E'],
    'Dividend Yield (%)': [2.7, 5.5, 6.4, 7.0],
})

# Dati per reset regolatorio e EBITDA
df_ebitda_reset = pd.DataFrame({
    'Anno': ['2023', '2024E', '2025E', '2026E', '2027E', '2028E', '2029E'],
    'EBITDA (€M)': [313.23, 311.0, 225.0, 246.0, 285.0, 325.0, 361.0],
    'Fase': ['Attuale', 'Attuale', 'Post-Reset', 'Recupero', 'Recupero', 'Recupero', 'Recupero']
})

# Dati per confronto yield con peers
df_yield_comp = pd.DataFrame({
    'Società': ['ENAV', 'Media Utilities IT', 'FTSE MIB', 'BTP 10Y', 'Media Infrastr. UE'],
    'Dividend Yield 2024E (%)': [7.0, 5.2, 4.5, 3.8, 4.1]
})

# Dati per composizione ricavi (regolati vs non regolati)
df_revenue_split_current = pd.DataFrame({
    'Segmento': ['Attività Regolamentate (En-route)', 'Attività Regolamentate (Terminal)', 'Attività Non Regolamentate'],
    'Ricavi 2023 (%)': [65, 30, 5]
})

df_revenue_split_future = pd.DataFrame({
    'Segmento': ['Attività Regolamentate (En-route)', 'Attività Regolamentate (Terminal)', 'Attività Non Regolamentate'],
    'Ricavi 2029E (%)': [60, 31, 9]
})

# Dati per impatto target 2025-2029
df_targets = pd.DataFrame({
    'Metrica': ['Ricavi', 'EBITDA', 'Utile Netto', 'FCF Cumulato', 'Dividendi Cumulati', 'Debt/EBITDA'],
    '2024': [1037, 311, 126, 'N/A', 'N/A', 0.8],
    '2029 Target': [1200, 361, 165, '€1 Mld', '€813M', 0.0],
    'CAGR/Diff': ['+3%', '+3% (+13% dal 2025)', '+6%', '€200M/anno medio', '€160M/anno medio', '-0.8x']
})

# Rischi e punti di forza
rischi = [
    "Reset regolatorio RP4 (2025): temporanea flessione dell'EBITDA del 28% nel 2025",
    "Potenziali eventi straordinari sul traffico aereo (come accaduto con COVID-19)",
    "Rischi esecutivi nelle iniziative di crescita non regolamentate",
    "Rischi legati alle acquisizioni M&A programmate (fino a €350M)",
    "Rischio di variazioni nei parametri regolatori che potrebbero influenzare la redditività"
]

punti_forza = [
    "Politica dividendi chiara: 80% del Free Cash Flow",
    "Dividend yield competitivo: >6% ai prezzi attuali (tra i più alti del FTSE MIB)",
    "Crescita annua programmata del dividendo (circa +4% annuo dal 2024 al 2029)",
    "Meccanismi regolatori che proteggono da inflazione e variazioni di traffico",
    "Previsione di generazione di €1 Miliardo di FCF nel periodo 2025-2029",
    "WACC regolatorio più elevato nel nuovo periodo (6.7% vs 4.4% precedente)"
]

# --- Titolo e Header ---
st.title(f"✈️ Analisi Dividendi: {NOME_SOCIETA} ({TICKER})")
st.caption(f"Analisi aggiornata al: {datetime.now().strftime('%d/%m/%Y')}. Dati finanziari storici fino al 2023, stime 2024, e Piano Industriale 2025-2029.")
st.markdown("---")

# --- Metriche Chiave Dividendo ---
st.subheader("📊 Indicatori Chiave del Dividendo")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label=f"Ultimo DPS Pagato (Esercizio {ANNO_ULTIMO_DPS})",
        value=f"€ {ULTIMO_DPS_PAGATO_VAL:.4f}",
        help="Dividendo relativo all'esercizio 2023, pagato nel 2024."
    )
with col2:
    st.metric(
        label=f"Dividend Yield (Attuale)",
        value=f"{YIELD_ATTUALE:.2f}%",
        help=f"Basato sull'ultimo DPS (€{ULTIMO_DPS_PAGATO_VAL:.4f}) e un prezzo di riferimento di €{PREZZO_RIFERIMENTO_APPROX:.2f}."
    )
with col3:
    st.metric(
        label="Politica di Payout",
        value=POLITICA_PAYOUT,
        help="Politica dichiarata dalla società per la distribuzione del free cash flow."
    )
with col4:
    st.metric(
        label="DPS Proposto (Esercizio 2024)",
        value=f"€ {DPS_ATTESO_2024_VAL:.4f}",
        delta=CRESCITA_ATTESA_DPS_2024,
        help=f"Dividendo proposto per l'esercizio 2024, con un incremento del 17.4% rispetto al 2023."
    )
st.markdown("---")

# --- Grafici Dividendi ---
st.subheader("📈 Analisi del Dividendo")

# Layout a 2 colonne per i grafici
col1, col2 = st.columns(2)

# GRAFICO 1: Storico DPS - nella prima colonna
with col1:
    fig_dps = px.bar(
        df_dps,
        x='Anno Esercizio',
        y='DPS (€)',
        title="Evoluzione del Dividendo per Azione ENAV (2019-2024)",
        text='DPS (€)',
        color='Tipo',
        color_discrete_map={'Storico': 'royalblue', 'Proposto': 'green'},
        barmode='group'
    )
    
    # Aggiunta di annotazioni per spiegare gli eventi chiave
    fig_dps.add_annotation(
        x=2020, y=0.01,
        text="Cancellato<br>per Covid-19",
        showarrow=True,
        font=dict(size=10, color="red"),
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        ax=-20, ay=-30
    )
    
    fig_dps.add_annotation(
        x=2022, y=0.22,
        text="Ripresa e<br>crescita post-Covid",
        showarrow=True,
        font=dict(size=10),
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        ax=20, ay=-30
    )
    
    fig_dps.update_traces(texttemplate='€%{y:.4f}', textposition="outside")
    fig_dps.update_layout(
        xaxis_title="Anno Esercizio Fiscale", 
        yaxis_title="Dividendo per Azione (€)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_dps, use_container_width=True)

# GRAFICO 2: Dividend Yield - nella seconda colonna
with col2:
    fig_yield = px.bar(
        df_yield,
        x='Anno',
        y='Dividend Yield (%)',
        title="Andamento del Dividend Yield",
        text='Dividend Yield (%)',
        color='Dividend Yield (%)',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_yield.update_traces(texttemplate='%{y:.1f}%', textposition="outside")
    fig_yield.update_layout(xaxis_title="Anno", yaxis_title="Dividend Yield (%)")
    st.plotly_chart(fig_yield, use_container_width=True)
    
st.caption("Fonte: Dati estratti dall'analisi e dalle relazioni finanziarie. Si nota la progressiva crescita del dividendo e del yield dopo la cancellazione dovuta alla pandemia.")
st.markdown("---")

# --- Sezione Sostenibilità del Dividendo ---
st.subheader("📊 Sostenibilità e Proiezioni del Dividendo")

# Layout a 2 colonne per i grafici
col1, col2 = st.columns(2)

# GRAFICO 3: Payout Ratio - nella prima colonna
with col1:
    fig_payout = px.bar(
        df_payout[df_payout['DPS (€)'] > 0],  # Esclude gli anni senza dividendi
        x='Anno',
        y='Payout Ratio (% di EPS)',
        title="Payout Ratio (DPS/EPS) %",
        text='Payout Ratio (% di EPS)',
        color='Payout Ratio (% di EPS)',
        color_continuous_scale=px.colors.sequential.Greens
    )
    fig_payout.update_traces(texttemplate='%{y:.1f}%', textposition="outside")
    fig_payout.update_layout(xaxis_title="Anno", yaxis_title="Payout Ratio (% dell'EPS)")
    
    # Aggiungi linea target policy
    fig_payout.add_shape(
        type="line",
        x0=df_payout['Anno'].min()-0.5,
        x1=df_payout['Anno'].max()+0.5,
        y0=80,
        y1=80,
        line=dict(color="red", width=2, dash="dash"),
    )
    fig_payout.add_annotation(
        x=2024,
        y=85,
        text="Target Payout: 80% del FCF",
        showarrow=False,
        font=dict(color="red")
    )
    
    st.plotly_chart(fig_payout, use_container_width=True)

# GRAFICO 4: FCF vs Dividend Paid - nella seconda colonna
with col2:
    # Calcoliamo i dividendi totali pagati (DPS * numero azioni approssimative - 541.74M azioni)
    azioni_totali = 541.74  # milioni

    df_fcf_div = pd.DataFrame({
        'Anno': [2021, 2022, 2023, 2024],
        'FCF (€M)': [-242.78, 139.13, 100.14, 199.0],
        'Dividendi Totali Pagati (€M)': [
            0.1081 * azioni_totali,
            0.1967 * azioni_totali,
            0.23 * azioni_totali,
            0.27 * azioni_totali
        ]
    })
    
    df_fcf_div['Dividendi Totali Pagati (€M)'] = df_fcf_div['Dividendi Totali Pagati (€M)'].round(1)
    
    # Calcoliamo la copertura FCF solo per gli anni con FCF positivo
    df_fcf_div['Copertura FCF'] = 0.0
    mask = df_fcf_div['FCF (€M)'] > 0
    df_fcf_div.loc[mask, 'Copertura FCF'] = (df_fcf_div.loc[mask, 'FCF (€M)'] / df_fcf_div.loc[mask, 'Dividendi Totali Pagati (€M)']).round(2)
    
    fig_fcf_div = go.Figure()
    fig_fcf_div.add_trace(go.Bar(
        x=df_fcf_div['Anno'],
        y=df_fcf_div['FCF (€M)'],
        name='Free Cash Flow',
        marker_color='royalblue'
    ))
    fig_fcf_div.add_trace(go.Bar(
        x=df_fcf_div['Anno'],
        y=df_fcf_div['Dividendi Totali Pagati (€M)'],
        name='Dividendi Pagati',
        marker_color='darkgreen'
    ))
    
    # Aggiungiamo la linea di Copertura FCF solo per gli anni con FCF positivo
    y_values = df_fcf_div['Copertura FCF'] * 100  # Scala per visualizzazione
    fig_fcf_div.add_trace(go.Scatter(
        x=df_fcf_div.loc[mask, 'Anno'],
        y=y_values[mask],
        name='Copertura FCF (volte)',
        mode='lines+markers+text',
        text=df_fcf_div.loc[mask, 'Copertura FCF'],
        textposition="top center",
        yaxis='y2',
        line=dict(color='red', width=2)
    ))
    
    fig_fcf_div.update_layout(
        title="Free Cash Flow vs Dividendi Pagati",
        barmode='group',
        xaxis_title="Anno",
        yaxis_title="Milioni di €",
        yaxis2=dict(
            title="Copertura FCF (volte)",
            overlaying="y",
            side="right",
            range=[0, 3],
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Aggiungiamo annotazione per spiegare il FCF negativo nel 2021
    fig_fcf_div.add_annotation(
        x=2021, y=-242.78/2,
        text="FCF negativo<br>post-Covid",
        showarrow=True,
        font=dict(color="white"),
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        ax=40, ay=0
    )
    
    st.plotly_chart(fig_fcf_div, use_container_width=True)

st.caption("Fonte: Elaborazione su dati finanziari. I grafici mostrano il payout ratio rispetto alla politica dichiarata (80% del FCF) e la capacità del FCF di coprire i dividendi distribuiti. Nel 2021 il FCF era negativo a causa degli impatti COVID, ma la società ha comunque ripreso la distribuzione dei dividendi con un approccio progressivo.")
st.markdown("---")

# --- Proiezione Futura dei Dividendi ---
st.subheader("🔮 Proiezione Futura del Dividendo (Piano Industriale 2025-2029)")

fig_proj = px.line(
    df_dps_projection,
    x='Anno',
    y='DPS (€)',
    title="Dividendo per Azione: Storico e Proiezione Piano Industriale",
    markers=True,
    text='DPS (€)',
    color='Tipo',
    color_discrete_map={'Storico': 'royalblue', 'Proposto': 'green', 'Piano': 'orange'}
)
fig_proj.update_traces(texttemplate='€%{y:.4f}', textposition="top center")

# Aggiungi etichette e annotazioni
fig_proj.add_vrect(
    x0=2024.5, x1=2029.5, 
    fillcolor="lightgreen", opacity=0.2, 
    line_width=0
)

fig_proj.add_annotation(
    x=2027, y=0.31,
    text="Piano Industriale<br>2025-2029",
    showarrow=True,
    arrowhead=2,
    arrowcolor="green",
    arrowwidth=2,
    arrowsize=1,
    ax=0,
    ay=-40
)

fig_proj.add_annotation(
    x=2025, y=0.25,
    text="Reset Regolatorio RP4<br>inizio 2025",
    showarrow=True,
    arrowhead=2,
    arrowcolor="red",
    arrowwidth=2,
    arrowsize=1,
    ax=-40,
    ay=30
)

fig_proj.update_layout(xaxis_title="Anno", yaxis_title="Dividendo per Azione (€)")
st.plotly_chart(fig_proj, use_container_width=True)

# Aggiungiamo una spiegazione del reset regolatorio
st.info("""
**Reset Regolatorio RP4 (2025-2029)**: All'inizio del nuovo periodo regolatorio nel 2025, ENAV subirà un temporaneo calo dell'EBITDA (-28%), 
che è un fenomeno fisiologico dovuto all'azzeramento dei meccanismi di bilanciamento del traffico e al reset dei parametri economici. 
Nonostante questo, la società ha confermato che i dividendi continueranno a crescere anche durante questa fase,
grazie alla forte posizione di cassa e alla generazione di Free Cash Flow.
""")

col1, col2 = st.columns(2)

# GRAFICO 5: Reset Regolatorio e EBITDA
with col1:
    fig_reset = px.line(
        df_ebitda_reset,
        x='Anno',
        y='EBITDA (€M)',
        title="EBITDA e Impatto Reset Regolatorio RP4",
        markers=True,
        text='EBITDA (€M)',
        color='Fase',
        color_discrete_map={'Attuale': 'blue', 'Post-Reset': 'red', 'Recupero': 'green'}
    )
    fig_reset.update_traces(texttemplate='%{y}M', textposition="top center")
    fig_reset.add_annotation(
        x='2025E', y=225,
        text="Reset -28%",
        showarrow=True,
        arrowhead=2,
        arrowwidth=2,
        arrowsize=1,
        ax=0,
        ay=30
    )
    fig_reset.add_annotation(
        x='2029E', y=361,
        text="CAGR +12.5%<br>dal 2025",
        showarrow=True,
        arrowhead=2,
        arrowwidth=2,
        arrowsize=1,
        ax=0,
        ay=-40
    )
    fig_reset.update_layout(xaxis_title="Anno", yaxis_title="EBITDA (€M)")
    st.plotly_chart(fig_reset, use_container_width=True)

# GRAFICO 6: Confronto Yield
with col2:
    fig_yield_comp = px.bar(
        df_yield_comp,
        x='Società',
        y='Dividend Yield 2024E (%)',
        title="Confronto Dividend Yield con altri Investimenti (2024E)",
        text='Dividend Yield 2024E (%)',
        color='Dividend Yield 2024E (%)',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_yield_comp.update_traces(texttemplate='%{y:.1f}%', textposition="outside")
    fig_yield_comp.update_layout(xaxis_title="Società/Benchmark", yaxis_title="Dividend Yield (%)")
    st.plotly_chart(fig_yield_comp, use_container_width=True)

st.caption("Fonte: Elaborazione su dati del Piano Industriale 2025-2029 e stime di mercato. Nonostante il reset regolatorio del 2025 che impatterà temporaneamente l'EBITDA, ENAV ha confermato la crescita costante del dividendo per azione. Il dividend yield di ENAV risulta tra i più elevati sia nel FTSE MIB che tra le utilities e infrastrutture europee.")
st.markdown("---")

# --- Evoluzione Business Regolamentato vs Non-regolamentato ---
st.subheader("🏢 Evoluzione del Business e Crescita delle Attività Non Regolamentate")

col1, col2 = st.columns(2)

# GRAFICO 7: Composizione Ricavi Attuale
with col1:
    fig_rev_current = px.pie(
        df_revenue_split_current,
        values='Ricavi 2023 (%)',
        names='Segmento',
        title="Composizione Ricavi ENAV 2023",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    fig_rev_current.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_rev_current, use_container_width=True)

# GRAFICO 8: Composizione Ricavi Futura
with col2:
    fig_rev_future = px.pie(
        df_revenue_split_future,
        values='Ricavi 2029E (%)',
        names='Segmento',
        title="Previsione Composizione Ricavi ENAV 2029",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    fig_rev_future.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_rev_future, use_container_width=True)

st.info("""
**Focus sulle Attività Non Regolamentate**: ENAV punta a raddoppiare i ricavi da attività non regolamentate da €49M nel 2024 a €106M nel 2029, 
raggiungendo circa il 9% dei ricavi totali. Questo business include:

1. **Evoluzione del portfolio prodotti/servizi core** (67% dei ricavi non-regolati)
   - Digital Towers, Digital Academy, nuove funzionalità per centri di controllo

2. **Espansione geografica** (23% dei ricavi non-regolati)
   - Nuovi uffici pianificati in India (2025), Brasile e Arabia Saudita (2026)
   - Presenza in 87 paesi globalmente

3. **Nuovi business** (10% dei ricavi non-regolati)
   - **Droni**: certificazioni CISP e USSP uniche in Europa
   - **Energy Service Company**: servizi di efficientamento energetico
   - **Digital Academy**: piattaforma e-learning per formazione aeronautica
""")
st.markdown("---")

# --- Target Piano Industriale 2025-2029 ---
st.subheader("🎯 Obiettivi Finanziari Piano Industriale 2025-2029")

# Visualizzazione dei target come tabella
st.dataframe(df_targets.set_index('Metrica'), use_container_width=True)

# Spiegazione degli investimenti
st.markdown("""
### Investimenti per la Crescita (2025-2029)

ENAV ha pianificato investimenti per **€570 milioni** (+15% rispetto al periodo precedente) così suddivisi:
- **Navigazione e sistemi ATM**: 50% degli investimenti
- **Infrastrutture civili e sistemi**: 27% degli investimenti
- **ICT e altro**: 23% degli investimenti

Progetti strategici principali:
- Consolidamento dei centri di controllo (da 4 a 2)
- Implementazione di 26 torri remote digitali
- Aggiornamento sistemi di monitoraggio meteorologico

### Piano M&A

ENAV ha definito un piano di acquisizioni selettivo con fondi disponibili fino a **€350 milioni**, con focus su:
1. Licenze e servizi software
2. Servizi tecnici e di ingegneria
3. Consulenza avionica
4. Meteorologia
5. Tecnologie per droni e UTM (Unmanned Traffic Management)
""")
st.markdown("---")

# --- Punti di Forza e Rischi ---
st.subheader("✅ Elementi Distintivi per l'Investitore a Dividendo")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Punti di Forza")
    for i, punto in enumerate(punti_forza):
        st.markdown(f"**{i+1}.** {punto}")

with col2:
    st.markdown("### Rischi da Considerare")
    for i, rischio in enumerate(rischi):
        st.markdown(f"**{i+1}.** {rischio}")

st.markdown("---")

# --- Tabella Finanziaria Riassuntiva ---
st.subheader("🔢 Tabella Finanziaria Riassuntiva")
st.dataframe(df_fin.set_index('Metrica'), use_container_width=True)
st.caption("Fonte: Dati estratti dai report finanziari. I dati 2024 sono stime basate sul piano industriale e sulle proiezioni di analisti.")
st.markdown("---")

# --- Conclusioni per l'Investitore ---
st.subheader("📝 Conclusioni per l'Investitore orientato al Dividendo")

st.markdown("""
ENAV S.p.A. emerge come una società solida e cash-generative, con un ruolo essenziale nel sistema del traffico aereo italiano e una strategia ben definita per crescere nei prossimi anni. Per un investitore orientato ai dividendi, ENAV offre attualmente:

- **Rendimento elevato**: Dividend yield di circa 7%, tra i più alti del FTSE MIB
- **Crescita stabile**: Incremento programmato del dividendo di circa 4% annuo fino al 2029
- **Sostenibilità**: La politica di payout dell'80% del FCF è supportata dalla generazione di cassa
- **Visibilità**: Piano industriale chiaro fino al 2029 con obiettivi finanziari dettagliati
- **Resilienza**: Modello di business regolato con protezioni incorporate contro inflazione e volatilità

Il temporaneo calo dell'EBITDA previsto nel 2025 (dovuto al reset regolatorio) non dovrebbe impattare la politica dei dividendi grazie alla solida posizione finanziaria della società. Inoltre, l'espansione nelle attività non regolamentate offre un potenziale di crescita aggiuntivo senza compromettere la generazione di cassa destinata agli azionisti.

In un'ottica di lungo periodo, ENAV rappresenta una potenziale "yield play" interessante: un titolo difensivo, capace di offrire reddito ricorrente superiore alla media di mercato e con un moderato potenziale di crescita sia del dividendo sia del valore del capitale.
""")

st.markdown("---")
st.caption("Disclaimer: Questa è un'analisi basata sui dati forniti. Non costituisce consulenza finanziaria. Effettuare sempre le proprie ricerche prima di investire.")

# Aggiungi firma
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    <p style="font-style: italic; color: #888;">Analisi generata tramite Dividend App Generator</p>
</div>
""", unsafe_allow_html=True)