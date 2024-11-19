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
    1. Convert the document into raw text
    2. Use text-processing techniques to extract the required fields
    3. Handle any errors or edge cases
        1. Edge cases may include
3. **Output:** JSON object containing extracted information.
