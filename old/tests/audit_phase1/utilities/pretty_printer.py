"""
Pretty Printer - Format audit data into readable tables and charts

Provides formatting utilities for generating ASCII tables, comparison tables,
statistics boxes, and histograms for the audit report.
"""
from typing import List, Dict, Any, Optional
import math


class PrettyPrinter:
    """Utility class for formatting audit data into human-readable output"""
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize Pretty Printer
        
        Args:
            use_colors: Whether to use terminal colors (green/red/yellow)
        """
        self.use_colors = use_colors
        
        # ANSI color codes
        self.COLORS = {
            "green": "\033[92m",
            "red": "\033[91m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "reset": "\033[0m",
        }
    
    def format_table(
        self, 
        data: List[Dict[str, Any]], 
        columns: List[str],
        align: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Format data as ASCII table with aligned columns
        
        Args:
            data: List of dictionaries containing row data
            columns: Column names to display
            align: Column alignment ('left', 'right', 'center'). Default: 'left'
        
        Returns:
            Formatted ASCII table string
        
        Example:
            >>> data = [{"name": "GARAN", "value": 1.15}, {"name": "THYAO", "value": 0.85}]
            >>> print(printer.format_table(data, ["name", "value"]))
            ┌───────┬───────┐
            │ name  │ value │
            ├───────┼───────┤
            │ GARAN │  1.15 │
            │ THYAO │  0.85 │
            └───────┴───────┘
        """
        if not data:
            return "No data available"
        
        align = align or {}
        
        # Calculate column widths
        col_widths = {}
        for col in columns:
            # Max of header width and all data widths
            max_width = len(col)
            for row in data:
                value = str(row.get(col, ""))
                max_width = max(max_width, len(value))
            col_widths[col] = max_width + 2  # Add padding
        
        # Build table
        lines = []
        
        # Top border
        top_border = "┌" + "┬".join("─" * col_widths[col] for col in columns) + "┐"
        lines.append(top_border)
        
        # Header row
        header_cells = []
        for col in columns:
            cell = self._align_text(col, col_widths[col], align.get(col, "left"))
            header_cells.append(cell)
        header_row = "│" + "│".join(header_cells) + "│"
        lines.append(header_row)
        
        # Header separator
        separator = "├" + "┼".join("─" * col_widths[col] for col in columns) + "┤"
        lines.append(separator)
        
        # Data rows
        for row in data:
            row_cells = []
            for col in columns:
                value = str(row.get(col, ""))
                cell = self._align_text(value, col_widths[col], align.get(col, "left"))
                row_cells.append(cell)
            data_row = "│" + "│".join(row_cells) + "│"
            lines.append(data_row)
        
        # Bottom border
        bottom_border = "└" + "┴".join("─" * col_widths[col] for col in columns) + "┘"
        lines.append(bottom_border)
        
        return "\n".join(lines)
    
    def format_comparison_table(
        self, 
        expected: Dict[str, float], 
        actual: Dict[str, float]
    ) -> str:
        """
        Format comparison table showing expected vs actual values with deltas
        
        Args:
            expected: Dictionary of expected values
            actual: Dictionary of actual values
        
        Returns:
            Formatted comparison table with percentage differences
        
        Example:
            >>> expected = {"current_ratio": 2.0, "debt_to_equity": 1.5}
            >>> actual = {"current_ratio": 2.03, "debt_to_equity": 1.48}
            >>> print(printer.format_comparison_table(expected, actual))
        """
        data = []
        for key in expected.keys():
            exp_val = expected[key]
            act_val = actual.get(key, None)
            
            if act_val is not None:
                delta = act_val - exp_val
                pct_diff = (delta / exp_val * 100) if exp_val != 0 else 0
                
                # Format delta with sign
                delta_str = f"{delta:+.2f}"
                pct_str = f"{pct_diff:+.2f}%"
                
                # Colorize status
                if abs(pct_diff) < 2.0:
                    status = self.colorize("✓ PASS", "green")
                else:
                    status = self.colorize("✗ FAIL", "red")
                
                data.append({
                    "ratio": key,
                    "expected": f"{exp_val:.4f}",
                    "actual": f"{act_val:.4f}",
                    "delta": delta_str,
                    "pct_diff": pct_str,
                    "status": status
                })
            else:
                data.append({
                    "ratio": key,
                    "expected": f"{exp_val:.4f}",
                    "actual": "N/A",
                    "delta": "N/A",
                    "pct_diff": "N/A",
                    "status": self.colorize("⚠ SKIP", "yellow")
                })
        
        return self.format_table(
            data, 
            ["ratio", "expected", "actual", "delta", "pct_diff", "status"],
            align={"expected": "right", "actual": "right", "delta": "right", "pct_diff": "right"}
        )
    
    def format_statistics(self, data: List[float]) -> str:
        """
        Format summary statistics (min, max, mean, median, std)
        
        Args:
            data: List of numeric values
        
        Returns:
            Formatted statistics box
        
        Example:
            >>> print(printer.format_statistics([5.2, 8.3, 11.9, 15.4, 18.7]))
            Statistics:
              Min:     5.20
              Max:    18.70
              Mean:   11.90
              Median: 11.90
              StdDev:  4.85
        """
        if not data:
            return "No data available"
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        min_val = sorted_data[0]
        max_val = sorted_data[-1]
        mean_val = sum(data) / n
        median_val = sorted_data[n // 2] if n % 2 == 1 else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        
        # Calculate standard deviation
        variance = sum((x - mean_val) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)
        
        lines = [
            "Statistics:",
            f"  Min:    {min_val:>7.2f}",
            f"  Max:    {max_val:>7.2f}",
            f"  Mean:   {mean_val:>7.2f}",
            f"  Median: {median_val:>7.2f}",
            f"  StdDev: {std_dev:>7.2f}",
        ]
        
        return "\n".join(lines)
    
    def format_histogram(self, data: List[float], bins: int = 10) -> str:
        """
        Format ASCII histogram
        
        Args:
            data: List of numeric values
            bins: Number of histogram bins
        
        Returns:
            ASCII histogram string
        
        Example:
            >>> data = [5, 7, 8, 9, 10, 12, 14, 15]
            >>> print(printer.format_histogram(data, bins=4))
            Distribution:
              5-7   : ████░░░░░░ (25.0%)
              7-9   : ████████░░ (37.5%)
              9-12  : ██░░░░░░░░ (12.5%)
              12-15 : ████████░░ (25.0%)
        """
        if not data:
            return "No data available"
        
        min_val = min(data)
        max_val = max(data)
        bin_width = (max_val - min_val) / bins if min_val != max_val else 1
        
        # Create bins
        bin_counts = [0] * bins
        for value in data:
            if min_val == max_val:
                bin_idx = 0
            else:
                bin_idx = min(int((value - min_val) / bin_width), bins - 1)
            bin_counts[bin_idx] += 1
        
        # Find max count for scaling
        max_count = max(bin_counts) if bin_counts else 1
        bar_width = 10
        
        lines = ["Distribution:"]
        for i, count in enumerate(bin_counts):
            bin_start = min_val + i * bin_width
            bin_end = min_val + (i + 1) * bin_width
            
            # Create bar
            filled = int((count / max_count) * bar_width) if max_count > 0 else 0
            empty = bar_width - filled
            bar = "█" * filled + "░" * empty
            
            percentage = (count / len(data) * 100) if data else 0
            
            lines.append(f"  {bin_start:.1f}-{bin_end:.1f} : {bar} ({percentage:.1f}%)")
        
        return "\n".join(lines)
    
    def format_percentage(self, value: float, decimals: int = 2) -> str:
        """
        Format number as percentage
        
        Args:
            value: Numeric value (0.15 → 15.00%)
            decimals: Number of decimal places
        
        Returns:
            Formatted percentage string
        """
        return f"{value * 100:.{decimals}f}%"
    
    def format_number(
        self, 
        value: float, 
        decimals: int = 2,
        thousands_sep: bool = True
    ) -> str:
        """
        Format number with optional thousands separator
        
        Args:
            value: Numeric value
            decimals: Number of decimal places
            thousands_sep: Whether to use thousands separator
        
        Returns:
            Formatted number string
        """
        if thousands_sep:
            return f"{value:,.{decimals}f}"
        else:
            return f"{value:.{decimals}f}"
    
    def colorize(self, text: str, status: str) -> str:
        """
        Add terminal color codes to text
        
        Args:
            text: Text to colorize
            status: Color name ('green', 'red', 'yellow', 'blue') or status ('PASS', 'FAIL', 'WARNING')
        
        Returns:
            Colorized text (or plain text if colors disabled)
        """
        if not self.use_colors:
            return text
        
        # Map status to color
        color_map = {
            "PASS": "green",
            "FAIL": "red",
            "WARNING": "yellow",
            "INFO": "blue",
        }
        
        color = color_map.get(status.upper(), status.lower())
        color_code = self.COLORS.get(color, "")
        reset_code = self.COLORS["reset"]
        
        if color_code:
            return f"{color_code}{text}{reset_code}"
        else:
            return text
    
    def _align_text(self, text: str, width: int, align: str = "left") -> str:
        """
        Align text within specified width
        
        Args:
            text: Text to align
            width: Total width
            align: Alignment ('left', 'right', 'center')
        
        Returns:
            Aligned text with padding
        """
        text_len = len(text)
        padding = width - text_len
        
        if align == "right":
            return " " * padding + text
        elif align == "center":
            left_pad = padding // 2
            right_pad = padding - left_pad
            return " " * left_pad + text + " " * right_pad
        else:  # left
            return text + " " * padding
