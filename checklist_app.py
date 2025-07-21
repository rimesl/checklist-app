import streamlit as st

st.set_page_config(page_title="Checklist PLG", layout="centered")

st.title("Règles de gestion PLG")
st.caption("Interface de checklist interactive")

if "checklist" not in st.session_state:
    st.session_state.checklist = []

# Helper function to update completion status
def toggle_completed(idx):
    st.session_state.checklist[idx]["completed"] = not st.session_state.checklist[idx]["completed"]

# Add single item
st.subheader("Ajouter une règle")
new_item = st.text_input("Nouvelle règle")
if st.button("Ajouter", key="add_single"):
    cleaned = new_item.strip()
    if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
        st.session_state.checklist.append({"text": cleaned, "completed": False})

# Add multiple items
with st.expander("Ajouter plusieurs règles"):
    multiline = st.text_area("Écris une règle par ligne")
    if st.button("Ajouter toutes les règles", key="add_multiple"):
        lines = multiline.strip().split("\n")
        for line in lines:
            cleaned = line.strip()
            if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
                st.session_state.checklist.append({"text": cleaned, "completed": False})

# Display checklist
st.subheader("Checklist")

for i, item in enumerate(st.session_state.checklist):
    cols = st.columns([0.07, 0.8, 0.13])
    with cols[0]:
        st.checkbox(
            "",
            value=item["completed"],
            key=f"check_{i}",
            on_change=toggle_completed,
            args=(i,),
        )
    with cols[1]:
        if item["completed"]:
            st.markdown(f"~~{item['text']}~~")
        else:
            st.markdown(item["text"])
    with cols[2]:
        if cols[2].button("Supprimer", key=f"delete_{i}"):
            st.session_state.checklist.pop(i)
            st.experimental_rerun()
