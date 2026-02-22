from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# ----------------------------
# FASTA conversion function
# ----------------------------
def multiline_to_singleline_fasta(input_file, output_file):
    """
    Converts a multi-line FASTA file to proper single-line FASTA.
    Headers remain on their own line.
    Sequence lines are fully merged into one line.
    """
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        header = None
        sequence = []

        for line in f_in:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            if line.startswith('>'):
                # Write previous sequence
                if header:
                    f_out.write(header + '\n')
                    f_out.write(''.join(sequence) + '\n')
                header = line
                sequence = []
            else:
                sequence.append(line)
        
        # Write last sequence
        if header:
            f_out.write(header + '\n')
            f_out.write(''.join(sequence) + '\n')

# ----------------------------
# Route: Home page (index.html)
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------
# Route: Handle conversion
# ----------------------------
@app.route("/convert", methods=["POST"])
def convert():
    fasta_file = request.files.get('fasta_file')
    fasta_text = request.form.get('fasta_text')

    input_path = "input.fasta"

    # Save uploaded file or textarea content
    if fasta_file and fasta_file.filename != '':
        fasta_file.save(input_path)
    elif fasta_text and fasta_text.strip() != '':
        with open(input_path, 'w') as f:
            f.write(fasta_text)
    else:
        return "No input provided", 400

    output_path = "output.fasta"
    multiline_to_singleline_fasta(input_path, output_path)

    # Read converted file
    with open(output_path, 'r') as f:
        fasta_content = f.read()

    return render_template("result.html", fasta_content=fasta_content)
# ----------------------------
# Run Flask app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)