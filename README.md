# Medsender Challenge - Lab Result Extraction

## Problem Statement

Medsender processes millions of medical documents monthly, making it challenging to extract relevant information due to:

1. The vast quantity of documents.
2. The variety of formats and layouts.

For this challenge, I focus on **lab results** and aim to extract the following fields:

- Patient Name
- Patient Date of Birth (DOB)
- Patient Address
- Patient Gender
- Ordering Physician Name

### Task Requirements

- Create an endpoint to:
    1. Accept a lab result document (PDF).
    2. Extract the specified fields.
    3. Return a structured JSON response.
- Ensure the solution is:
    - **Robust**: Handle edge cases like malformed files, missing fields, etc.
    - **Maintainable**: Production-level documentation, error handling, and modularity.
    - **Portable**: Dockerized for easy deployment.

---

## Approach and Workflow

### Core Workflow

1. **Input**: Accept a lab result PDF.
2. **Processing**:
    - Validate file type, size, and structure.
    - Extract raw text from the document (using OCR for scanned PDFs if needed).
    - Process the text to extract relevant fields.
    - Handle errors and edge cases.
3. **Output**: Return a JSON object with extracted information.

### Requirements

### Functional:

- Accept and process PDF documents.
- Extract and return specified fields as JSON.
- Handle diverse layouts and formats.

### Non-Functional:

- Code should be maintainable, modular, and extensible.
- Comprehensive documentation and tests.
- Scalable design for future enhancements.

### Initial Assumptions

- Input documents are PDFs (scanned or native) with a maximum of 2 pages.
- Text is in English.
- Variations in layout are expected but not extreme.

---

## Challenges and Solutions

### **1. Text Extraction**

### Challenges:

- **Issue**: PDFs with complex layouts often lose logical ordering during text extraction.
- **Tried**: Libraries like `pdfplumber` and EasyOCR.
    - Results: Text extracted successfully but lacked meaningful structure.

### Solution:

- Used **Llama Parse** from LlamaIndex for text extraction.
    - Leverages LLMs to extract and organize text in Markdown format.
    - Maintains logical ordering and categorization, addressing layout challenges.

### **2. Noisy Data**

### Challenges:

- Extracted text included irrelevant information and inconsistent formatting.
- Regex and Named Entity Recognition (NER) were ineffective for cleaning noisy text across varying layouts.

### Solution:

- Combined **Llama Parse** with targeted prompt engineering to improve logical structure and clean extracted data.

### **3. Field Extraction**

### Challenges:

- Accurately extracting fields like "Patient Name" and "DOB" across inconsistent layouts. Some documents have “Date of Birth” whereas some have “DOB”. Some documents have “Patient Name” while others have “Pt. Name”. This is why regex is a complex approach.
- I noticed that I can turn this into a document question answering task which is a machine learning task focused on answering questions on document images. Essentially, you pass a pair into the model (document, question) as input and the model returns an output in natural language. QA models are trained on data of images of pdfs which were annotated with bounding boxes around relevant fields of extraction. However, off-the-shelf multi-modal models like LayoutLMV3 struggled without fine-tuning due to a lack of annotated training data. I didn’t have access to huge samples of lab results annotated with bounding boxes around the relevant fields, so this wasn’t a trustworthy solution. **Additionally, some of QA models take a long time to return an output, which is not ideal.** Here is the code for the QA models I wrote before concluding this was not a scalable approach:
    
    ```python
    !pip install transformers datasets pillow pypdf2 pdf2image
    !apt-get install -y poppler-utils
    !apt-get update
    !apt-get install -y tesseract-ocr
    !pip install pytesseract
    !pip install transformers datasets pytesseract pillow
    !apt-get install -y tesseract-ocr
    
    from transformers import pipeline
    from PIL import Image
    from pdf2image import convert_from_path
    import json
    
    # Convert the pdf to an image
    images = convert_from_path("/content/lab-result1.pdf")
    images[0].save("page1.png", "PNG")
    image = Image.open("page1.png")
    
    # Load the document qna pipeline with naver-clova-ix/donut-base-finetuned-docvqa model
    doc_qa_pipeline = pipeline("document-question-answering", model="naver-clova-ix/donut-base-finetuned-docvqa")
    
    # Ask the model for all the fields we need
    patient_name = doc_qa_pipeline(image="page1.png", question="What is the patient's name?")
    patient_dob = doc_qa_pipeline(image="page1.png", question="What is the patient's date of birth?")
    patient_gender = doc_qa_pipeline(image="page1.png", question="What is the patient's gender?")
    patient_address = doc_qa_pipeline(image="page1.png", question="What is the patient's address?")
    physician_name = doc_qa_pipeline(image="page1.png", question="Who is the ordering physician?")
    
    # Create a json
    output = {
        "Patient Name": patient_name,
        "Patient Date of Birth": patient_dob,
        "Patient Gender": patient_address,
        "Patient Address": patient_gender,
        "Ordering Physician Name": physician_name
    }
    
    print(output) # Some fields were correct, but some were wrong
    ```
    

### Solution:

- Used **OpenAI's GPT-4o-mini API**:
    - Provided well-structured parsed text as input.
    - Designed a prompt to ensure consistent and accurate JSON outputs.

---

### Key Design Principles

1. **Modular Design**:
    - Abstracted functionality into reusable components for validation, processing, and modeling.
    - Example: Validators for file size, extension, and MIME type are modular and easily extendable.
2. **Extensibility**:
    - Prepared for future enhancements (e.g., adding new document types or models) with minimal changes to the core structure.
3. **Simplicity**:
    - Followed SOLID principles to ensure each class has a single responsibility and is open for extension, not modification.

---

## Software Architecture

### UML Overview

![structure](https://github.com/user-attachments/assets/a87cfc42-0bf2-42da-9f55-427b69728e0e)

### Highlights:

- **Validators**: Modular and reusable for file validation (size, type, etc.).
- **Processors**: Extendable to handle different file types (e.g., PDF, spreadsheets).
- **Models**: Base model class for easy integration of different AI models (e.g., OpenAI, LayoutLMV3).

This was designed with the purpose of being maintainable and extensible. Later down the line, we may have to parse through other document types. It should be easy to add this functionality. All you have to do is extend the BaseProcessor class and implement your new logic in there. This promotes single responsibility and the open-closed principle of software design. Similarly, if you wanted to use a different model, say some model on the HuggingFace Model Hub, you can simply add this functionality by extending the ModelHandler class and implementing your logic there. Same approach with the file handling validators. However, there is even more abstraction as all you have to do is instantiate a CompositeValidator and specify which validations you want done and it will handle all that for you. Additionally, the individual validator classes are designed to work with any document type, so they aren’t tailored for pdfs.

### Pipeline:

![pipeline](https://github.com/user-attachments/assets/d93e25a4-3298-4458-ab34-560113861b2c)

### Tech Stack Used:

**1. Programming Language**

- Python:
    - Used for its simplicity, rich ecosystem of libraries, and strong support for handling text extraction, API development, and machine learning integrations.

**2. Backend Framework**

- FastAPI:
    - Lightweight and modern Python framework for building RESTful APIs.
    - Provides built-in support for asynchronous requests and interactive API documentation through Swagger UI.

**3. API’s**

- OpenAI API:
    - Used GPT-4o-mini to extract relevant fields from parsed text with high accuracy.
- Llama Parse:
    - Leveraged Llama Parse for structured and logical text extraction from complex PDFs.

**4. PDF Handling and Text Extraction**

- pdfplumber:
    - Extracted raw text from native PDFs.
- PyPDF2:
    - Validated and processed PDF structure.

**5. Containerization/Deployment**

- Docker

**6. Testing**

- Pytest

**7. Development Tools**

- PyCharm
- Git and GitHub

This stack was chosen to ensure the application is reliable, maintainable, and extensible while meeting production-grade standards.

---

## Edge Cases and Error Handling

### File Handling

- **Unsupported Formats**: Validate file extensions and MIME types.
- **Malformed/Empty Files**: Reject invalid or empty PDFs with meaningful error messages.
- **Large Files**: Reject PDFs exceeding a size limit.

### Text Extraction

- Handle mixed scanned and text-based pages using OCR and text parsing tools.

### Data Extraction

- **Missing Fields**: Include placeholders like `"not present"` for unavailable fields.
- **Ambiguity**: Use proximity-based heuristics or NLP techniques for disambiguation.

### Security

- Reject malicious files and securely delete temporary files to avoid sensitive data leakage.

---

## Implementation Highlights

1. **Input Validation**:
    - Used composite validators for file type, size, and content validation.
2. **Text Parsing**:
    - Leveraged Llama Parse for structured text extraction.
3. **Field Extraction**:
    - Passed structured text to GPT-4o-mini with a carefully crafted prompt.
4. **Error Handling**:
    - Comprehensive handling of edge cases with user-friendly error messages.

---

## Key Decisions

### 1. Text Extraction Techniques:

- OCR libraries like EasyOCR and tools like `pdfplumber` struggled with noisy text and complex layouts.
- Chose Llama Parse for its ability to maintain logical structure.

### 2. Model Selection:

- Explored document question-answering models like LayoutLM but lacked annotated data for fine-tuning.
- Chose OpenAI GPT-4o-mini for its robustness and ease of integration.

---

## Conclusion

This solution demonstrates a practical approach to extracting structured data from lab results:

- **Scalable**: The architecture can easily be extended to handle new formats and models.
- **Reliable**: Handles edge cases and provides consistent outputs.
- **Efficient**: Combines the power of Llama Parse and GPT-4o-mini for accurate field extraction.

---

## Is this my ideal solution?

No. I would keep my current solution but on the side I would be working on this approach:

- Collect a couple thousand samples of lab results similar to the ones given by LabCorp
- Use an annotation tool like Library Studio to annotate the lab results with bounding boxes around the relevant fields (this is a long process, so not ideal, but it would lead to high accuracy)
- Train a LayoutLMV3 model on this data to identify with high accuracy and precision, the relevant fields.
- Develop a validation algorithm that will validate the answers given by the model before returning the structured JSON.

Due to the way the design was set up, this approach would be easy to add to the codebase as well.

---

## **How to Run the App**

This section provides two ways to run the app: 

1. locally for development and testing
2. Using Docker for a portable, containerized deployment.

### **1. Running Locally**

1. **Clone the Repository**:
    
    ```bash
    git clone git@github.com:AHMEDELZARIA/medsender-challenge.git
    cd medsender-challenge
    ```
    
2. **Set Up a Virtual Environment (Optional)**:
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    ```
    
3. **Install Dependencies**:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Run the App**:
    
    ```bash
    uvicorn app.main:app --reload
    ```
    
5. **Access the API**:
    - Visit `http://localhost:8000/docs` to view the interactive Swagger API documentation. The endpoint is called “/extract”

---

### **2. Running with Docker**

1. **Build the Docker Image**:
    
    ```bash
    docker build -t medsender-challenge .
    ```
    
2. **Run the Docker Container**:
    
    ```bash
    docker run -d -p 8000:8000 medsender-challenge
    
    ```
    
3. **Access the API**:
    - Visit `http://localhost:8000/docs` to view the interactive Swagger API documentation.
4. **Stop the Docker Container** (if needed):
    
    ```bash
    docker ps  # Find the container ID
    docker stop <container_id>
    ```
