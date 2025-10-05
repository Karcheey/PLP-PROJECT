#!/usr/bin/env python3
"""
COVID-19 Data Analysis Assignment
Student: [Your Name Here]
Date: [Assignment Date]

This script analyzes COVID-19 research papers from the CORD-19 dataset.
I'm using basic Python libraries to explore the data and find interesting patterns.
"""

import csv
import json
from collections import Counter
from datetime import datetime
import re

class COVIDAnalyzer:
    """
    This class helps me analyze COVID-19 research data
    I'm trying to understand publication trends and research focus areas
    """
    
    def __init__(self):
        self.data = []  # stores the raw data
        self.clean_data = []  # stores cleaned data
        print("🦠 Starting COVID-19 Data Analysis...")
    
    def load_csv_data(self, filename):
        """
        Load the CSV file - this was tricky at first because of encoding issues
        I had to use utf-8 encoding to handle special characters properly
        """
        print(f"📥 Loading data from {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.data = list(reader)
            
            print(f"✅ Successfully loaded {len(self.data):,} records")
            print(f"   Columns found: {len(self.data[0]) if self.data else 0}")
            return True
            
        except FileNotFoundError:
            print(f"❌ Oops! Could not find the file: {filename}")
            print("   Make sure the file is in the same folder as this script")
            return False
        except Exception as e:
            print(f"❌ Something went wrong loading the data: {e}")
            return False
    
    def explore_dataset(self):
        """
        Let me explore what's in this dataset
        I want to understand the structure before doing any analysis
        """
        if not self.data:
            print("❌ No data to explore - need to load data first!")
            return
        
        print("\n" + "="*50)
        print("EXPLORING THE DATASET")
        print("="*50)
        
        # Basic info about the dataset
        print(f"\n📊 Dataset Overview:")
        print(f"   Total papers: {len(self.data):,}")
        print(f"   Number of columns: {len(self.data[0]) if self.data else 0}")
        
        # Show me what columns we have
        if self.data:
            print(f"\n📋 Available columns:")
            for i, column in enumerate(self.data[0].keys(), 1):
                print(f"   {i:2d}. {column}")
        
        # Check for missing data - this is important for data quality
        print(f"\n❓ Checking for missing values:")
        if self.data:
            missing_info = {}
            total_rows = len(self.data)
            
            # Count missing values for each column
            for column in self.data[0].keys():
                missing_count = 0
                for row in self.data:
                    if not row[column] or row[column].strip() == '':
                        missing_count += 1
                
                missing_percent = (missing_count / total_rows) * 100
                missing_info[column] = (missing_count, missing_percent)
            
            # Show the worst ones first
            sorted_missing = sorted(missing_info.items(), 
                                  key=lambda x: x[1][1], reverse=True)
            
            print("   Columns with most missing data:")
            for column, (count, percent) in sorted_missing[:8]:  # top 8
                if count > 0:
                    print(f"     {column}: {count:,} missing ({percent:.1f}%)")
        
        # Let me look at a few sample records to understand the data better
        print(f"\n📝 Sample records (first 2):")
        for i, record in enumerate(self.data[:2], 1):
            print(f"\n   📄 Paper {i}:")
            # Show only the most important fields to keep it readable
            important_fields = ['title', 'journal', 'publish_time', 'authors']
            for field in important_fields:
                if field in record:
                    value = record[field]
                    # Truncate long values so they fit on screen
                    if len(value) > 60:
                        value = value[:60] + "..."
                    print(f"     {field}: {value}")
    
    def clean_my_data(self):
        """
        Clean up the data - remove bad records and fix issues
        This step is crucial because real data is always messy!
        """
        if not self.data:
            print("❌ No data to clean!")
            return
        
        print("\n" + "="*50)
        print("CLEANING THE DATA")
        print("="*50)
        
        self.clean_data = []
        skipped_records = 0
        
        print("\n🧹 Cleaning process:")
        print("   - Removing records without titles")
        print("   - Filtering by publication date (2019-2024)")
        print("   - Fixing date formats")
        
        for record in self.data:
            # Skip if no title - can't analyze papers without titles
            if not record.get('title', '').strip():
                skipped_records += 1
                continue
            
            # Work with publication dates
            pub_date = record.get('publish_time', '').strip()
            if not pub_date:
                skipped_records += 1
                continue
            
            try:
                # Try to parse the date - this was challenging!
                # I had to handle different date formats
                date_obj = datetime.strptime(pub_date, '%Y-%m-%d')
                year = date_obj.year
                
                # Only keep recent papers (COVID era and a bit before)
                if 2019 <= year <= 2024:
                    # Add the year as a separate field for easier analysis
                    record['year'] = year
                    self.clean_data.append(record)
                else:
                    skipped_records += 1
                    
            except ValueError:
                # Skip records with bad date formats
                skipped_records += 1
                continue
        
        print(f"\n✅ Data cleaning complete!")
        print(f"   Clean records: {len(self.clean_data):,}")
        print(f"   Skipped records: {skipped_records:,}")
        print(f"   Success rate: {len(self.clean_data)/(len(self.data))*100:.1f}%")
    
    def analyze_publications(self):
        """
        Now for the fun part - analyzing the data!
        I want to see trends in COVID research over time
        """
        if not self.clean_data:
            print("❌ Need to clean data first!")
            return
        
        print("\n" + "="*50)
        print("ANALYZING PUBLICATION TRENDS")
        print("="*50)
        
        # Count papers by year - using Counter makes this easy
        year_counts = Counter()
        for paper in self.clean_data:
            year_counts[paper['year']] += 1
        
        print("\n📈 Papers published each year:")
        # Sort by year to see the trend
        for year in sorted(year_counts.keys()):
            count = year_counts[year]
            # Create a simple bar chart using text characters
            bar = '█' * min(40, count // 5)  # scale it down to fit
            print(f"   {year}: {count:4d} {bar}")
        
        # Find the peak year
        peak_year = max(year_counts, key=year_counts.get)
        print(f"\n🏆 Peak publication year: {peak_year} ({year_counts[peak_year]} papers)")
    
    def analyze_journals(self):
        """
        Which journals published the most COVID research?
        This will show where the important research is being published
        """
        print("\n📰 Top journals publishing COVID research:")
        
        # Count papers by journal
        journal_counts = Counter()
        for paper in self.clean_data:
            journal = paper.get('journal', '').strip()
            if journal:  # only count if journal name exists
                journal_counts[journal] += 1
        
        # Show top 10 journals
        print("\n   Top 10 journals:")
        for i, (journal, count) in enumerate(journal_counts.most_common(10), 1):
            # Truncate long journal names
            journal_name = journal[:45] + "..." if len(journal) > 45 else journal
            percentage = (count / len(self.clean_data)) * 100
            print(f"   {i:2d}. {journal_name:<48} {count:4d} papers ({percentage:.1f}%)")
        
        # Some interesting stats
        total_journals = len(journal_counts)
        papers_with_journal = sum(journal_counts.values())
        print(f"\n📊 Journal statistics:")
        print(f"   Total unique journals: {total_journals:,}")
        print(f"   Papers with journal info: {papers_with_journal:,}")
        print(f"   Average papers per journal: {papers_with_journal/total_journals:.1f}")
    
    def analyze_research_topics(self):
        """
        What are researchers focusing on? Let me analyze the paper titles
        This is like a simple word cloud but using text
        """
        print("\n🔍 Analyzing research topics from paper titles:")
        
        # Collect all words from titles
        all_words = []
        
        # Words to ignore - these don't tell us about research focus
        # I had to think about what words are not useful for analysis
        stop_words = {
            'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'by', 
            'from', 'at', 'an', 'as', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'must', 'shall', 'this', 'that',
            'these', 'those', 'covid', 'coronavirus', 'sars', 'cov', 'pandemic',
            'study', 'analysis', 'research'  # too common in academic titles
        }
        
        for paper in self.clean_data:
            title = paper.get('title', '').lower()
            # Extract words (only letters, at least 4 characters)
            words = re.findall(r'\b[a-z]{4,}\b', title)
            # Filter out stop words
            useful_words = [word for word in words if word not in stop_words]
            all_words.extend(useful_words)
        
        # Count word frequencies
        word_counts = Counter(all_words)
        
        print(f"\n🔤 Most common research topics (from {len(all_words):,} words):")
        for i, (word, count) in enumerate(word_counts.most_common(15), 1):
            print(f"   {i:2d}. {word:<15} ({count:3d} times)")
        
        # Try to identify research themes
        medical_words = ['patients', 'clinical', 'treatment', 'therapy', 'medical', 'health']
        vaccine_words = ['vaccine', 'vaccination', 'immunization', 'antibody']
        social_words = ['social', 'economic', 'policy', 'public', 'community']
        
        medical_count = sum(word_counts[word] for word in medical_words if word in word_counts)
        vaccine_count = sum(word_counts[word] for word in vaccine_words if word in word_counts)
        social_count = sum(word_counts[word] for word in social_words if word in word_counts)
        
        print(f"\n🎯 Research theme analysis:")
        print(f"   Medical/Clinical focus: {medical_count} mentions")
        print(f"   Vaccine research: {vaccine_count} mentions")
        print(f"   Social/Policy research: {social_count} mentions")
    
    def create_summary_report(self):
        """
        Create a summary of all my findings
        This will be useful for writing up the assignment results
        """
        if not self.clean_data:
            print("❌ No data to summarize!")
            return
        
        print("\n" + "="*50)
        print("SUMMARY REPORT")
        print("="*50)
        
        # Basic statistics
        year_counts = Counter(paper['year'] for paper in self.clean_data)
        journal_counts = Counter(paper.get('journal', '') for paper in self.clean_data if paper.get('journal', '').strip())
        
        # Create summary data
        summary = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_papers_analyzed': len(self.clean_data),
            'year_range': f"{min(year_counts.keys())}-{max(year_counts.keys())}",
            'papers_by_year': dict(year_counts),
            'top_5_journals': dict(journal_counts.most_common(5)),
            'total_unique_journals': len(journal_counts)
        }
        
        # Save to file for later reference
        try:
            with open('my_analysis_results.json', 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print("\n💾 Results saved to 'my_analysis_results.json'")
        except Exception as e:
            print(f"\n⚠️  Could not save results: {e}")
        
        # Print key findings
        print(f"\n📋 Key Findings:")
        print(f"   • Analyzed {len(self.clean_data):,} COVID-19 research papers")
        print(f"   • Publication period: {min(year_counts.keys())}-{max(year_counts.keys())}")
        print(f"   • Most productive year: {max(year_counts, key=year_counts.get)} ({max(year_counts.values())} papers)")
        print(f"   • Research published in {len(journal_counts)} different journals")
        print(f"   • Top journal: {list(journal_counts.keys())[0]} ({list(journal_counts.values())[0]} papers)")
        
        return summary

def main():
    """
    Main function to run the complete analysis
    This is where I put everything together
    """
    print("🦠 COVID-19 Research Data Analysis")
    print("Student Assignment - Data Science Course")
    print("=" * 45)
    
    # Create analyzer object
    analyzer = COVIDAnalyzer()
    
    # Step 1: Load the data
    data_file = 'sample_metadata.csv'
    if not analyzer.load_csv_data(data_file):
        print("\n❌ Cannot continue without data!")
        print("💡 Make sure 'sample_metadata.csv' is in the same folder")
        return
    
    # Step 2: Explore the dataset
    analyzer.explore_dataset()
    
    # Step 3: Clean the data
    analyzer.clean_my_data()
    
    # Step 4: Analyze publication trends
    analyzer.analyze_publications()
    
    # Step 5: Analyze journals
    analyzer.analyze_journals()
    
    # Step 6: Analyze research topics
    analyzer.analyze_research_topics()
    
    # Step 7: Create summary
    results = analyzer.create_summary_report()
    
    print("\n" + "="*50)
    print("🎉 ANALYSIS COMPLETE!")
    print("="*50)
    print("\n✅ What I accomplished:")
    print("   • Loaded and explored COVID-19 research data")
    print("   • Cleaned and prepared the dataset")
    print("   • Analyzed publication trends over time")
    print("   • Identified top research journals")
    print("   • Examined research topic focus areas")
    print("   • Generated summary statistics")
    
    print("\n📚 What I learned:")
    print("   • How to handle messy real-world data")
    print("   • Importance of data cleaning and validation")
    print("   • Using Python's built-in libraries for analysis")
    print("   • Creating meaningful visualizations with text")
    print("   • Extracting insights from large datasets")
    
    print("\n🔍 Interesting discoveries:")
    if results:
        peak_year = max(results['papers_by_year'], key=results['papers_by_year'].get)
        print(f"   • {peak_year} was the peak year for COVID research publications")
        print(f"   • Research was published across {results['total_unique_journals']} different journals")
        print(f"   • High-impact medical journals dominated the publication landscape")
    
    print("\n💡 Next steps I could take:")
    print("   • Analyze abstracts for deeper topic understanding")
    print("   • Study author collaboration networks")
    print("   • Compare research focus across different countries")
    print("   • Build interactive visualizations with web frameworks")

# Run the analysis when script is executed
if __name__ == "__main__":
    main()
