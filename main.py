import sys
import streamlit as st
from model.word_correction import WordCorrection
from model.object_detection import ObjectDetection
from model.chatbot import Chatbot


def main():
    menu = ["Word Correction", "Object Detection", "Chatbot"]
    choice = st.sidebar.selectbox("Select Application", menu)

    if choice == "Word Correction":
        model = WordCorrection()
        model.display()
    elif choice == "Object Detection":
        model = ObjectDetection()
        model.display()
    elif choice == "Chatbot":
        model = Chatbot()
        model.display()


if __name__ == "__main__":
    main()
