import streamlit as st
from api_calls import (
    get_competitor_ads,
    generate_creative_ideas,
    create_final_ad_text,
    create_final_ad_image,
)

# Initialize session state variables
if "product_name" not in st.session_state:
    st.session_state.product_name = None
if "competitor_ads" not in st.session_state:
    st.session_state.competitor_ads = None
if "creative_ideas" not in st.session_state:
    st.session_state.creative_ideas = None
if "chosen_ad" not in st.session_state:
    st.session_state.chosen_ad = None
if "custom_text" not in st.session_state:
    st.session_state.custom_text = ""
if "final_text" not in st.session_state:
    st.session_state.final_text = None
if "final_image" not in st.session_state:
    st.session_state.final_image = None
if "generate_final" not in st.session_state:
    st.session_state.generate_final = False


def set_chosen_ad(idea):
    st.session_state.chosen_ad = idea
    # Reset final generation flags when new ad is chosen
    st.session_state.final_text = None
    st.session_state.final_image = None
    st.session_state.generate_final = False


def handle_custom_text_submit():
    st.session_state.generate_final = True


st.title("Marketing Creatives Generator")
print("initialized application")

# Step 1: Onboarding - Collect company details
st.header("Onboarding")
company_name = st.text_input("Company Name", placeholder="Enter your company name")
company_description = st.text_input(
    "About Your Company", placeholder="Describe your company..."
)

# Step 2: Product Details - Collect product name
if company_name and company_description:
    st.header("Product Information")
    product_name = st.text_input(
        "Product Name",
        placeholder="Enter the product name, you wish to create creative/advertisement for",
    )

    # Step 3: API Call to Analyze Competitor Ads
    if product_name:
        st.write("Analyzing competitor ads for:", product_name)

        if st.session_state.competitor_ads is None:
            with st.spinner("Fetching competitors' ads..."):
                try:
                    competitor_ads_json = get_competitor_ads(company_name, product_name)
                    st.session_state.competitor_ads = competitor_ads_json["ads"]
                except Exception as e:
                    st.error(f"Error fetching competitor ads: {str(e)}")
                    st.stop()

        if st.session_state.competitor_ads:
            competitor_names = [
                ad["page_name"] for ad in st.session_state.competitor_ads
            ]
            print(competitor_names)
            st.write(f"Analyzing ads from competitors: {', '.join(competitor_names)}")

            # Step 4: Generate Creative Ideas Based on Competitor Ads
            if st.session_state.creative_ideas is None:
                with st.spinner("Generating creative ad ideas..."):
                    try:
                        creative_ideas_json = generate_creative_ideas(
                            st.session_state.competitor_ads, product_name
                        )
                        st.session_state.creative_ideas = creative_ideas_json[
                            "ad_ideas"
                        ]
                    except Exception as e:
                        st.error(f"Error generating creative ideas: {str(e)}")
                        st.stop()

            if st.session_state.creative_ideas:
                # Step 5: Display Generated Creative Ideas
                st.header("Ad Creative Ideas")

                for i, idea in enumerate(st.session_state.creative_ideas, start=1):
                    st.markdown(
                        """
                        <style>
                        .idea-container {
                            height:1px;
                            
                            border-radius: 10px;
                            background-color: #f0f2f6;
                            margin-bottom: 20px;
                        }
                        .idea-header {
                            font-size: 18px;
                            font-weight: bold;
                            margin-bottom: 10px;
                        }
                        </style>
                    """,
                        unsafe_allow_html=True,
                    )

                    with st.container():
                        st.markdown(
                            '<div class="idea-container">',
                            unsafe_allow_html=True,
                        )

                        # col1, col2, col3 = st.columns([1, 2, 2])
                        col1, col2 = st.columns([1, 2])

                        with col1:
                            if st.button(
                                f"Select Inspiration {i}",
                                key=f"select_idea_{i}",
                                on_click=set_chosen_ad,
                                args=(idea,),
                            ):
                                pass
                            st.image(idea["image_url"], caption="Idea Image", width=150)

                        with col2:
                            st.markdown(
                                f'<p class="idea-header">Ad Text</p>',
                                unsafe_allow_html=True,
                            )
                            st.markdown(idea["ad_text"])
                            # st.markdown(
                            #     f'<p class="idea-header">Text Idea</p>',
                            #     unsafe_allow_html=True,
                            # )
                            st.markdown(idea["text_prompt"])

                        # with col3:
                        #     st.markdown(
                        #         f'<p class="idea-header">Image Idea</p>',
                        #         unsafe_allow_html=True,
                        #     )
                        #     st.markdown(idea["image_prompt"])

                        st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.chosen_ad:
                    # Step 6: Custom Text Input
                    st.header("Customize Your Ad")

                    # Create columns for text input and submit button
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        custom_text = st.text_input(
                            "Custom Text",
                            value=st.session_state.custom_text,
                            placeholder="Add something special, like '50% Off!'",
                            key="custom_text_input",
                        )
                    with col2:
                        if st.button("Generate Final Ad", key="generate_button"):
                            st.session_state.custom_text = custom_text
                            st.session_state.generate_final = True

                    # Step 7: Final API Calls for Text and Image Generation
                    if st.session_state.generate_final and st.session_state.custom_text:
                        if st.session_state.final_text is None:
                            with st.spinner("Generating your final text..."):
                                st.session_state.final_text = create_final_ad_text(
                                    st.session_state.chosen_ad["text_prompt"],
                                    company_name,
                                    product_name,
                                    st.session_state.custom_text,
                                )

                        if st.session_state.final_image is None:
                            with st.spinner("Generating your final image..."):
                                st.session_state.final_image = create_final_ad_image(
                                    st.session_state.chosen_ad["image_prompt"]
                                )

                        if st.session_state.final_image and st.session_state.final_text:
                            st.header("Your Final Ad")
                            st.write(
                                f"**Final Ad Text:** {st.session_state.final_text['marketing_text']}"
                            )
                            st.image(
                                st.session_state.final_image["image_url"],
                                caption="Final Ad Image",
                            )
                            st.success("Your ad is ready!")

# Add a reset button at the bottom of the page
if st.button("Start Over"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
