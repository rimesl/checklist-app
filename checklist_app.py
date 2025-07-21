import streamlit as st
import json
import os
import uuid

CHECKLIST_FILE = "checklist_data.json"

# Load checklist from JSON file
def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save checklist to JSON file
def save_checklist(data):
    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Initialize checklist in session state
if "checklist" not in st.session_state:
    st.session_state.checklist = load_checklist()

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

if "edit_text" not in st.session_state:
    st.session_state.edit_text = ""

st.set_page_config(page_title="Checklist PLG", layout="centered")

st.title("Règles de gestion PLG")
st.caption("Interface de checklist interactive")

# Functions
def toggle_completed(item_id):
    for item in st.session_state.checklist:
        if item["id"] == item_id:
            item["completed"] = not item["completed"]
            break
    save_checklist(st.session_state.checklist)

def delete_item(item_id):
    st.session_state.checklist = [item for item in st.session_state.checklist if item["id"] != item_id]
    save_checklist(st.session_state.checklist)

def update_item(item_id, new_text):
    for item in st.session_state.checklist:
        if item["id"] == item_id:
            item["text"] = new_text
            break
    save_checklist(st.session_state.checklist)

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
        save_checklist(st.session_state.checklist)
        st.experimental_rerun()

# Add multiple items
with st.expander("Ajouter plusieurs règles"):
    multiline = st.text_area("Écris une règle par ligne")
    if st.button("Ajouter toutes les règles", key="add_multiple"):
        lines = multiline.strip().split("\n")
        added = 0
        for line in lines:
            cleaned = line.strip()
            if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
                st.session_state.checklist.append({
                    "id": str(uuid.uuid4()),
                    "text": cleaned,
                    "completed": False
                })
                added += 1
        if added:
            save_checklist(st.session_state.checklist)
            st.experimental_rerun()

# Display checklist
st.subheader("Checklist")

for item in st.session_state.checklist:
    cols = st.columns([0.07, 0.5, 0.16, 0.16, 0.11])
    with cols[0]:
        st.checkbox(
            "",
            value=item["completed"],
            key=f"check_{item['id']}",
            on_change=toggle_completed,
            args=(item["id"],),
        )
    with cols[1]:
        if st.session_state.edit_id == item["id"]:
            st.session_state.edit_text = st.text_input("Modifier la règle", value=item["text"], key=f"edit_input_{item['id']}")
        else:
            display_text = f"~~{item['text']}~~" if item["completed"] else item["text"]
            st.markdown(display_text)
    with cols[2]:
        if st.session_state.edit_id == item["id"]:
            if cols[2].button("✅ Mettre à jour", key=f"update_{item['id']}", use_container_width=True):
                updated = st.session_state.edit_text.strip()
                if updated:
                    update_item(item["id"], updated)
                st.session_state.edit_id = None
                st.session_state.edit_text = ""
                st.experimental_rerun()
        else:
            if cols[2].button("✏️ Modifier", key=f"edit_{item['id']}", use_container_width=True):
                st.session_state.edit_id = item["id"]
                st.session_state.edit_text = item["text"]
    with cols[3]:
        if cols[3].button("Supprimer", key=f"delete_{item['id']}", use_container_width=True):
            delete_item(item["id"])
            st.experimental_rerun()
