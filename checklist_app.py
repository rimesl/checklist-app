#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 14:22:43 2025

@author: rimeslaoui
"""
import streamlit as st
import json
import os

CHECKLIST_FILE = "checklist.json"

# Load checklist from file
def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save checklist to file
def save_checklist(data):
    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- UI begins here ---

st.set_page_config(page_title="Checklist PLG", layout="centered")

st.title("Règles de gestion PLG")
st.caption("Interface de checklist interactive")

# Light/Dark mode toggle
theme = st.sidebar.radio("Thème", ["Clair", "Sombre"])
if theme == "Sombre":
    st.markdown(
        """<style>
            html, body, [class*="css"] {
                background-color: #0e1117;
                color: #FAFAFA;
            }
        </style>""",
        unsafe_allow_html=True
    )

# Load or init checklist
if "checklist" not in st.session_state:
    st.session_state.checklist = load_checklist()

# Add single item
st.subheader("Ajouter une règle")
new_item = st.text_input("Nouvelle règle")
if st.button("Ajouter"):
    cleaned = new_item.strip()
    if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
        st.session_state.checklist.append({"text": cleaned, "completed": False})
        save_checklist(st.session_state.checklist)
        st.experimental_rerun()

# Add multiple items
with st.expander("Ajouter plusieurs règles"):
    multiline = st.text_area("Écris une règle par ligne")
    if st.button("Ajouter toutes les règles"):
        lines = multiline.strip().split("\n")
        added = 0
        for line in lines:
            cleaned = line.strip()
            if cleaned and cleaned not in [i["text"] for i in st.session_state.checklist]:
                st.session_state.checklist.append({"text": cleaned, "completed": False})
                added += 1
        if added:
            save_checklist(st.session_state.checklist)
            st.experimental_rerun()

# Progress
total = len(st.session_state.checklist)
done = sum(1 for i in st.session_state.checklist if i["completed"])
if total > 0:
    st.subheader("Progression")
    st.write(f"{done} sur {total} règles complétées ({int((done/total)*100)}%)")
    st.progress(done / total)

# Display checklist
st.subheader("Checklist")

for i, item in enumerate(st.session_state.checklist):
    cols = st.columns([0.07, 0.8, 0.13])
    with cols[0]:
        checked = st.checkbox("", value=item["completed"], key=f"check_{i}")
        st.session_state.checklist[i]["completed"] = checked
    with cols[1]:
        st.markdown(f"<div style='line-height: 1.6;'>{'~~' + item['text'] + '~~' if item['completed'] else item['text']}</div>", unsafe_allow_html=True)
    with cols[2]:
        if cols[2].button("Supprimer", key=f"delete_{i}"):
            st.session_state.checklist.pop(i)
            save_checklist(st.session_state.checklist)
            st.experimental_rerun()

# Save on checkbox change
save_checklist(st.session_state.checklist)
