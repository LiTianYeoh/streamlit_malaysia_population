# streamlit_malaysia_population
A simple streamlit app created using malaysia population data from DOSM, mainly for trial purposes.
 
To run, simply clone the repo, install the necessary libraries and run `streamlit run .\Homepage.py`. \
Then head to any browser to view the streamlit app at the default streamlit port (http://localhost:8501).

## Running with docker
Again, this is mainly for my own trial purpose. \
To create image: run `docker build -f .\test_streamlit_github_dockerfile -t test_streamlit .` \
To create container from the image above: `docker run -d -p 8501:8501 test_streamlit`
