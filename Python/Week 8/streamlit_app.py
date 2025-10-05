#!/usr/bin/env python3
"""
Simple COVID-19 Data Explorer - Streamlit App
Basic version that works with minimal dependencies

This app provides a simple interface for exploring COVID-19 research data.
For full functionality, install all packages from requirements.txt
"""

try:
    import streamlit as st
except ImportError:
    print("❌ Streamlit not installed. Please run: pip install streamlit")
    exit(1)

import csv
import json
from collections import Counter
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="COVID-19 Research Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.chart-container {
    background-color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(filename):
    """
    Load and cache the CSV data
    """
    try:
        data = []
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        return data, None
    except FileNotFoundError:
        return None, f"File not found: {filename}"
    except Exception as e:
        return None, f"Error loading data: {e}"

@st.cache_data
def clean_and_process_data(data):
    """
    Clean and process the loaded data
    """
    cleaned_data = []
    
    for row in data:
        # Skip rows without essential data
        if not row.get('title', '').strip():
            continue
            
        pub_time = row.get('publish_time', '')
        if not pub_time:
            continue
            
        try:
            # Parse date and extract year
            date_obj = datetime.strptime(pub_time, '%Y-%m-%d')
            if 2019 <= date_obj.year <= 2024:
                row['publication_year'] = date_obj.year
                cleaned_data.append(row)
        except ValueError:
            continue
    
    return cleaned_data

def create_year_chart(data, selected_years):
    """
    Create a simple year distribution chart
    """
    # Filter data by selected years
    filtered_data = [row for row in data if row['publication_year'] in selected_years]
    
    # Count publications by year
    year_counts = Counter(row['publication_year'] for row in filtered_data)
    
    if not year_counts:
        st.warning("No data available for selected years")
        return
    
    # Create simple bar chart data
    years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in years]
    
    # Display as Streamlit bar chart
    chart_data = {"Year": years, "Publications": counts}
    st.bar_chart(chart_data, x="Year", y="Publications")
    
    # Display summary statistics
    total_papers = sum(counts)
    avg_per_year = total_papers / len(years) if years else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Papers", f"{total_papers:,}")
    with col2:
        st.metric("Years Covered", len(years))
    with col3:
        st.metric("Avg per Year", f"{avg_per_year:.0f}")

def display_journal_analysis(data, top_n=10):
    """
    Display top journals analysis
    """
    journal_counts = Counter()
    
    for row in data:
        journal = row.get('journal', '').strip()
        if journal:
            journal_counts[journal] += 1
    
    if not journal_counts:
        st.warning("No journal data available")
        return
    
    # Get top journals
    top_journals = journal_counts.most_common(top_n)
    
    # Create chart data
    journals = [j[0][:30] + "..." if len(j[0]) > 30 else j[0] for j, _ in top_journals]
    counts = [count for _, count in top_journals]
    
    # Display as horizontal bar chart
    chart_data = {"Journal": journals, "Papers": counts}
    st.bar_chart(chart_data, x="Papers", y="Journal")
    
    # Display detailed table
    st.subheader(f"Top {top_n} Journals (Detailed)")
    journal_data = []
    for journal, count in top_journals:
        percentage = (count / len(data)) * 100
        journal_data.append({
            "Journal": journal,
            "Papers": count,
            "Percentage": f"{percentage:.1f}%"
        })
    
    st.dataframe(journal_data, use_container_width=True)

def display_word_analysis(data, top_n=20):
    """
    Display word frequency analysis from titles
    """
    all_words = []
    stop_words = {
        'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'by', 'from', 'at', 'an', 'as',
        'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall',
        'covid', 'coronavirus', 'sars', 'cov', 'pandemic', 'study', 'analysis', 'research'
    }
    
    for row in data:
        title = row.get('title', '').lower()
        # Extract words (simple approach)
        words = re.findall(r'\b[a-z]{4,}\b', title)
        filtered_words = [w for w in words if w not in stop_words]
        all_words.extend(filtered_words)
    
    if not all_words:
        st.warning("No words found in titles")
        return
    
    word_counts = Counter(all_words)
    top_words = word_counts.most_common(top_n)
    
    # Create chart
    words = [word for word, _ in top_words]
    counts = [count for _, count in top_words]
    
    chart_data = {"Word": words, "Frequency": counts}
    st.bar_chart(chart_data, x="Frequency", y="Word")
    
    # Display word cloud alternative (text-based)
    st.subheader("Word Cloud (Text-based)")
    word_cloud_text = " ".join([f"{word}({count})" for word, count in top_words[:15]])
    st.text_area("Most frequent words:", word_cloud_text, height=100)

def display_data_sample(data, n_samples=5):
    """
    Display sample data
    """
    if not data:
        st.warning("No data available")
        return
    
    sample_data = data[:n_samples]
    
    for i, row in enumerate(sample_data, 1):
        with st.expander(f"Paper {i}: {row.get('title', 'No Title')[:60]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Title:**", row.get('title', 'N/A'))
                st.write("**Journal:**", row.get('journal', 'N/A'))
                st.write("**Publication Date:**", row.get('publish_time', 'N/A'))
                st.write("**DOI:**", row.get('doi', 'N/A'))
            
            with col2:
                st.write("**Authors:**", row.get('authors', 'N/A')[:200] + "..." if len(row.get('authors', '')) > 200 else row.get('authors', 'N/A'))
                st.write("**Source:**", row.get('source_x', 'N/A'))
                st.write("**PMC ID:**", row.get('pmcid', 'N/A'))
            
            abstract = row.get('abstract', 'N/A')
            if abstract and abstract != 'N/A':
                st.write("**Abstract:**")
                st.write(abstract[:500] + "..." if len(abstract) > 500 else abstract)

def main():
    """
    Main Streamlit application
    """
    # Header
    st.markdown('<h1 class="main-header">🦠 COVID-19 Research Explorer</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Analysis of COVID-19 Research Papers")
    
    # Sidebar
    st.sidebar.header("📊 Analysis Options")
    
    # Load data
    data_file = "sample_metadata.csv"
    
    with st.spinner("Loading data..."):
        raw_data, error = load_data(data_file)
    
    if error:
        st.error(f"❌ {error}")
        st.info("💡 Make sure to run 'python create_sample_data.py' first to create sample data")
        return
    
    if not raw_data:
        st.error("❌ No data loaded")
        return
    
    # Process data
    with st.spinner("Processing data..."):
        processed_data = clean_and_process_data(raw_data)
    
    if not processed_data:
        st.error("❌ No valid data after processing")
        return
    
    # Sidebar filters
    available_years = sorted(set(row['publication_year'] for row in processed_data))
    selected_years = st.sidebar.multiselect(
        "Select Years",
        available_years,
        default=available_years
    )
    
    if not selected_years:
        st.warning("Please select at least one year")
        return
    
    # Filter data
    filtered_data = [row for row in processed_data if row['publication_year'] in selected_years]
    
    # Main content
    st.header("📈 Dataset Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", f"{len(filtered_data):,}")
    
    with col2:
        unique_journals = len(set(row.get('journal', '') for row in filtered_data if row.get('journal', '').strip()))
        st.metric("Unique Journals", unique_journals)
    
    with col3:
        papers_with_doi = sum(1 for row in filtered_data if row.get('doi', '').strip())
        st.metric("Papers with DOI", f"{papers_with_doi:,}")
    
    with col4:
        year_range = f"{min(selected_years)}-{max(selected_years)}"
        st.metric("Year Range", year_range)
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Publication Trends", "📰 Journal Analysis", "🔤 Text Analysis", "📄 Data Sample"])
    
    with tab1:
        st.header("Publication Trends Over Time")
        create_year_chart(filtered_data, selected_years)
    
    with tab2:
        st.header("Journal Analysis")
        top_n_journals = st.slider("Number of top journals to show", 5, 20, 10)
        display_journal_analysis(filtered_data, top_n_journals)
    
    with tab3:
        st.header("Text Analysis")
        top_n_words = st.slider("Number of top words to show", 10, 30, 20)
        display_word_analysis(filtered_data, top_n_words)
    
    with tab4:
        st.header("Sample Data")
        n_samples = st.slider("Number of samples to show", 3, 10, 5)
        display_data_sample(filtered_data, n_samples)
    
    # Download section
    st.header("💾 Export Data")
    
    if st.button("Generate Analysis Report"):
        # Create summary report
        report = {
            "analysis_date": datetime.now().isoformat(),
            "dataset_summary": {
                "total_papers": len(filtered_data),
                "year_range": f"{min(selected_years)}-{max(selected_years)}",
                "unique_journals": len(set(row.get('journal', '') for row in filtered_data if row.get('journal', '').strip()))
            },
            "top_journals": dict(Counter(row.get('journal', '') for row in filtered_data if row.get('journal', '').strip()).most_common(10)),
            "year_distribution": dict(Counter(row['publication_year'] for row in filtered_data))
        }
        
        # Convert to JSON string for download
        report_json = json.dumps(report, indent=2, default=str)
        
        st.download_button(
            label="📥 Download Analysis Report (JSON)",
            data=report_json,
            file_name=f"covid_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        st.success("✅ Report generated successfully!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **📝 About this App:**
    - This is a simplified version of the COVID-19 research data explorer
    - Data source: CORD-19 Dataset (sample)
    - Built with Streamlit for interactive analysis
    - For full functionality, install all dependencies from requirements.txt
    """)

if __name__ == "__main__":
    main()
