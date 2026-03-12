#!/usr/bin/env python3
"""
Test script for OntoCast extraction on example_paper.md
"""
import os
import sys

# Change to ontocast directory
os.chdir('./ontocast')

# Add ontocast to path
sys.path.insert(0, '.')

from ontocast.core import OntoCast

def main():
    print("=" * 60)
    print("OntoCast Test - Extracting from example_paper.md")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv('LLM_API_KEY', 'your_openai_api_key_here')
    if api_key == 'your_openai_api_key_here':
        print("\n⚠️  WARNING: OpenAI API key not configured!")
        print("Please set your API key in ontocast/.env file")
        print("Or set environment variable: export LLM_API_KEY='your-key'")
        return 1
    
    print(f"\n📄 Processing: working/example_paper.md")
    print(f"🧠 Using model: gpt-4o-mini")
    print(f"📊 Output format: RDF/Turtle")
    print(f"🔧 Mode: ontology (instance extraction only)")
    print()
    
    try:
        # Initialize OntoCast
        app = OntoCast()
        
        # Process the markdown file
        result = app.process_document(
            file_path="working/example_paper.md",
            output_format="turtle"
        )
        
        print("\n" + "=" * 60)
        print("✅ Extraction completed!")
        print("=" * 60)
        print(f"\n📁 Output saved to: working/extracted.ttl")
        print(f"📊 Triples extracted: {result.get('triple_count', 'N/A')}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
