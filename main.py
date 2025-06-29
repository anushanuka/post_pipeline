#!/usr/bin/env python3
"""
Daily AI Post Pipeline - Main Script
Fetches AI content via Gemini API and posts to Supabase database.
"""

import json
import requests
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai


def load_config():
    """Load configuration from environment variables with fallback to config.json."""
    try:
        # Try environment variables first (for GitHub Actions)
        load_dotenv()
        
        config = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "SUPABASE_PROJECT_URL": os.getenv("SUPABASE_PROJECT_URL"), 
            "SUPABASE_KEY": os.getenv("SUPABASE_KEY")
        }
        
        # Check if all required variables are present
        missing_vars = [key for key, value in config.items() if not value]
        if not missing_vars:
            print("✅ Using environment variables")
            return config
        else:
            print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
            print("🔄 Falling back to config.json...")
            
    except Exception as e:
        print(f"⚠️ Error loading environment variables: {e}")
        print("🔄 Falling back to config.json...")
    
    # Fallback to config.json for local development
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ Using config.json")
        return config
    except FileNotFoundError:
        print("❌ Error: No configuration found! Need either .env file or config.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in config.json!")
        sys.exit(1)


def load_query():
    """Load search query from query.txt file."""
    try:
        with open('query.txt', 'r', encoding='utf-8') as f:
            query = f.read().strip()
        if not query:
            raise ValueError("Query file is empty")
        print(f"📝 Loaded query: {query}")
        return query
    except FileNotFoundError:
        print("❌ Error: query.txt file not found!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading query: {e}")
        sys.exit(1)


def load_prompt_template():
    """Load prompt template from external file."""
    try:
        with open('prompt_template.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ Warning: prompt_template.txt not found, using default prompt")
        return """
Please provide the latest information and developments about '{query}' from the last 24 hours (since {yesterday}).

Focus on recent news, updates, technical developments, and community insights.

Please structure your response with:
- Title: A catchy title for the update
- Summary: Brief overview of key developments
- Key Points: Bullet points of important updates
- Technical Details: Any technical information or examples

Current date: {current_date}
Query: {query}
Time range: Last 24 hours
"""


def generate_content(api_key, query):
    """Generate content using Gemini API."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Prepare date variables
        current_date = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Load and format prompt template
        prompt_template = load_prompt_template()
        prompt = prompt_template.format(
            query=query,
            current_date=current_date,
            yesterday=yesterday
        )
        
        print("🤖 Generating content with Gemini Flash 2.5...")
        response = model.generate_content(prompt)
        
        # Structure the response
        content = {
            "query": query,
            "generated_at": datetime.now().isoformat(),
            "model": "gemini-2.0-flash-exp",
            "content": response.text,
            "search_date_range": f"{yesterday} to {current_date}",
            "prompt_version": "template_v1"
        }
        
        return content
        
    except Exception as e:
        print(f"❌ Error with Gemini API: {e}")
        return None


def post_to_database(supabase_url, supabase_key, post_data, source="github_actions"):
    """Post content to Supabase database."""
    url = f"{supabase_url}/rest/v1/post_pipeline"
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    payload = {
        "post": post_data,
        "source": source
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error posting to Supabase: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


def main():
    """Main execution function."""
    print("🚀 Starting Daily AI Post Pipeline...")
    
    # Load configuration
    config = load_config()
    
    # Extract credentials
    gemini_api_key = config.get("GEMINI_API_KEY")
    supabase_url = config.get("SUPABASE_PROJECT_URL")
    supabase_key = config.get("SUPABASE_KEY")
    
    if not all([gemini_api_key, supabase_url, supabase_key]):
        print("❌ Missing required credentials!")
        sys.exit(1)
    
    # Load search query
    query = load_query()
    
    # Generate content
    content = generate_content(gemini_api_key, query)
    
    if not content:
        print("❌ Failed to generate content!")
        sys.exit(1)
    
    print("✅ Content generated successfully!")
    print(f"📝 Preview: {content['content'][:150]}...")
    
    # Post to database
    print("\n📤 Posting to database...")
    result = post_to_database(supabase_url, supabase_key, content)
    
    if result:
        print("✅ Successfully posted to database!")
        print(f"📊 Record ID: {result[0]['id']}")
        print(f"🕒 Created at: {result[0]['created_at']}")
        print(f"📋 Source: {result[0]['source']}")
        print("🎉 Pipeline completed successfully!")
    else:
        print("❌ Failed to post to database!")
        sys.exit(1)


if __name__ == "__main__":
    main() 