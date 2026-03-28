#!/usr/bin/env python3
"""Memo extraction helpers for Star Office backend.

Reads and sanitizes daily memo content from memory/*.md for the yesterday-memo API.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import random
import re


def get_yesterday_date_str() -> str:
    """Return yesterday's date as YYYY-MM-DD."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def sanitize_content(text: str) -> str:
    """Redact PII and sensitive patterns (OpenID, paths, IPs, email, phone) for safe display."""
    text = re.sub(r'ou_[a-f0-9]+', '[User]', text)
    text = re.sub(r'user_id="[^"]+"', 'user_id="[Hidden]"', text)
    text = re.sub(r'/root/[^"\s]+', '[Path]', text)
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '[IP]', text)

    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[Email]', text)
    text = re.sub(r'1[3-9]\d{9}', '[Phone]', text)

    return text


def extract_memo_from_file(file_path: str) -> str:
    """Extract display-safe memo text from a memory markdown file; sanitizes and truncates with a short fallback."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract real content without over-wrapping
        lines = content.strip().split("\n")

        # Extract core points
        core_points = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("- "):
                core_points.append(line[2:].strip())
            elif len(line) > 10:
                core_points.append(line)

        if not core_points:
            return "「No record for yesterday」\n\nIf you have perseverance, why sleep at midnight and wake up at dawn; the most useless thing is to work hard for one day and rest for ten."

        # Extract 2-3 key points from the core content
        selected_points = core_points[:3]

        # Wisdom quotes library
        wisdom_quotes = [
            "「To do a good job, an artisan needs the best tools.」",
            "「A journey of a thousand miles begins with a single step.」",
            "「Knowledge and action combined lead to a far journey.」",
            "「Excellence comes from diligence, neglect from play.」",
            "「The road ahead is long and hard, I will search high and low.」",
            "「Last night the west wind withered the green trees, alone I climb the high tower, gazing at the endless road.」",
            "「I have no regrets as my clothes grow loose, pining for her I grow thin.」",
            "「Hundreds and thousands of times I searched for her in the crowd, suddenly turning back, she is there in the dim light.」",
            "「A clear understanding of world affairs is genuine knowledge.」",
            "「What is learned from books feels shallow, to truly understand it you must practice it.」"
        ]

        quote = random.choice(wisdom_quotes)

        # Assemble content
        result = []

        # Add core content
        if selected_points:
            for point in selected_points:
                # Privacy cleanup
                point = sanitize_content(point)
                # Truncate overly long content
                if len(point) > 40:
                    point = point[:37] + "..."
                # Max 20 characters per line
                if len(point) <= 20:
                    result.append(f"· {point}")
                else:
                    # Split by 20 characters
                    for j in range(0, len(point), 20):
                        chunk = point[j:j+20]
                        if j == 0:
                            result.append(f"· {chunk}")
                        else:
                            result.append(f"  {chunk}")

        # Add wisdom quote
        if quote:
            if len(quote) <= 20:
                result.append(f"\n{quote}")
            else:
                for j in range(0, len(quote), 20):
                    chunk = quote[j:j+20]
                    if j == 0:
                        result.append(f"\n{chunk}")
                    else:
                        result.append(chunk)

        return "\n".join(result).strip()

    except Exception as e:
        print(f"extract_memo_from_file failed: {e}")
        return "「Failed to load yesterday's record」\n\n「The past cannot be undone, the future can still be pursued.」"
