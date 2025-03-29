import PyPDF2
import docx
from openai import OpenAI

class AIReader:
    def __init__(self):
        self.client = OpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1"
        )
        self.model = "deepseek-r1"
        
    def extract_text(self, uploaded_file):
        text = ""
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()  # Corrigé '*=' en '+='
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # Corrigé l'orthographe
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = str(uploaded_file.read(), "utf-8")
        return text
        
    def analyze_content(self, text, query):
        # Limiter le texte à 3200 caractères de manière sécurisée
        truncated_text = text[:3200] + "..." if len(text) > 3200 else text
        
        prompt = f"""Analyse text and answer the following query:
        Text: {truncated_text}
        Query: {query}
        Provide:
        1. Direct answer to the query
        2. Supporting evidence
        3. Key findings
        4. Limitations of the analysis
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "you are... "
                    },
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            
            import streamlit as st  # Importation ajoutée
            
            result = st.empty()
            collected_chunks = []
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    collected_chunks.append(chunk.choices[0].delta.content)
                    result.markdown("".join(collected_chunks))  # Corrigé 'mardown' en 'markdown'
            
            return "".join(collected_chunks)
        except Exception as e:  # Gestion des exceptions ajoutée
            return f"Erreur lors de l'analyse: {str(e)}"