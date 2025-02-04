import streamlit as st

#### To run this, run 'streamlit run interface.py' in the terminal


# Streamlit app
st.title("Paper Submission Advisor :sunglasses:")

st.subheader("This model compares your abstract with abstracts from five academic journals and tells you to which journal you should submit your paper.")
st.divider()
st.subheader("Enter the abstract of your paper:")

# User input abstracts
topic = st.text_input("   ")

# Generate button
if st.button("Decide My Journal"):
        with st.spinner("Finding choices..."):
            decision = outputclass()  ##
        st.subheader("Recommended Journal:")
        st.write(decision)