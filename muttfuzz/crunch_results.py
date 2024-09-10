# Note: This was authored by claude.ai

import csv
import sys
import math

def read_csv(file_path):
    data = []
    total_count = 0
    non_zero_count = 0
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 3:
                    print(f"Warning: Skipping malformed row: {row}")
                    continue
                symbol, duration, exit_code = row
                try:
                    total_count += 1
                    if int(exit_code) != 0:
                        non_zero_count += 1
                        data.append(float(duration))
                except ValueError:
                    print(f"Warning: Skipping row with invalid data: {row}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{file_path}'.")
        sys.exit(1)
    return data, total_count, non_zero_count

def calculate_overall_stats(data):
    if not data:
        return None
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n if n > 1 else 0
    sem = math.sqrt(variance / n)
    median = sorted(data)[n//2] if n % 2 != 0 else (sorted(data)[n//2 - 1] + sorted(data)[n//2]) / 2
    return {'mean': mean, 'sem': sem, 'median': median, 'count': n}

def display_overall_stats(stats, total_count, non_zero_count):
    if stats is None:
        print("No valid data to analyze.")
        return

    mutation_score = (non_zero_count / total_count) * 100 if total_count > 0 else 0

    print("Results")
    print("=" * 50)
    print(f"Total number of evaluated mutants: {total_count}")
    print(f"Number of detected mutants: {non_zero_count}")
    print(f"Mutation Score: {mutation_score:.2f}%")
    print(f"Mean Duration: {stats['mean']:.2f} seconds")
    print(f"Median Duration: {stats['median']:.2f} seconds")
    print(f"Standard Error of the Mean: {stats['sem']:.2f} seconds")
    print(f"95% Confidence Interval for Mean: ({stats['mean'] - 1.96*stats['sem']:.2f}, {stats['mean'] + 1.96*stats['sem']:.2f}) seconds")

    # Create a simple ASCII representation of the mean, median, and confidence interval
    bar_width = 40
    mean_position = int((stats['mean'] - min(data)) / (max(data) - min(data)) * bar_width)
    median_position = int((stats['median'] - min(data)) / (max(data) - min(data)) * bar_width)
    ci_start = max(0, int((stats['mean'] - 1.96*stats['sem'] - min(data)) / (max(data) - min(data)) * bar_width))
    ci_end = min(bar_width, int((stats['mean'] + 1.96*stats['sem'] - min(data)) / (max(data) - min(data)) * bar_width))

    print("\nVisual Representation:")
    print("  " + "-" * bar_width)
    print("  " + " " * ci_start + "[" + "-" * (ci_end - ci_start) + "]")
    print("  " + " " * mean_position + "M" + " " * (median_position - mean_position) + "m" if mean_position < median_position else "  " + " " * median_position + "m" + " " * (mean_position - median_position) + "M")
    print("  " + "-" * bar_width)
    print(f"  {min(data):.2f}" + " " * (bar_width - 12) + f"{max(data):.2f}")
    print("M: Mean, m: Median, []: 95% Confidence Interval")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <results_csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    data, total_count, non_zero_count = read_csv(csv_file)
    stats = calculate_overall_stats(data)
    display_overall_stats(stats, total_count, non_zero_count)
