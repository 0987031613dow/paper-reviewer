import os
import streamlit as st
import subprocess
import json
import shutil
from pathlib import Path
import time
import threading

# Include the necessary paper-reviewer modules
from pipeline.download import (
    remove_version_from_string,
    download_pdf_from_arxiv,
    download_pdf_from_openreview,
    get_paper_from_arxiv_by_openreview
)

def read_review_data(paper_id):
    """Read the generated review data for display"""
    paper_id = remove_version_from_string(paper_id)
    
    data = {}
    
    # Read essential info
    try:
        with open(f"{paper_id}/essential.json", "r") as f:
            data["essential"] = json.load(f)
    except:
        data["essential"] = {}
    
    # Read sections
    try:
        with open(f"{paper_id}/sections.json", "r") as f:
            data["sections"] = json.load(f)
    except:
        data["sections"] = []
    
    # Read figures
    try:
        with open(f"{paper_id}/figures.json", "r") as f:
            data["figures"] = json.load(f)
    except:
        data["figures"] = []
    
    # Read tables
    try:
        with open(f"{paper_id}/tables.json", "r") as f:
            data["tables"] = json.load(f)
    except:
        data["tables"] = []
    
    # Read references
    try:
        with open(f"{paper_id}/references.json", "r") as f:
            data["references"] = json.load(f)
    except:
        data["references"] = {}
    
    return data

def process_arxiv_id(arxiv_id, use_upstage, use_mineru, stop_at_no_html):
    """Process an arXiv ID to generate a paper review"""
    if not arxiv_id:
        return "Please provide an arXiv ID", None
    
    # Clean up input - remove any "arXiv:" prefix and whitespace
    arxiv_id = arxiv_id.strip()
    if arxiv_id.lower().startswith("arxiv:"):
        arxiv_id = arxiv_id[6:].strip()
    
    # Create command to execute collect.py with appropriate options
    cmd = ["python", "collect.py", "--arxiv-id", arxiv_id]
    
    if use_upstage:
        cmd.append("--use-upstage")
    if use_mineru:
        cmd.append("--use-mineru")
    if stop_at_no_html:
        cmd.append("--stop-at-no-html")
    
    try:
        # Run the collect.py script
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Process output
        clean_arxiv_id = remove_version_from_string(arxiv_id)
        review_data = read_review_data(clean_arxiv_id)
        
        # Run convert.py to generate a blog post
        convert_cmd = ["python", "convert.py", "--arxiv-id", arxiv_id]
        convert_result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        # Find the HTML file path
        html_output_path = None
        if os.path.exists(f"{clean_arxiv_id}/index.html"):
            html_output_path = f"{clean_arxiv_id}/index.html"
        
        return "Review generated successfully!", review_data
        
    except subprocess.CalledProcessError as e:
        return f"Error processing paper: {e.stderr}", None
    except Exception as e:
        return f"Error: {str(e)}", None

def process_openreview_id(openreview_id, use_upstage, use_mineru, stop_at_no_html):
    """Process an OpenReview ID to generate a paper review"""
    if not openreview_id:
        return "Please provide an OpenReview ID", None
    
    # Create command to execute collect.py with appropriate options
    cmd = ["python", "collect.py", "--openreview-id", openreview_id]
    
    if use_upstage:
        cmd.append("--use-upstage")
    if use_mineru:
        cmd.append("--use-mineru")
    if stop_at_no_html:
        cmd.append("--stop-at-no-html")
    
    try:
        # Run the collect.py script
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Process output
        review_data = read_review_data(openreview_id)
        
        # Run convert.py to generate a blog post
        convert_cmd = ["python", "convert.py", "--openreview-id", openreview_id]
        convert_result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        # Find the HTML file path
        html_output_path = None
        if os.path.exists(f"{openreview_id}/index.html"):
            html_output_path = f"{openreview_id}/index.html"
        
        return "Review generated successfully!", review_data
        
    except subprocess.CalledProcessError as e:
        return f"Error processing paper: {e.stderr}", None
    except Exception as e:
        return f"Error: {str(e)}", None

def display_review_data(review_data):
    # Essential info
    essential = review_data.get("essential", {})
    if essential:
        st.title(essential.get('title', 'Unknown Title'))
        st.write(f"**Authors:** {essential.get('authors', 'Unknown')}")
        
        st.subheader("Abstract")
        st.write(essential.get('abstract', 'Not available'))
        
        # Add affiliations if available
        affiliation = essential.get("affiliation", [])
        if affiliation:
            st.subheader("Affiliations")
            for aff in affiliation:
                st.write(f"- {aff}")
        
        # Add categories if available
        categories = essential.get("categories", [])
        if categories:
            st.subheader("Categories")
            st.write(", ".join(categories))
    
    # Sections
    sections = review_data.get("sections", [])
    if sections:
        st.header("Paper Structure")
        for section in sections:
            with st.expander(section.get('title', 'Unknown Section')):
                st.write(section.get('details', 'No details available'))
    
    # Figures
    figures = review_data.get("figures", [])
    if figures:
        st.header(f"Figures ({len(figures)})")
        for i, figure in enumerate(figures):
            with st.expander(f"Figure {i+1}: {figure.get('caption', 'No caption')}"): 
                st.write(figure.get('description', 'No description available'))
                # If there's a figure path, display it
                if 'path' in figure and os.path.exists(figure['path']):
                    st.image(figure['path'])
    
    # References
    references = review_data.get("references", {}).get("references", [])
    if references:
        st.header(f"References ({len(references)})")
        with st.expander("Show References"):
            for i, ref in enumerate(references):
                st.write(f"{i+1}. {ref}")

def main():
    st.set_page_config(
        page_title="AI Paper Reviewer",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.sidebar.title("AI Paper Reviewer")
    st.sidebar.info(
        "Generate comprehensive reviews of academic papers from arXiv or OpenReview using the "
        "[paper-reviewer](https://github.com/deep-diver/paper-reviewer) project."
    )
    
    # Add API key configuration in sidebar
    with st.sidebar.expander("API Configuration", expanded=False):
        gemini_api_key = st.text_input("Gemini API Key", type="password")
        if gemini_api_key:
            os.environ["GEMINI_API_KEY"] = gemini_api_key
            st.success("Gemini API Key set!")
        
        upstage_api_key = st.text_input("Upstage API Key (Optional)", type="password")
        if upstage_api_key:
            os.environ["UPSTAGE_API_KEY"] = upstage_api_key
            st.success("Upstage API Key set!")
    
    tab1, tab2, tab3 = st.tabs(["Review arXiv Papers", "Review OpenReview Papers", "About"])
    
    with tab1:
        st.header("Review arXiv Papers")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            arxiv_id = st.text_input("arXiv ID (e.g., 2310.06825)", placeholder="Enter arXiv ID")
        with col2:
            st.write("")
            st.write("")
            process_button = st.button("Process Paper", type="primary", key="arxiv_process")
        
        with st.expander("Advanced Options"):
            use_upstage = st.checkbox("Use Upstage for figure extraction", value=False, key="arxiv_upstage")
            use_mineru = st.checkbox("Use MinerU for figure extraction", value=False, key="arxiv_mineru")
            stop_at_no_html = st.checkbox("Stop if no HTML is found", value=True, key="arxiv_html")
        
        if process_button and arxiv_id:
            if not os.environ.get("GEMINI_API_KEY") and not gemini_api_key:
                st.error("Please set your Gemini API Key in the sidebar first!")
            else:
                with st.spinner("Processing paper... This may take a few minutes."):
                    # Create a progress bar
                    progress_bar = st.progress(0)
                    
                    # Update progress in a separate thread
                    def update_progress():
                        for i in range(100):
                            progress_bar.progress(i/100)
                            time.sleep(1.5)  # Slower progress to account for longer processing time
                    
                    progress_thread = threading.Thread(target=update_progress)
                    progress_thread.start()
                    
                    # Process the paper
                    message, review_data = process_arxiv_id(
                        arxiv_id,
                        use_upstage,
                        use_mineru,
                        stop_at_no_html
                    )
                    
                    # Stop the progress thread
                    progress_thread.join(timeout=0.1)
                    progress_bar.progress(1.0)
                    
                    # Display the result
                    if "Error" in message:
                        st.error(message)
                    else:
                        st.success(message)
                    
                    if review_data:
                        st.subheader("Paper Review")
                        display_review_data(review_data)
                        
                        # Show download link for the full HTML review if available
                        clean_arxiv_id = remove_version_from_string(arxiv_id)
                        html_path = f"{clean_arxiv_id}/index.html"
                        if os.path.exists(html_path):
                            with open(html_path, "r", encoding="utf-8") as f:
                                html_content = f.read()
                            st.download_button(
                                "Download Full HTML Review",
                                html_content,
                                file_name=f"review_{clean_arxiv_id}.html",
                                mime="text/html"
                            )
    
    with tab2:
        st.header("Review OpenReview Papers")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            openreview_id = st.text_input("OpenReview ID", placeholder="Enter OpenReview ID")
        with col2:
            st.write("")
            st.write("")
            process_or_button = st.button("Process Paper", type="primary", key="openreview_process")
        
        with st.expander("Advanced Options"):
            use_upstage_or = st.checkbox("Use Upstage for figure extraction", value=False, key="or_upstage")
            use_mineru_or = st.checkbox("Use MinerU for figure extraction", value=False, key="or_mineru")
            stop_at_no_html_or = st.checkbox("Stop if no HTML is found", value=True, key="or_html")
        
        if process_or_button and openreview_id:
            if not os.environ.get("GEMINI_API_KEY") and not gemini_api_key:
                st.error("Please set your Gemini API Key in the sidebar first!")
            else:
                with st.spinner("Processing paper... This may take a few minutes."):
                    # Create a progress bar
                    progress_bar = st.progress(0)
                    
                    # Update progress in a separate thread
                    def update_progress():
                        for i in range(100):
                            progress_bar.progress(i/100)
                            time.sleep(1.5)  # Slower progress to account for longer processing time
                    
                    progress_thread = threading.Thread(target=update_progress)
                    progress_thread.start()
                    
                    # Process the paper
                    message, review_data = process_openreview_id(
                        openreview_id,
                        use_upstage_or,
                        use_mineru_or,
                        stop_at_no_html_or
                    )
                    
                    # Stop the progress thread
                    progress_thread.join(timeout=0.1)
                    progress_bar.progress(1.0)
                    
                    # Display the result
                    if "Error" in message:
                        st.error(message)
                    else:
                        st.success(message)
                    
                    if review_data:
                        st.subheader("Paper Review")
                        display_review_data(review_data)
                        
                        # Show download link for the full HTML review if available
                        html_path = f"{openreview_id}/index.html"
                        if os.path.exists(html_path):
                            with open(html_path, "r", encoding="utf-8") as f:
                                html_content = f.read()
                            st.download_button(
                                "Download Full HTML Review",
                                html_content,
                                file_name=f"review_{openreview_id}.html",
                                mime="text/html"
                            )
    
    with tab3:
        st.header("About AI Paper Reviewer")
        st.write(
            """
            This application is powered by the [paper-reviewer](https://github.com/deep-diver/paper-reviewer) project by deep-diver,
            which uses AI to generate comprehensive reviews of academic papers.
            
            ### Features
            
            - Extract and visualize key information from research papers
            - Generate detailed summaries of each section
            - Identify and extract figures and tables with captions
            - Compile references and citations
            
            ### How It Works
            
            1. Enter an arXiv ID or OpenReview ID
            2. The application will download the paper and extract its contents
            3. It processes the paper using Google's Gemini API to generate a comprehensive review
            4. The review is presented in an easy-to-navigate format
            
            ### Requirements
            
            - Google Gemini API Key (required)
            - Upstage API Key (optional, for better figure extraction)
            
            ### Credits
            
            - Original project: [deep-diver/paper-reviewer](https://github.com/deep-diver/paper-reviewer)
            - Website implementation: [AI Paper Reviewer](https://deep-diver.github.io/ai-paper-reviewer)
            """
        )

if __name__ == "__main__":
    main()
