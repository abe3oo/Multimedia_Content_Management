LETS DO THIS !!!
Sure! Here's the README content translated into English for your project:

---

## Project Overview

This project aims to analyze two CSV files containing information about images and articles. After analyzing and storing the data in a PostgreSQL database, the information is displayed on a website designed with Flask. Additionally, to complete the missing information about the images, an API from the website phototag.ai is used to fill in the missing details in the database.

### Features
- Analyze CSV files with image and article data.
- Store analyzed data in a PostgreSQL database.
- Display the data on a Flask-based website.
- Utilize the phototag.ai API to supplement missing image information.

### Installation
To set up this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database and update the configuration in the `database.ini` file.

5. Run the application:
    ```bash
    flask run
    ```

### Usage
1. Place the CSV files in the designated directory.
2. Run the data analysis script to process and store the data in the database.
3. Access the Flask application to view the data.

### API Integration
The project integrates with the phototag.ai API to complete missing image information. Ensure you have the API key and update the configuration accordingly.
