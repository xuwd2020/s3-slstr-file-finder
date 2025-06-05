# S3 SLSTR File Finder

A Python script to find and analyze Sentinel-3 SLSTR (Sea and Land Surface Temperature Radiometer) files with specific date patterns. The script can search through file lists, identify files matching specific date patterns, and analyze temporal relationships between files.

## Features

- Search for S3A/S3B files using date patterns or custom regex patterns
- Display full file paths or just filenames
- Save results to an output file
- Identify files with timestamps less than 2 minutes apart
- Flexible command-line interface

## Installation

No special installation is required. The script uses only Python standard library modules.

```bash
git clone https://github.com/xuwd2020/s3-slstr-file-finder.git
cd s3-slstr-file-finder
```

## Usage

```bash
python count_s3_files.py [file_path] [-d DATE] [-p PATTERN] [-o OUTPUT] [-f]
```

### Arguments

- `file_path`: Path to the list file (optional, has a default value)
- `-d, --date`: Date to search for in format YYYYMMDD (e.g., 20240914)
- `-p, --pattern`: Custom regex pattern to search for
- `-o, --output`: Save results to output file
- `-f, --full-path`: Show full paths instead of just filenames

### Example

```bash
# Search for files from September 14, 2024
python count_s3_files.py -d 20240914

# Search with a custom pattern and save results
python count_s3_files.py -p "S3A.*20240914" -o results.txt

# Show full file paths
python count_s3_files.py -d 20240914 -f
```

## Output

The script provides:
1. Number of files matching the pattern
2. List of matching files
3. Analysis of files with timestamps less than 2 minutes apart
4. Optional output file with the results

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.