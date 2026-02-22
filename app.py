import streamlit as st

# ----------------------------
# FASTA conversion function
# ----------------------------
def multiline_to_singleline_fasta(input_text):
    lines = input_text.splitlines()
    output = []
    header = None
    sequence = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header:
                output.append(header)
                output.append("".join(sequence))
            header = line
            sequence = []
        else:
            sequence.append(line)

    if header:
        output.append(header)
        output.append("".join(sequence))

    return "\n".join(output)


# ----------------------------
# Load HTML helper
# ----------------------------
def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------
# Show index.html
# ----------------------------
index_html = load_html("templates/index.html")

# Remove Flask form section
if "<form" in index_html:
    start = index_html.find("<form")
    end = index_html.find("</form>") + len("</form>")
    index_html = index_html[:start] + index_html[end:]

# Replace Flask static path
index_html = index_html.replace(
    "{{ url_for('static', filename='images/proteins2.gif') }}",
    "static/images/proteins2.gif"
)

st.markdown(index_html, unsafe_allow_html=True)

# ----------------------------
# Streamlit Input Section
# ----------------------------
st.markdown("### Place your multi-line FASTA sequence here:")

fasta_text = st.text_area("", height=200)
uploaded_file = st.file_uploader("Or upload FASTA file", type=["fasta", "fa", "txt"])

if st.button("Submit"):

    if uploaded_file:
        fasta_text = uploaded_file.read().decode("utf-8")

    if not fasta_text.strip():
        st.error("No input provided.")
    else:
        result = multiline_to_singleline_fasta(fasta_text)

        # Load result.html
        result_html = load_html("templates/result.html")

        # Replace Jinja variable manually
        result_html = result_html.replace("{{ fasta_content }}", result)

        st.markdown(result_html, unsafe_allow_html=True)
