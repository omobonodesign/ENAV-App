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

# Dati storici Dividendo Per Azione (DPS) - CORRETTO per il 2019
dps_storico_data = {
    'Anno Esercizio': [2019, 2020, 2021, 2022, 2023, 2024],
    'DPS (€)': [0.21, 0.0, 0.1081, 0.1967, 0.23, 0.27],  # 2024 proposto, 2019 corretto
    'Nota': ['Pre-Covid', 'Covid (Cancellato)', 'Ripresa', 'Crescita', 'Record', 'Proposto'],
    'Tipo': ['Storico', 'Storico', 'Storico', 'Storico', 'Storico', 'Proposto']
}
df_dps = pd.DataFrame(dps_storico_data)

# Dati Finanziari Chiave - CORRETTO per il 2019
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
        0.21      # DPS - CORRETTO
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

# Creazione di un DataFrame più pulito per grafici finanziari - CORRETTO per il 2019
df_fin_clean = pd.DataFrame({
    'Anno': ['2019', '2020', '2021', '2022', '2023', '2024E'],
    'Ricavi (€M)': [911.91, 780.87, 845.11, 952.78, 1011.31, 1037.0],
    'EBITDA (€M)': [312.27, 210.42, 238.83, 284.38, 313.23, 311.0],
    'Utile Netto (€M)': [118.43, 54.28, 78.37, 105.0, 112.92, 126.0],
    'EPS (€)': [0.22, 0.10, 0.14, 0.19, 0.21, 0.23],
    'FCF (€M)': [225.32, -264.55, -242.78, 139.13, 100.14, 199.0],
    'DPS (€)': [0.21, 0.0, 0.1081, 0.1967, 0.23, 0.27]  # CORRETTO per il 2019
})

# Calcoliamo il payout ratio (DPS/EPS e DPS/FCF) - CORRETTO per il 2019
df_payout = pd.DataFrame({
    'Anno': [2019, 2020, 2021, 2022, 2023, 2024],
    'EPS (€)': [0.22, 0.10, 0.14, 0.19, 0.21, 0.23],
    'DPS (€)': [0.21, 0.0, 0.1081, 0.1967, 0.23, 0.27],  # CORRETTO per il 2019
    'FCF per Share (€)': [0.42, -0.49, -0.45, 0.26, 0.19, 0.37]
})

df_payout['Payout Ratio (% di EPS)'] = (df_payout['DPS (€)'] / df_payout['EPS (€)']) * 100
df_payout['Payout Ratio (% di FCF)'] = (df_payout['DPS (€)'] / df_payout['FCF per Share (€)']) * 100
df_payout.loc[df_payout['FCF per Share (€)'] <= 0, 'Payout Ratio (% di FCF)'] = 0  # Gestisce divisione per zero o FCF negativo

# Dati proiezione dividendi futuri basati sul piano industriale - CORRETTO per il 2019
df_dps_projection = pd.DataFrame({
    'Anno': [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029],
    'DPS (€)': [0.21, 0.0, 0.1081, 0.1967, 0.23, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32],  # CORRETTO per il 2019
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

# GRAFICO 1: Storico DPS - nella prima colonna - CORRETTO
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
        x=2019, y=0.21,
        text="Dividendo<br>pre-Covid",
        showarrow=True,
        font=dict(size=10, color="navy"),
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        ax=-20, ay=-20
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

# GRAFICO 3: Payout Ratio migliorato - nella prima colonna
with col1:
    # Creamo un grafico combinato che mostri entrambi i tipi di payout ratio
    fig_payout = go.Figure()
    
    # Filtriamo gli anni con dividendi positivi
    df_payout_filtered = df_payout[df_payout['DPS (€)'] > 0]
    
    # Aggiungiamo barre per il payout ratio rispetto all'EPS
    fig_payout.add_trace(go.Bar(
        x=df_payout_filtered['Anno'],
        y=df_payout_filtered['Payout Ratio (% di EPS)'],
        name='% dell\'EPS',
        text=df_payout_filtered['Payout Ratio (% di EPS)'].round(1).astype(str) + '%',
        textposition="outside",
        marker_color='rgba(0, 128, 0, 0.7)',
    ))
    
    # Aggiungiamo barre per il payout ratio rispetto al FCF dove FCF è positivo
    df_payout_fcf = df_payout_filtered[df_payout_filtered['FCF per Share (€)'] > 0]
    fig_payout.add_trace(go.Bar(
        x=df_payout_fcf['Anno'],
        y=df_payout_fcf['Payout Ratio (% di FCF)'],
        name='% del FCF',
        text=df_payout_fcf['Payout Ratio (% di FCF)'].round(1).astype(str) + '%',
        textposition="outside",
        marker_color='rgba(65, 105, 225, 0.7)',
        visible='legendonly'  # Inizialmente nascosto, attivabile dalla legenda
    ))
    
    # Aggiungiamo linea target policy (80% del FCF)
    fig_payout.add_shape(
        type="line",
        x0=df_payout_filtered['Anno'].min()-0.5,
        x1=df_payout_filtered['Anno'].max()+0.5,
        y0=80,
        y1=80,
        line=dict(color="red", width=2, dash="dash"),
    )
    
    fig_payout.add_annotation(
        x=df_payout_filtered['Anno'].max(),
        y=85,
        text="Target Payout: 80% del FCF",
        showarrow=False,
        font=dict(color="red")
    )
    
    # Aggiungiamo annotazione per spiegare il payout ratio alto nel 2021
    if df_payout_filtered['Anno'].min() <= 2021 <= df_payout_filtered['Anno'].max():
        eps_2021 = df_payout_filtered.loc[df_payout_filtered['Anno'] == 2021, 'Payout Ratio (% di EPS)'].values[0]
        if eps_2021 > 70:  # Solo se è un valore alto
            fig_payout.add_annotation(
                x=2021,
                y=eps_2021,
                text="EPS impattato<br>dal COVID",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor="green",
                ax=25,
                ay=-30
            )
    
    fig_payout.update_layout(
        title={
            'text': "Payout Ratio di ENAV",
            'font': {'size': 16}
        },
        xaxis_title="Anno",
        yaxis_title="Payout Ratio (%)",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            range=[0, max(df_payout_filtered['Payout Ratio (% di EPS)'].max(), 
                          df_payout_fcf['Payout Ratio (% di FCF)'].max() if not df_payout_fcf.empty else 0) * 1.15]
        )
    )
    
    st.plotly_chart(fig_payout, use_container_width=True)
    
    # Aggiungiamo una spiegazione più chiara sotto il grafico
    st.info("""
    **Note sul Payout Ratio:**
    - ENAV ha una politica di dividendi basata sull'80% del Free Cash Flow (FCF)
    - Il grafico mostra il dividendo come percentuale dell'Utile per Azione (EPS)
    - È possibile visualizzare anche il ratio basato sul FCF attivandolo dalla legenda (solo per anni con FCF positivo)
    - Nel 2021, il FCF era negativo a causa degli impatti COVID, ma la società ha comunque ripreso la distribuzione dei dividendi
    """)


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

# GRAFICO 5: Reset Regolatorio e EBITDA - Versione corretta
with col1:
    # Invece di usare barre per fase, usiamo un approccio più semplice con colori per fase
    # Questo evita i problemi di visualizzazione con le barre raggruppate
    
    # Mappatura dei colori per ogni fase
    color_map = {
        'Attuale': 'rgb(65, 105, 225)',      # Blu
        'Post-Reset': 'rgb(220, 20, 60)',    # Rosso
        'Recupero': 'rgb(46, 139, 87)'       # Verde
    }
    
    # Creiamo un array di colori basato sulla fase di ogni punto dati
    colors = [color_map[fase] for fase in df_ebitda_reset['Fase']]
    
    # Creiamo un grafico a barre semplice con colori diversi per ogni barra
    fig_reset = go.Figure()
    
    # Aggiungiamo le barre dell'EBITDA con colori personalizzati
    fig_reset.add_trace(go.Bar(
        x=df_ebitda_reset['Anno'],
        y=df_ebitda_reset['EBITDA (€M)'],
        marker_color=colors,
        text=df_ebitda_reset['EBITDA (€M)'].round().astype(int).astype(str) + "M€",
        textposition='auto',
        width=0.6,
        showlegend=False
    ))
    
    # Aggiungiamo la linea di tendenza
    fig_reset.add_trace(go.Scatter(
        x=df_ebitda_reset['Anno'],
        y=df_ebitda_reset['EBITDA (€M)'],
        mode='lines+markers',
        line=dict(color='rgba(0, 0, 0, 0.7)', width=2, dash='dot'),
        showlegend=False
    ))
    
    # Aggiungiamo una legenda manuale con div colorati
    fig_reset.add_annotation(
        x=0.02, y=1.12,
        xref="paper", yref="paper",
        text="<span style='color:rgb(65, 105, 225);'>■</span> Attuale &nbsp;&nbsp; <span style='color:rgb(220, 20, 60);'>■</span> Post-Reset &nbsp;&nbsp; <span style='color:rgb(46, 139, 87);'>■</span> Recupero",
        showarrow=False,
        font=dict(size=12),
        align="left"
    )
    
    # Evidenziamo il calo dal 2024 al 2025
    fig_reset.add_shape(
        type="line",
        x0='2024E', y0=311,
        x1='2025E', y1=225,
        line=dict(color="red", width=2, dash="dot"),
        xref='x', yref='y'
    )
    
    # Aggiungiamo frecce e annotazioni
    fig_reset.add_annotation(
        x='2024E', y=311,
        xshift=20,
        text="€311M",
        showarrow=False,
        font=dict(size=12, color="navy")
    )
    
    fig_reset.add_annotation(
        x='2025E', y=225,
        xshift=15, yshift=-25,
        text="€225M<br><b>-28%</b>",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red",
        arrowwidth=2,
        arrowsize=1,
        ax=-25, ay=30
    )
    
    # Evidenziamo la crescita dal 2025 al 2029
    fig_reset.add_annotation(
        x='2027E', y=285,
        text="Fase di Recupero",
        showarrow=False,
        font=dict(size=12, color="darkgreen")
    )
    
    fig_reset.add_annotation(
        x='2029E', y=361,
        xshift=0, yshift=20,
        text="€361M<br><b>+60%</b> vs 2025<br>CAGR +12.5%",
        showarrow=True,
        arrowhead=2,
        arrowcolor="green",
        arrowwidth=2,
        arrowsize=1,
        ax=0, ay=-40
    )
    
    # Area evidenziata per periodo di recupero
    fig_reset.add_vrect(
        x0='2025E', x1='2029E',
        fillcolor="rgba(50, 205, 50, 0.1)",
        layer="below",
        line_width=0,
        annotation_text="Periodo di Recupero RP4",
        annotation_position="top right",
        annotation=dict(font_size=10, font_color="green")
    )
    
    # Titolo e layout
    fig_reset.update_layout(
        title={
            'text': "Impatto del Reset Regolatorio RP4 sull'EBITDA",
            'font': {'size': 16}
        },
        xaxis_title="Anno",
        yaxis_title="EBITDA (€M)",
        yaxis=dict(
            tickformat=",.0f",
            gridcolor='rgba(0,0,0,0.1)'
        ),
        margin=dict(t=80, b=50, l=50, r=50)
    )
    
    st.plotly_chart(fig_reset, use_container_width=True)
    
    # Aggiungiamo una spiegazione sotto il grafico
    st.info("""
    **Cosa mostra questo grafico:**
    - **Barre blu**: EBITDA nel periodo attuale (2023-2024)
    - **Barra rossa**: Calo dell'EBITDA a €225M nel 2025 (-28%) dovuto al reset regolatorio RP4
    - **Barre verdi**: Fase di recupero con crescita costante (CAGR +12.5%) fino a superare i livelli pre-reset nel 2028-2029
    
    Questo calo temporaneo è pianificato e non influenzerà la politica dei dividendi della società.
    """)

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

# --- NUOVA SEZIONE: Analisi Completa di ENAV ---
st.subheader("📑 Analisi Completa di ENAV S.p.A.")
st.markdown("""
Questa sezione contiene l'analisi completa ed approfondita di ENAV S.p.A. per gli investitori orientati al dividendo.
Clicca su ciascuna sezione per visualizzare il contenuto dettagliato.
""")

# Analisi completa - contenuto del file Analisi_ENAV_C.md
with st.expander("**Executive Summary**", expanded=True):
    st.markdown("""
ENAV S.p.A., il gestore del traffico aereo italiano, presenta un profilo interessante per gli investitori focalizzati sul reddito. Con un dividend yield attuale di circa 7%, una politica di distribuzione chiara basata sull'80% del free cash flow, e un piano industriale 2025-2029 che prevede crescita costante dei dividendi, ENAV offre un'opportunità di investimento potenzialmente attraente per chi cerca flussi di cassa stabili e prevedibili nel lungo periodo.

Il titolo si distingue per una combinazione di caratteristiche difensive tipiche di un'utility regolamentata con prospettive di crescita moderata ma visibile.
    """)

with st.expander("**1. Storico dei Dividendi e Rendimento**"):
    st.markdown("""
ENAV ha ripristinato e incrementato progressivamente la distribuzione di dividendi dopo la pausa dovuta alla pandemia. Negli ultimi anni i dividendi per azione (DPS) sono cresciuti in modo significativo, accompagnati da rendimenti (dividend yield) interessanti per gli azionisti orientati al reddito.

### Evoluzione recente dei dividendi:

| Bilancio (anno)    | Dividendo per Azione (€) | Data Stacco    | Dividend Yield (circa) |
|--------------------|--------------------------|----------------|---------------------------|
| **2021** (pag. 2022)| 0,1081                   | 24 ott 2022    | ~2,7%                    |
| **2022** (pag. 2023)| 0,1967                   | 23 ott 2023    | ~5%–6%                   |
| **2023** (pag. 2024)| 0,2300                   | 27 mag 2024    | ~6,4%                    |
| **2024** (proposto) | **0,2700**               | **23 giu 2025**| ~7% (stimato)            |

Nel 2020 la distribuzione del dividendo fu cancellata a causa della crisi Covid-19, riprendendo poi nell'esercizio 2021. Il dividendo 2023 di €0,23 per azione (pagato nell'ottobre 2023) è risultato il più alto di sempre per ENAV, e il management ha proposto un ulteriore aumento a €0,27 per azione sul bilancio 2024.

### Piano di crescita dei dividendi 2025-2029:

ENAV prevede di aumentare il dividendo per azione ogni anno fino al 2029. Partendo da €0,27 per azione sul 2024, il DPS è atteso salire a:
- €0,28 nel 2025
- €0,29 nel 2026
- €0,30 nel 2027
- €0,31 nel 2028
- €0,32 per azione nel 2029

Si tratta di una crescita annua intorno al +4% composta, che garantirebbe che il potere d'acquisto del dividendo aumenti nel tempo (almeno in linea con l'inflazione moderata).
    """)

with st.expander("**2. Modello di Business e Stabilità dei Flussi di Cassa**"):
    st.markdown("""
La solidità del modello di business di ENAV è basata su un core business regolato (il controllo del traffico aereo nazionale) che genera ricavi stabili e prevedibili. L'azienda beneficia di un quadro regolatorio che le assicura la copertura dei costi e rendimenti predeterminati sulle attività core, riducendo la volatilità dei risultati.

### Composizione dei ricavi:

Dai dati 2029 previsti nel piano industriale:
- 75% En-route (sorvoli e traffico aereo)
- 25% Terminal (servizi aeroportuali)

Il business è suddiviso in:
- **Attività regolamentate**: rappresentano il core business, con ricavi prevedibili e protetti da meccanismi regolatori
- **Attività non regolamentate**: in forte crescita, passeranno da €49M nel 2024 a €106M nel 2029 (CAGR +6%)

### Solidità dei flussi di cassa:

ENAV adotta da anni una politica dei dividendi orientata al cash flow: almeno l'80% del Free Cash Flow normalizzato viene distribuito annualmente. Di fatto, oltre l'80% del free cash flow generato nel periodo 2015-2023 è stato restituito agli azionisti sotto forma di dividendi.

Nel 2024, la società ha generato:
- Free Cash Flow: €199M (in crescita del 43% rispetto al 2023)
- Debt/EBITDA ratio: 0,8x (in miglioramento rispetto a 1,1x del 2023)

La capacità di ENAV di sostenere un alto payout è confermata dai recenti risultati di cassa. Nel 2024 la società ha generato forti flussi di cassa che le hanno permesso sia di finanziare gli investimenti correnti sia di ridurre l'indebitamento finanziario netto di oltre €60 milioni.
    """)

with st.expander("**3. Piano Industriale 2025-2029 e Prospettive di Crescita**"):
    st.markdown("""
Il piano industriale 2025-2029 si fonda su quattro pilastri strategici:

1. **Potenziamento del mercato regolato**:
   - Modernizzazione delle infrastrutture di controllo
   - Introduzione di torri di controllo digitali remote
   - Consolidamento dei centri di controllo da 4 a 2 (Milano e Roma)

2. **Espansione del mercato non regolato**:
   - Ampliamento dell'offerta di servizi digitali
   - Ingresso in nuovi mercati esteri (India 2025, Brasile e Arabia Saudita 2026)
   - Sviluppo di nuovi business (droni, energy service company, digital academy)

3. **Innovazione e sostenibilità**:
   - Investimenti in soluzioni digitali e "green"
   - Impegno per la decarbonizzazione (riduzione del 87,4% delle emissioni Scope 1 e 2 vs 2019)

4. **Efficienza operativa e governance**:
   - Riorganizzazione interna
   - Ottimizzazione delle risorse

### Investimenti e target finanziari:

Il piano prevede:
- Investimenti totali: €570M entro il 2029
- Crescita dei ricavi: da €1.037M (2024) a €1.200M (2029) - CAGR +3%
- Aumento EBITDA: da €311M (2024) a €361M (2029) - CAGR +3%
- Crescita utile netto: da €126M (2024) a €165M (2029) - CAGR +6%
- FCF cumulato 2025-2029: circa €1 miliardo

### Focus sul traffico aereo:

Lo scenario atteso è di traffico aereo in crescita progressiva: per l'Italia si stima un CAGR del +2,5% annuo nel periodo 2025-2029, con un balzo di circa +6% nel 2025 secondo le ultime proiezioni Eurocontrol.
    """)

with st.expander("**4. Focus sulle Attività Non Regolamentate**"):
    st.markdown("""
Le attività non regolamentate rappresentano un pilastro fondamentale della strategia di crescita di ENAV, con l'obiettivo di raddoppiare i ricavi da €49M nel 2024 a €106M nel 2029, raggiungendo circa il 9% dei ricavi totali.

### Composizione del business non regolamentato (previsione 2029):

- **Evoluzione del portfolio prodotti/servizi core** (67% dei ricavi non-regolati)
  - Monetizzazione dell'expertise su Digital Towers
  - Scale-up della Digital Academy anche verso terze parti
  - Nuove funzionalità di prodotto per centri di controllo e torri
  - Upgrade HW/SW per monitoraggio meteorologico

- **Nuove geografie e mercati** (23% dei ricavi non-regolati)
  - Nuovi uffici pianificati in mercati strategici:
    - India (Q3 2025)
    - Brasile (Q1 2026)
    - Arabia Saudita (Q1 2026)
  - Presenza in 87 paesi globalmente
  - Focus su aree con alti investimenti aeroportuali previsti

- **Nuovi business** (10% dei ricavi non-regolati)
  - **Droni**: ENAV è l'unico player certificato sia CISP che USSP in Europa, posizionamento unico nell'ecosistema dei droni
  - **Energy Service Company**: trasformazione dei costi operativi in opportunità di business
  - **Digital Academy**: piattaforma di e-learning per formazione aeronautica

### Business dei droni in dettaglio:

Il piano industrisale evidenzia come ENAV abbia una posizione unica nel settore dei droni, con applicazioni in:
- Monitoraggio di aree/infrastrutture critiche
- Sistemi di rilevamento droni (DDS)
- Consegne logistiche
- Ispezioni infrastrutturali
- Eventi (es. F1 GP Imola per rilevamento droni)

ENAV offre una piattaforma "Drone as a Service" modulare e scalabile che include:
- Fornitura di flotte di droni
- Operazioni di volo
- Gestione dei dati
- Formazione specifica (Drone Academy)

La società si avvantaggia del fatto che il mercato dei droni è in rapida crescita, con proiezioni di crescita a doppia cifra entro il 2030.

### Energy Service Company e Digital Academy:

ENAV sta inoltre sviluppando due nuove linee di business che non sono ancora state valorizzate nelle proiezioni finanziarie del piano industriale, rappresentando quindi un potenziale upside:

- **Energy Service Company (ESCO)**:
  - Servizi di consulenza e soluzioni chiavi in mano per aeroporti
  - Valutazione energetica, studi di fattibilità, esecuzione e monitoraggio
  - Inizialmente focalizzata sull'ottimizzazione dei consumi energetici interni di ENAV
  - Espandibile al più ampio mercato aeroportuale e ad altri settori

- **Digital Academy**:
  - Piattaforma e-learning per formazione aeronautica
  - Target: ANSP, gestori aeroportuali, operatori dell'aviazione, piloti di droni
  - Valorizzazione del know-how di ENAV in formazione ATM (Air Traffic Management)
    """)

with st.expander("**5. Investimenti per la Crescita**"):
    st.markdown("""
ENAV ha pianificato investimenti significativi per sostenere la propria crescita nel periodo 2025-2029, con un impegno finanziario complessivo di €570 milioni, in aumento del 15% rispetto al periodo regolatorio precedente (€494 milioni nel 2020-2024).

### Dettaglio degli investimenti previsti (2025-2029):

- **Navigazione e sistemi ATM** (50% del totale):
  - Software e piattaforme ATM per centri di controllo, approach e torri
  - Sistemi di comunicazione radio centralizzati e remoti
  - Sistemi di navigazione aerea, meteorologia e sorveglianza

- **Infrastrutture civili e sistemi** (27% del totale):
  - Conformità regolamentare delle infrastrutture civili
  - Allineamento dei sistemi infrastrutturali all'innovazione tecnologica

- **ICT e altro** (23% del totale):
  - Sistemi operativi e piattaforme IT per supportare il core business
  - Infrastrutture di rete nazionali
  - Applicazioni gestionali
  - Investimenti in sicurezza e safety

### Iniziative strategiche specifiche:

1. **Integrazione degli APP (Approach Units) nei ACC (Area Control Centers)** - completamento previsto nel 2027
   - Trasferimento delle attività di gestione degli avvicinamenti ai Centri di Controllo d'Area

2. **Consolidamento dei centri di controllo (ACC)** - completamento previsto nel 2030
   - Riduzione da 4 a 2 centri (Milano e Roma)

3. **Torri Remote** - completamento previsto nel 2033
   - Digitalizzazione di 26 torri in 2 Remote Tower Control Centers

4. **Monitoraggio meteorologico** - completamento previsto nel 2028
   - Upgrade software e hardware per migliorare e automatizzare l'osservazione meteorologica

5. **Piattaforma ATM** - completamento previsto nel 2030
   - Nuova piattaforma di gestione del traffico aereo per il personale ATC

Queste iniziative strategiche dovrebbero generare risparmi cumulati durante il periodo di piano di circa €21 milioni, aumentando a circa €47 milioni a regime.

### Piano M&A e crescita esterna:

ENAV ha definito un piano di acquisizioni selettivo con fondi disponibili fino a €350 milioni, che sarà finanziato attraverso nuovo debito senza intaccare la solidità finanziaria. Le aree di interesse per M&A includono:

1. **Licenze e servizi software**
   - Consolidamento del posizionamento come leader globale
   - Espansione delle competenze complementari

2. **Servizi tecnici e di ingegneria**
   - Rafforzamento del know-how attuale
   - Consolidamento dell'hub ingegneristico del Gruppo

3. **Consulenza avionica**
   - Scale-up delle attività di consulenza
   - Espansione del portfolio clienti
   - Valorizzazione del know-how

4. **Meteorologia**
   - Acquisizione di know-how e capacità
   - Sviluppo di software innovativi

5. **Droni/UTM (Unmanned Traffic Management)**
   - Rafforzamento della posizione in un ambiente in crescita
   - Sviluppo di servizi UTM nel mercato domestico
    """)

with st.expander("**6. Elementi Distintivi per l'Investitore a Dividendo**"):
    st.markdown("""
### Politica dei dividendi chiara e misurabile:

Questa politica è stata confermata e rafforzata nel nuovo Piano Industriale, che prevede un payout medio attorno all'80% del FCF anche negli anni 2025-2029. Il management, e in particolare l'Amministratore Delegato, hanno sottolineato l'impegno a remunerare generosamente gli azionisti.

Monti (CEO) ha dichiarato che "tutto il cash che si forma [dal core business regolato] deve andare a premiare i nostri azionisti", mentre le iniziative non regolate devono servire a creare ulteriore valore e saranno finanziate con debito per non intaccare i flussi destinabili ai dividendi.

### Rendimento competitivo:

Ai prezzi attuali di mercato, il titolo ENAV offre un rendimento da dividendo superiore al 6% annuo, collocandosi tra le società italiane con yield più elevati e stabili. Se i piani di ENAV si realizzano, un investitore di lungo periodo beneficerà non solo dei dividendi annuali elevati, ma anche di una possibile rivalutazione del capitale.

### Meccanismi di protezione regolatori:

Il nuovo periodo regolatorio **RP4 (2025-2029)** offre stabilità e protezione attraverso:
- Meccanismi di protezione per inflazione e variazioni di traffico
- Recupero dei costi operativi
- Remunerazione del capitale investito (WACC più alto: ~6.7% vs 4.4% del periodo precedente)
    """)

with st.expander("**7. Analisi del Reset Regolatorio RP4**"):
    st.markdown("""
Un elemento importante da comprendere è l'impatto del "reset regolatorio" che avviene all'inizio di ogni periodo regolatorio quinquennale:

- EBITDA 2024: €311M
- EBITDA 2025: previsto calo a €225M (-28%) a causa del reset regolatorio
- EBITDA 2029: previsto recupero a €361M (CAGR +12,5% dal 2025)

Questo calo temporaneo è un elemento fisiologico dovuto a:
- Azzeramento dei meccanismi di bilanciamento del traffico
- Reset dei parametri economici e finanziari
- Rimozione del balance dalla formula RAB

È importante notare che questo reset non compromette la sostenibilità del dividendo, che continuerà a crescere anche nel 2025-2026 grazie alla forte posizione di cassa e alla generazione di FCF.
    """)

with st.expander("**8. Sostenibilità finanziaria e posizione di cassa**"):
    st.markdown("""
Il piano industriale 2025-2029 evidenzia una forte sostenibilità finanziaria che supporta sia gli investimenti che la remunerazione degli azionisti:

- **Capacità di generazione di cassa**: circa €1,6 miliardi di operating cash flow nel periodo 2025-2029
- **Free Cash Flow previsto**: circa €1 miliardo dopo aver finanziato €568M di CAPEX
- **Dividendi previsti**: circa €813M nel periodo di piano (80% del FCF)
- **Posizione finanziaria netta**: previsto azzeramento del debito entro il 2029 (da €258M nel 2024 a €0 nel 2029)

Il Net Debt/EBITDA passerà da 0,8x nel 2024 a 0,6x nel 2025 per poi azzerarsi entro il 2029, creando un headroom di circa €350M che potrebbe essere utilizzato per accelerare la crescita organica o per operazioni di M&A.
    """)

with st.expander("**9. Principali Rischi da Considerare**"):
    st.markdown("""
### Rischi regolatori:
- Cambiamenti nei parametri regolatori potrebbero influenzare la redditività
- Il reset regolatorio causa temporanea flessione dei risultati

### Rischi di traffico:
- Eventi straordinari (come accaduto con il COVID-19) possono impattare significativamente i volumi
- Esistono tuttavia meccanismi di compensazione nel medio termine

### Rischi esecutivi:
- Execution risk nelle iniziative di crescita non regolamentate
- Rischi legati alle acquisizioni (M&A) programmate fino a €350M
    """)

with st.expander("**10. Valutazione e Prospettive per l'Investitore**"):
    st.markdown("""
### Metrics chiave:
- P/E 2024: ~13x
- EV/EBITDA 2024: ~8.5x
- FCF Yield 2024: ~7-8%
- Dividend Yield 2024: ~7.1%

La valutazione riflette un profilo di basso rischio operativo e ottimo rendimento, tipico di un titolo "core" per investitori a dividendo. Il mercato sembra aver reagito positivamente ai piani di ENAV, con diversi broker come Intesa Sanpaolo (target €5,10) ed Equita SIM (target €4,50) che raccomandano l'acquisto.

### Potenziale di apprezzamento:

Considerando:
1. Un rendimento da dividendo stabile al 7-8%
2. Una crescita annua del dividendo del 4%
3. Un potenziale apprezzamento del capitale dovuto all'espansione delle attività non regolate

ENAV potrebbe offrire un rendimento totale annuo (Total Shareholder Return) a doppia cifra nel lungo periodo.
    """)

with st.expander("**11. Conclusioni**"):
    st.markdown("""
ENAV S.p.A. emerge come una società solida e cash-generative, con un ruolo essenziale nel sistema del traffico aereo italiano e una strategia ben definita per crescere nei prossimi anni. Per un investitore orientato ai dividendi, ENAV offre attualmente un rendimento elevato e prospettive di incremento dei flussi cedolari, sostenuti da piani industriali credibili e da una disciplina finanziaria focalizzata sulla remunerazione degli azionisti.

La politica dei dividendi di ENAV appare sostenibile nel lungo termine – circa l'80% del free cash flow atteso verrà distribuito annualmente – lasciando comunque margine per finanziare la crescita. Il significativo piano di investimenti di €570M e l'espansione nelle attività non regolate potrebbero creare ulteriore valore per gli azionisti senza compromettere la capacità di distribuzione dei dividendi.

In un'ottica di lungo periodo, ENAV rappresenta una potenziale "yield play" interessante: un titolo difensivo, capace di offrire reddito ricorrente superiore alla media di mercato e con un moderato potenziale di crescita sia del dividendo sia del valore del capitale, man mano che il settore del trasporto aereo consolida la propria ripresa e le iniziative strategiche cominciano a generare risultati.

---

*Nota: Questo documento è stato creato sulla base dei dati forniti nei file di analisi e nella presentazione del Piano Industriale 2025-2029 di ENAV. Gli investitori dovrebbero condurre ulteriori ricerche e consultare un consulente finanziario prima di prendere decisioni di investimento.*
    """)

st.markdown("---")

# Disclaimer aggiornato con formattazione migliore
st.markdown("""
<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff;">
    <h3 style="color: #007bff; margin-top: 0;">DISCLAIMER</h3>
    <p style="font-size: 14px;">
    Le informazioni contenute in questa presentazione sono fornite esclusivamente a scopo informativo generale e/o educativo. 
    Non costituiscono e non devono essere interpretate come consulenza finanziaria, legale, fiscale o di investimento.
    </p>
    <p style="font-size: 14px;">
    Investire nei mercati finanziari comporta rischi significativi, inclusa la possibilità di perdere l'intero capitale investito. 
    Le performance passate non sono indicative né garanzia di risultati futuri.
    </p>
    <p style="font-size: 14px;">
    Si raccomanda vivamente di condurre la propria analisi approfondita (due diligence) e di consultare un consulente finanziario 
    indipendente e qualificato prima di prendere qualsiasi decisione di investimento.
    </p>
</div>
""", unsafe_allow_html=True)

# Aggiungi firma
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    <p style="font-style: italic; color: #888;">Realizzazione a cura della Barba Sparlante</p>
</div>
""", unsafe_allow_html=True)
