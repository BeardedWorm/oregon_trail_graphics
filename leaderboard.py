"""
Leaderboard system with graphical display of high scores
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class LeaderboardEntry:
    """Single leaderboard entry."""
    
    def __init__(self, player_name: str, score: int, difficulty: str,
                 date: str, stats: Dict[str, Any]):
        """Initialize leaderboard entry.
        
        Args:
            player_name: Player name
            score: Score
            difficulty: Difficulty level
            date: Date string
            stats: Game statistics
        """
        self.player_name = player_name
        self.score = score
        self.difficulty = difficulty
        self.date = date
        self.stats = stats
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'player_name': self.player_name,
            'score': self.score,
            'difficulty': self.difficulty,
            'date': self.date,
            'stats': self.stats,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'LeaderboardEntry':
        """Create from dictionary.
        
        Args:
            data: Dictionary with entry data
            
        Returns:
            LeaderboardEntry instance
        """
        return LeaderboardEntry(
            player_name=data['player_name'],
            score=data['score'],
            difficulty=data['difficulty'],
            date=data['date'],
            stats=data.get('stats', {}),
        )


class Leaderboard:
    """Main leaderboard manager."""
    
    def __init__(self, max_entries: int = 50):
        """Initialize leaderboard.
        
        Args:
            max_entries: Maximum entries to keep
        """
        self.entries = []
        self.max_entries = max_entries
        self.file_path = Path('leaderboard.json')
        self.load()
    
    def add_entry(self, player_name: str, score: int, difficulty: str,
                 stats: Dict[str, Any]) -> bool:
        """Add entry to leaderboard.
        
        Args:
            player_name: Player name
            score: Score
            difficulty: Difficulty
            stats: Game statistics
            
        Returns:
            True if entry was added to top scores
        """
        entry = LeaderboardEntry(
            player_name=player_name,
            score=score,
            difficulty=difficulty,
            date=datetime.now().isoformat(),
            stats=stats,
        )
        
        # Check if qualifies
        if len(self.entries) < self.max_entries or score > self.entries[-1].score:
            self.entries.append(entry)
            self.entries.sort(key=lambda e: e.score, reverse=True)
            self.entries = self.entries[:self.max_entries]
            self.save()
            return True
        
        return False
    
    def get_rank(self, score: int) -> int:
        """Get rank for score.
        
        Args:
            score: Score value
            
        Returns:
            Rank (1-based)
        """
        for i, entry in enumerate(self.entries):
            if score > entry.score:
                return i + 1
        return len(self.entries) + 1
    
    def get_entries(self, count: int = 10, offset: int = 0) -> List[LeaderboardEntry]:
        """Get leaderboard entries.
        
        Args:
            count: Number of entries
            offset: Offset from top
            
        Returns:
            List of entries
        """
        return self.entries[offset:offset + count]
    
    def get_top_entries(self, count: int = 10) -> List[LeaderboardEntry]:
        """Get top entries.
        
        Args:
            count: Number of entries
            
        Returns:
            List of top entries
        """
        return self.entries[:count]
    
    def filter_by_difficulty(self, difficulty: str) -> List[LeaderboardEntry]:
        """Filter by difficulty.
        
        Args:
            difficulty: Difficulty level
            
        Returns:
            Filtered entries
        """
        return [e for e in self.entries if e.difficulty == difficulty]
    
    def save(self) -> bool:
        """Save leaderboard to file.
        
        Returns:
            True if successful
        """
        try:
            data = [entry.to_dict() for entry in self.entries]
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            return False
    
    def load(self) -> bool:
        """Load leaderboard from file.
        
        Returns:
            True if successful
        """
        try:
            if not self.file_path.exists():
                return True
            
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            
            self.entries = [LeaderboardEntry.from_dict(entry) for entry in data]
            self.entries.sort(key=lambda e: e.score, reverse=True)
            return True
        
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear leaderboard.
        
        Returns:
            True if successful
        """
        self.entries = []
        return self.save()


class LeaderboardScreen:
    """Visual leaderboard display."""
    
    def __init__(self, leaderboard: Leaderboard):
        """Initialize leaderboard screen.
        
        Args:
            leaderboard: Leaderboard instance
        """
        self.leaderboard = leaderboard
        self.selected_index = 0
        self.current_page = 0
        self.entries_per_page = 10
        self.filter_difficulty = None  # None = all
    
    def draw(self, surface, renderer):
        """Draw leaderboard screen.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        surface.fill(COLORS['black'])
        
        # Draw title
        renderer.draw_text("Leaderboard", WINDOW_WIDTH // 2 - 50, 20,
                         COLORS['light_green'], 'large')
        
        # Draw filter
        filter_text = f"Filter: {self.filter_difficulty or 'All Difficulties'}"
        renderer.draw_text(filter_text, 20, 60, COLORS['cyan'], 'small')
        
        # Get entries
        if self.filter_difficulty:
            entries = self.leaderboard.filter_by_difficulty(self.filter_difficulty)
        else:
            entries = self.leaderboard.get_entries(self.entries_per_page, 
                                                  self.current_page * self.entries_per_page)
        
        # Draw header
        y = 100
        renderer.draw_text("Rank", 20, y, COLORS['light_cyan'], 'small')
        renderer.draw_text("Player", 80, y, COLORS['light_cyan'], 'small')
        renderer.draw_text("Score", 300, y, COLORS['light_cyan'], 'small')
        renderer.draw_text("Difficulty", 420, y, COLORS['light_cyan'], 'small')
        renderer.draw_text("Date", 580, y, COLORS['light_cyan'], 'small')
        
        y += 30
        
        # Draw entries
        for i, entry in enumerate(entries):
            rank = (self.current_page * self.entries_per_page) + i + 1
            
            if i == self.selected_index:
                # Highlight selected
                pygame.draw.rect(surface, COLORS['gray'], (10, y - 5, WINDOW_WIDTH - 20, 25))
            
            # Rank
            renderer.draw_text(f"#{rank}", 20, y, COLORS['white'], 'small')
            
            # Player name
            renderer.draw_text(entry.player_name, 80, y, COLORS['light_green'], 'small')
            
            # Score
            renderer.draw_text(str(entry.score), 300, y, COLORS['yellow'], 'small')
            
            # Difficulty
            diff_color = {
                'easy': COLORS['green'],
                'normal': COLORS['yellow'],
                'hard': COLORS['red'],
            }.get(entry.difficulty, COLORS['white'])
            
            renderer.draw_text(entry.difficulty.capitalize(), 420, y, diff_color, 'small')
            
            # Date
            date_short = entry.date[:10]
            renderer.draw_text(date_short, 580, y, COLORS['white'], 'small')
            
            y += 30
        
        # Draw instructions
        renderer.draw_text("UP/DOWN to scroll | LEFT/RIGHT to filter | ESC to return",
                         20, WINDOW_HEIGHT - 40, COLORS['light_white'], 'small')
    
    def handle_input(self, event):
        """Handle input.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = max(0, self.selected_index - 1)
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = min(self.entries_per_page - 1, 
                                         self.selected_index + 1)
            
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.current_page = max(0, self.current_page - 1)
                self.selected_index = 0
            
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                max_pages = (len(self.leaderboard.entries) + self.entries_per_page - 1) // \
                           self.entries_per_page
                self.current_page = min(max_pages - 1, self.current_page + 1)
                self.selected_index = 0


class ScoreCalculator:
    """Calculates final score based on game stats."""
    
    @staticmethod
    def calculate_score(distance: int, alive_members: int, total_members: int,
                       final_food: int, days_survived: int, 
                       victory: bool) -> int:
        """Calculate final score.
        
        Args:
            distance: Distance traveled
            alive_members: Number alive at end
            total_members: Total party members
            final_food: Food remaining
            days_survived: Days survived
            victory: Whether victorious
            
        Returns:
            Final score
        """
        score = 0
        
        # Distance points
        score += distance * 5
        
        # Survivor points
        score += alive_members * 500
        
        # Food bonus
        score += final_food * 2
        
        # Days survived
        score += days_survived * 10
        
        # Victory bonus
        if victory:
            score += 5000
        
        return max(0, score)


class StatsCollector:
    """Collects game statistics."""
    
    def __init__(self):
        """Initialize stats collector."""
        self.stats = {}
    
    def record_stat(self, key: str, value: Any):
        """Record statistic.
        
        Args:
            key: Stat key
            value: Stat value
        """
        self.stats[key] = value
    
    def get_final_stats(self) -> dict:
        """Get final stats for submission.
        
        Returns:
            Dictionary of stats
        """
        return self.stats.copy()


# Import pygame for screen drawing
import pygame
