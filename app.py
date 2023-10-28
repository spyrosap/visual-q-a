from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic
import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()

schema = {
        "properties": {
            "sentiment": {"type": "string"},
            "language": {"type": "string"},
            }
        }
def tag_document(text) :
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    chain = create_tagging_chain(schema, llm)
    result = chain.run(text)
    return result


#Get text from the pdf 
def get_pdf_text(pdf_docs): 
    text="" 
    for pdf in pdf_docs : 
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages :
            text += page.extract_text()
    return text


def main(): 
    load_dotenv()
    st.set_page_config(page_title='Tag your pdf documents',
                        page_icon=':books:')
    st.header('Tag your documents')
    
    with st.sidebar : 
        st.subheader('Your documents')
        pdf_docs = st.file_uploader(
            "Upload your PDF here and click on process",accept_multiple_files=True
        )
        if st.button('Process'):
            with st.spinner('Processing'):
                #transform PDF to text 
                raw_text= get_pdf_text(pdf_docs)
                tagged = tag_document(raw_text)
                st.write(tagged)

    
if __name__ == '__main__':
    main()