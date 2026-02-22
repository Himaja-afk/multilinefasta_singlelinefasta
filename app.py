import streamlit as st
import streamlit.components.v1 as components
import os

# ----------------------------
# FASTA conversion function (UNCHANGED)
# ----------------------------
def multiline_to_singleline_fasta(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        header = None
        sequence = []

        for line in f_in:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if header:
                    f_out.write(header + '\n')
                    f_out.write(''.join(sequence) + '\n')
                header = line
                sequence = []
            else:
                sequence.append(line)

        if header:
            f_out.write(header + '\n')
            f_out.write(''.join(sequence) + '\n')

# ----------------------------
# Load HTML file
# ----------------------------
def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ----------------------------
# Show index.html
# ----------------------------
html_content = load_html("templates/index.html")
st.markdown(html_content, unsafe_allow_html=True)

# ----------------------------
# Upload & Convert Section
# ----------------------------
uploaded_file = st.file_uploader("Upload FASTA file")
fasta_text = st.text_area("Or paste FASTA here")

if st.button("Convert"):

    input_path = "input.fasta"

    if uploaded_file:
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())
    elif fasta_text.strip():
        with open(input_path, "w") as f:
            f.write(fasta_text)
    else:
        st.error("No input provided")
        st.stop()

    output_path = "output.fasta"
    multiline_to_singleline_fasta(input_path, output_path)

    with open(output_path, "r") as f:
        result = f.read()

    # Load result template and inject content
    result_html = load_html("templates/result.html")
    result_html = result_html.replace("{{ fasta_content }}", result)

    st.markdown(result_html, unsafe_allow_html=True)
