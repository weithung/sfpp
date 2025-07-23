# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="Yeppuda - Perfect Skin Solutions",
    page_icon="🌸",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary: #c77dff;
        --secondary: #7ae5ff;
        --background: #fdf7ff;
    }
    .stApp {
        background-image: linear-gradient(135deg, #fdf7ff, #f7f0ff);
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(45deg, #c77dff, #7ae5ff) !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
    }
    .st-bb { background-color: var(--background); }
    .st-at { background-color: #ffffff; }
    h1, h2, h3 {
        color: #7b2cbf !important;
        text-align: center;
        font-family: 'Georgia', serif;
    }
    .stMarkdown img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sample product database
PRODUCT_DATA = [
    {"name": "Glow Revival Serum", "brand": "Glow Recipe", "type": "Serum", 
     "skin_type": "Dry", "concern": "Hydration", "price": 35, "rating": 4.8,
     "desc": "Hyaluronic acid serum for intense hydration"},
    {"name": "Acne Control Solution", "brand": "La Roche-Posay", "type": "Treatment", 
     "skin_type": "Oily", "concern": "Acne", "price": 28, "rating": 4.6,
     "desc": "Oil-free gel with salicylic acid"},
    {"name": "Age Renewal Cream", "brand": "CeraVe", "type": "Moisturizer", 
     "skin_type": "All", "concern": "Aging", "price": 24, "rating": 4.7,
     "desc": "Retinol-infused night cream"},
    {"name": "Soothing Toner", "brand": "Klairs", "type": "Toner", 
     "skin_type": "Sensitive", "concern": "Redness", "price": 22, "rating": 4.9,
     "desc": "Alcohol-free calming toner"},
    {"name": "Radiance Essence", "brand": "COSRX", "type": "Essence", 
     "skin_type": "Combination", "concern": "Dullness", "price": 27, "rating": 4.5,
     "desc": "Brightening essence with vitamin C"},
    {"name": "Sun Shield SPF 50+", "brand": "Neutrogena", "type": "Sunscreen", 
     "skin_type": "All", "concern": "UV Protection", "price": 18, "rating": 4.8,
     "desc": "Lightweight non-greasy sunscreen"},
    {"name": "Clarifying Cleanser", "brand": "CeraVe", "type": "Cleanser", 
     "skin_type": "Oily", "concern": "Acne", "price": 16, "rating": 4.7,
     "desc": "Foaming cleanser with niacinamide"},
    {"name": "Overnight Mask", "brand": "Laneige", "type": "Mask", 
     "skin_type": "Dry", "concern": "Hydration", "price": 30, "rating": 4.9,
     "desc": "Sleeping mask for intense moisture"}
]

# App functions
def load_data():
    return pd.DataFrame(PRODUCT_DATA)

def show_product_card(product):
    with st.container():
        st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)
        st.image(f"https://picsum.photos/300/200?random={product.name}", 
                 use_column_width=True)
        st.subheader(product["name"])
        st.caption(f"**Brand**: {product['brand']} | **Type**: {product['type']}")
        st.markdown(f"⭐ **{product['rating']}**/5 | **Price**: ${product['price']}")
        st.caption(product["desc"])
        st.button("Add to Routine", key=f"btn_{product.name}")
        st.markdown("</div>", unsafe_allow_html=True)

# Main app
def main():
    # Header
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/6399/6399355.png", width=100)
    with col2:
        st.title("🌸 Yeppuda")
        st.markdown("### Your Perfect Skincare Match")
    
    st.markdown("---")
    
    # User input section
    with st.expander("✨ Start Your Skin Analysis", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            skin_type = st.radio("Your Skin Type", 
                                ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
        with col2:
            concerns = st.multiselect("Main Concerns", 
                                    ["Acne", "Aging", "Hydration", "Redness", 
                                     "Dullness", "Dark Spots", "UV Protection"])
        budget = st.slider("Budget Range (USD)", 10, 100, (15, 40))
        st.caption("We'll recommend products within your budget")

    # Recommendation engine
    df = load_data()
    
    # Filter products
    filtered = df[
        (df["skin_type"].str.contains(skin_type) |
        (df["skin_type"] == "All")
    ]
    if concerns:
        filtered = filtered[filtered["concern"].isin(concerns)]
    filtered = filtered[
        (filtered["price"] >= budget[0]) & 
        (filtered["price"] <= budget[1])
    ].sort_values("rating", ascending=False)

    # Show results
    st.subheader(f"✨ Personalized Recommendations for {skin_type} Skin")
    if filtered.empty:
        st.warning("No products match your criteria. Try adjusting filters.")
    else:
        for _, product in filtered.iterrows():
            show_product_card(product)

    # Skincare education
    st.markdown("---")
    st.subheader("📚 Skincare Guide")
    tab1, tab2, tab3 = st.tabs(["Skin Types", "Concerns", "Routine Builder"])
    
    with tab1:
        st.markdown("""
        **Understanding Your Skin Type**:
        - 🌀 **Combination**: Oily T-zone, dry cheeks
        - 💧 **Dry**: Flaky patches, tight feeling
        - 🛢️ **Oily**: Shiny appearance, enlarged pores
        - 🌸 **Sensitive**: Redness, easy irritation
        - ⚖️ **Normal**: Balanced, few concerns
        
        *Yeppuda Tip: Your skin type can change with seasons!*
        """)
        
    with tab2:
        concern = st.selectbox("Learn about skincare concerns", 
                              ["Acne", "Aging", "Hydration", "Redness", "Dullness"])
        if concern == "Acne":
            st.info("""
            **Acne Solutions**:
            - Salicylic acid: Unclogs pores
            - Benzoyl peroxide: Kills acne bacteria
            - Retinoids: Prevent clogged pores
            - Non-comedogenic products won't clog pores
            """)
        elif concern == "Aging":
            st.info("""
            **Anti-Aging Solutions**:
            - Retinol: Boosts collagen production
            - Vitamin C: Fights free radicals
            - Peptides: Support skin structure
            - SPF: Prevents photoaging
            """)
        elif concern == "Hydration":
            st.info("""
            **Hydration Solutions**:
            - Hyaluronic acid: Holds 1000x its weight in water
            - Glycerin: Humectant that draws moisture
            - Ceramides: Reinforce skin barrier
            - Occlusives: Prevent moisture loss
            """)
        elif concern == "Redness":
            st.info("""
            **Redness Solutions**:
            - Centella asiatica: Calms inflammation
            - Niacinamide: Strengthens barrier
            - Green tea extract: Antioxidant protection
            - Avoid fragrances and alcohol
            """)
        else:
            st.info("""
            **Brightening Solutions**:
            - Vitamin C: Inhibits melanin production
            - AHAs: Exfoliate dull surface cells
            - Niacinamide: Reduces hyperpigmentation
            - Licorice root extract: Brightening properties
            """)
            
    with tab3:
        st.write("Build your custom skincare routine:")
        steps = ["Cleanser", "Toner", "Serum", "Moisturizer", "Sunscreen (AM)", "Treatment (PM)"]
        routine = st.multiselect("Select products for your routine", 
                                options=steps,
                                default=["Cleanser", "Moisturizer", "Sunscreen (AM)"])
        
        if st.button("Create Routine"):
            st.success("Your personalized routine created!")
            st.write("Morning Routine:")
            for step in routine:
                if "Sunscreen" in step:
                    st.checkbox(step, value=True)
            st.write("Evening Routine:")
            for step in routine:
                if "Sunscreen" not in step:
                    st.checkbox(step.replace("(AM)", "(PM)"), value=True)
    
    # Data visualization
    st.markdown("---")
    st.subheader("📊 Skincare Insights")
    fig = px.bar(
        df.groupby("type").agg(avg_price=("price", "mean"), 
                              avg_rating=("rating", "mean")).reset_index(),
        x="type",
        y="avg_price",
        color="avg_rating",
        hover_data=["avg_rating"],
        labels={"type": "Product Type", "avg_price": "Average Price"},
        color_continuous_scale="purples"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("© 2023 Yeppuda Skincare | All recommendations are personalized and based on dermatological research")

if __name__ == "__main__":
    main()
