# Understanding the Problem

After reading the introduction thoroughly a couple of times. The first step is to define the problem, its significance, and the requirements expected from our end product.

### Problem

Medsender comes across millions of medical documents each month and it can be quite difficult to extract relevant information from these documents given a) the vast amount of documents and b) the vast amount of document types. For simplicity, the category of medical documents I am working with is lab results. For this challenge I am concerned with extracting the following information:

- Patient Name
- Patient Date of Birth (DOB)
- Patient Address
- Patient Gender
- Ordering Physician Name

My task is to create an endpoint that:

- Accept a lab result document as input
- Proceeds to process the document to extract the information specified above
- Returns the information in the form of a JSON object
- The endpoint should be robust, documented, and easy to read
- As a recommendation for portability, the application should also be dockerized

### Requirements and Goals

I can break down the requirements into two categories: functional and non-functional

Functional Requirements:

- Accept a document
- Extract and return a JSON object of the lab result information above
- Handle a variety of layouts and formats of lab results (although most follow a similar format but can vary in layouts)

Non-Functional Requirements:

- Readable and maintainable code
- Production-level standards for documentation, error handling, modularity, simplicity, etc.
- A design that is able to be extended in the future to handle other requests (this ties into the maintainability non-functional requirement I mentioned first)
- README with clear outline of my problem solving process (what you are reading right now)

### Initial Assumptions

As mentioned, the challenge is open ended so it’s a good idea to make some initial assumptions to help me get started.

- Documents will be provided in a consistent format or a close variation of it. Layouts may vary.
- Input format is likely PDF (should clarify with Mahmoud)
- Documents are English only

### Walking Skeleton

I should start off by outlining the high-level core workflow of this application.

1. **Input:** Lab result pdf document
2. **Processing:**
    1. Validate that the file uploaded is valid
    2. Convert the document into raw text
        1. Another set of validation checks to ensure that the text is able to be extracted accurately
    3. Use text-processing techniques to extract the required fields
    4. Handle any errors or edge cases
3. **Output:** JSON object containing extracted information.

Possible edge cases can occur in the three phases of processing:

### **File Handling Edge Cases**

1. **Unsupported File Format:**
    - Files that are not PDFs (e.g., `.docx`, `.jpg`).
    - Solution: Validate the file extension and MIME type before processing.
2. **Malformed PDFs:**
    - Corrupted or partially downloaded files.
    - Solution: Catch exceptions during PDF parsing and return a meaningful error message.
3. **Encrypted PDFs:**
    - Password-protected files.
    - Solution: Check for encryption and either reject them or request a password (out of scope for now).
4. **Empty Files:**
    - Files with zero content or empty pages.
    - Solution: Validate the file size and check for extracted text content. Return an error if none is found.
5. **Large PDFs:**
    - Documents with an unusually high number of pages or images.
    - Solution: Limit the number of pages processed (e.g., first 50 pages) or log a warning for long processing times.

---

### **Text Extraction Edge Cases**

1. **Scanned PDFs with Poor Quality:**
    - Low-resolution scans or poorly aligned text/images.
    - Solution: Preprocess images (e.g., deskewing, binarization) before OCR.
2. **Non-standard Fonts or Encodings:**
    - Custom fonts or encodings that make text unreadable.
    - Solution: No direct solution, but log the issue and skip problematic sections.
3. **Multi-language Text:**
    - Lab reports containing sections in multiple languages.
    - Solution: Use an OCR/NLP pipeline that supports multiple languages (if required).
4. **Mixed Regular and Scanned Pages:**
    - Some pages with text, others as images.
    - Solution: Detect and process each page type separately (e.g., `pdfplumber` for text, OCR for images).

---

### **Data Extraction Edge Cases**

1. **Missing Fields:**
    - Lab reports without some required fields (e.g., no patient address or gender).
    - Solution: Return a partial JSON with placeholders (`null` or `missing`) for missing fields.
2. **Ambiguous Information:**
    - Multiple occurrences of the same field (e.g., two names that could be the patient’s).
    - Solution: Use NLP models or heuristics to prioritize likely matches (e.g., proximity to known labels like "Patient Name").
3. **Unstructured Data:**
    - Fields appearing in free-form paragraphs or non-tabular formats.
    - Solution: Use regex or Named Entity Recognition (NER) models to extract relevant information.
4. **Inconsistent Layouts:**
    - Lab reports with varying formats and layouts (e.g., header/footer placement, table structures).
    - Solution: Test on multiple layouts and consider a hybrid approach (regex + ML models).

---

### **API-Level Edge Cases**

1. **Multiple File Uploads:**
    - Users accidentally upload multiple files when only one is expected.
    - Solution: Restrict uploads to one file per request.
2. **Interrupted Uploads:**
    - Files that fail to upload completely.
    - Solution: Validate the file size and check for valid content before processing.
3. **Invalid JSON Responses:**
    - Issues in the data extraction logic causing malformed JSON.
    - Solution: Ensure extracted data is validated and serialized properly.
4. **Timeouts:**
    - Long processing times for large or complex PDFs.
    - Solution: Set a reasonable timeout and return an error message if exceeded.
5. **Concurrent Requests:**
    - Multiple users uploading files simultaneously.
    - Solution: Test concurrency limits and optimize memory usage (e.g., process files in chunks).

---

### **Security Edge Cases**

1. **Malicious Files:**
    - PDFs containing malicious code or extremely large sizes to cause a denial-of-service (DoS) attack.
    - Solution: Limit file size and validate files before processing. Use a secure library for parsing.
2. **Sensitive Data Handling:**
    - Logs or temporary files inadvertently storing sensitive information.
    - Solution: Avoid logging sensitive data and securely delete temporary files after use.

---

### **Output Edge Cases**

1. **Partially Extracted Data:**
    - Returning incomplete or incorrect data due to parsing errors.
    - Solution: Clearly indicate which fields were successfully extracted and log issues for debugging.
2. **Unexpected JSON Structure:**
    - Inconsistent field names or structures in the output JSON.
    - Solution: Use a data model (e.g., Pydantic) to enforce a consistent schema.

---

### **How to Handle These Edge Cases**

1. **Validation:**
    - Validate inputs (e.g., file type, size) before processing.
2. **Graceful Failure:**
    - Catch exceptions and return informative error messages instead of crashing.
3. **Logging:**
    - Log issues with sufficient detail for debugging.
4. **Testing:**
    - Create test cases for each edge case (e.g., corrupted files, missing fields).
5. **Documentation:**
    - Document assumptions (e.g., handling missing fields) and known limitations.