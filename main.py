import streamlit as st
from readPDF import AIReader  # Supposons que votre classe est dans un fichier nommé aireader.py

def main():
    st.title("Analyseur de Documents IA")
    st.write("Téléchargez un document et posez vos questions")
    
    # Initialisation de l'AIReader
    reader = AIReader()
    
    # Zone de téléchargement de fichier
    uploaded_file = st.file_uploader("Choisissez un fichier", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        # Afficher des informations sur le fichier téléchargé
        st.write(f"Fichier téléchargé: {uploaded_file.name} ({uploaded_file.type})")
        
        # Extraire le texte du document
        with st.spinner("Extraction du texte..."):
            text = reader.extract_text(uploaded_file)
            st.success("Texte extrait avec succès!")
        
        # Prévisualisation du texte (limitée)
        with st.expander("Aperçu du texte extrait"):
            st.write(text[:500] + "..." if len(text) > 500 else text)
        
        # Zone pour entrer la requête
        query = st.text_area("Posez votre question concernant le document:", height=100)
        
        if st.button("Analyser"):
            if query:
                with st.spinner("Analyse en cours..."):
                    # Analyse du contenu avec la requête
                    result = reader.analyze_content(text, query)
                    
                    # Affichage du résultat (déjà géré par le streaming, mais au cas où)
                    if not any(chunk.strip() for chunk in result.split()):
                        st.error("Aucun résultat n'a été obtenu. Veuillez vérifier votre question.")

if __name__ == "__main__":
    main()