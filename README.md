# Data-Res-Aview

## Streamlit App

This is a Streamlit app that provides Youtube trend analysis for top channel, youtuber, and videos.

### Installation and Setup

1. Clone the repository: 

`git clone https://github.com/samwong21/Data-Res-Aview.git`

2. Navigate to the project directory:

`cd [your-repo]`

3. Install packages automatically managed by pipenv using pipenv:

`pipenv install`

4. Install other required dependencies using pip:

`pip install -r [Whatever package is not installed when running streamlit run dashboard.py]`

5. add a `.env` file to folder 

In `.env` file, add

`YOUTUBE_API_KEY = [YOUR API KEY HERE]`


## Usage

1. Run the Streamlit app:

`streamlit run dashboard.py`

2. If app does not pop up automatically, access the app in your web browser by opening the provided URL (usually http://localhost:8501).


## Folder Structure

- `dashboard.py`:  Main entry point of the Streamlit app.
- pages/                 # Folder containing subpages
  - .py ...               # Subpages end in .py

## Contributing

[TODO: Provide guidelines for others to contribute to your project if applicable].

## License

[TODO: Specify the license under which your project is distributed].

## Contact

[TODO: Provide your contact information if users have any questions or feedback].


