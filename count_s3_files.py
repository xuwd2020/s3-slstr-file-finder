#!/usr/bin/env python3
"""
This script finds S3A/S3B files with a specific date pattern and offers multiple output options.
It can display full filenames, paths, and save results to a file.
"""
import re
import sys
import os
import argparse

def find_matching_files(file_path, pattern=None, output_file=None, full_path=False, date=None):
    # Use provided pattern or build one based on the date
    if not pattern:
        if date:
            # Build pattern using the specified date (format: YYYYMMDD)
            pattern = rf'S3A.*{date}T[0-9]{{6}}_{date}T[0-9]{{6}}'
        else:
            # Default pattern (September 14, 2024)
            pattern = r'S3A.*20240914T[0-9]{6}_20240914T[0-9]{6}'
    
    print(f"Searching for pattern: {pattern}")
    
    try:
        # Open and read the file
        with open(file_path, 'r') as file:
            content = file.readlines()
        
        # Store matching results
        matching_results = []
        
        # Process each line
        for line in content:
            if re.search(pattern, line):
                # Extract the desired information based on user preference
                parts = line.strip().split()
                if len(parts) >= 7:  # Ensure we have enough parts
                    full_filepath = parts[-1]  # The last part is the full path
                    if full_path:
                        matching_results.append(full_filepath)
                    else:
                        filename = os.path.basename(full_filepath)  # Extract just the filename
                        matching_results.append(filename)
        
        # Print the results to console
        count = len(matching_results)
        print(f"Found {count} files matching the pattern.")
        
        # Print all matching results
        if count > 0:
            print("\nMatching files:")
            for i, result in enumerate(matching_results):
                print(f"{i+1}. {result}")
        
        # Save to output file if specified
        if output_file and matching_results:
            with open(output_file, 'w') as f:
                for result in matching_results:
                    f.write(f"{result}\n")
            print(f"\nResults saved to {output_file}")
        
        # Find files with timestamps less than 2 minutes apart
        if matching_results:
            # Extract timestamps and organize files by timestamp
            timestamp_dict = {}
            for result in matching_results:
                # Extract timestamp from filename (format: S3A_SL_2_FRP____20240914T073214_...)
                match = re.search(r'S3A_SL_2_FRP____(\d{8}T\d{6})_', result)
                if match:
                    timestamp = match.group(1)
                    if timestamp not in timestamp_dict:
                        timestamp_dict[timestamp] = []
                    timestamp_dict[timestamp].append(result)
            
            # Convert timestamps to sortable format and sort them
            sorted_timestamps = sorted(timestamp_dict.keys())
            
            # Find timestamps less than 2 minutes apart
            if len(sorted_timestamps) > 1:
                print("\nFiles with timestamps less than 2 minutes apart:")
                found_close_files = False
                
                for i in range(len(sorted_timestamps) - 1):
                    current = sorted_timestamps[i]
                    next_ts = sorted_timestamps[i + 1]
                    
                    # Convert timestamps to minutes for comparison
                    current_minutes = int(current[9:11]) * 60 + int(current[11:13])
                    next_minutes = int(next_ts[9:11]) * 60 + int(next_ts[11:13])
                    
                    # Calculate difference in minutes
                    diff_minutes = abs(next_minutes - current_minutes)
                    
                    # If difference is less than 2 minutes, print the files
                    if diff_minutes < 2:
                        found_close_files = True
                        print(f"\nTimestamps {current} and {next_ts} are {diff_minutes} minutes apart:")
                        for file in timestamp_dict[current]:
                            print(f"  - {file}")
                        for file in timestamp_dict[next_ts]:
                            print(f"  - {file}")
                
                if not found_close_files:
                    print("  No files found with timestamps less than 2 minutes apart.")
        
        return matching_results
                
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Find S3A files matching a specific date pattern.')
    parser.add_argument('file_path', nargs='?', default="/mnt/j/BC_data/BC_frp-l2-monthly/2024-09/frp-l2-2024-09.list",
                        help='Path to the list file')
    parser.add_argument('-d', '--date', help='Date to search for in format YYYYMMDD (e.g., 20240914)')
    parser.add_argument('-p', '--pattern', help='Custom regex pattern to search for')
    parser.add_argument('-o', '--output', help='Save results to output file')
    parser.add_argument('-f', '--full-path', action='store_true', help='Show full paths instead of just filenames')
    
    args = parser.parse_args()
    
    find_matching_files(args.file_path, args.pattern, args.output, args.full_path, args.date)

if __name__ == "__main__":
    main()