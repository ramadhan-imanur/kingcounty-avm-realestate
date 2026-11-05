"""
Modul Tampilan: Market Overview & Spatial Explorer (Modul 2)
Visualisasi ringkasan KPI pasar, sebaran spasial 22.847 properti, dan heatmap harga.
"""

import streamlit as st
import plotly.express as px

def render_explorer(clean_df):
    """
    Merender halaman peta sebaran spasial dan kartu metrik pasar.
    """
    st.markdown(
        """
        <div style="margin-bottom:20px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span class="aeris-badge badge-primary">Geospatial Intelligence</span>
                <span class="aeris-badge badge-muted">Cartographic Projection: EPSG:4326</span>
            </div>
            <h1 style="font-size:2.2rem; font-weight:800; color:#0b1c30; margin:0 0 6px 0;">
                Market Overview & Spatial Explorer
            </h1>
            <p style="color:#475569; font-size:0.95rem; margin:0;">
                Geographic clustering and price dispersion across 22,847 King County parcel sales.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top KPI Metrics Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="aeris-card" style="padding:16px;">
                <div style="font-size:0.75rem; color:#64748B; font-weight:600;">TOTAL ANALYZED PARCELS</div>
                <div style="font-family:'JetBrains Mono'; font-size:1.8rem; font-weight:800; color:#0b1c30;">{len(clean_df):,}</div>
                <div style="font-size:0.75rem; color:#006948;">✓ 100% Validated Deeds</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            f"""
            <div class="aeris-card" style="padding:16px;">
                <div style="font-size:0.75rem; color:#64748B; font-weight:600;">MEDIAN SALE PRICE</div>
                <div style="font-family:'JetBrains Mono'; font-size:1.8rem; font-weight:800; color:#006398;">${clean_df['SalePrice'].median():,.0f}</div>
                <div style="font-size:0.75rem; color:#475569;">King County Benchmark</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            f"""
            <div class="aeris-card" style="padding:16px;">
                <div style="font-size:0.75rem; color:#64748B; font-weight:600;">MEDIAN PRICE PER SQFT</div>
                <div style="font-family:'JetBrains Mono'; font-size:1.8rem; font-weight:800; color:#006948;">${clean_df['PricePerSqFt'].median():,.0f}</div>
                <div style="font-size:0.75rem; color:#006948;">Standard Living Footprint</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            f"""
            <div class="aeris-card" style="padding:16px;">
                <div style="font-size:0.75rem; color:#64748B; font-weight:600;">MEDIAN FOOTPRINT</div>
                <div style="font-family:'JetBrains Mono'; font-size:1.8rem; font-weight:800; color:#7C3AED;">{clean_df['SqFtTotLiving'].median():,.0f} sqft</div>
                <div style="font-size:0.75rem; color:#475569;">Avg Lot: {clean_df['SqFtLot'].median():,.0f} sqft</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        tier_sel = st.multiselect("Market Cohort Filter", ['Entry-Level', 'Mid-Market', 'Luxury'], default=['Entry-Level', 'Mid-Market', 'Luxury'])
    with f_col2:
        price_range = st.slider("Sale Price Boundary ($)", 50000, 3000000, (100000, 1600000), step=50000)
    with f_col3:
        only_water = st.checkbox("Waterfront Estates Only", value=False)

    df_view = clean_df[
        (clean_df['PropertyTier'].isin(tier_sel)) &
        (clean_df['SalePrice'] >= price_range[0]) &
        (clean_df['SalePrice'] <= price_range[1])
    ]
    if only_water:
        df_view = df_view[df_view['IsWaterfront'] == 1]

    # Map Card
    st.markdown('<div class="aeris-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Spatial Distribution & Valuation Heatmap")
    sample_size = min(3500, len(df_view))
    df_sample = df_view.sample(sample_size, random_state=42)

    fig_map = px.scatter(
        df_sample,
        x="Longitude",
        y="Latitude",
        color="SalePrice",
        size="SqFtTotLiving",
        hover_data=["ZipCode", "BldgGrade", "Bedrooms", "TotalBaths"],
        color_continuous_scale="Viridis",
        title=f"Sampled Spatial Coordinates ({sample_size:,} King County Parcels)"
    )
    fig_map.update_layout(
        font_family="Plus Jakarta Sans",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.6)",
        height=580,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
