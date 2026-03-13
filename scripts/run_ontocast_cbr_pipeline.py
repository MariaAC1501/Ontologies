#!/usr/bin/env python3
"""
Complete OntoCast → CBR Integration Pipeline

This script runs the full workflow:
1. Start OntoCast server
2. Process PDF with OMSSA ontology
3. Convert RDF to CBR CSV
4. Copy to CBR data directory
5. Provide next steps

Usage:
    python run_ontocast_cbr_pipeline.py --pdf path/to/paper.pdf --start-id 439
"""

import argparse
import subprocess
import sys
import time
import shutil
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

# Configuration
ONTOCAST_DIR = Path(__file__).parent.parent / "ontocast"
CBR_DATA_DIR = Path(__file__).parent.parent / "CBR-Ontology-For-Predictive-Maintenance" / "CBR-Ontology" / "CBRproject" / "data"
ONTOCAST_PORT = 8999


def check_ontocast_server(timeout: int = 30) -> bool:
    """Check if OntoCast server is running."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = urlopen(f"http://localhost:{ONTOCAST_PORT}/health", timeout=1)
            return response.status == 200
        except URLError:
            time.sleep(0.5)
    return False


def start_ontocast_server() -> subprocess.Popen:
    """Start OntoCast server."""
    print("Starting OntoCast server...")
    
    env_file = ONTOCAST_DIR / ".env"
    if not env_file.exists():
        print(f"Error: .env file not found at {env_file}")
        print("Please configure ontocast/.env first")
        sys.exit(1)
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, "-m", "ontocast.serve",
         "--env-path", str(env_file),
         "--working-directory", str(ONTOCAST_DIR / "working"),
         "--ontology-directory", str(ONTOCAST_DIR / "ontologies")],
        cwd=ONTOCAST_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to be ready
    if not check_ontocast_server():
        process.terminate()
        print("Error: OntoCast server failed to start")
        sys.exit(1)
    
    print("OntoCast server started successfully")
    return process


def process_pdf(pdf_path: Path, output_dir: Path) -> Path:
    """Process PDF through OntoCast."""
    print(f"\nProcessing PDF: {pdf_path}")
    
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)
    
    output_file = output_dir / "extracted_cases.ttl"
    
    # Use curl to process document
    cmd = [
        "curl", "-s", "-X", "POST",
        f"http://localhost:{ONTOCAST_PORT}/process",
        "-F", f"file=@{pdf_path}",
        "-F", "format=turtle",
        "--output", str(output_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error processing PDF: {result.stderr}")
        sys.exit(1)
    
    if not output_file.exists() or output_file.stat().st_size == 0:
        print("Error: OntoCast produced no output")
        sys.exit(1)
    
    print(f"Extracted cases saved to: {output_file}")
    return output_file


def convert_to_cbr(ttl_file: Path, csv_file: Path, start_id: int) -> int:
    """Convert Turtle RDF to CBR CSV."""
    print(f"\nConverting to CBR CSV format...")
    
    converter_script = Path(__file__).parent / "ontocast_to_cbr.py"
    
    if not converter_script.exists():
        print(f"Error: Converter script not found: {converter_script}")
        sys.exit(1)
    
    cmd = [
        sys.executable, str(converter_script),
        "--input", str(ttl_file),
        "--output", str(csv_file),
        "--start-id", str(start_id)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"Error converting to CSV: {result.stderr}")
        sys.exit(1)
    
    return result.returncode


def copy_to_cbr(csv_file: Path) -> Path:
    """Copy CSV to CBR data directory."""
    print("\nCopying to CBR data directory...")
    
    if not CBR_DATA_DIR.exists():
        print(f"Error: CBR data directory not found: {CBR_DATA_DIR}")
        print("Please check the CBR repository is cloned correctly")
        sys.exit(1)
    
    dest = CBR_DATA_DIR / "new_cases_from_ontocast.csv"
    shutil.copy(csv_file, dest)
    print(f"Copied to: {dest}")
    
    return dest


def print_cbr_instructions(csv_file: Path):
    """Print instructions for CBR import."""
    print("\n" + "="*60)
    print("CBR IMPORT INSTRUCTIONS")
    print("="*60)
    print(f"""
The CSV file has been generated and copied to the CBR data directory.

Next steps to complete the integration:

1. Open Eclipse IDE
   File → Import → Existing Projects into Workspace
   Select: CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject

2. Configure AppConfiguration.java
   Open: src/User/AppConfiguration.java
   Update these values:
     - data_path = "{CBR_DATA_DIR}"
     - csv = "{csv_file.name}"
     - ont_file_name = "OPMADdatabase_new.owl"
     - base_ont_file_name = "OPMAD.owl"

3. Prepare clean ontology
   Delete: {CBR_DATA_DIR}/OPMADdatabase.owl (if exists)
   Copy:   {CBR_DATA_DIR}/OPMAD.owl → {CBR_DATA_DIR}/OPMADdatabase.owl

4. Run CSVtoOntologyExec.java
   Right-click → Run As → Java Application
   This imports the CSV cases into the OWL ontology

5. Run myCBRSetting.java
   Right-click → Run As → Java Application
   This generates the .prj configuration file
   (Note: This takes several minutes as it runs the HermiT reasoner)

6. Run CBR Query Interface
   GUI2.java - for similarity-based retrieval
   GUI3.java - for weighted retrieval

Troubleshooting:
- If you get encoding errors: Ensure files are UTF-8
- If imports fail: Check semicolon separator in CSV
- If cases not found: Verify column names match expected schema
""")


def main():
    parser = argparse.ArgumentParser(
        description='Run complete OntoCast → CBR pipeline'
    )
    parser.add_argument('--pdf', '-p', type=Path, required=True,
                        help='PDF file to process')
    parser.add_argument('--output', '-o', type=Path,
                        default=Path("working/output"),
                        help='Output directory (default: working/output)')
    parser.add_argument('--start-id', '-s', type=int, default=439,
                        help='Starting reference ID (default: 439)')
    parser.add_argument('--keep-server', '-k', action='store_true',
                        help='Keep server running after processing')
    
    args = parser.parse_args()
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    server_process = None
    try:
        # Step 1: Start OntoCast server
        server_process = start_ontocast_server()
        
        # Step 2: Process PDF
        ttl_file = process_pdf(args.pdf, args.output)
        
        # Step 3: Convert to CBR CSV
        csv_file = args.output / "cbr_cases.csv"
        convert_to_cbr(ttl_file, csv_file, args.start_id)
        
        # Step 4: Copy to CBR
        dest_csv = copy_to_cbr(csv_file)
        
        # Step 5: Print instructions
        print_cbr_instructions(dest_csv)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    finally:
        if server_process and not args.keep_server:
            print("\nStopping OntoCast server...")
            server_process.terminate()
            server_process.wait()


if __name__ == "__main__":
    exit(main())
