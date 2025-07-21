import streamlit as st
import uuid

st.set_page_config(page_title="Checklist PLG", layout="centered")

st.title("Règles de gestion PLG")
st.caption("Interface de checklist interactive")

if "checklist" not in st.session_state:
    st.session_state.checklist = []

if "delete_id" not in st.session_state:
    st.session_state.delete_id = None

def toggle_completed(item_id):
    for item in st.session_state.checklist:
        if item["id"] == item_id:
            item["completed"] = not item["completed"]
            break

def delete_item(item_id):
    st.session_state.checklist = [item for item in st.session_state.checklist if item["id"] != item_id]

# Add single item
st.subheader("Ajouter une règle")
new_item = st.text_input("Nouvelle règle")
if st.button("Ajouter", key="add_single"):
    cleaned = new_item.strip()
    if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
        st.session_state.checklist.append({
            "id": str(uuid.uuid4()),
            "text": cleaned,
            "completed": False
        })

# Add multiple items
with st.expander("Ajouter plusieurs règles"):
    multiline = st.text_area("Écris une règle par ligne")
    if st.button("Ajouter toutes les règles", key="add_multiple"):
        lines = multiline.strip().split("\n")
        for line in lines:
            cleaned = line.strip()
            if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
                st.session_state.checklist.append({
                    "id": str(uuid.uuid4()),
                    "text": cleaned,
                    "completed": False
                })

# Display checklist
st.subheader("Checklist")

for item in st.session_state.checklist:
    cols = st.columns([0.07, 0.75, 0.18])
    with cols[0]:
        st.checkbox(
            "",
            value=item["completed"],
            key=f"check_{item['id']}",
            on_change=toggle_completed,
            args=(item["id"],),
        )
    with cols[1]:
        if item["completed"]:
            st.markdown(f"~~{item['text']}~~")
        else:
            st.markdown(item["text"])
    with cols[2]:
        if cols[2].button("Supprimer", key=f"delete_{item['id']}", use_container_width=True):
            st.session_state.delete_id = item["id"]

if st.session_state.delete_id is not None:
    delete_item(st.session_state.delete_id)
    st.session_state.delete_id = None
